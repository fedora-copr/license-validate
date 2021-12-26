Name:           license-validate
Version:        2
Release:        1%{?dist}
Summary:        Validate SPEC license string

License:        MIT
URL:            https://pagure.io/copr/license-validate/
# source is created by:
# git clone https://pagure.io/copr/license-validate.git
# cd license-validate; tito build --tgz
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

#for test
BuildRequires:  python3dist(lark-parser)
Requires:       python3dist(lark-parser)

%description
Validate whether the license string conforms to Fedora Licensing.

%prep
%autosetup


%build
./create-grammar.py fedora-approved-licenses.txt > full-grammar.lark


%install
mkdir -p %{buildroot}%{_bindir}
install license-validate.py %{buildroot}%{_bindir}/license-validate

mkdir -p %{buildroot}%{_datadir}/%{name}/
install full-grammar.lark %{buildroot}%{_datadir}/%{name}/grammar.lark

%check
./validate-grammar.py full-grammar.lark

%files
%license LICENSE
%doc README.md
%{_bindir}/license-validate
%{_datadir}/%{name}


%changelog
* Sun Dec 26 2021 Miroslav Suchý <msuchy@redhat.com> 2-1
- correctly handle parenthesis (msuchy@redhat.com)
- grammar fixes (msuchy@redhat.com)

* Sun Dec 26 2021 Miroslav Suchý <msuchy@redhat.com> 1-1
- initial package
* Sun Dec 26 2021 msuchy <msuchy@redhat.com>
- 
