#!/usr/bin/bash

ls rpm-specs/*spec | xargs basename -s .spec > all-packages.txt

cat packages-without-spdx-final.txt | grep -v "valid as old and new and no changelong entry, please check" | awk '{print $1 }' > not-migrated-packages.txt

# Use grep to find lines in file1 that are not in file2
grep -Fxv -f "not-migrated-packages.txt" "all-packages.txt" > already-migrated-packages.txt
