#!/usr/bin/bash

pushd /tmp >/dev/null
timeout 60 fedpkg clone -a "$1" -- -q >/dev/null
cd "$1"
git log --pretty=format:%s
rm -rf "/tmp/$1"
popd >/dev/null
