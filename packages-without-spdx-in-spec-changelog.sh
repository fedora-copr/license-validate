#!/usr/bin/bash

for spec in rpm-specs/*.spec; do
#        print-spec-changelog.py "$spec" |grep -i spdx >/dev/null || echo $(basename "$spec" .spec) 
#         print-spec-changelog.py "$spec" >/tmp/foo ; grep -i spdx >/dev/null </tmp/foo && grep  'msuchy@redhat.com' >/dev/null  </tmp/foo || echo $(basename "$spec" .spec)
         echo $(basename "$spec" .spec)
done
