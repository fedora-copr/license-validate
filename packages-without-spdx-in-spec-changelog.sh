#!/usr/bin/bash

for spec in rpm-specs/*.spec; do
        print-spec-changelog.py "$spec" |grep -i spdx >/dev/null || echo $(basename "$spec" .spec) 
done
