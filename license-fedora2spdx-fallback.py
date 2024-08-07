#!/usr/bin/python3
""" Copy of license-fedora2spdx but:
when license cannot be converted 1:1 it will convert it to License-Callaway-*
Public domain -> LicenseRef-Callaway-Public-Domain
Freely redistributable without restrictions -> LicenseRef-Callaway-Freely-redistributable-without-restrictions
Freely redistributable, no modification permitted -> LicenseRef-Callaway-Freely-redistributable-no-modification-permitted
Copyright only -> LicenseRef-Callaway-Copyright-only
"""
import argparse
import os.path
import sys
from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError
import json

allowed_values = [
    "allowed",
    "allowed-content",
    "allowed-documentation",
    "allowed-fonts",
    "allowed-firmware",
]
set_allowed_values = set(allowed_values)

class T(Transformer):
    def license_item(self, s):
        return str(s[0])
    def license(self, s):
        return " ".join(s)
    def start(self, s):
        return s[0]
    def left_parenthesis(self, s):
        return '('
    def right_parenthesis(self, s):
        return ')'
    def operator(self, s):
        return str(s[0]) 
    def __default_token__(self, token):
        if token.value in LICENSES:
            if COUNT[token] > 1:
                token.value = f"License-Callaway-{token.value}"
            else:
                token.value = LICENSES[token]
        elif token in ["(", ")"]:
            pass
        elif token in ["and", "or"]:
            token.value = token.upper()
        else:
            print("Warning: we do not have SPDX identifier for {}".format(token))
        return token.value


parser = argparse.ArgumentParser(description='Converts old Fedora license string to SPDX identifier.')
parser.add_argument('license', help='license string')
parser.add_argument('--file', help='read the grammar from this file (default /usr/share/license-validate/grammar-shortnames.lark)')
parser.add_argument('--verbose', '-v', action='count', default=0)
opts = parser.parse_args()

data = json.load(open('/usr/share/fedora-license-data/licenses/fedora-licenses.json'))
LICENSES={}
COUNT={}
VARIATIONS={}

if opts.file:
    filename = opts.file
else:
    filename = "/usr/share/license-validate/grammar-shortnames.lark"
    if not os.path.exists(filename):
        filename = 'full-grammar-shortnames.lark'

if not os.path.exists(filename):
    print("The file {0} does not exists.".format(filename))
    sys.exit(128)

with open(filename) as f:
    grammar = f.read()

# read data from fedora-license-data and populate LICENSES, COUNT and VARIATIONS
for l in data.keys():
    license_item = data[l].get("license")
    fedora_item = data[l].get("fedora")
    if license_item:
        if not set_allowed_values.intersection(set(license_item["status"])):
            continue
        if not fedora_item or not fedora_item["legacy-abbreviation"]:
            continue
        for legacy_abbrev in fedora_item["legacy-abbreviation"]:
            spdx = license_item["expression"]
            LICENSES[legacy_abbrev] = spdx
            COUNT[legacy_abbrev] = COUNT.get(legacy_abbrev, 0) + 1
            if not spdx:
                spdx = "no-spdx-yet ({})".format(l)
            if VARIATIONS.get(legacy_abbrev):
                if spdx not in VARIATIONS[legacy_abbrev]:
                    VARIATIONS[legacy_abbrev].append(spdx)
            else:
                VARIATIONS[legacy_abbrev] = [spdx]

LICENSES["Public domain"] = "LicenseRef-Callaway-Public-Domain"
LICENSES["Freely redistributable without restrictions"] = "LicenseRef-Callaway-Freely-redistributable-without-restrictions"
LICENSES["Freely redistributable, no modification permitted"] = "LicenseRef-Callaway-Freely-redistributable-no-modification-permitted"
LICENSES["Copyright only"] = "LicenseRef-Callaway-Copyright-only"

parser = Lark(grammar, parser="lalr", keep_all_tokens=True)

def check_if_already_spdx(message):
    # check if it is already SPDX formula
    filename = "/usr/share/fedora-license-data/grammar.lark"
    with open(filename) as f:
        grammar = f.read()
    new_parser = Lark(grammar)
    try:
        new_parser.parse(text)
        print(message)
    except LarkError as e:
        pass

try:
    text = opts.license
    tree = parser.parse(text)
    result = T(visit_tokens=True).transform(tree)
    result = result.replace("( ", "(")
    result = result.replace(" )", ")")
    print(result)
    # approved license
    if opts.verbose > 0:
        print("Approved license")
    check_if_already_spdx("""
Note: the input is already valid SPDX formula, But that may be a coincidence,
because the legacy identifier represented the whole family of licenses.
Please check if the license would match one of the licenses above.
""")
except LarkError as e:
    # not approved license
    print("Not a valid license string in legacy syntax. Pass '--verbose' to get full parser error.")
    if opts.verbose > 0:
        print(e)
    check_if_already_spdx("Note: the input is already valid SPDX formula")
    sys.exit(1)
