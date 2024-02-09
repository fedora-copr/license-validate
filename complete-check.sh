#!/usr/bin/bash
rm -rf rpm-specs/*
rm -f final_just_packages.txt
rm -f eln-list.txt

wget https://tiny.distro.builders/view-all-source-package-name-list--view-eln.txt -O eln-list.txt
wget https://tiny.distro.builders/view-source-package-name-list--view-eln.txt -O eln-without-buildroot.txt

# creates package-license.txt and license.txt
./download-all-fedora-licenses


./packages-without-spdx-in-spec-changelog.sh | tee ./packages-without-spdx-in-spec-changelog.txt | \
# ignore packages reported by maintainers that are ok, but do not have {spec,git}log entry
./ignore-packages.py ignore-packages.txt | tee packages-without-spdx-in-spec-changelog-grepped.txt | \
# ignore packages that has been already migrated
#./ignore-packages.py already-migrated-packages.txt | tee packages-has-not-been-migrated.txt | \
./git-clone-packages.sh | tee ./packages-with-git-up2date.txt | \
./packages-without-spdx-in-distgit-changelog.sh | tee ./packages-without-spdx-in-distgit-changelog.txt | \
./packages-before-spdx-was-standard.sh | tee ./packages-before-spdx-was-standard.txt | \
./packages-with-invalid-license.sh > packages-without-spdx-final.txt

./generate-done-list.sh

cat final_just_packages.txt |sort | uniq > /tmp/final_just_packages.txt
grep -Fx -f  not-migrated-packages.txt eln-list.txt > eln-not-migrated.txt
./show-statistics.sh
find-package-maintainers /tmp/final_just_packages.txt > packages-without-spdx-final-maintainers.txt
