#!/usr/bin/bash

test -d ~/spdx || mkdir ~/spdx/

pushd ~/spdx/ >/dev/null

# the leading dot is important otherwise the change dir will not work
. ./fedpkg-clone-and-cd-package.sh "$1"
git log --pretty=format:%s
popd >/dev/null
