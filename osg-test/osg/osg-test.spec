%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib(1)')}
%endif

Summary:   Tests an OSG Software installation
Name:      osg-test
Version:   1.4.9
Release:   1%{?dist}
License:   Apache License, 2.0
Group:     Applications/Grid
Packager:  VDT <vdt-support@opensciencegrid.org>
Source0:   %{name}-%{version}.tar.gz
AutoReq:   yes
AutoProv:  yes
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

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
* Tue Mar 04 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.9-1
- Add password to usercert (SOFTWARE-1377)
- Fix condor_ce_trace test (SOFTWARE-1338)
- Update gratia probe dependencies (SOFTWARE-1375)
- Add more errors to yum retry

* Mon Feb 03 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.8-1
- Add retries to package updates
- Use SHA2 CAs/usercerts and test RFC proxies (SOFTWARE-1371)
- Add badskips to globus-job-run tests (SOFTWARE-1363)
- Add preliminary htcondor-ce tests (SOFTWARE-1338)
- Skip osg-configure-cemon tests in OSG 3.2

* Fri Jan 24 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.7-1
- Add retries to package installs
- Downgrade packages that were updated in installation
- Fix bug in osg-release upgrades

* Wed Jan 08 2014 Brian Lin <blin@cs.wisc.edu> - 1.4.6-1
- Increase VOMS admin timeouts
- Clean yum cache after updating osg-release
- Better messages for failed installs

* Tue Dec 17 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.5-1
- Improve yum installation and cleanup

* Mon Nov 25 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.4-1
- All proxies created are now 1024 bits
- Add blahp test and updated PBS setup test accordingly
- Add support for testing updates between OSG versions

* Wed Oct 30 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.3-1
- Add gratia-probe-sge tests
- Add BeStMan debugging
- Additional MySQL backup fixes

* Wed Oct 16 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.2-1
- MySQL backup bug fixes

* Wed Oct 16 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.1-1
- Preserve old MySQL data and restore them on test completion

* Fri Oct 11 2013 Brian Lin <blin@cs.wisc.edu> - 1.4.0-1
- Add creation of OSG CA/CRL and ability to sign host certs

* Wed Oct 9 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.7-1
- Reliability improvements to Gratia tests
- Fixed a file reading bug in monitor_file()
- Added a missing import in the timeout handler
- Removed --quiet option to rpm --verify
- Merge EL5 get_package_envra() fix from the ca-certs branch
- Made the global timeout value a config file option

* Thu Oct 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.6-2
- Bump release for 3.2 testing -- no functional change

* Fri Sep 27 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.6-1
- Fixed package requirements on two RSV tests

* Thu Sep 26 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.5-1
- Many small fixes, especially for VM universe tests

* Fri Sep 20 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.4-1
- Add Java7 specific installation logic

* Fri Sep 20 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.3-1
- New version: fix GUMS tests, add global timeout, add java-version RSV probe
- Fix for monitoring a file that has been log rotated

* Wed Sep 04 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.2-1
- Add GUMS and tarball tests

* Thu Aug 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.1-1
- Fix bug where certain config file options weren't being read

* Wed Aug 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.0-1
- Add support for a configuration file

* Mon Aug 12 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.11-1
- Added gratia probe tests
- Fixed bestman test bugs

* Mon Jul 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.10-1
- New version: Made improvements to core and files library

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-3
- rebuilt

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-2
- Bump to rebuild

* Mon Jul 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9-1
- Fix CVMFS test to work with new CVMFS 2.1

* Fri May 23 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.8-1
- Fix glexec create create user proxy test

* Thu May 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.7-1
- Fix lockfile name for HTCondor 7.8.8

* Wed Apr 10 2013 Brian Lin <blin@cs.wisc.edu> - 1.2.6-1
- New version: Add tests for update installations

* Mon Jan 14 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.5-1
- New version: OkSkip/BadSkip test statuses; updated epel-release-6 rpm filename

* Fri Dec 21 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.4-2
- Remove python-nose dependency

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
