%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib(1)')}
%endif

Summary:   Tests an OSG Software installation
Name:      osg-test
Version:   1.2.4
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
/etc/grid-security/certificates/bffdd190.*

%changelog
* Wed Dec 19 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.4-1
- New version: some xrootd and fetch-crl test fixes 

* Tue Nov 13 2012 Doug Strain <dstrain@fnal.gov> - 1.2.3-1
- New Version to correct xrootd tests (SL6 GSI now working)

* Wed Oct 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.2-1
- New version of upstream software

* Tue Jul 31 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.1-1
- New version of upstream software: new RSV tests; cleanup fix

* Tue Jun 19 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.2.0-1
- New version of upstream software: better backups, more tests

* Wed May 09 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.1.1-1
- New version of upstream software: improve cleanup, fix RSV test

* Mon Apr 23 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.1.0-1
- New version of upstream software: LOTS of new tests, library code

* Wed Mar 14 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.0.1-1
- New version of upstream software: Bug fixes

* Thu Feb 23 2012 Tim Cartwright <cat@cs.wisc.edu> - 1.0.0-1
- New version of upstream software: Fix cert hashes and bootstrap script

* Tue Feb 21 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.12-1
- New version of upstream software: Cleanup bug, new CA certificate hashes

* Mon Feb 20 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.11-1
- New version of upstream software: Fixed bug when tailing files

* Fri Feb 17 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.10-1
- New version of upstream software: Fixed install target

* Fri Feb 17 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.9-1
- New version of upstream software: New library, gLExec tests.
- First release to be built for EL 5 and 6.

* Thu Jan 19 2012 Tim Cartwright <cat@cs.wisc.edu> - 0.0.8-1
- New version of upstream software: UberFTP tests, small bug fixes.

* Wed Dec 21 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.7-1
- New version of upstream software: VOMS tests; *many* other improvements.

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
