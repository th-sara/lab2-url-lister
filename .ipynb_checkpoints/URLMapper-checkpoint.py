#!/usr/bin/env python3
import sys
import re

# Pattern to find href="something"
url_pattern = re.compile(r'href="([^"]*)"')

for line in sys.stdin:
    # Find all URLs in this line
    urls = url_pattern.findall(line)
    
    # Output each URL with count 1
    for url in urls:
        print(f"{url}\t1")