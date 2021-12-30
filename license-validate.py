#!/usr/bin/python3
import argparse
import os.path
import sys
from lark import Lark
from lark.exceptions import LarkError

parser = argparse.ArgumentParser(description='Validate Fedora RPM license string.')
parser.add_argument('license', help='license string')
parser.add_argument('--file', help='read the grammar from this file (default /usr/share/license-validate/grammar.lark)')
parser.add_argument('--verbose', '-v', action='count', default=0)
opts = parser.parse_args()

if opts.file:
    filename = opts.file
else:
    filename = "/usr/share/license-validate/grammar.lark"
    if not os.path.exists(filename):
        filename = 'full-grammar.lark'

if not os.path.exists(filename):
    print("The file {0} does not exists.".format(filename))
    sys.exit(128)

with open(filename) as f:
    grammar = f.read()

parser = Lark(grammar)  # Scannerless Earley is the default

try:
    text = opts.license
    parser.parse(text)
    # approved license
    if opts.verbose > 0:
        print("Approved license")
except LarkError as e:
    # not approved license
    print(e)
    if opts.verbose > 0:
        print("Not a valid license string")
    sys.exit(1)
