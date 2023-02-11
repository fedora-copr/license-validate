#!/usr/bin/bash
rm -rf rpm-specs/*
rm -f final_just_packages.txt

# creates package-license.txt and license.txt
./download-all-fedora-licenses


./packages-without-spdx-in-spec-changelog.sh | tee ./packages-without-spdx-in-spec-changelog.txt | \
# rubygem and rust is handled separately
grep -v '^rubygem-' |grep -v '^rust-' | tee packages-without-spdx-in-spec-changelog-grepped.txt | \
./packages-without-spdx-in-distgit-changelog.sh | tee ./packages-without-spdx-in-distgit-changelog.txt | \
./packages-with-invalid-license.sh > packages-without-spdx-final.txt

cat final_just_packages.txt |sort | uniq > /tmp/final_just_packages.txt
find-package-maintainers /tmp/final_just_packages.txt > packages-without-spdx-final-maintainers.txt
