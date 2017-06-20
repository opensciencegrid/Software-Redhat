# Created by pyp2rpm-3.1.3
%global pypi_name pyaml

Name:           python-%{pypi_name}
Version:        16.12.2
Release:        1%{?dist}
Summary:        PyYAML-based module to produce pretty and readable YAML-serialized data

License:        WTFPL
URL:            https://github.com/mk-fg/pretty-yaml
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-setuptools
BuildRequires:  python2-devel

%description
prettyyaml (or pyaml) PyYAMLbased python module to produce pretty and readable
YAMLserialized data... contents:: :backlinks: nonePrime goal of this module is
to produce humanreadable output that can be easily manipulated and reused, but
maybe with some occasional caveats.One good example of such "caveat" is that
e.g. {'foo': '123'} will serialize to foo: 123, which for PyYAML would be a
bug, ...

%package -n     python2-%{pypi_name}
Summary:        PyYAML-based module to produce pretty and readable YAML-serialized data
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       PyYAML
%description -n python2-%{pypi_name}
prettyyaml (or pyaml) PyYAMLbased python module to produce pretty and readable
YAMLserialized data... contents:: :backlinks: nonePrime goal of this module is
to produce humanreadable output that can be easily manipulated and reused, but
maybe with some occasional caveats.One good example of such "caveat" is that
e.g. {'foo': '123'} will serialize to foo: 123, which for PyYAML would be a
bug, ...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install


%files -n python2-%{pypi_name}
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Fri Dec 16 2016 root - 16.12.2-1
- Initial package.