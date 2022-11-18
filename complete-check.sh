#!/usr/bin/bash

# creates package-license.txt and license.txt
./download-all-fedora-licenses

# creates 
./packages-without-spdx-in-spec-changelog.sh | tee ./packages-without-spdx-in-spec-changelog.txt | \
# rubygem and rust is handled separately
grep -v '^rubygem-' |grep -v '^rust-' > package-license-filtered.txt
mv package-license-filtered.txt packages-without-spdx-in-spec-changelog.txt

./packages-without-spdx-in-distgit-changelog.sh > packages-without-spdx-in-distgit-changelog.txt

for i in $(cat packages-without-spdx-in-distgit-changelog.txt); do
        ./license-invalid-as-spdx.sh "$i"
done > packages-without-spdx-final.txt
