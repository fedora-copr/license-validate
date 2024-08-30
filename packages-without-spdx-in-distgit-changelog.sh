#!/usr/bin/bash

while read -r package; do
       print-distgit-log.sh "$package" >/tmp/bar ; grep -i spdx </tmp/bar >/dev/null && grep  'msuchy@redhat.com' >/dev/null  </tmp/bar || echo "$package"
done
