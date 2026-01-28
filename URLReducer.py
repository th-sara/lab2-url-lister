#!/usr/bin/env python3
import sys

current_url = None
current_count = 0

for line in sys.stdin:
    # Parse the input from mapper
    url, count = line.strip().split('\t', 1)
    count = int(count)
    
    # If same URL, add to count
    if url == current_url:
        current_count += count
    else:
        # New URL found - output previous if count > 5
        if current_url and current_count > 5:
            print(f"{current_url}\t{current_count}")
        
        # Start counting new URL
        current_url = url
        current_count = count


if current_url and current_count > 5:
    print(f"{current_url}\t{current_count}")
