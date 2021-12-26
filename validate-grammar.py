#!/usr/bin/python3
import argparse
import sys
from lark import Lark
from lark.exceptions import UnexpectedCharacters

parser = argparse.ArgumentParser(description='Validate Fedora RPM license string.')
parser.add_argument('grammar', help='file with a grammar')
opts = parser.parse_args()

with open(opts.grammar) as f:
    grammar = f.read()

parser = Lark(grammar)  # Scannerless Earley is the default
