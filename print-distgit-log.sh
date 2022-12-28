#!/usr/bin/bash

test -d /var/tmp/spdx || mkdir /var/tmp/spdx/

pushd /var/tmp/spdx/ >/dev/null

if [ -d "$1" ]; then
        cd "$1"
        timeout 60 fedpkg pull
else
        timeout 60 fedpkg clone -a "$1" -- -q >/dev/null
        cd "$1"
fi
git log --pretty=format:%s
popd >/dev/null
