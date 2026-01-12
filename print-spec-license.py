#!/usr/bin/python3
import logging
import sys
from specfile import Specfile

logger = logging.getLogger('specfile.spec_parser')
logger.setLevel(logging.CRITICAL)

# this is dump, but do the work
filename = sys.argv[1]
specfile = Specfile(filename, force_parse=True)
#print('dbg\n')
with specfile.sections() as sections:
    for section in sections:
        if section.name.startswith("package"):
            with specfile.tags(section) as tags:
                if 'License' in tags:
                    license = tags.license.value
                    print(license)
