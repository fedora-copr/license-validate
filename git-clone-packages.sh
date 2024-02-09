#!/usr/bin/bash

while read -r package; do
       git-clone-package.sh "$package"
       echo "$package"
done
