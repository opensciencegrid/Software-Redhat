Summary: osg-pki-tools
Name: osg-pki-tools
Version: 1.0
Release: 1%{?dist}
Source: OSGPKITools-%{version}.tar.gz
License: Apache 2.0
Group: Grid
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: python 

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}

%package tests
Summary: tests for osg-pki-tools
Requires: %{name} = %{version}
Group: Grid

%description tests
tests for osg-pki-tools

%prep
%setup -n OSGPKITools-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=%{buildroot}
rm -f %{buildroot}%{python_sitelib}/*.egg-info || :
install -d %{buildroot}%{_sbindir}
install -m 755 osgpkitools/osg-cert-request %{buildroot}%{_sbindir}
install -m 755 osgpkitools/osg-cert-retrieve %{buildroot}%{_sbindir}
install -m 755 osgpkitools/osg-gridadmin-manage %{buildroot}%{_sbindir}
install -m 755 osgpkitools/osg-gridadmin-cert-request %{buildroot}%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%{python_sitelib}/osgpkitools/*
/usr/sbin/*

%files tests
%defattr(-,root,root)
%{python_sitelib}/tests/*


%changelog
* Thu Sep 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1
- Initial packaging

