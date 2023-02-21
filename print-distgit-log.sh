#!/usr/bin/bash

test -d ~/spdx || mkdir ~/spdx/

pushd ~/spdx/ >/dev/null

if [ -d "$1" ]; then
        cd "$1"
        git reset --hard HEAD
        timeout 60 fedpkg pull
else
        timeout 60 fedpkg clone -a "$1" -- -q >/dev/null
        cd "$1"
fi
git log --pretty=format:%s
popd >/dev/null
