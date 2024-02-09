#!/usr/bin/bash

DIR=${PWD}

pushd ~/spdx/"$1" >/dev/null

git log --pretty=format:%s
popd >/dev/null
