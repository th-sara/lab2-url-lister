# Lab 2: URLCount Solution

## Implementation Approach

I implemented URLCount using Python with Hadoop Streaming API rather than Java.

### URLMapper.py
The mapper uses the regex pattern `href="([^"]*)"` to extract URLs from HTML content. This pattern matches the href attribute format and captures the URL inside the quotes. The mapper processes the input line by line and outputs each URL it finds with a count of 1. Multiple URLs can appear on a single line, and the mapper extracts all of them.

### URLReducer.py
The reducer aggregates counts for each URL from all mappers. It filters the output to only show URLs that appear more than 5 times. The implementation makes sure to handle the final URL properly to avoid the common bug of missing the last entry.

### Software Requirements
- Python 3
- Hadoop 3.3.6 with Hadoop Streaming
- Google Cloud Dataproc cluster
- Input files: Two Wikipedia articles (file01, file02)

## Resources Used
I referred to the Hadoop Streaming Tutorial, Python regex documentation, and the Hadoop MapReduce tutorial while working on this implementation. I worked independently with no collaboration with other students.

## Combiner Problem

The Java WordCount implementation used a Combiner to improve efficiency by performing local aggregation at each mapper before sending data to reducers. However, using a Combiner would cause incorrect results for this URLCount application.

The problem occurs because we filter URLs based on count greater than 5 in the Reducer, but the Combiner runs at each mapper node before data is combined across all mappers.

Here is an example scenario that shows the problem. Say Mapper 1 finds a URL 3 times and Mapper 2 finds the same URL 4 times. With a Combiner, both would be filtered out because 3 is less than 5 and 4 is less than 5. Without a Combiner, the Reducer sees the total which is 7 and correctly outputs it.

The Combiner would apply the "greater than 5" filter too early in the pipeline, before all counts are aggregated across mappers, losing valid URLs that should appear in the final output.

## Execution Time Comparison

### 2 Worker Cluster
**Execution time:** 1 minute 30 seconds (90.048 seconds)  
**Cluster creation time:** 4 minutes 0.839 seconds  
**Cluster configuration:** 1 master and 2 workers  
**Machine type:** n1-standard-2  
**Number of map tasks:** 10  
**Number of reduce tasks:** 3  
**Shuffled maps:** 30

### 4 Worker Cluster
**Execution time:** 1 minute 26 seconds (86.389 seconds)  
**Cluster creation time:** Approximately 4 minutes  
**Cluster configuration:** 1 master and 4 workers  
**Machine type:** n1-standard-2  
**Number of map tasks:** 22  
**Number of reduce tasks:** 7  
**Shuffled maps:** 154

### Analysis

The most surprising outcome is that doubling the number of workers from 2 to 4 only reduced execution time by approximately 4 seconds, representing just a 4% improvement. This minimal speedup contradicts the expectation that doubling workers should significantly reduce processing time.

This occurs because the dataset is extremely small with only two Wikipedia articles totaling approximately 600KB. For such small data, Hadoop's distributed processing overhead dominates the actual computation time. The overhead includes job setup and initialization, task scheduling and coordination, data shuffling between map and reduce phases, and network communication between nodes.

Notice that the 4 worker cluster created 22 map tasks versus only 10 for the 2 worker cluster. More tasks means more coordination overhead despite having more workers to process them. The job spent considerably more time on shuffle operations with 154 shuffled maps versus 30 for the 2 worker cluster. The additional coordination overhead nearly canceled out the benefits of having more workers.

This result demonstrates an important principle about distributed systems. They excel with large datasets where processing time dominates overhead, but for small data like our 600KB input, the coordination overhead outweighs the parallelization benefits. A single machine would likely complete this task faster than either cluster configuration.

With datasets in the gigabyte or terabyte range, we would expect much better scaling as computation time would significantly outweigh the coordination overhead, and the additional workers would provide meaningful performance improvements approaching linear speedup.

## Output

I found 10 URLs with count greater than 5:
```
mw-data:TemplateStyles:r1333433106      121
mw-data:TemplateStyles:r1295599781      33
/wiki/ISBN_(identifier)                 18
/wiki/Doi_(identifier)                  18
#                                       18
/wiki/S2CID_(identifier)                14
mw-data:TemplateStyles:r886049734       12
mw-data:TemplateStyles:r1333133064      7
/wiki/MapReduce                         7
/wiki/Google_File_System                6
```

**Note:** The Wikipedia files have been updated since the original assignment was written. The original expected output listed 4 URLs with specific counts, but the current Wikipedia articles contain 10 URLs that appear more than 5 times with different version numbers for the TemplateStyles references.
