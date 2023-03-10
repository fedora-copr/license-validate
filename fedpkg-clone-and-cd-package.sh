#!/usr/bin/bash

if [ -d "$1" ]; then
        cd "$1"
        git reset --hard HEAD >/dev/null
        timeout 60 fedpkg pull -- -q  >/dev/null 
else
        timeout 60 fedpkg clone -a "$1" -- -q >/dev/null
        cd "$1"
fi
