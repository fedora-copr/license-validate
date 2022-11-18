#!/usr/bin/bash

SPEC="$1"

LICENSE=$(grep '^License:' "rpm-specs/${SPEC}.spec" | cut '-d:' -f2- )

if license-validate --old "$LICENSE" >/dev/null;  then
        if license-validate "$LICENSE" >/dev/null; then
                echo "$1 warning: valid as old and new and now changelong entry, please check"
        else
                if license-fedora2spdx "$LICENSE" | grep Warning >/dev/null; then
                        # this is not straight forward conversion
                        echo "$1"
                else
                        SPDXLICENSE=$(license-fedora2spdx "$LICENSE")
                        echo "$1 - can be trivialy converted to $SPDXLICENSE"
                fi
        fi
else
        if license-validate "$LICENSE" >/dev/null; then
                true;
        else
                echo "$1 warning: not valid as calaway nor as SPDX, please check"
        fi
fi

