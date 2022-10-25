#!/usr/bin/bash

for spec in rpm-specs/*; do
        print-spec-changelog.py "$spec" |grep -i spdx >/dev/null || echo $(basename "$spec") 
done
