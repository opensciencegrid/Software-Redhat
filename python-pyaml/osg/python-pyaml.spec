# Created by pyp2rpm-3.1.3
%global pypi_name pyaml

Name:           python-%{pypi_name}
Version:        16.12.2
Release:        1.1%{?dist}
Summary:        PyYAML-based module to produce pretty and readable YAML-serialized data

License:        WTFPL
URL:            https://github.com/mk-fg/pretty-yaml
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python-setuptools
BuildRequires:  python2-devel

%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}

%{!?autosetup: %global autosetup %setup -q}

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
* Tue Jun 20 2017 Carl Edquist <edquist@cs.wisc.edu> - 16.12.2-1.1
- fixes for building in koji

* Fri Dec 16 2016 root - 16.12.2-1
- Initial package.
