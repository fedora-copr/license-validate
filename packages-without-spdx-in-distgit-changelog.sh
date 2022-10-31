#!/usr/bin/bash

for package in $(cat packages-without-spdx-in-spec-changelog.txt); do
       print-distgit-log.sh "$package" |grep -i spdx >/dev/null || echo "$package"
done
