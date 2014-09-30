Summary:   Profiles your system for debugging
Name:      osg-system-profiler
Version:   1.1.0
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
The OSG System Profiler runs a series of commands on your system to provide
a clear picture of your environment for debugging.  If you report problems
with your installation, there is a good chance that the person who helps
you will ask for the output of the profiler.

%package viewer
Summary:   Views the output of %{name}
Group:     Applications/Grid
Requires:  tkinter

%description viewer
A GUI for viewing the output of %{name} in a structured manner.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/osg-installed-versions

%files viewer
%defattr(-,root,root)
%{_bindir}/%{name}-viewer

%changelog
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
