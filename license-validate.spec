Name:           license-validate
Version:        3
Release:        1%{?dist}
Summary:        Validate SPEC license string

License:        MIT
URL:            https://pagure.io/copr/license-validate/
# source is created by:
# git clone https://pagure.io/copr/license-validate.git
# cd license-validate; tito build --tgz
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

# man pages
BuildRequires:  asciidoc
BuildRequires:  libxslt

# for test
BuildRequires:  python3dist(lark-parser)
Requires:       python3dist(lark-parser)


%description
Validate whether the license string conforms to Fedora Licensing.


%prep
%autosetup


%build
./create-grammar.py fedora-approved-licenses.txt > full-grammar.lark
for i in license-validate.1.asciidoc; do
  a2x -d manpage -f manpage "$i"
done


%install
mkdir -p %{buildroot}%{_bindir}
install license-validate.py %{buildroot}%{_bindir}/license-validate

mkdir -p %{buildroot}%{_datadir}/%{name}/
install full-grammar.lark %{buildroot}%{_datadir}/%{name}/grammar.lark

mkdir -p %{buildroot}%{_mandir}/man1
install -m644 license-validate.1 %{buildroot}/%{_mandir}/man1/


%check
./validate-grammar.py full-grammar.lark


%files
%license LICENSE
%doc README.md
%{_bindir}/license-validate
%{_datadir}/%{name}
%doc %{_mandir}/man1/license-validate.1*


%changelog
* Wed Jan 05 2022 Miroslav Suchý <msuchy@redhat.com> 3-1
- fixes for package review
- code cleanup
- catch all lark errors
- allow bad license with or operator
- add comment aboutlicense_item
- add general redistributable license
- add missing OFL license
- add scripts to check all fedora licenses
- add man page
- remove COMMENTS from grammar

* Sun Dec 26 2021 Miroslav Suchý <msuchy@redhat.com> 2-1
- correctly handle parenthesis (msuchy@redhat.com)
- grammar fixes (msuchy@redhat.com)

* Sun Dec 26 2021 Miroslav Suchý <msuchy@redhat.com> 1-1
- initial package
