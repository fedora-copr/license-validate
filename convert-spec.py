#!/usr/bin/python3
from specfile import Specfile
import subprocess
import sys


def alter_license(tags):
    data = subprocess.Popen(['license-fedora2spdx', tags.license.value], stdout = subprocess.PIPE)
    output = data.communicate()
    if "Warning" in str(output[0]):
        sys.stderr.write("Error: Cannot convert automatically.")
        sys.exit(-1)
    print(tags.license.value)
    print("DBG" , output)

# this is dump, but do the work
filename = sys.argv[1]
specfile = Specfile(filename)

with specfile.sections() as sections:
    for section in sections:
        if section.name.startswith("package"):
            with specfile.tags(section) as tags:
                if 'License' in tags:
                    alter_license(tags)
                    #print(section.name, tags.license.value)
                    #tags.license = "MIT"
specfile.save()
