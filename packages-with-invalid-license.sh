#!/usr/bin/bash
while read -r package; do
       ./license-invalid-as-spdx.sh "$package"
done
