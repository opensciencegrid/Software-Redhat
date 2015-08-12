Name:           ndt
Version:        3.6.5
Release:        3%{?dist}
Summary:        Network Diagnostic Tool

Group:          Applications/Networking
License:        BSDish
URL:            http://e2epi.internet2.edu/ndt/
Vendor:         MCNC - Advanced Services
Source0:        %{name}-%{version}.tar.gz
Source1:        ndt-init
Source2:        ndt-sysconfig
Source3:        ndt-logrotate
Source4:        tcpbw100.html
# disabling the janalyze build - should be moved to an external package
Patch0:         ndt-Makefile.in.patch
Patch1:         ndt-configure.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       ndt-server, ndt-client
BuildRequires:  web100_userland, libpcap-devel, jpackage-utils, I2util
BuildRequires:  mysql-connector-odbc, unixODBC-devel, zlib-devel

BuildRequires:  java7-devel
BuildRequires:  jpackage-utils


%description
The Network Diagnostic Tool (NDT) is a client/server program that provides
network configuration and performance testing to a users desktop or laptop
computer.  The system is composed of a client program (command line or java
applet) and a pair of server programs (a webserver and a testing/analysis
engine).  Both command line and web-based clients communicate with a
Web100-enhanced server to perform these diagnostic functions.  Multi-level
results allow novice and expert users to view and understand the test results.

%package client
Summary: NDT client
Group: Applications/Network
Obsoletes: ndt <= 3.6.4
%description client
NDT command line tool for scheduling bandwidth measurements with an NDT
server.

%package server
Summary: NDT server
Group: Applications/Network
Requires: I2util, chkconfig, initscripts, shadow-utils, coreutils
Requires: web100_userland, libpcap
%description server
NDT server that enables end users to run performance tests


%prep
%setup -q

%patch0 -p0
%patch1 -p1

%build
%configure --with-I2util=%{_libdir}

#make %{?_smp_mflags}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%{__install} -D -m 0755 %SOURCE1 %{buildroot}%{_initrddir}/%{name}
%{__install} -D -m 0644 %SOURCE2 %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -D -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -D -m 0755 %SOURCE4 %{buildroot}%{_prefix}/%{name}/

%{__mkdir} -p %{buildroot}%{_localstatedir}/lib/%{name}
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}

%{__rm} -rf %{buildroot}%{_prefix}/%{name}/Tcpbw100*.class
%{__rm} -rf %{buildroot}%{_prefix}/%{name}/serverdata

%clean
rm -rf $RPM_BUILD_ROOT

%post server

/sbin/chkconfig --add %{name} || :

%preun server
if [ $1 = 0 ]; then
	/sbin/service ndt stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del %{name} || :
fi

%files

%files server
%defattr(-,root,root,-)
%{_sbindir}/*
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_prefix}/%{name}
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/log/%{name}
%{_prefix}/%{name}/[^d]*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/man1/analyze.1.gz
%{_mandir}/man1/genplot.1.gz
%{_mandir}/man1/tr-mkmap.1.gz
%{_mandir}/man1/viewtrace.1.gz
%{_bindir}/analyze
%{_bindir}/genplot
%{_bindir}/tr-mkmap
%{_bindir}/viewtrace

%files client
%defattr(-,root,root,-)
%{_mandir}/man1/web100clt.1.gz
%{_bindir}/web100clt
%{_bindir}/ndtclt

%changelog
* Wed Apr 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.6.5-3
- Build with OpenJDK7

* Thu Aug 30 2012 Doug Strain <dstrain@fnal.gov> - 3.6.5-2
- Updated Obsoletes so that OSG clients will update from ndt to ndt-client

* Tue May 16 2012 Kavitha Kumar <kkumar@internet2.edu> - 3.6.5
- Change NDT version 3.6.5, remove RC1

* Tue May 1 2012 Kavitha Kumar <kkumar@internet2.edu> - 3.6.5-1
- Bump NDT version up to 3.6.5

* Fri Sep 30 2011 Aaron Brown <aaron@internet2.edu> - 3.6.4-2
- Bugfix for the init script

* Thu May 26 2011 Aaron Brown <aaron@internet2.edu> - 3.6.4-1
- Bump NDT version to 3.6.4
- Split out RPM into client and server packages
- Fix a bug when compiling on 64-bit hosts

* Wed Jul 29 2009 Tom Throckmorton <throck@mcnc.org> - 3.4.4a-4
- add build support for db logging
- add restart in %post

* Mon Sep 08 2008 Tom Throckmorton <throck@mcnc.org> - 3.4.4a-3
- disable I2util build
- major rework of the init script; use of fakewww managed through /etc/sysconfig/ndt
- relocation of data, log dirs
- add logrotate script
- remove unnecessary files from package

* Wed Sep 03 2008 Tom Throckmorton <throck@mcnc.org> - 3.4.4a-2
- corrected a problem with the admin applet not loading
- included the tcpbw100.html template

* Mon Jul 21 2008 Tom Throckmorton <throck@mcnc.org> - 3.4.4a-1
- initial package build
