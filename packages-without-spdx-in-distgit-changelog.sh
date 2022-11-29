#!/usr/bin/bash

while read -r package; do
       print-distgit-log.sh "$package" |grep -i spdx >/dev/null || echo "$package"
done
