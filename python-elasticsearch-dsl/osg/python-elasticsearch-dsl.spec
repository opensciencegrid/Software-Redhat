# Created by pyp2rpm-2.0.0
%global pypi_name elasticsearch-dsl

Name:           python-%{pypi_name}
Version:        2.0.0
Release:        1%{?dist}
Summary:        Python client for Elasticsearch

License:        ASL 
URL:            https://pypi.python.org/pypi/elasticsearch-dsl
Source0:        elasticsearch-dsl-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-mock
BuildRequires:  pytest
BuildRequires:  python2-pytest-cov
BuildRequires:  pytz

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
* Tue Jun 28 2016 Cloud User - 2.0.0-1
- Initial package.
