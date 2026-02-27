#!/usr/bin/python3
import argparse
import json
import os.path
import sys
from lark import Lark, Transformer
from lark.exceptions import LarkError
from specfile import Specfile

parser = argparse.ArgumentParser(description='Validate Fedora RPM license string.')
parser.add_argument('license', help='license string', nargs='?')
parser.add_argument('--file', help='read the grammar from this file (default /usr/share/license-validate/grammar.lark)')
parser.add_argument('--old', action='store_true', help="validate using old Fedora's shortnames")
parser.add_argument('--package', help='name of the package - can return "valid" for not-allowed license if package is known exception')
parser.add_argument('--spec', help="read the license strings from SPEC file")
parser.add_argument('--verbose', '-v', action='count', default=0)
opts = parser.parse_args()
VALID = True

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

def read_from_spec(filename):
    """ Reads licensens from SPEC file and return list of strings. One for each license tag. """
    specfile = Specfile(filename, force_parse=True)
    result = []
    with specfile.sections() as sections:
        for section in sections:
            if section.name.startswith("package"):
                with specfile.tags(section) as tags:
                    if 'License' in tags:
                        result.append(tags.license.value.expanded_value)
    return result

class T(Transformer):
    def license_item(self, token):
        global VALID
        global LICENSES
        global PACKAGE
        global VERBOSE
        item = token[0]
        if item in LICENSES and "not-allowed" in LICENSES[item]["status"]:
            print("Warning: {} is not-allowed license".format(item))
            if ("usage" in LICENSES[item]) and VERBOSE:
                print("{0} can be used under this condition:\n{1}\n".format(item, LICENSES[item]["usage"]))
            if "packages_with_exceptions" in LICENSES[item] :
                if VERBOSE:
                    print("These packages are known to use this {} license as an exception: {}".format(item, LICENSES[item]["packages_with_exceptions"]))
                if PACKAGE in LICENSES[item]["packages_with_exceptions"]:
                    pass
                else:
                    VALID = False
            else:
                VALID = False
        if item in LICENSES:
            return token


if not opts.license and not opts.spec:
    print("Error: you either have to specify license as a string or use --spec")
    sys.exit(2)

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

PACKAGE = None
if opts.package:
    PACKAGE = opts.package

LICENSES = load_licenses()

lark_parser = Lark(grammar)  # Scannerless Earley is the default
#lark_parser_with_not_allowed = Lark(grammar_with_not_allowed, parser="lalr", keep_all_tokens=True)
lark_parser_with_not_allowed = Lark(grammar_with_not_allowed, keep_all_tokens=True)

if opts.spec:
    licenses = read_from_spec(opts.spec)
else:
    licenses = [opts.license]

VERBOSE = False
if opts.verbose > 0:
    VERBOSE = True

VALID_ALL = True
for text in licenses:
    VALID = True
    try:
        if VERBOSE:
            print(f"License: {text}")
        tree = lark_parser.parse(text)
        # approved license
        if VERBOSE:
            print("Approved license")
    except LarkError as e:
        # not approved license
        try:
            VALID = True
            tree_with_not_allowed = lark_parser_with_not_allowed.parse(text)
            if opts.verbose > 0:
                T(visit_tokens=True).transform(tree_with_not_allowed)
            if VALID and PACKAGE:
                print("Uses not-allowed license, but package is known to be exception.")
            else: 
                print("Uses not-allowed license.")
                VALID = False
        except LarkError as ee:
            VALID = False
            if opts.verbose > 0:
                print(f"License: {text}")
                print(str(e).split("Expected one of")[0])
            print("Not a valid license string")
            if opts.verbose > 0:
                print("Please check https://docs.fedoraproject.org/en-US/legal/all-allowed/")
        if not opts.verbose:
            print("Run with -v option to see more information.")
    VALID_ALL = VALID_ALL and VALID

if not VALID_ALL:
    sys.exit(1)
