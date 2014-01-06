%{!?perl_vendorarch: %global perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}

%{?perl_default_filter}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		xrootd
Epoch:		1
Version:	3.3.5
Release:	1.1%{?dist}
Summary:	Extended ROOT file server

Group:		System Environment/Daemons
License:	LGPLv3+
URL:		http://xrootd.org/
Source0:	http://xrootd.org/download/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
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
%if %{?fedora}%{!?fedora:0} >= 7 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	perl-devel
%else
BuildRequires:	perl
%endif
BuildRequires:	swig
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif

Provides:	%{name}-server = %{epoch}:%{version}-%{release}
Provides:	%{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-server < %{epoch}:%{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}

Requires(pre):		shadow-utils
Requires(pre):		chkconfig
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

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

%package libs
Summary:	Libraries used by xrootd servers and clients
Group:		System Environment/Libraries
#		Java admin client no longer supported
Obsoletes:	%{name}-client-admin-java < 1:3.3.0

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

%package client-admin-perl
Summary:	Xrootd client administration Perl module
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description client-admin-perl
This package contains a swig generated xrootd client administration
Perl module.

%package doc
Summary:	Developer documentation for the xrootd libraries
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%description doc
This package contains the API documentation of the xrootd libraries.

%package server
Summary:        Transitional package for xrootd server
Group:          System Environment/Daemons
Requires:       xrootd >= 1:3.3.1

%description server
A transitional package to ease the upgrade path from pre-3.3.1 to 3.3.1.

%prep
%setup -q

%build
mkdir build

pushd build
PERLPATH=$(eval "`perl -V:archlib`"; echo $archlib/CORE)
%cmake -DPERL_LIBRARY=$PERLPATH/libperl.so -DPERL_INCLUDE_PATH=$PERLPATH ..
make %{?_smp_mflags}
popd

doxygen Doxyfile

%install
rm -rf %{buildroot}

pushd build
make install DESTDIR=%{buildroot}
popd

# Perl module
mkdir -p %{buildroot}%{perl_vendorarch}/auto/XrdClientAdmin
mv %{buildroot}/%{_libdir}/XrdClientAdmin.pm \
   %{buildroot}%{perl_vendorarch}
mv %{buildroot}/%{_libdir}/XrdClientAdmin.so \
   %{buildroot}%{perl_vendorarch}/auto/XrdClientAdmin

# Service start-up scripts et al.
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

install -p packaging/rhel/cmsd.init %{buildroot}%{_initrddir}/cmsd
install -p packaging/rhel/frm_purged.init %{buildroot}%{_initrddir}/frm_purged
install -p packaging/rhel/frm_xfrd.init %{buildroot}%{_initrddir}/frm_xfrd
install -p packaging/rhel/%{name}.init %{buildroot}%{_initrddir}/%{name}

sed s/%{name}.functions/%{name}-functions/ -i %{buildroot}%{_initrddir}/*

install -m 644 -p packaging/rhel/%{name}.functions \
    %{buildroot}%{_initrddir}/%{name}-functions

sed -e 's/XROOTD_USER=daemon/XROOTD_USER=%{name}/g' \
    -e 's/XROOTD_GROUP=daemon/XROOTD_GROUP=%{name}/g' \
    packaging/rhel/%{name}.sysconfig > \
    %{buildroot}%{_sysconfdir}/sysconfig/%{name}
chmod 644 %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -m 644 packaging/common/%{name}-clustered.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-clustered.cfg
install -m 644 packaging/common/%{name}-standalone.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-standalone.cfg

chmod 644 %{buildroot}%{_datadir}/%{name}/utils/XrdCmsNotify.pm

sed 's!/usr/bin/env perl!/usr/bin/perl!' -i \
    %{buildroot}%{_datadir}/%{name}/utils/netchk \
    %{buildroot}%{_datadir}/%{name}/utils/XrdCmsNotify.pm \
    %{buildroot}%{_datadir}/%{name}/utils/XrdOlbMonPerf

mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/spool/%{name}

mkdir %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

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

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -s /sbin/nologin \
  -d %{_localstatedir}/spool/%{name} -c "XRootD runtime user" %{name}

# Remove obsolete service
/sbin/service olbd stop >/dev/null 2>&1 || :
/sbin/chkconfig --del olbd >/dev/null 2>&1 || :

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
    /sbin/chkconfig --add cmsd
    /sbin/chkconfig --add frm_purged
    /sbin/chkconfig --add frm_xfrd
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/service cmsd stop >/dev/null 2>&1 || :
    /sbin/service frm_purged stop >/dev/null 2>&1 || :
    /sbin/service frm_xfrd stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
    /sbin/chkconfig --del cmsd
    /sbin/chkconfig --del frm_purged
    /sbin/chkconfig --del frm_xfrd
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
    /sbin/service cmsd condrestart >/dev/null 2>&1 || :
    /sbin/service frm_purged condrestart >/dev/null 2>&1 || :
    /sbin/service frm_xfrd condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
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
%{_bindir}/xrdpwdadmin
%{_bindir}/xrdsssadmin
%{_bindir}/%{name}
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
%{_mandir}/man8/%{name}.8*
%{_datadir}/%{name}
%{_initrddir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_sysconfdir}/%{name}
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/%{name}/*.cfg
%attr(-,xrootd,xrootd) %{_localstatedir}/log/%{name}
%attr(-,xrootd,xrootd) %{_localstatedir}/spool/%{name}

%files libs
%defattr(-,root,root,-)
%{_libdir}/libXrdAppUtils.so.*
%{_libdir}/libXrdCksCalczcrc32.so.*
%{_libdir}/libXrdCrypto.so.*
%{_libdir}/libXrdCryptoLite.so.*
%{_libdir}/libXrdCryptossl.so.*
%{_libdir}/libXrdMain.so.*
%{_libdir}/libXrdSec*.so.*
%{_libdir}/libXrdUtils.so.*
# Some of the libraries are used as plugins - need the .so symlink at runtime
%{_libdir}/libXrdCksCalczcrc32.so
%{_libdir}/libXrdCryptossl.so
%{_libdir}/libXrdSec*.so
%doc COPYING* LICENSE

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/XProtocol
%{_includedir}/%{name}/Xrd
%{_includedir}/%{name}/XrdCks
%{_includedir}/%{name}/XrdNet
%{_includedir}/%{name}/XrdOuc
%{_includedir}/%{name}/XrdSec
%{_includedir}/%{name}/XrdSys
%{_includedir}/%{name}/XrdVersion.hh
%{_includedir}/%{name}/XrdVersionPlugin.hh
# These libraries are not used as plugins
%{_libdir}/libXrdAppUtils.so
%{_libdir}/libXrdCrypto.so
%{_libdir}/libXrdCryptoLite.so
%{_libdir}/libXrdMain.so
%{_libdir}/libXrdUtils.so

%files client-libs
%defattr(-,root,root,-)
%{_libdir}/libXrdCl.so.*
%{_libdir}/libXrdClient.so.*
%{_libdir}/libXrdFfs.so.*
%{_libdir}/libXrdPosix.so.*
%{_libdir}/libXrdPosixPreload.so.*
# Some of the libraries are used as plugins - need the .so symlink at runtime
%{_libdir}/libXrdPosixPreload.so

%files client-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/XrdCl
%{_includedir}/%{name}/XrdClient
%{_includedir}/%{name}/XrdPosix
# These libraries are not used as plugins
%{_libdir}/libXrdCl.so
%{_libdir}/libXrdClient.so
%{_libdir}/libXrdFfs.so
%{_libdir}/libXrdPosix.so

%files server-libs
%defattr(-,root,root,-)
%{_libdir}/libXrdBwm.so.*
%{_libdir}/libXrdPss.so.*
%{_libdir}/libXrdOfs.so.*
%{_libdir}/libXrdServer.so.*
%{_libdir}/libXrdXrootd.so.*
# Some of the libraries are used as plugins - need the .so symlink at runtime
%{_libdir}/libXrdBwm.so
%{_libdir}/libXrdPss.so
%{_libdir}/libXrdXrootd.so

%files server-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/XrdAcc
%{_includedir}/%{name}/XrdCms
%{_includedir}/%{name}/XrdOss
%{_includedir}/%{name}/XrdSfs
%{_includedir}/%{name}/XrdXrootd
# These libraries are not used as plugins
%{_libdir}/libXrdOfs.so
%{_libdir}/libXrdServer.so

%files private-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/private

%files client
%defattr(-,root,root,-)
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
%defattr(-,root,root,-)
%{_bindir}/xrootdfs
%{_mandir}/man1/xrootdfs.1*
%dir %{_sysconfdir}/%{name}

%files client-admin-perl
%defattr(-,root,root,-)
%{perl_vendorarch}/XrdClientAdmin.pm
%{perl_vendorarch}/auto/XrdClientAdmin

%files doc
%defattr(-,root,root,-)
%doc %{_pkgdocdir}

%changelog
* Mon Jan 06 2014 Matyas Selmeci <matyas@cs.wisc.edu> - 1:3.3.5-1.1.osg
- Merge OSG changes (SOFTWARE-1322)

* Tue Dec 03 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.5-1
- Update to version 3.3.5

* Tue Nov 19 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.4-1
- Update to version 3.3.4

* Mon Oct 14 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1:3.3.3-1.1.osg
- Merge OSG changes

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.3-1
- Update to version 3.3.3
- Change License tag to LGPLv3+ due to upstream license change

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:3.3.2-2
- Perl 5.18 rebuild

* Sun Apr 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.2-1
- Update to version 3.3.2

* Tue Apr 23 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1:3.3.1-1.2.osg
- Add xrootd-server dummy package

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
