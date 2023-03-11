#!/usr/bin/bash

ls rpm-specs/*spec | xargs basename -s .spec > all-packages.txt
