# Created by pyp2rpm-3.1.2
%global pypi_name toml

Name:           python-%{pypi_name}
Version:        0.9.1
Release:        1%{?dist}
Summary:        Python Library for Tom's Obvious, Minimal Language

License:        License :: OSI Approved :: MIT License
URL:            https://github.com/uiri/toml
Source0:        https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-srpm-macros 
BuildRequires:  python-rpm-macros 
BuildRequires:  python2-rpm-macros 
BuildRequires:  python-setuptools
BuildRequires:  python2-devel

%description
Original repository: https://github.com/uiri/tomlSee also
https://github.com/mojombo/tomlPython module which parses and emits
TOML.Released under the MIT license.Passes
https://github.com/BurntSushi/tomltestSee http://j.xqz.ca/tomlstatus
for up to
date test results.Current Version of the Specification
https://github.com/mojombo/toml/blob/v0.4.0/README.mdQUICK GUIDE pip
install
tomltoml.loads  ...

%package -n     python2-%{pypi_name}
Summary:        Python Library for Tom's Obvious, Minimal Language
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Original repository: https://github.com/uiri/tomlSee also
https://github.com/mojombo/tomlPython module which parses and emits
TOML.Released under the MIT license.Passes
https://github.com/BurntSushi/tomltestSee http://j.xqz.ca/tomlstatus
for up to
date test results.Current Version of the Specification
https://github.com/mojombo/toml/blob/v0.4.0/README.mdQUICK GUIDE pip
install
tomltoml.loads  ...


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build

%install
%py2_install


%files -n python2-%{pypi_name} 
%doc README.rst LICENSE

%{python2_sitelib}/%{pypi_name}.py*
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Wed Jun 29 2016 copr-service - 0.9.1-1
- Initial package.
