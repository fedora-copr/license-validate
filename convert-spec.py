#!/usr/bin/python3
from specfile import Specfile
import subprocess
import sys
from datetime import datetime

def alter_license(license):
    data = subprocess.Popen(['license-fedora2spdx', license], stdout = subprocess.PIPE)
    output = data.communicate()[0].strip().decode()
    if "Warning" in str(output[0]):
        sys.stderr.write("Error: Cannot convert automatically.")
        sys.exit(-1)
    #print(license)
    #print("DBG" , output)
    return output

# this is dump, but do the work
filename = sys.argv[1]
old_license = sys.argv[2]
new_license = alter_license(old_license)
specfile = Specfile(filename)

with specfile.sections() as sections:
    for section in sections:
        if section.name.startswith("package"):
            with specfile.tags(section) as tags:
                if 'License' in tags:
                    license = tags.license.value
                    if license == old_license:
                        tags.license.value = new_license
                    #print(section.name, tags.license.value)
                    #tags.license = "MIT"
if not specfile.has_autorelease:
    specfile.release = str(int(specfile.expanded_release) + 1)
if not specfile.has_autochangelog:
    specfile.add_changelog_entry(
        f"- convert license to SPDX",
        author='Miroslav Suchý',
        email='msuchy@redhat.com',
        timestamp=datetime.now().date(),
    )
specfile.save()
