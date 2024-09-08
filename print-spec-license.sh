#!/usr/bin/bash

NAME=$1
RETURN=0
pushd ~/spdx/"$NAME"  >/dev/null
if [ -f "$NAME.spec" ]; then
        rpmspec -q --qf '%{license}\n' --define='_sourcedir .' "$NAME.spec" >/dev/null  2>/dev/null || RETURN=1
fi
popd >/dev/null
exit $RETURN
