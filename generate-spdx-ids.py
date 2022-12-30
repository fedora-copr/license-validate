#!/usr/bin/python3

"""
Takes data from `fedora-license-data` and prints the list of SPDX abbrevs of
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
    if license_item and set_allowed_values.intersection(set(license_item["status"])):
        licenses_list.append(license_item["expression"])

print('\n'.join(set(licenses_list)))

