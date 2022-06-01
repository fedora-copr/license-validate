#!/usr/bin/python3

"""
Takes data from `fedora-license-data` and prints the list of short names of
approved licenses.
"""

import json

file_data = open("/usr/share/fedora-license-data/licenses/fedora-licenses.json", "r")
data = json.load(file_data)

licenses_list = []
for license in data.values():
        if license.get("approved") == "yes":
                licenses_list.append(license.get("fedora_abbrev"))

print('\n'.join(licenses_list))

