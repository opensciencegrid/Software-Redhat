Summary: osg-pki-tools
Name: osg-pki-tools
Version: 1.0.3
Release: 1%{?dist}
Source: OSGPKITools-%{version}.tar.gz
License: Apache 2.0
Group: Grid
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: python 
Requires: m2crypto
Requires: python-simplejson

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
install -d %{buildroot}%{_bindir}
install -m 755 osgpkitools/osg-cert-request %{buildroot}%{_bindir}
install -m 755 osgpkitools/osg-cert-retrieve %{buildroot}%{_bindir}
install -m 755 osgpkitools/osg-gridadmin-cert-request %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}/osg
install -m 644 osgpkitools/pki-clients.ini %{buildroot}%{_sysconfdir}/osg
mv -f %{buildroot}%{python_sitelib}/tests %{buildroot}%{python_sitelib}/osgpkitools/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%dir %{python_sitelib}/osgpkitools
%{python_sitelib}/osgpkitools/*.py*
/usr/bin/*
%dir %{_sysconfdir}/osg
%config(noreplace) %{_sysconfdir}/osg/pki-clients.ini

%files tests
%defattr(-,root,root)
%dir %{python_sitelib}/osgpkitools/tests
%{python_sitelib}/osgpkitools/tests/*


%changelog
* Thu Oct 04 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.3-1
- Version update

* Fri Sep 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.2-1
- Version update

* Thu Sep 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.1-1
- Version update
- Add python-simplejson dependency
- Move unit tests
- Rename and move OSGPKIClients.ini
- Remove python-argparse dependency for tests

* Tue Sep 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-4
- Add m2crypto dependency
- Add OSGPKIClients.ini

* Mon Sep 24 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-3
- Use correct sources
- Remove patches, since they're upstream

* Fri Sep 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-2
- Fix imports
- Fix os.system calls
- Catch SystemExit

* Thu Sep 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1
- Initial packaging

