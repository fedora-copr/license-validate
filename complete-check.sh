#!/usr/bin/bash

# creates package-license.txt and license.txt
./download-all-fedora-licenses


./packages-without-spdx-in-spec-changelog.sh | tee ./packages-without-spdx-in-spec-changelog.txt | \
# rubygem and rust is handled separately
grep -v '^rubygem-' |grep -v '^rust-' | tee packages-without-spdx-in-spec-changelog-grepped.txt | \
./packages-without-spdx-in-distgit-changelog.sh | tee./packages-without-spdx-in-distgit-changelog.txt | \
./packages-with-invalid-license.sh > packages-without-spdx-final.txt
