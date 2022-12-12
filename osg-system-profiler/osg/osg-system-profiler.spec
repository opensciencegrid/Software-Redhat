Summary:   Profiles your system for debugging
Name:      osg-system-profiler
Version:   1.6.0
Release:   2%{?dist}
License:   Apache License, 2.0
Source0:   %{name}-%{version}.tar.gz
BuildArch: noarch

Requires: setroubleshoot-server

%description
The OSG System Profiler runs a series of commands on your system to provide
a clear picture of your environment for debugging.  If you report problems
with your installation, there is a good chance that the person who helps
you will ask for the output of the profiler.

%package viewer
Summary:   Views the output of %{name}
%if 0%{?rhel} >= 8
Requires:  python2-tkinter
%else
Requires:  tkinter
%endif

%description viewer
A GUI for viewing the output of %{name} in a structured manner.

%prep
%setup -q

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_bindir}/osg-installed-versions
%{_libexecdir}/%{name}/gratia-pbs-lsf-config-check

%files viewer
%{_bindir}/%{name}-viewer

%changelog
* Mon Dec 12 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.6.0-2
- Bump to rebuild (SOFTWARE-5384)

* Wed Jun 24 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.6.0-1
- Query multiple python executables, not just `which python` (which may not exist on EL8) (SOFTWARE-4146)

* Thu Apr 23 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.5.0-2
- Build for EL8 (SOFTWARE-4050)

* Mon Jan 27 2020 Diego Davila <didavila@ucsd.edu> - 1.5.0-1
- Include xrootd configuration (SOFTWARE-3876)
- don't verify kernel-devel packages (SOFTWARE-3804)

* Fri Aug 02 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.3-1
- Drop unused files:
    - httpcert.pem
    - tomcat config
    - edg-mkgridmap.log
    - bestman2 logs

* Mon Dec 11 2017 Suchandra Thapa <sthapa@ci.uchicago.edu> - 1.4.2-1
- Update email address given to user (SOFTWARE-3016)

* Thu Oct 05 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.1-1
- Drop osg-version check (SOFTWARE-2916)
- Update instructions for getting help (SOFTWARE-2908)
- Don't include logs for deprecated software (SOFTWARE-2905)

* Mon Jun 27 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-1
- Include dump of tomcat server config (SOFTWARE-1099)
- Create osg-profile.txt in temp dir, do not include old profiles in
  directory dumps (SOFTWARE-1773)

* Mon Apr 18 2016 Matyas Selmeci <matyas@cs.wisc.edu> 1.3.0-1
- Add SELinux audit logs to osg-system-profiler and URL support to
  osg-system-profiler-viewer (SOFTWARE-2275)

* Thu Jan 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.0-1
- Add gratia-pbs-lsf-config-check (SOFTWARE-1674)

* Mon Sep 29 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1.0-1
- Look for enabled gratia probe cronjobs
- Add osg-installed-versions script

* Tue Apr 02 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.11-2
- Fix for looking at fetch-crl.conf in tarball case

* Tue Apr 02 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.11-1
- Work with tarball client as well

* Tue Oct 09 2012 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.10-1
- Save old profiler output
- Update user instructions
- Verify all packages

* Wed May 09 2012 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.9-1
- Show all kernel packages
- Sort environment and some other output

* Mon May 07 2012 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.8-1
- Add viewer subpackage

* Tue May 1 2012 Alain Roy <roy@cs.wisc.edu> 1.0.7-1
- Dump /etc/globus/

* Thu Apr 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.6-1
- Fixed iptables args

* Thu Apr 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.5-1
- Verbose output for iptables

* Wed Apr 18 2012 Alain Roy <roy@cs.wisc.edu> 1.0.4-1
- Include /etc/lcmaps.db in the profile.

* Fri Feb 24 2012 Alain Roy <roy@cs.wisc.edu> 1.0.3-1
- Added more log files (osg-configure & Bestman)

* Fri Jan 13 2012 Alain Roy <roy@cs.wisc.edu> 1.0.2-1
- Fixed minor typo

* Fri Jan 13 2012 Alain Roy <roy@cs.wisc.edu> 1.0.1-1
- Ensure that stderr goes to the profile.

* Thu Jan 12 2012 Alain Roy <roy@cs.wisc.edu> 1.0.0-1
- Rewrite to make it easier to maintain
- Tail some log files
- Dump RPM information
- More Python details

* Tue Aug 23 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.0.4-1
- Added profiler info about CA Certificate installation

* Fri Jul 22 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.0.3-1
- Renamed vdt-system-profiler to osg-system-profiler

* Wed Jul 20 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.2-1
- New release of vdt-system-profiler, now as an upstream source tarball
- Change to use Makefile for installation
- Other spec file simplifications

* Thu Jun 09 2011 matyas@cs.wisc.edu - 0.0.1-1
- Initial spec file
