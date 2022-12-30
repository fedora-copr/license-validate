#!/usr/bin/python3

"""
Takes data from `fedora-license-data` and prints the list of short names of
approved licenses.
"""

import json

allowed_values = [
    "allowed",
    "allowed-content",
    "allowed-documentation",
    "allowed-fonts",
    "allowed-firmware",
]
set_allowed_values = set(allowed_values)

file_data = open("/usr/share/fedora-license-data/licenses/fedora-licenses.json", "r")
data = json.load(file_data)

licenses_list = []
for license in data.values():
        license_item = license.get("license")
        fedora_item = license.get("fedora")
        if license_item and set_allowed_values.intersection(set(license_item["status"])) and \
                fedora_item and fedora_item["legacy-abbreviation"]:
                licenses_list.extend(fedora_item["legacy-abbreviation"])

print('\n'.join(licenses_list))

