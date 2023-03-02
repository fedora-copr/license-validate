#!/usr/bin/bash

# SPDX became standard on 2022-07-27
# https://pagure.io/packaging-committee/pull-request/1142#request_diff
# consider everything created after 2022-08-01 as SPDX

test -d ~/spdx || mkdir ~/spdx/

while read -r package; do

        pushd ~/spdx/ >/dev/null

        ./fedpkg-clone-and-cd-package.sh "$package"
        DATE=$(git log --reverse --format="format:%as" --all | head -n 1)
        if [[ "$DATE" < 2022-08-01 ]]; then
                echo "$package"
        fi
        popd >/dev/null
done
