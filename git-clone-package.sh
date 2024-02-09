#!/usr/bin/bash

test -d ~/spdx || mkdir ~/spdx/

DIR=${PWD}

pushd ~/spdx/ >/dev/null

# the leading dot is important otherwise the change dir will not work
. ${DIR}/fedpkg-clone-and-cd-package.sh "$1"
popd >/dev/null
