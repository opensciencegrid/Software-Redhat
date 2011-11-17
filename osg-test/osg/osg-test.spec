%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib(1)')}
%endif

Summary:   Tests an OSG Software installation
Name:      osg-test
Version:   0.0.6
Release:   1%{?dist}
License:   Apache License, 2.0
Group:     Applications/Grid
Packager:  VDT <vdt-support@opensciencegrid.org>
Source0:   %{name}-%{version}.tar.gz
AutoReq:   yes
AutoProv:  yes
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires:  python-nose

%description
The OSG Test system runs functional integration tests against an OSG Software
installation.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/osg-test
%{_sbindir}/%{name}
%{python_sitelib}/osgtest
/etc/grid-security/certificates/4eca18ce.*

%changelog
* Tue Nov 16 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.6-1
- New version of upstream software: Better logging and first VOMS-related tests.

* Tue Nov 08 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.5-1
- New version of upstream software: Added GRAM tests.

* Mon Sep 26 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.4-1
- New version of upstream software.

* Thu Sep 15 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.3-1
- Skip the uninstall command when there are no RPMs to remove.

* Thu Sep 15 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.2-1
- Added a command-line option to add extra Yum repos when installing
- Removed the extraneous (and occasionally invalid) user password
- Tightened the verify options for epel- and osg-release

* Mon Sep 12 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.1-2
- Added the python-nose dependency

* Fri Sep 09 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.1-1
- Initial release
