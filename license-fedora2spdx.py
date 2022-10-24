#!/usr/bin/python3
import argparse
import os.path
import sys
from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError
import json

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
            token.value = LICENSES[token]
            if COUNT[token] > 1:
                print("Warning: more options how to interpret {}. Possible options: {}".format(
                        token, VARIATIONS[token]))
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
        filename = 'full-grammar.lark'

if not os.path.exists(filename):
    print("The file {0} does not exists.".format(filename))
    sys.exit(128)

with open(filename) as f:
    grammar = f.read()

# read data from rpminspect-data-fedora and populate LICENSES, COUNT and VARIATIONS
for l in data.keys():
    if "spdx_abbrev" in data[l]:
        if data[l].get("approved") != "yes":
            continue
        if "fedora_abbrev" not in data[l]:
            continue
        LICENSES[data[l]["fedora_abbrev"]] = data[l]["spdx_abbrev"]
        COUNT[data[l]["fedora_abbrev"]] = COUNT.get(data[l]["fedora_abbrev"], 0) + 1
        spdx = data[l]["spdx_abbrev"]
        if not spdx:
            spdx = "no-spdx-yet ({})".format(l)
        if VARIATIONS.get(data[l]["fedora_abbrev"]):
            VARIATIONS[data[l]["fedora_abbrev"]].append(spdx)
        else:
            VARIATIONS[data[l]["fedora_abbrev"]] = [spdx]

parser = Lark(grammar, parser="lalr", keep_all_tokens=True)

try:
    text = opts.license
    tree = parser.parse(text)
    print(T(visit_tokens=True).transform(tree))
    # approved license
    if opts.verbose > 0:
        print("Approved license")
except LarkError as e:
    # not approved license
    print("Not a valid license string. Pass '--verbose' to get full parser error.")
    if opts.verbose > 0:
        print(e)
    sys.exit(1)
