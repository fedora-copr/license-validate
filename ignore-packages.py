#!/usr/bin/python3

"""
Reads stdin and print everything to stdout. But skip lines
that matches at least one regexp in "ignore-packages.txt"
"""

import re
import sys

#filename = "ignore-packages.txt"
filename = sys.argv[1]
regex_list = []

def matches_regex_list(regex_list, string):
    for regex in regex_list:
        if re.match(regex, string):
            return True
    return False

with open(filename, "r") as f:
    for line in f:
        line = line.strip()  # remove leading/trailing whitespace
        if not line or line.startswith("#"):  # skip empty or comment lines
            continue
        regex_list.append(line)  # add non-empty, non-comment lines to list

for line in sys.stdin:
    # Remove any trailing whitespace
    line = line.rstrip()
    # If line matches some regexp then skip it
    if matches_regex_list(regex_list, line):
        continue
    print(line) 
