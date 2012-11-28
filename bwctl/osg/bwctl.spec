Name: bwctl
Summary: bwctl - network throughput tester
Version: 1.4
Release:        7%{?dist}
License: Apache License v2.0
Group: *Development/Libraries*
URL: http://e2epi.internet2.edu/bwctl/
Source: %{name}-%{version}.tar.gz
Patch0: nonetwork.patch
Packager: Aaron Brown <aaron@internet2.edu>
BuildRequires:  libtool, I2util
Requires: bwctl-client, bwctl-server
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
BWCTL is a command line client application and a scheduling and policy daemon
that wraps Iperf, Thrulay or nuttcp.

%files


%package client
Summary: bwctl client
Group: Applications/Network
Requires:   iperf
%description client
bwctl command line tool for scheduling bandwidth measurements with a bwctl
server.

%package server
Summary: bwctl server
Group: Applications/Network
Requires: I2util, chkconfig, initscripts, shadow-utils, coreutils
Requires:   iperf
%description server
bwctl server

%package devel
Group: Development/Libraries
Summary: bwctl library headers.
%description devel
This package includes header files, and static link libraries for building
applications that use the bwctl library.


# Thrulay and I2Util get installed, but really, shouldn't be instaled.
#%define _unpackaged_files_terminate_build      0

%prep
%setup -q
pwd
%patch0 -p0

%build
%configure --prefix=%{_prefix} --with-thrulay=no --with-I2util=no --enable-nuttcp

make

%install
%makeinstall
%{__install} -D -p -m 0755 conf/bwctld.init %{buildroot}%{_sysconfdir}/rc.d/init.d/bwctld
%{__install} -D -p -m 0755 conf/bwctld.limits.default %{buildroot}%{_sysconfdir}/bwctld/bwctld.limits
%{__install} -D -p -m 0755 conf/bwctld.conf %{buildroot}%{_sysconfdir}/bwctld/bwctld.conf

%clean
rm -rf $RPM_BUILD_ROOT 

%post server
/sbin/chkconfig --add bwctld
if [ "$1" = "1" ]; then
    # If this is a first time install, add the users and enable it by default
	/usr/sbin/useradd -r -s /bin/nologin -d /tmp bwctl || :
fi

# Due to problem in 1.3, init script needs to be disabled.
if [ $1 -gt 1 ]; then
    # Set aside init script to avoid restart behavior in old %postun
    if [ -d %{_defaultdocdir}/bwctl-server-1.3 ]; then
        mv %{_initrddir}/bwctld %{_initrddir}/bwctld.osgpostsave || :
	cp -p /bin/true %{_initrddir}/bwctld
    fi
fi

%posttrans server
if [ -f %{_initrddir}/bwctld.osgpostsave ]; then
    # Restore real init script, if it was set aside in %post
    rm -f %{_initrddir}/bwctld
    mv -f %{_initrddir}/bwctld.osgpostsave %{_initrddir}/bwctld || :
fi


%preun server
if [ "$1" = "0" ]; then
    # If this is an actual uninstall, stop the service and remove its links
    /sbin/service bwctld stop >/dev/null 2>&1
    /sbin/chkconfig --del bwctld
fi

%postun server
if [ "$1" = "0" ]; then
    # If this is an actual uninstall, delete the user after the software has been removed
	/usr/sbin/userdel bwctl || :
fi

%files client
%defattr(-,root,root,0755)
%doc README
%{_bindir}/bwctl
%{_mandir}/man1/bwctl.1.gz

%files server
%defattr(-,root,root,0755)
%doc README contrib/sample_hook.pl
%{_bindir}/bwctld
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/rc.d/init.d/bwctld
%config(noreplace) %{_sysconfdir}/bwctld/*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/libbwlib.a
%{_includedir}/bwctl/*

%changelog
* Wed Nov 27 2012 Doug Strain <dstrain@fnal.gov> - 1.4-7
- Fixed moving behavior of post script

* Wed Nov 27 2012 Doug Strain <dstrain@fnal.gov> - 1.4-5
- Changing post and postun scripts to fix upgrade from 1.3

* Thu Aug 30 2012 Doug Strain <dstrain@fnal.gov> - 1.4-2
- Disabled network startup by default in init.d script

* Fri Aug 20 2010 Tom Throckmorton <throck@mcnc.org> - 1.3-4
- minor spec changes to enable rebuilds via mock
- disable I2util, thrulay at buildtime; enable nuttcp

* Fri Jan 11 2008 aaron@internet2.edu 1.0-1
- Initial RPM
