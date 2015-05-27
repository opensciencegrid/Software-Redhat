#Defining python macros
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif



%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if %{?fedora}%{!?fedora:0} >= 19 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

Name:		xrootd
Epoch:		1
Version:	4.2.0
Release:	2%{?dist}%{?_with_cpp11:.cpp11}%{?_with_clang:.clang}
Summary:	Extended ROOT file server

Group:		System Environment/Daemons
License:	LGPLv3+
URL:		http://xrootd.org/
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	krb5-devel
BuildRequires:	libevent-devel
BuildRequires:	libxml2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	fuse-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	selinux-policy-devel
%if %{use_systemd}
BuildRequires:	systemd
%endif
BuildRequires: python2-devel



%if %{?_with_clang:1}%{!?_with_clang:0}
BuildRequires: clang
%endif


Requires:	%{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-selinux = %{epoch}:%{version}-%{release}
Obsoletes:	%{name} < 1:4.0.0

%description
The Extended root file server consists of a file server called xrootd
and a cluster management server called cmsd.

The xrootd server was developed for the root analysis framework to
serve root files. However, the server is agnostic to file types and
provides POSIX-like access to any type of file.

The cmsd server is the next generation version of the olbd server,
originally developed to cluster and load balance Objectivity/DB AMS
database servers. It provides enhanced capability along with lower
latency and increased throughput.

%package server
Summary:	Xrootd server daemons
Group:		System Environment/Daemons
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	expect
Requires(pre):		shadow-utils
%if %{use_systemd}
Requires(pre):		systemd
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%else
Requires(pre):		chkconfig
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif

%description server
This package contains the xrootd servers without the SELinux support.
Unless you are installing on a system without SELinux also install the
xrootd-selinux package.

%package selinux
Summary:	SELinux policy module for the xrootd server
Group:		System Environment/Daemons
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	selinux-policy
Requires(post):		policycoreutils
Requires(postun):	policycoreutils

%description selinux
This package contains SELinux policy module for the xrootd server package.

%package libs
Summary:	Libraries used by xrootd servers and clients
Group:		System Environment/Libraries
#		Java admin client no longer supported
Obsoletes:	%{name}-client-admin-java < 1:3.3.0
#		Perl admin client no longer supported
Obsoletes:	%{name}-client-admin-perl < 1:4.0.0

%description libs
This package contains libraries used by the xrootd servers and clients.

%package devel
Summary:	Development files for xrootd
Group:		Development/Libraries
Provides:	%{name}-libs-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-libs-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-libs-devel < %{epoch}:%{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
This package contains header files and development libraries for xrootd
development.

%package client-libs
Summary:	Libraries used by xrootd clients
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client-libs
This package contains libraries used by xrootd clients.

%package client-devel
Summary:	Development files for xrootd clients
Group:		Development/Libraries
Provides:	%{name}-cl-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-cl-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-cl-devel < %{epoch}:%{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client-devel
This package contains header files and development libraries for xrootd
client development.

%package server-libs
Summary:	Libraries used by xrootd servers
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description server-libs
This package contains libraries used by xrootd servers.

%package server-devel
Summary:	Development files for xrootd servers
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description server-devel
This package contains header files and development libraries for xrootd
server development.

%package private-devel
Summary:	Legacy xrootd headers
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%description private-devel
This package contains some private xrootd headers. The use of these
headers is strongly discouraged. Backward compatibility between
versions is not guaranteed for these headers.

%package client
Summary:	Xrootd command line client tools
Group:		Applications/Internet
Provides:	%{name}-cl = %{epoch}:%{version}-%{release}
Provides:	%{name}-cl%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-cl < %{epoch}:%{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client
This package contains the command line tools used to communicate with
xrootd servers.

%package fuse
Summary:	Xrootd FUSE tool
Group:		Applications/Internet
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	fuse

%description fuse
This package contains the FUSE (file system in user space) xrootd mount
tool.
#-------------------------------------------------------------------------------                                                                             
# python                                                                                                                                                     
#-------------------------------------------------------------------------------                                                                             
%package python
Summary:        Python bindings for XRootD
Group:          Development/Libraries
Requires:       %{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description python
Python bindings for XRootD

%package doc
Summary:	Developer documentation for the xrootd libraries
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%description doc
This package contains the API documentation of the xrootd libraries.


#-------------------------------------------------------------------------------                                                                             
# tests                                                                                                                                                      
#-------------------------------------------------------------------------------                                                                             
%if %{?_with_tests:1}%{!?_with_tests:0}
%package tests
Summary: CPPUnit tests
Group:   Development/Tools
Requires: %{name}-client = %{epoch}:%{version}-%{release}
%description tests
This package contains a set of CPPUnit tests for xrootd.
%endif


%prep
%setup -q
#%setup -c -n xrootd

%if %{?fedora}%{!?fedora:0} <= 9 && %{?rhel}%{!?rhel:0} <= 5
# Older versions of SELinux do not have policy for open
sed 's/ open / /' -i packaging/common/%{name}.te
%endif

%build
%if %{?_with_cpp11:1}%{!?_with_cpp11:0}
export CXXFLAGS=-std=c++11
%endif

%if %{?_with_clang:1}%{!?_with_clang:0}
export CC=clang
export CXX=clang++
%endif

mkdir build

pushd build
#%cmake ..                                                                                                                                                   
#make %{?_smp_mflags}                                                                                                                                        
#popd 
%if %{?_with_tests:1}%{!?_with_tests:0}
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo -DENABLE_TESTS=TRUE ../
%else
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo ../
%endif

make -i VERBOSE=1 %{?_smp_mflags}
popd

pushd packaging/common
make -f /usr/share/selinux/devel/Makefile
popd

doxygen Doxyfile



%install
rm -rf %{buildroot}

pushd build
make install DESTDIR=%{buildroot}
#cat PYTHON_INSTALLED | sed -e "s|$RPM_BUILD_ROOT||g" > PYTHON_INSTALLED_FILES
popd

# configuration stuff                                                                                                                                        
rm -rf %{buildroot}%{_sysconfdir}/xrootd/*

# Service start-up scripts / unit files
%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -m 644 packaging/common/xrootd@.service %{buildroot}%{_unitdir}
install -m 644 packaging/common/cmsd@.service %{buildroot}%{_unitdir}
install -m 644 packaging/common/frm_xfrd@.service %{buildroot}%{_unitdir}
install -m 644 packaging/common/frm_purged@.service %{buildroot}%{_unitdir}
%else
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p packaging/rhel/xrootd.init %{buildroot}%{_initrddir}/xrootd
install -p packaging/rhel/cmsd.init %{buildroot}%{_initrddir}/cmsd
install -p packaging/rhel/frm_purged.init %{buildroot}%{_initrddir}/frm_purged
install -p packaging/rhel/frm_xfrd.init %{buildroot}%{_initrddir}/frm_xfrd
sed s/%{name}.functions/%{name}-functions/ -i %{buildroot}%{_initrddir}/*
install -m 644 -p packaging/rhel/%{name}.functions \
    %{buildroot}%{_initrddir}/%{name}-functions
install -m 644 -p packaging/rhel/%{name}.sysconfig \
    %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%endif

# Server config
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -p packaging/common/%{name}-clustered.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-clustered.cfg
install -m 644 -p packaging/common/%{name}-standalone.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-standalone.cfg

# Client config
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/client.plugins.d
install -m 644 -p packaging/common/client.conf \
    %{buildroot}%{_sysconfdir}/%{name}/client.conf
install -m 644 -p packaging/common/client-plugin.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/client.plugins.d

chmod 644 %{buildroot}%{_datadir}/%{name}/utils/XrdCmsNotify.pm

sed 's!/usr/bin/env perl!/usr/bin/perl!' -i \
    %{buildroot}%{_datadir}/%{name}/utils/netchk \
    %{buildroot}%{_datadir}/%{name}/utils/XrdCmsNotify.pm \
    %{buildroot}%{_datadir}/%{name}/utils/XrdOlbMonPerf

mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/spool/%{name}

mkdir %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 -p packaging/common/%{name}.logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p %{buildroot}%{_datadir}/selinux/packages/%{name}
install -m 644 -p packaging/common/%{name}.pp \
    %{buildroot}%{_datadir}/selinux/packages/%{name}

# Documentation
mkdir -p %{buildroot}%{_pkgdocdir}
cp -pr doxydoc/html %{buildroot}%{_pkgdocdir}

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post client-libs -p /sbin/ldconfig

%postun client-libs -p /sbin/ldconfig

%post server-libs -p /sbin/ldconfig

%postun server-libs -p /sbin/ldconfig

%pre server
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -s /sbin/nologin \
  -d %{_localstatedir}/spool/%{name} -c "XRootD runtime user" %{name}

# Remove obsolete service
/sbin/service olbd stop >/dev/null 2>&1 || :
/sbin/chkconfig --del olbd >/dev/null 2>&1 || :

%if %{use_systemd}
# Remove old init config when systemd is used
/sbin/service xrootd stop >/dev/null 2>&1 || :
/sbin/service cmsd stop >/dev/null 2>&1 || :
/sbin/service frm_purged stop >/dev/null 2>&1 || :
/sbin/service frm_xfrd stop >/dev/null 2>&1 || :
/sbin/chkconfig --del xrootd 2>&1 || :
/sbin/chkconfig --del cmsd 2>&1 || :
/sbin/chkconfig --del frm_purged 2>&1 || :
/sbin/chkconfig --del frm_xfrd 2>&1 || :
%endif

%if %{use_systemd}

%post server
if [ $1 -eq 1 ] ; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun server
if [ $1 -eq 0 ] ; then
    for DAEMON in xrootd cmsd frm_purged frm xfrd; do
	for INSTANCE in `systemctl | grep $DAEMON@ | awk '{print $1;}'`; do
	    systemctl --no-reload disable $INSTANCE > /dev/null 2>&1 || :
	    systemctl stop $INSTANCE > /dev/null 2>&1 || :
	done
    done
fi

%postun server
if [ $1 -ge 1 ] ; then
    systemctl daemon-reload >/dev/null 2>&1 || :
    for DAEMON in xrootd cmsd frm_purged frm xfrd; do
	for INSTANCE in `systemctl | grep $DAEMON@ | awk '{print $1;}'`; do
	    systemctl try-restart $INSTANCE >/dev/null 2>&1 || :
	done
    done
fi

%else

%post server
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add xrootd
    /sbin/chkconfig --add cmsd
    /sbin/chkconfig --add frm_purged
    /sbin/chkconfig --add frm_xfrd
fi

%preun server
if [ $1 -eq 0 ]; then
    /sbin/service xrootd stop >/dev/null 2>&1 || :
    /sbin/service cmsd stop >/dev/null 2>&1 || :
    /sbin/service frm_purged stop >/dev/null 2>&1 || :
    /sbin/service frm_xfrd stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del xrootd
    /sbin/chkconfig --del cmsd
    /sbin/chkconfig --del frm_purged
    /sbin/chkconfig --del frm_xfrd
fi

%postun server
if [ $1 -ge 1 ]; then
    /sbin/service xrootd condrestart >/dev/null 2>&1 || :
    /sbin/service cmsd condrestart >/dev/null 2>&1 || :
    /sbin/service frm_purged condrestart >/dev/null 2>&1 || :
    /sbin/service frm_xfrd condrestart >/dev/null 2>&1 || :
fi

%endif

%post selinux
/usr/sbin/semodule -i %{_datadir}/selinux/packages/%{name}/%{name}.pp >/dev/null 2>&1 || :

%postun selinux
if [ $1 -eq 0 ] ; then
    /usr/sbin/semodule -r %{name} >/dev/null 2>&1 || :
fi

%files
# Empty

%files server
%{_bindir}/cconfig
%{_bindir}/cmsd
%{_bindir}/cns_ssi
%{_bindir}/frm_admin
%{_bindir}/frm_purged
%{_bindir}/frm_xfragent
%{_bindir}/frm_xfrd
%{_bindir}/mpxstats
%{_bindir}/wait41
%{_bindir}/XrdCnsd
%{_bindir}/xrdmapc
%{_bindir}/xrdpwdadmin
%{_bindir}/xrdsssadmin
%{_bindir}/xrootd
%{_bindir}/xrdpfc_print

%{_mandir}/man8/cmsd.8*
%{_mandir}/man8/cns_ssi.8*
%{_mandir}/man8/frm_admin.8*
%{_mandir}/man8/frm_purged.8*
%{_mandir}/man8/frm_xfragent.8*
%{_mandir}/man8/frm_xfrd.8*
%{_mandir}/man8/mpxstats.8*
%{_mandir}/man8/XrdCnsd.8*
%{_mandir}/man8/xrdpwdadmin.8*
%{_mandir}/man8/xrdsssadmin.8*
%{_mandir}/man8/xrootd.8*
%{_mandir}/man8/xrdpfc_print.8*
%{_datadir}/%{name}
%if %{use_systemd}
%{_unitdir}/*
%else
%{_initrddir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/%{name}/*.cfg
%attr(-,xrootd,xrootd) %{_localstatedir}/log/%{name}
%attr(-,xrootd,xrootd) %{_localstatedir}/spool/%{name}

%files selinux
%{_datadir}/selinux/packages/%{name}/%{name}.pp

%files libs
%{_libdir}/libXrdAppUtils.so.*
%{_libdir}/libXrdCrypto.so.*
%{_libdir}/libXrdCryptoLite.so.*
%{_libdir}/libXrdUtils.so.*
# Plugins
%{_libdir}/libXrdCksCalczcrc32-4.so
%{_libdir}/libXrdCryptossl-4.so
%{_libdir}/libXrdSec*-4.so
%doc COPYING* LICENSE

%files devel
%{_bindir}/xrootd-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/XProtocol
%{_includedir}/%{name}/Xrd
%{_includedir}/%{name}/XrdCks
%{_includedir}/%{name}/XrdNet
%{_includedir}/%{name}/XrdOuc
%{_includedir}/%{name}/XrdSec
%{_includedir}/%{name}/XrdSys
%{_includedir}/%{name}/XrdVersion.hh
%{_libdir}/libXrdAppUtils.so
%{_libdir}/libXrdCrypto.so
%{_libdir}/libXrdCryptoLite.so
%{_libdir}/libXrdUtils.so

%files client-libs
%{_libdir}/libXrdCl.so.*
%{_libdir}/libXrdClient.so.*
%{_libdir}/libXrdFfs.so.*
%{_libdir}/libXrdPosix.so.*
%{_libdir}/libXrdPosixPreload.so.*
# This lib may be used for LD_PRELOAD so the .so link needs to be included
%{_libdir}/libXrdPosixPreload.so
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/client.conf
%dir %{_sysconfdir}/%{name}/client.plugins.d
%config(noreplace) %{_sysconfdir}/%{name}/client.plugins.d/client-plugin.conf.example

%files client-devel
%{_includedir}/%{name}/XrdCl
%{_includedir}/%{name}/XrdClient
%{_includedir}/%{name}/XrdPosix
%{_libdir}/libXrdCl.so
%{_libdir}/libXrdClient.so
%{_libdir}/libXrdFfs.so
%{_libdir}/libXrdPosix.so

%files server-libs
%{_libdir}/libXrdServer.so.*
# Plugins
%{_libdir}/libXrdBwm-4.so
%{_libdir}/libXrdFileCache-4.so
%{_libdir}/libXrdHttp-4.so
%{_libdir}/libXrdOssSIgpfsT-4.so
%{_libdir}/libXrdPss-4.so
%{_libdir}/libXrdXrootd-4.so
%{_libdir}/libXrdThrottle-4.so

%files server-devel
%{_includedir}/%{name}/XrdAcc
%{_includedir}/%{name}/XrdCms
%{_includedir}/%{name}/XrdOss
%{_includedir}/%{name}/XrdSfs
%{_includedir}/%{name}/XrdXrootd
%{_includedir}/%{name}/XrdHttp
%{_libdir}/libXrdServer.so

%files private-devel
%{_includedir}/%{name}/private

%files client
%{_bindir}/xprep
%{_bindir}/xrd
%{_bindir}/xrdadler32
%{_bindir}/xrdcopy
%{_bindir}/xrdcp
%{_bindir}/xrdcp-old
%{_bindir}/xrdfs
%{_bindir}/xrdgsiproxy
%{_bindir}/xrdstagetool
%{_mandir}/man1/xprep.1*
%{_mandir}/man1/xrd.1*
%{_mandir}/man1/xrdadler32.1*
%{_mandir}/man1/xrdcopy.1*
%{_mandir}/man1/xrdcp.1*
%{_mandir}/man1/xrdcp-old.1*
%{_mandir}/man1/xrdfs.1*
%{_mandir}/man1/xrdgsiproxy.1*
%{_mandir}/man1/xrdstagetool.1*

%files fuse
%{_bindir}/xrootdfs
%{_mandir}/man1/xrootdfs.1*

%files python
%{python2_sitearch}/XRootD/*
%{python2_sitearch}/pyxrootd*

%files doc
%doc %{_pkgdocdir}

%changelog
* Wed May 27 2015 Edgar Fajardo <efajardo@physics.ucsd.edu> -1:4.2.0-2
- Fixed the dist tag been twice in the release field

* Tue May 26 2015 Edgar Fajardo <efajardo@physics.ucsd.edu> -1:4.2.0-1
- Update to 4.2.0
- Added some macros for the python bindings

* Mon Dec 08 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.1.1-1
- Update to version 4.1.1
- Drop patch xrootd-signed-char.patch (accepted upstream)

* Fri Nov 28 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.1.0-1
- Update to version 4.1.0
- Install systemd unit files (F21+, EPEL7+)

* Sat Nov 01 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.4-1
- Update to version 4.0.4

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.3-1
- Update to version 4.0.3

* Fri Jul 11 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.1-1
- Update to version 4.0.1
- Split main package into server and selinux
- New main package installs server and selinux
- Drop patches accepted upstream (-32bit, -range, -narrowing)

* Sun Jun 29 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.0-1
- Update to version 4.0.0
- Remove the perl package - no longer part of upstream sources

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 30 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.6-1
- Update to version 3.3.6

* Tue Dec 03 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.5-1
- Update to version 3.3.5

* Tue Nov 19 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.4-1
- Update to version 3.3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.3-1
- Update to version 3.3.3
- Change License tag to LGPLv3+ due to upstream license change

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:3.3.2-2
- Perl 5.18 rebuild

* Sun Apr 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.2-1
- Update to version 3.3.2

* Wed Mar 06 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.1-1
- Update to version 3.3.1
- Remove the java package - no longer part of upstream sources
- Drop patches fixed upstream: xrootd-cryptoload.patch, xrootd-init.patch and
  xrootd-perl.patch
- Drop obsolete patch: xrootd-java.patch
- Add private-devel package for deprecated header files

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.7-1
- Update to version 3.2.7
- Split libs package into libs, client-libs and server-libs
- Split devel package into devel, client-devel and server-devel

* Fri Oct 12 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.5-1
- Update to version 3.2.5

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.2-1
- Update to version 3.2.2

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:3.2.1-2
- Perl 5.16 rebuild

* Thu May 17 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.1-1
- Update to version 3.2.1

* Sat Mar 17 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.1.1-1
- Update to version 3.1.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.5-3
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.5-1
- Update to version 3.0.5

* Mon Jul 18 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-2.1
- Rebuild for new gridsite (EPEL 5 only)

* Tue Jun 28 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-2
- Add missing BuildRequires ncurses-devel

* Tue Jun 28 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-1.1
- Remove xrootdfs man page on EPEL 4

* Mon Jun 27 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-1
- Update to version 3.0.4
- Drop patches fixed upstream: xrootd-man.patch, xrootd-rhel5-no-atomic.patch
- Drop the remaining man-pages copied from root - now provided by upstream

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:3.0.3-3
- Perl mass rebuild

* Mon May 02 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.3-2
- Proper fix for the atomic detection on ppc - no bug in gcc after all

* Sun Apr 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.3-1.1
- Workaround for broken gcc on RHEL5 ppc (rhbz #699149)

* Fri Apr 22 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.3-1
- Update to version 3.0.3
- Use upstream's manpages where available (new in this release)
- Use upstream's start-up scripts (new in this release)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.2-1
- Update to version 3.0.2
- Patch XrdCms makefile to make the Xmi interface public

* Fri Dec 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.0-2
- Rebuilt for updated gridsite package

* Mon Dec 13 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.0-1
- Update to version 3.0.0
- New subpackage - xrootd-fuse
- New version scheme inroduced by upstream - add epoch

* Wed Sep 01 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-5
- Disable threads in doxygen - causes memory corruption on ppc

* Wed Sep 01 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-4
- Add startup scripts for cmsd service that replaces the deprecated
  olbd service

* Fri Jul 09 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-3
- Fix broken jar

* Mon Jun 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-2
- Add LGPLv2+ to License tag due to man pages
- Better package description

* Wed Jun 09 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-1
- Initial packaging
