%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:           python-simplejson

Version:        2.0.9
Release:        1%{?dist}
Summary:        Simple, fast, extensible JSON encoder/decoder for Python

Group:          System Environment/Libraries
# The main code is licensed MIT.
# The docs include jquery which is licensed MIT or GPLv2
License: MIT and (MIT or GPLv2)
URL:            http://simplejson.github.com/simplejson/
Source0:        python-simplejson-%{version}.tar.gz 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}


%description
simplejson is a simple, fast, complete, correct and extensible JSON
<http://json.org> encoder and decoder for Python 2.4+. It is pure Python code
with no dependencies, but includes an optional C extension for a serious speed
boost.

The encoder may be subclassed to provide serialization in any kind of
situation, without any special support by the objects to be serialized
(somewhat like pickle).

The decoder can handle incoming JSON strings of any specified encoding (UTF-8
by default).

simplejson is the externally maintained development version of the json library
included with Python 2.6 and Python 3.0, but maintains backwards compatibility
with Python 2.4.


%prep
%setup -q -n python-simplejson-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root=%{buildroot}

%check
nosetests -q

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%{python_sitearch}/*


%changelog
* Thu Aug 2 2012 Alain Roy <roy@cs.wisc.edu> - 2.0.9-1
  Borrowed 2.6.0 spec file from Fedora to build v2.0.9, which is compatible 
  with Python 2.4.

