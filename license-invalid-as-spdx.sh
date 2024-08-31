#!/usr/bin/bash

SPEC="$1"
FILENAME_ALL_PACKAGES="final_just_packages.txt"
POSITIVE=""

grep '^License:' "rpm-specs/${SPEC}.spec" | cut '-d:' -f2- | \
while read -r LICENSE; do 
  if license-validate --old "$LICENSE" >/dev/null;  then
        if license-validate --package "${SPEC}" "$LICENSE" >/dev/null; then
                print-spec-changelog.py "rpm-specs/${SPEC}.spec" > /tmp/spec-changelog.txt
                if grep -i spdx >/dev/null < /tmp/spec-changelog.txt; then
                        # valid as old and new but has changelog entry
                        true
                else
                        print-distgit-log.sh "$package" > /tmp/distgit-changelog.txt
                        if grep -i spdx </tmp/distgit-changelog.txt  >/dev/null && grep  'msuchy@redhat.com' >/dev/null  </tmp/distgit-changelog.txt; then
                                # valid as old and new but has dist-git changelog entry
                                true
                        else
                                echo "$SPEC warning: valid as old and new and no changelong entry, please check"
                                echo "${SPEC}" >> $FILENAME_ALL_PACKAGES
                        fi
                fi
        else
                if license-fedora2spdx "$LICENSE" | grep Warning >/dev/null; then
                        # this is not straight forward conversion
                        echo "$SPEC"
                else
                        SPDXLICENSE=$(license-fedora2spdx "$LICENSE")
                        echo "$SPEC - can be trivially converted to $SPDXLICENSE"
                fi
                echo "${SPEC}" >> $FILENAME_ALL_PACKAGES
        fi
  else
        if license-validate --package "${SPEC}" "$LICENSE" >/dev/null; then
                # not valid as old, but valid as new
                true;
        else
                if [[ "$LICENSE" == *"LicenseRef-Callaway-"* ]]; then
                    echo "$SPEC contains LicenseRef-Callaway, needs to be manually converted"
                else
                        echo "$1 warning: not valid neither as Callaway nor as SPDX, please check"
                        echo "${SPEC}" >> $FILENAME_ALL_PACKAGES
                fi
                echo "${SPEC}" >> $FILENAME_ALL_PACKAGES
        fi
  fi
done
