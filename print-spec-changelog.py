#!/usr/bin/python3
from specfile import Specfile
import sys

# this is dump, but do the work
filename = sys.argv[1]
specfile = Specfile(filename, force_parse=True)

with specfile.sections() as sections:
    print(sections.changelog)
