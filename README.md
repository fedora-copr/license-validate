# license-validate

Validate whether license is in approved set

This script checks whether **string** specified in SPEC file conforms to [list of approved licenses](https://fedoraproject.org/wiki/Licensing:Main#Software_License_List).

E.g. `MIT or GPLv1` is good license string, but `BSD and GPL` will fail to validate, because Fedora use `GPLv1` short name for GPL.

This script does **not** check source files and does not check whether the license is actually correct. For this purpose you may use [licensecheck](https://metacpan.org/dist/App-Licensecheck).

Content:

 * `fedora-approved-licenses.txt` - contains list of licenses from [Fedora Licensing:Main](https://fedoraproject.org/wiki/Licensing:Main#Software_License_List). This is manually synced with the wiki. The file can contain empty lines and comments.
 * `grammar.lark` - this file contains BNF grammar for [Lark](https://lark-parser.readthedocs.io/en/latest/). It miss one line: `license_item: "MIT"|"GPLv1"|..."`. This line is added there dynamically by `create-grammar.py`.
 * `create-grammar.py` - read `grammar.lark` and accepts filename as argument (usually `approved-licenses.txt`) and prints complete grammar.

## Quickstart

```
dnf install license-validate
license-validate 'LGPL-2.1-or-later AND GPL-2.0-or-later'
license-fedora2spdx 'GPLv1'
# GPL-1.0-only
```

## Run from checkout

```
./create-grammar.py fedora-approved-licenses.txt > full-grammar.lark
# optionally to test the grammar
./validate-grammar.py full-grammar.lark
./license-validate.py -v --file full-grammar.lark 'GPLv1 or MIT'
```

## LICENSE

MIT
