# Lab 2: URLCount Solution

## Implementation Approach

I implemented URLCount using Python with Hadoop Streaming API.

### URLMapper.py

The mapper uses the regex pattern `href="([^"]*)"` to extract URLs from HTML content. It processes the input line by line and outputs each URL it finds with a count of 1.

### URLReducer.py

The reducer aggregates counts for each URL from all mappers. It filters the output to only show URLs that appear more than 5 times. The implementation makes sure to handle the final URL properly to avoid the common bug of missing the last entry.

## Resources Used

I referred to the Hadoop Streaming Tutorial, Python regex documentation, and the Hadoop MapReduce tutorial while working on this implementation.

## Combiner Problem

Using a Combiner would cause incorrect results for this task. The Combiner runs at each mapper node before sending data to the reducer, but our requirement is to filter URLs with count greater than 5 after combining all mappers.

Here is an example scenario that shows the problem. Say Mapper 1 finds URL "X" 3 times and Mapper 2 finds URL "X" 4 times. With a Combiner, both would be filtered out because 3 is less than 5 and 4 is less than 5. Without a Combiner, the Reducer sees the total which is 7 and correctly outputs it.

The Combiner would apply the "greater than 5" filter too early, losing valid URLs that should appear in the final output.

## Execution Time Comparison

### 2 Worker Cluster

**Execution time:** [Fill in after running on Dataproc]

**Cluster configuration:** 1 master and 2 workers

### 4 Worker Cluster

**Execution time:** [Fill in after running on Dataproc]

**Cluster configuration:** 1 master and 4 workers

### Analysis

[Fill in discussion on speedup, overhead, and whether doubling workers halved execution time]

## Output

I found 10 URLs with count greater than 5:

- `mw-data:TemplateStyles:r1333433106` appears 121 times
- `mw-data:TemplateStyles:r1295599781` appears 33 times
- `/wiki/ISBN_(identifier)` appears 18 times
- `/wiki/Doi_(identifier)` appears 18 times
- `` appears 18 times
- `/wiki/S2CID_(identifier)` appears 14 times
- `mw-data:TemplateStyles:r886049734` appears 12 times
- `mw-data:TemplateStyles:r1333133064` appears 7 times
- `/wiki/MapReduce` appears 7 times
- `/wiki/Google_File_System` appears 6 times

**Note:** The Wikipedia files have been updated since the original assignment was written, so some URLs differ from the expected output in the README.
