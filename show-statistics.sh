#!/usr/bin/bash

echo -n "License Tags"
wc -l package-license.txt

echo -n "Not converted yet"
wc -l packages-without-spdx-final.txt

echo -n "Trivial conversion: "
grep trivial packages-without-spdx-final.txt |wc -l
