#!/usr/bin/bash

if [ -d "$1" ]; then
        cd "$1"
        git reset --hard HEAD >/dev/null
        timeout 60 fedpkg pull -- -q  >/dev/null || echo "Error pulling '$1'"
else
        timeout 60 fedpkg clone -a "$1" -- -q >/dev/null || echo "Error clonnig '$1'"
        cd "$1"
fi
