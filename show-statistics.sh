#!/usr/bin/bash

echo -n "SPEC files: "
ls rpm-specs/*spec |wc -l
 
echo -n "License Tags: "
wc -l < package-license.txt

echo -n "Not SPDX complient: "
grep -v '^$' < packages-without-spdx-final.txt | grep -v "valid as old and new and no changelong entry, please check" | grep -v "contains LicenseRef-Callaway, needs to be manually converted" | wc -l

echo -n "Not converted yet: "
grep -v '^$' < packages-without-spdx-final.txt | grep -v "valid as old and new and no changelong entry, please check"  | wc -l

echo -n "Trivial conversion: "
grep trivial packages-without-spdx-final.txt |wc -l

echo -n "Number of ELN+buildroot packages: "
wc -l < eln-list.txt

echo -n "Number of ELN packages: "
wc -l < eln-without-buildroot.txt

echo -n "Not converted ELN packages: "
wc -l < eln-not-migrated.txt

