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

def increment_last_number(input_string):
    # Split the input string into parts based on the dot
    parts = input_string.split('.')
    
    index = -1
    success = False
    while not success:
        try:
            # Convert the last part to an integer, increment it by 1, and convert it back to string
            parts[index] = str(int(parts[index]) + 1)
            success = True
        except ValueError:
            index -= 1
    
    # Join the parts back into a single string with dots
    return '.'.join(parts)

# this is dump, but do the work
filename = sys.argv[1]
old_license = sys.argv[2]
new_license = alter_license(old_license)
specfile = Specfile(filename)
migrated = False

with specfile.sections() as sections:
    for section in sections:
        if section.name.startswith("package"):
            with specfile.tags(section) as tags:
                if 'License' in tags:
                    license = tags.license.value
                    if license == old_license:
                        tags.license.value = new_license
                        migrated = True
                    #print(section.name, tags.license.value)
                    #tags.license = "MIT"
if migrated:
    if not specfile.has_autorelease:
        specfile.release = str(increment_last_number(specfile.expanded_release))
    if not specfile.has_autochangelog:
        specfile.add_changelog_entry(
            f"- convert license to SPDX",
            author='Miroslav Suchý',
            email='msuchy@redhat.com',
            timestamp=datetime.now().date(),
        )
    specfile.save()
