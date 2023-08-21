#!/usr/bin/python3
import argparse
import json
import os.path
import sys
from lark import Lark, Transformer
from lark.exceptions import LarkError

parser = argparse.ArgumentParser(description='Validate Fedora RPM license string.')
parser.add_argument('license', help='license string')
parser.add_argument('--old', action='store_true', help="validate using old Fedora's shortnames")
parser.add_argument('--file', help='read the grammar from this file (default /usr/share/license-validate/grammar.lark)')
parser.add_argument('--verbose', '-v', action='count', default=0)
opts = parser.parse_args()

def load_licenses():
    data = json.load(open('/usr/share/fedora-license-data/licenses/fedora-licenses.json'))
    LICENSES={}
    # read data from fedora-license-data and populate LICENSES, COUNT and VARIATIONS
    for l in data.keys():
        license_item = data[l].get("license")
        if license_item:
            spdx = license_item["expression"]
            LICENSES[spdx]=license_item
    return LICENSES

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
        if token.value in LICENSES and "not-allowed" in LICENSES[token.value]["status"]:
            print("Warning: {} is not-allowed license".format(token.value))
            if "usage" in LICENSES[token.value]:
                print("{0} can be used under this condition:\n{1}\n".format(token.value, LICENSES[token.value]["usage"]))
        if token.value in LICENSES:
            pass
        elif token in ["(", ")"]:                                                                                                                                                
            pass
        elif token in ["AND", "OR"]:
            pass
        else:
            print("Warning: we do not have SPDX identifier for {}".format(token))
        return token.value



if opts.file:
    filename = opts.file
elif opts.old:
    filename = "/usr/share/license-validate/grammar-shortnames.lark"
else:
    filename = "/usr/share/fedora-license-data/grammar.lark"
    if not os.path.exists(filename):
        filename = 'full-grammar.lark'
if not os.path.exists(filename):
    print("The file {0} does not exists.".format(filename))
    sys.exit(128)

not_allowed_filename = "/usr/share/fedora-license-data/grammar-with-not-allowed.lark"
if not os.path.exists(not_allowed_filename):
    print("The file {0} does not exists.".format(not_allowed_filename))
    sys.exit(128)

with open(filename) as f:
    grammar = f.read()
with open(not_allowed_filename) as f:
    grammar_with_not_allowed = f.read()

LICENSES = load_licenses()

lark_parser = Lark(grammar)  # Scannerless Earley is the default
lark_parser_with_not_allowed = Lark(grammar_with_not_allowed, parser="lalr", keep_all_tokens=True)

try:
    text = opts.license
    tree = lark_parser.parse(text)
    # approved license
    if opts.verbose > 0:
        print("Approved license")
except LarkError as e:
    # not approved license
    if opts.verbose > 0:
        try:
            tree_with_not_allowed = lark_parser_with_not_allowed.parse(text)
            #print("DBG")
            #import pdb;pdb.set_trace()
            T(visit_tokens=True).transform(tree_with_not_allowed)
            print("Uses not-allowed license.")
        except LarkError as ee:
            print(e)
            print("Not a valid license string")
    sys.exit(1)
