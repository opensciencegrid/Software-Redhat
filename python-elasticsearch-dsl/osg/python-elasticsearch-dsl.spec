# Created by pyp2rpm-2.0.0
%global pypi_name elasticsearch-dsl

Name:           python-%{pypi_name}
Version:        2.0.0
Release:        1.2%{?dist}
Summary:        Python client for Elasticsearch

License:        ASL 
URL:            https://pypi.python.org/pypi/elasticsearch-dsl
Source0:        elasticsearch-dsl-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
#BuildRequires:  python-mock
#BuildRequires:  pytest
#BuildRequires:  python2-pytest-cov
BuildRequires:  pytz

%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}

%{!?autosetup: %global autosetup %setup -q}

%description
Python client for Elasticsearch

Elasticsearch DSL is a high-level library whose aim is to help with writing and running queries against Elasticsearch. It is built on top of the official low-level client (elasticsearch-py).


%package -n     python2-%{pypi_name}
Summary:        Python client for Elasticsearch
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python-six
Requires:       python-dateutil
Requires:       python-elasticsearch >= 2.0.0
Requires:       python-elasticsearch < 3.0.0
Provides:       python-%{pypi_name} = %{version}-%{release}
%description -n python2-%{pypi_name}
Python client for Elasticsearch


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install


%check
#%{__python2} setup.py test

%files -n python2-%{pypi_name} 
%doc 
%{python2_sitelib}/elasticsearch_dsl
%{python2_sitelib}/elasticsearch_dsl-%{version}-py?.?.egg-info

%changelog
* Thu Apr 06 2017 Carl Edquist <edquist@cs.wisc.edu> - 2.0.0-1.2
- Provides python-elasticsearch-dsl (GRACC-18)

* Tue Nov 15 2016 Carl Edquist <edquist@cs.wisc.edu> - 2.0.0-1.1
- Fixes to build on el6/koji

* Tue Jun 28 2016 Cloud User - 2.0.0-1
- Initial package.
