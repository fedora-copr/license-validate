#!/usr/bin/bash

test -d ~/spdx || mkdir ~/spdx/

pushd ~/spdx/ >/dev/null

./fedpkg-clone-and-cd-package.sh "$1"
git log --pretty=format:%s
popd >/dev/null
