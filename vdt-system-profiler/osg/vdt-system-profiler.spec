Summary: Profiles your system for install debugging
Name: vdt-system-profiler
Version: 0.0.2
Release: 1%{?dist}
License: Apache License, 2.0
Group: Applications/Grid
Packager: VDT <vdt-support@opensciencegrid.org>
Source0: %{name}-%{version}.tar.gz
AutoReq: yes
AutoProv: yes
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
The VDT System Profiler runs a series of commands on your system to provide
a clear picture of your environment for debugging.  If you report problems
with your installation, there is a good chance that the person who helps
you will ask for the output of the profiler.

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

%changelog
* Wed Jul 20 2011 Tim Cartwright <cat@cs.wisc.edu> - 0.0.2-1
- New release of vdt-system-profiler, now as an upstream source tarball
- Change to use Makefile for installation
- Other spec file simplifications

* Thu Jun 09 2011 matyas@cs.wisc.edu - 0.0.1-1
- Initial spec file
