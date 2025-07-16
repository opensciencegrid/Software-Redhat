# OSG additions
%if 0%{?osg:1}%{!?osg:0} && 0%{?rhel} < 9
    # Make available the --without-compat argument, i.e., enable compat by default
    %bcond_without compat
%else
    # Make available the --with-compat argument, i.e., disable compat by default
    %bcond_with    compat
%endif

%bcond_with    asan
%bcond_with    ceph
%bcond_with    clang
%bcond_with    debug
%bcond_without docs
%bcond_with    tests

# This is the directory the tarball extracts to. This may be "xrootd" or "xrootd-%%{version}" depending on where the tarball was downloaded from.
# GitHub releases use "xrootd-%%{version}"
%global build_dir xrootd-%{version}

#-------------------------------------------------------------------------------
# Helper macros
#-------------------------------------------------------------------------------
%if %{with ceph11}
    %define with_ceph 1
%endif

%global compat_version 4.12.6

# Remove default rpm python bytecompiling scripts
%global __os_install_post \
    %(echo '%{__os_install_post}' | \
      sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g \
              s!/usr/lib[^[:space:]]*/brp-python-hardlink[[:space:]].*$!!g')

#-------------------------------------------------------------------------------
# Package definitions
#-------------------------------------------------------------------------------
Name:		xrootd
Epoch:		1
Version:	5.8.4
Release:	1.1%{?dist}%{?with_clang:.clang}%{?with_asan:.asan}
Summary:	Extended ROOT File Server
Group:		System Environment/Daemons
License:	LGPL-3.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND curl AND MIT AND Zlib
URL:		https://xrootd.slac.stanford.edu


Source0:   xrootd-%{version}.tar.gz

# always include the tarball in the SRPM even if we don't build it because the
# SRPM build may have a different build environment than the RPM build
Source1:   xrootd-%{compat_version}.tar.gz

# PelicanPlatform/xrootd #1 (xrootd/xrootd #1868):
Patch1: 0001-1-Allow-hostname-used-by-XRootD-to-be-overridden-by~7c119b0.patch
# PelicanPlatform/xrootd #4 (xrootd/xrootd #2269):
Patch2: 0002-4-XrdTls-Allow-disabling-of-X.509-client-auth~18e1c81.patch
# PelicanPlatform/xrootd #6 (xrootd/xrootd #2397):
Patch3: 0003-6-XrdSciTokens-Handle-multiple-authorization-token-s~b82ddc3.patch
# PelicanPlatform/xrootd #14 (no upstream):
Patch4: 0004-14-XrdHttp-Undo-HTTP-PUT-response-code-change~43ed40b.patch
# Next 2: PelicanPlatform/xrootd #23
Patch5: 0005-23-Re-engineer-concurrency-limits-for-throttles~39fea57.patch
Patch6: 0006-23-Modify-XrdThrottle-to-be-an-OSS-plugin~921fef5.patch
# PelicanPlatform/xrootd #25
Patch7: 0007-25-XRootD-s-xml-response-for-PROPFIND-will-now-inclu~aacf631.patch
# PelicanPlatform/xrootd #32 (xrootd/xrootd #2472)
Patch8: 0008-32-Enable-write-through-mode-for-cache~330eac1.patch

BuildRequires:	cmake
BuildRequires:	krb5-devel
BuildRequires:	readline-devel
BuildRequires:	fuse-devel
BuildRequires:	libxml2-devel
BuildRequires:	krb5-devel
BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel
BuildRequires:	libcurl-devel
BuildRequires:	libuuid-devel
BuildRequires:	voms-devel >= 2.0.6
BuildRequires:	git
BuildRequires:	pkgconfig
BuildRequires:	libmacaroons-devel
BuildRequires:	json-c-devel

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

BuildRequires:	openssl-devel

BuildRequires:	selinux-policy-devel

%if %{with tests}
BuildRequires:	cppunit-devel
BuildRequires:	gtest-devel
%endif

%if %{with ceph}
    %if %{with ceph11}
BuildRequires:	librados-devel >= 11.0
BuildRequires:	libradosstriper-devel >= 11.0
    %else
BuildRequires:	ceph-devel >= 0.87
    %endif
%endif

BuildRequires:	davix-devel

%if %{with docs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif

%if %{with clang}
BuildRequires:	clang
%endif

%if %{with asan}
BuildRequires:	libasan
Requires: libasan
%endif

BuildRequires:	scitokens-cpp-devel

%if %{with isal}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	yasm
%endif

Requires:	%{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-selinux = %{epoch}:%{version}-%{release}

BuildRequires:	systemd
BuildRequires:	systemd-devel
Requires(pre):		systemd
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

BuildRequires:	gcc-c++

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

#-------------------------------------------------------------------------------
# libs
#-------------------------------------------------------------------------------
%package libs
Summary:	Libraries used by XRootD servers and clients
Group:		System Environment/Libraries

%description libs
This package contains libraries used by the XRootD servers and clients.

#-------------------------------------------------------------------------------
# devel
#------------------------------------------------------------------------------
%package devel
Summary:	Development files for XRootD
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
This package contains header files and development libraries for XRootD
development.

#-------------------------------------------------------------------------------
# client-libs
#-------------------------------------------------------------------------------
%package client-libs
Summary:	Libraries used by XRootD clients
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client-libs
This package contains libraries used by XRootD clients.

#-------------------------------------------------------------------------------
# client-devel
#-------------------------------------------------------------------------------
%package client-devel
Summary:	Development files for XRootD clients
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client-devel
This package contains header files and development libraries for XRootD
client development.

#-------------------------------------------------------------------------------
# server-libs
#-------------------------------------------------------------------------------
%package server-libs
Summary:	Libraries used by XRootD servers
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:  xrootd-macaroons
Obsoletes:  xrootd-tpc

%description server-libs
This package contains libraries used by XRootD servers.

#-------------------------------------------------------------------------------
# server-devel
#-------------------------------------------------------------------------------
%package server-devel
Summary:	Development files for XRootD servers
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description server-devel
This package contains header files and development libraries for XRootD
server development.

#-------------------------------------------------------------------------------
# private devel
#-------------------------------------------------------------------------------
%package private-devel
Summary:	Private XRootD headers
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description private-devel
This package contains some private XRootD headers. Backward and forward
compatibility between versions is not guaranteed for these headers.

#-------------------------------------------------------------------------------
# client
#-------------------------------------------------------------------------------
%package client
Summary:	XRootD command line client tools
Group:		Applications/Internet
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client
This package contains the command line tools used to communicate with
XRootD servers.

#-------------------------------------------------------------------------------
# server
#-------------------------------------------------------------------------------
%package server
Summary:   Extended ROOT file server
Group:     System Environment/Daemons
Requires:  %{name}-libs        = %{epoch}:%{version}-%{release}
Requires:  %{name}-client-libs = %{epoch}:%{version}-%{release}
Requires:  %{name}-server-libs = %{epoch}:%{version}-%{release}
Requires:  expect

%description server
XRootD server binaries

#-------------------------------------------------------------------------------
# fuse
#-------------------------------------------------------------------------------
%package fuse
Summary:	XRootD FUSE tool
Group:		Applications/Internet
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	fuse

%description fuse
This package contains the FUSE (file system in user space) XRootD mount
tool.

#-------------------------------------------------------------------------------
# Python bindings
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# python3
#-------------------------------------------------------------------------------
%package -n python%{python3_pkgversion}-%{name}
Summary:       Python 3 bindings for XRootD
Group:         Development/Libraries
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
Requires:      %{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}
Python 3 bindings for XRootD

%if %{with docs}
#-------------------------------------------------------------------------------
# doc
#-------------------------------------------------------------------------------
%package doc
Summary:	Developer documentation for the xrootd libraries
Group:		Documentation
# Not noarch: generated documentation different between noarch packages built on different arches
#BuildArch:	noarch

%description doc
This package contains the API documentation of the xrootd libraries.

%endif
#-------------------------------------------------------------------------------
# selinux
#-------------------------------------------------------------------------------
%package selinux
Summary:	 SELinux policy extensions for xrootd.
Group:		 System Environment/Base
BuildArch: noarch
Requires(post):   policycoreutils
Requires(postun): policycoreutils
Requires:         selinux-policy

%description selinux
SELinux policy extensions for running xrootd while in enforcing mode.

#-------------------------------------------------------------------------------
# ceph
#-------------------------------------------------------------------------------
%if %{with ceph}
%package ceph
Summary: Ceph back-end plug-in for XRootD
Group:   Development/Tools
Requires: %{name}-server = %{epoch}:%{version}-%{release}
%description ceph
Ceph back-end plug-in for XRootD.
%endif

#-------------------------------------------------------------------------------
# xrdcl-http
#-------------------------------------------------------------------------------
%package -n xrdcl-http
Summary:  HTTP client plug-in for XRootD client
Group:    System Environment/Libraries
Requires: %{name}-client = %{epoch}:%{version}-%{release}
%description -n xrdcl-http
xrdcl-http is an XRootD client plugin which allows XRootD to interact 
with HTTP repositories.

#-------------------------------------------------------------------------------
# xrootd-voms
#-------------------------------------------------------------------------------
%package   voms
Summary:   VOMS attribute extractor plug-in for XRootD
Group:     System Environment/Libraries
Provides:  vomsxrd = %{epoch}:%{version}-%{release}
Obsoletes: vomsxrd < 1:4.12.4-1
Requires:  %{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes: xrootd-voms-plugin
%description voms
The VOMS attribute extractor plug-in for XRootD.

#-------------------------------------------------------------------------------
# xrootd-scitokens
#-------------------------------------------------------------------------------
%package scitokens
Summary: SciTokens authentication plugin for XRootD
Group:   Development/Tools
Requires: %{name}-server = %{epoch}:%{version}-%{release}
%description scitokens
SciToken athorization plug-in for XRootD.

#-------------------------------------------------------------------------------
# tests
#-------------------------------------------------------------------------------
%if %{with tests}
%package tests
Summary: CPPUnit tests
Group:   Development/Tools
Requires: %{name}-client = %{epoch}:%{version}-%{release}
%description tests
This package contains a set of CPPUnit tests for xrootd.
%endif

%if %{with compat}
#-------------------------------------------------------------------------------
# client-compat
#-------------------------------------------------------------------------------
%package client-compat
Summary:	XRootD 4 compatibility client libraries
Group:		System Environment/Libraries

%description client-compat
This package contains compatibility libraries for XRootD 4 clients.

#-------------------------------------------------------------------------------
# server-compat
#-------------------------------------------------------------------------------
%package server-compat
Summary:	XRootD 4 compatibility server binaries
Group:		System Environment/Daemons
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description server-compat
This package contains compatibility binaries for XRootD 4 servers.
%endif

#-------------------------------------------------------------------------------
# Build instructions
#-------------------------------------------------------------------------------
%prep
%if %{with compat}
%setup -c -n xrootd-compat -a 1 -T
%endif

%setup -c -n %{build_dir}
cd %{build_dir}
%autopatch -p1
cd ..

%build

cd %{build_dir}

%if %{with clang}
export CC=clang
export CXX=clang++
%endif

mkdir build
pushd build

cmake  \
      -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=%{?with_debug:Debug}%{!?with_debug:RelWithDebInfo} \
      -DFORCE_WERROR=TRUE \
%if %{with tests}
      -DENABLE_TESTS=TRUE \
%else
      -DENABLE_TESTS=FALSE \
%endif
%if %{with asan}
      -DENABLE_ASAN=TRUE \
%endif
%if %{with ceph}
      -DXRDCEPH_SUBMODULE=TRUE \
%endif
      -DENABLE_XRDCLHTTP=TRUE \
%if %{with isal}
      -DENABLE_XRDEC=TRUE \
%endif
      -DXRootD_VERSION_STRING=v%{version} \
      -DINSTALL_PYTHON_BINDINGS=FALSE \
      ../

make -i VERBOSE=1 %{?_smp_mflags}
popd

pushd packaging/common
make -f /usr/share/selinux/devel/Makefile
popd

%if %{with docs}
doxygen Doxyfile
%endif

%if %{with compat}
pushd $RPM_BUILD_DIR/xrootd-compat/xrootd*
mkdir build
pushd build
cmake  \
      -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DFORCE_WERROR=TRUE \
%if %{with tests}
      -DENABLE_TESTS=TRUE \
%else
      -DENABLE_TESTS=FALSE \
%endif
%if %{with ceph}
      -DXRDCEPH_SUBMODULE=TRUE \
%endif
      -DENABLE_XRDEC=TRUE \
      ../

make -i VERBOSE=1 %{?_smp_mflags}
popd
popd
%endif

%undefine _hardened_build

pushd build/bindings/python
# build python3 bindings
%py3_build
popd

%check
cd %{build_dir}
ctest --output-on-failure

#-------------------------------------------------------------------------------
# Installation
#-------------------------------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT

#-------------------------------------------------------------------------------
# Install compat
#-------------------------------------------------------------------------------
%if %{with compat}
pushd $RPM_BUILD_DIR/xrootd-compat/xrootd*/build
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_datadir}
rm -f $RPM_BUILD_ROOT%{_bindir}/{cconfig,cns_ssi,frm_admin,frm_xfragent,mpxstats}
rm -f $RPM_BUILD_ROOT%{_bindir}/{wait41,xprep,xrd,xrdadler32,xrdcrc32c,XrdCnsd,xrdcopy}
rm -f $RPM_BUILD_ROOT%{_bindir}/{xrdcks,xrdcp,xrdcp-old,xrdfs,xrdgsiproxy,xrdpwdadmin}
rm -f $RPM_BUILD_ROOT%{_bindir}/{xrdqstats,xrdsssadmin,xrdstagetool,xrootdfs}
rm -f $RPM_BUILD_ROOT%{_libdir}/libXrdAppUtils.so
rm -f $RPM_BUILD_ROOT%{_libdir}/{libXrdClient.so,libXrdCl.so,libXrdCryptoLite.so}
rm -f $RPM_BUILD_ROOT%{_libdir}/{libXrdCrypto.so,libXrdFfs.so,libXrdMain.so}
rm -f $RPM_BUILD_ROOT%{_libdir}/{libXrdOfs.so,libXrdPosixPreload.so,libXrdPosix.so}
rm -f $RPM_BUILD_ROOT%{_libdir}/{libXrdServer.so,libXrdUtils.so}

for i in cmsd frm_purged frm_xfrd xrootd; do
  mv $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/${i}-4
done

rm -f $RPM_BUILD_ROOT%{python2_sitearch}/xrootd-v%{compat_version}*.egg-info
popd
%endif

#-------------------------------------------------------------------------------
# Install 5.x.y
#-------------------------------------------------------------------------------
pushd %{build_dir}
pushd  build
make install DESTDIR=$RPM_BUILD_ROOT
popd

# configuration stuff
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/*

# ceph posix unversioned so
rm -f $RPM_BUILD_ROOT%{_libdir}/libXrdCephPosix.so

# config paths
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.d/

# var paths
mkdir -p $RPM_BUILD_ROOT%{_var}/log/xrootd
mkdir -p $RPM_BUILD_ROOT%{_var}/run/xrootd
mkdir -p $RPM_BUILD_ROOT%{_var}/spool/xrootd

# init stuff
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xrootd

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 644 packaging/common/xrootd@.service $RPM_BUILD_ROOT%{_unitdir}
install -m 644 packaging/common/xrdhttp@.socket   $RPM_BUILD_ROOT%{_unitdir}
install -m 644 packaging/common/xrootd@.socket    $RPM_BUILD_ROOT%{_unitdir}
install -m 644 packaging/common/cmsd@.service $RPM_BUILD_ROOT%{_unitdir}
install -m 644 packaging/common/frm_xfrd@.service $RPM_BUILD_ROOT%{_unitdir}
install -m 644 packaging/common/frm_purged@.service $RPM_BUILD_ROOT%{_unitdir}

# tmpfiles.d
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 0644 packaging/rhel/xrootd.tmpfiles $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf

# logrotate
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -p -m 644 packaging/common/xrootd.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/xrootd

install -m 644 packaging/common/xrootd-clustered.cfg $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd-clustered.cfg
install -m 644 packaging/common/xrootd-standalone.cfg $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd-standalone.cfg
install -m 644 packaging/common/xrootd-filecache-clustered.cfg $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd-filecache-clustered.cfg
install -m 644 packaging/common/xrootd-filecache-standalone.cfg $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd-filecache-standalone.cfg
install -m 644 packaging/common/xrootd-http.cfg $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd-http.cfg

# client plug-in config
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.plugins.d
install -m 644 packaging/common/client-plugin.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.plugins.d/client-plugin.conf.example
install -m 644 packaging/common/recorder.conf              $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.plugins.d/recorder.conf

install -m 644 packaging/common/http.client.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.plugins.d/xrdcl-http-plugin.conf

# client config
install -m 644 packaging/common/client.conf $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/client.conf

%if %{with docs}
# documentation
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
cp -pr doxydoc/html %{buildroot}%{_docdir}/%{name}-%{version}
%endif

# selinux
mkdir -p %{buildroot}%{_datadir}/selinux/packages/%{name}
install -m 644 -p packaging/common/xrootd.pp \
    %{buildroot}%{_datadir}/selinux/packages/%{name}/%{name}.pp

pushd build/bindings/python
# install python3 bindings
%py3_install
popd

%clean
rm -rf $RPM_BUILD_ROOT

#-------------------------------------------------------------------------------
# RPM scripts
#-------------------------------------------------------------------------------
%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post   client-libs -p /sbin/ldconfig
%postun client-libs -p /sbin/ldconfig

%post   server-libs -p /sbin/ldconfig
%postun server-libs -p /sbin/ldconfig

%pre server

getent group xrootd >/dev/null || groupadd -r xrootd
getent passwd xrootd >/dev/null || \
       useradd -r -g xrootd -c "XRootD runtime user" \
       -s /sbin/nologin -d %{_localstatedir}/spool/xrootd xrootd
exit 0

%post server
if [ $1 -eq 1 ] ; then
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun server
if [ $1 -eq 0 ] ; then
    for DAEMON in xrootd cmsd frm_purged frm_xfrd; do
        for INSTANCE in `/usr/bin/systemctl | grep $DAEMON@ | awk '{print $1;}'`; do
            /usr/bin/systemctl --no-reload disable $INSTANCE > /dev/null 2>&1 || :
            /usr/bin/systemctl stop $INSTANCE > /dev/null 2>&1 || :
        done
    done
fi

%postun server
if [ $1 -ge 1 ] ; then
    /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
    for DAEMON in xrootd cmsd frm_purged frm_xfrd; do
        for INSTANCE in `/usr/bin/systemctl | grep $DAEMON@ | awk '{print $1;}'`; do
            /usr/bin/systemctl try-restart $INSTANCE >/dev/null 2>&1 || :
        done
    done
fi


#-------------------------------------------------------------------------------
# Add a new user and group if necessary
#-------------------------------------------------------------------------------
%pre fuse
getent group xrootd >/dev/null || groupadd -r xrootd
getent passwd xrootd >/dev/null || \
       useradd -r -g xrootd -c "XRootD runtime user" \
       -s /sbin/nologin -d %{_localstatedir}/spool/xrootd xrootd
exit 0

#-------------------------------------------------------------------------------
# Selinux
#-------------------------------------------------------------------------------
%post selinux
/usr/sbin/semodule -i %{_datadir}/selinux/packages/%{name}/%{name}.pp >/dev/null 2>&1 || :

%postun selinux
if [ $1 -eq 0 ] ; then
    /usr/sbin/semodule -r %{name} >/dev/null 2>&1 || :
fi

#-------------------------------------------------------------------------------
# Files
#-------------------------------------------------------------------------------
%files
# Empty

%files server
%{_bindir}/cconfig
%{_bindir}/cmsd
%{_bindir}/frm_admin
%{_bindir}/frm_purged
%{_bindir}/frm_xfragent
%{_bindir}/frm_xfrd
%{_bindir}/mpxstats
%{_bindir}/wait41
%{_bindir}/xrdpwdadmin
%{_bindir}/xrdsssadmin
%{_bindir}/xrootd
%{_bindir}/xrdpfc_print
%{_bindir}/xrdacctest
%{_mandir}/man8/cmsd.8*
%{_mandir}/man8/frm_admin.8*
%{_mandir}/man8/frm_purged.8*
%{_mandir}/man8/frm_xfragent.8*
%{_mandir}/man8/frm_xfrd.8*
%{_mandir}/man8/mpxstats.8*
%{_mandir}/man8/xrdpwdadmin.8*
%{_mandir}/man8/xrdsssadmin.8*
%{_mandir}/man8/xrootd.8*
%{_mandir}/man8/xrdpfc_print.8*
%{_datadir}/xrootd/utils
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/xrootd/xrootd-clustered.cfg
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/xrootd/xrootd-standalone.cfg
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/xrootd/xrootd-filecache-clustered.cfg
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/xrootd/xrootd-filecache-standalone.cfg
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/xrootd/xrootd-http.cfg
%attr(-,xrootd,xrootd) %dir %{_var}/log/xrootd
%attr(-,xrootd,xrootd) %dir %{_var}/run/xrootd
%attr(-,xrootd,xrootd) %dir %{_var}/spool/xrootd
%attr(-,xrootd,xrootd) %dir %{_sysconfdir}/%{name}/config.d
%config(noreplace) %{_sysconfdir}/logrotate.d/xrootd

%{_unitdir}/*
%{_tmpfilesdir}/%{name}.conf

%files libs
%{_libdir}/libXrdAppUtils.so.2*
%{_libdir}/libXrdClProxyPlugin-5.so
%{_libdir}/libXrdCks*-5.so
%{_libdir}/libXrdCrypto.so.2*
%{_libdir}/libXrdCryptoLite.so.2*
%{_libdir}/libXrdCryptossl-5.so
%{_libdir}/libXrdSec-5.so
%{_libdir}/libXrdSecProt-5.so
%{_libdir}/libXrdSecgsi-5.so
%{_libdir}/libXrdSecgsiAUTHZVO-5.so
%{_libdir}/libXrdSecgsiGMAPDN-5.so
%{_libdir}/libXrdSeckrb5-5.so
%{_libdir}/libXrdSecpwd-5.so
%{_libdir}/libXrdSecsss-5.so
%{_libdir}/libXrdSecunix-5.so
%{_libdir}/libXrdSecztn-5.so
%{_libdir}/libXrdUtils.so.3*
%{_libdir}/libXrdXml.so.3*

%files devel
%dir %{_includedir}/xrootd
%{_bindir}/xrootd-config
%{_includedir}/xrootd/XProtocol
%{_includedir}/xrootd/Xrd
%{_includedir}/xrootd/XrdCks
%{_includedir}/xrootd/XrdNet
%{_includedir}/xrootd/XrdOuc
%{_includedir}/xrootd/XrdSec
%{_includedir}/xrootd/XrdSys
%{_includedir}/xrootd/XrdVersion.hh
%{_libdir}/libXrdAppUtils.so
%{_libdir}/libXrdCrypto.so
%{_libdir}/libXrdCryptoLite.so
%{_libdir}/libXrdUtils.so
%{_libdir}/libXrdXml.so
%{_includedir}/xrootd/XrdXml/XrdXmlReader.hh
%{_libdir}/cmake/XRootD
# %{_datadir}/xrootd/cmake

%files client-libs
%defattr(-,root,root,-)
%{_libdir}/libXrdCl.so.3*
%{_libdir}/libXrdFfs.so.3*
%{_libdir}/libXrdPosix.so.3*
%{_libdir}/libXrdPosixPreload.so.2*
%{_libdir}/libXrdSsiLib.so.2*
%{_libdir}/libXrdSsiShMap.so.2*
%{_libdir}/libXrdClRecorder-5.so
%if %{with isal}
%{_libdir}/libXrdEc.so.1*
%endif
%{_sysconfdir}/xrootd/client.plugins.d/client-plugin.conf.example
%{_sysconfdir}/xrootd/client.plugins.d/recorder.conf
%config(noreplace) %{_sysconfdir}/xrootd/client.conf
# This lib may be used for LD_PRELOAD so the .so link needs to be included
%{_libdir}/libXrdPosixPreload.so

%files client-devel
%{_bindir}/xrdgsitest
%{_includedir}/xrootd/XrdCl
%{_includedir}/xrootd/XrdPosix
%{_libdir}/libXrdCl.so
%{_libdir}/libXrdFfs.so
%{_libdir}/libXrdPosix.so
%{_mandir}/man1/xrdgsitest.1*

%files server-libs
%{_libdir}/libXrdBwm-5.so
%{_libdir}/libXrdPss-5.so
%{_libdir}/libXrdXrootd-5.so
%{_libdir}/libXrdPfc-5.so
%{_libdir}/libXrdPfcPurgeQuota-5.so
%{_libdir}/libXrdFileCache-5.so
%{_libdir}/libXrdBlacklistDecision-5.so
%{_libdir}/libXrdHttp-5.so
%{_libdir}/libXrdHttpTPC-5.so
%{_libdir}/libXrdHttpUtils.so.2*
%{_libdir}/libXrdMacaroons-5.so
%{_libdir}/libXrdN2No2p-5.so
%{_libdir}/libXrdOssCsi-5.so
%{_libdir}/libXrdOssSIgpfsT-5.so
%{_libdir}/libXrdOssStats-5.so
%{_libdir}/libXrdServer.so.3*
%{_libdir}/libXrdSsi-5.so
%{_libdir}/libXrdSsiLog-5.so
%{_libdir}/libXrdThrottle-5.so
%{_libdir}/libXrdCmsRedirectLocal-5.so
%{_libdir}/libXrdOfsPrepGPI-5.so

%files server-devel
%{_includedir}/xrootd/XrdAcc
%{_includedir}/xrootd/XrdCms
%{_includedir}/xrootd/XrdPfc
%{_includedir}/xrootd/XrdOss
%{_includedir}/xrootd/XrdOfs
%{_includedir}/xrootd/XrdSfs
%{_includedir}/xrootd/XrdXrootd
%{_includedir}/xrootd/XrdHttp
%{_libdir}/libXrdServer.so
%{_libdir}/libXrdHttpUtils.so

%files private-devel
%{_includedir}/xrootd/private
%{_libdir}/libXrdSsiLib.so
%{_libdir}/libXrdSsiShMap.so
%if %{with isal}
%{_libdir}/libXrdEc.so
%endif

%files client
%{_bindir}/xrdadler32
%{_bindir}/xrdcks
%{_bindir}/xrdcopy
%{_bindir}/xrdcp
%{_bindir}/xrdcrc32c
%{_bindir}/xrdfs
%{_bindir}/xrdgsiproxy
%{_bindir}/xrdmapc
%{_bindir}/xrdpinls
%{_bindir}/xrdreplay
%{_mandir}/man1/xrdadler32.1*
%{_mandir}/man1/xrdcopy.1*
%{_mandir}/man1/xrdcp.1*
%{_mandir}/man1/xrdfs.1*
%{_mandir}/man1/xrdgsiproxy.1*
%{_mandir}/man1/xrdmapc.1*

%files fuse
%{_bindir}/xrootdfs
%{_mandir}/man1/xrootdfs.1*
%dir %{_sysconfdir}/xrootd

%files -n python%{python3_pkgversion}-%{name}
%defattr(-,root,root,-)
%{python3_sitearch}/*

%files voms
%{_libdir}/libXrdVoms-5.so
%{_libdir}/libXrdSecgsiVOMS-5.so
%{_libdir}/libXrdHttpVOMS-5.so
%doc %{_mandir}/man1/libXrdVoms.1.gz
%doc %{_mandir}/man1/libXrdSecgsiVOMS.1.gz

%if %{with docs}
%files doc
%doc %{_docdir}/%{name}-%{version}
%endif

%if %{with ceph}
%files ceph
%{_libdir}/libXrdCeph-5.so
%{_libdir}/libXrdCephXattr-5.so
%{_libdir}/libXrdCephPosix.so*
%endif

%files -n xrdcl-http
%{_libdir}/libXrdClHttp-5.so
%{_sysconfdir}/xrootd/client.plugins.d/xrdcl-http-plugin.conf

%files scitokens
%{_libdir}/libXrdAccSciTokens-5.so

%if %{with tests}
%files tests
%{_bindir}/test-runner
%{_bindir}/xrdshmap
%{_libdir}/libXrdClTests.so
%{_libdir}/libXrdClTestsHelper.so
%{_libdir}/libXrdClTestMonitor*.so
%if %{with isal}
%{_libdir}/libXrdEcTests.so
%endif
%if %{with ceph}
%{_libdir}/libXrdCephTests*.so
%endif
%endif

%files selinux
%{_datadir}/selinux/packages/%{name}/%{name}.pp

%if %{with compat}
%files client-compat
# from xrootd-libs:
%{_libdir}/libXrdAppUtils.so.1*
%{_libdir}/libXrdCks*-4.so
%{_libdir}/libXrdClProxyPlugin-4.so
%{_libdir}/libXrdCrypto.so.1*
%{_libdir}/libXrdCryptoLite.so.1*
%{_libdir}/libXrdCryptossl-4.so
%{_libdir}/libXrdSec*-4.so
%{_libdir}/libXrdUtils.so.2*
%{_libdir}/libXrdXml.so.2*

# from xrootd-client-libs
%{_libdir}/libXrdCl.so.2*
%{_libdir}/libXrdClient.so.2*
%{_libdir}/libXrdFfs.so.2*
%{_libdir}/libXrdPosix.so.2*
%{_libdir}/libXrdPosixPreload.so.1*
%{_libdir}/libXrdSsiLib.so.1*
%{_libdir}/libXrdSsiShMap.so.1*

%files server-compat
# from server (renamed)
%{_bindir}/cmsd-4
%{_bindir}/frm_purged-4
%{_bindir}/frm_xfrd-4
%{_bindir}/xrootd-4
# from server-libs
%{_libdir}/libXrdBwm-4.so
%{_libdir}/libXrdPss-4.so
%{_libdir}/libXrdXrootd-4.so
%{_libdir}/libXrdFileCache-4.so
%{_libdir}/libXrdBlacklistDecision-4.so
%{_libdir}/libXrdHttp-4.so
%{_libdir}/libXrdHttpTPC-4.so
%{_libdir}/libXrdHttpUtils.so.1*
%{_libdir}/libXrdMacaroons-4.so
%{_libdir}/libXrdN2No2p-4.so
%{_libdir}/libXrdOssSIgpfsT-4.so
%{_libdir}/libXrdServer.so.2*
%{_libdir}/libXrdSsi-4.so
%{_libdir}/libXrdSsiLog-4.so
%{_libdir}/libXrdThrottle-4.so
%{_libdir}/libXrdCmsRedirectLocal-4.so
%{_libdir}/libXrdVoms-4.so

%endif
# end with_compat

#-------------------------------------------------------------------------------
# Changelog
#-------------------------------------------------------------------------------
%changelog
* Tue Jul 15 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.4-1.1
- Update to XRootD 5.8.4 (SOFTWARE-6187)
    - Patches added:
    - Patches kept:
        - 0001-Allow-hostname-used-by-XRootD-to-be-overridden-by-en~7c119b0.patch -> 0001-1-Allow-hostname-used-by-XRootD-to-be-overridden-by~7c119b0.patch
        - 0002-XrdTls-Allow-disabling-of-X.509-client-auth~18e1c81.patch -> 0002-4-XrdTls-Allow-disabling-of-X.509-client-auth~18e1c81.patch
        - 0003-XrdSciTokens-Handle-multiple-authorization-token-set~b82ddc3.patch -> 0003-6-XrdSciTokens-Handle-multiple-authorization-token-s~b82ddc3.patch
        - 0004-XrdHttp-Undo-HTTP-PUT-response-code-change~43ed40b.patch -> 0004-14-XrdHttp-Undo-HTTP-PUT-response-code-change~43ed40b.patch
        - 0006-Re-engineer-concurrency-limits-for-throttles~39fea57.patch -> 0005-23-Re-engineer-concurrency-limits-for-throttles~39fea57.patch
        - 0007-Modify-XrdThrottle-to-be-an-OSS-plugin~921fef5.patch -> 0006-23-Modify-XrdThrottle-to-be-an-OSS-plugin~921fef5.patch
        - 0008-XRootD-s-xml-response-for-PROPFIND-will-now-include~aacf631.patch -> 0007-25-XRootD-s-xml-response-for-PROPFIND-will-now-inclu~aacf631.patch
        - 0011-Enable-write-through-mode-for-cache~330eac1.patch -> 0008-32-Enable-write-through-mode-for-cache~330eac1.patch
    - Patches dropped:
        - 0009-Avoid-reference-beyond-end-of-table~80b938c.patch
        - 0010-XrdPfc-Ensure-a-reference-to-the-file-is-kept-when-s~aa225e2.patch

* Tue Jun 24 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.3-1.3
- Add patch 0011-Enable-write-through-mode-for-cache~330eac1.patch (SOFTWARE-6179)

* Tue Jun 10 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.3-1.1
- Update to XRootD 5.8.3 (SOFTWARE-6164)
    - Patches added:
        - 0009-Avoid-reference-beyond-end-of-table~80b938c.patch
        - 0010-XrdPfc-Ensure-a-reference-to-the-file-is-kept-when-s~aa225e2.patch
    - Patches kept:
        - 0001-Allow-hostname-used-by-XRootD-to-be-overridden-by-en~7c119b0.patch
        - 0002-XrdTls-Allow-disabling-of-X.509-client-auth~18e1c81.patch
        - 0003-XrdSciTokens-Handle-multiple-authorization-token-set~b82ddc3.patch
        - 0004-XrdHttp-Undo-HTTP-PUT-response-code-change~956b9fa.patch -> 0004-XrdHttp-Undo-HTTP-PUT-response-code-change~43ed40b.patch
        - 0006-Re-engineer-concurrency-limits-for-throttles~39fea57.patch
        - 0007-Modify-XrdThrottle-to-be-an-OSS-plugin~921fef5.patch
        - 0008-XRootD-s-xml-response-for-PROPFIND-will-now-include~aacf631.patch
    - Patches dropped:
        - 0005-XrdHttp-Fix-HTTP-protocol-errors-on-failure~4fb2221.patch
        - 0009-Fix-life-time-of-a-variable-used-for-signaling-that~286b8ca.patch
        - 0010-Correct-concurrency-and-state-tracking-around-Redriv~86d48f1.patch
        - 0011-Fix-race-conditions-around-use-of-ecMsg~803dc26.patch

* Wed May 21 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.2-1.5
- Add 0011-Fix-race-conditions-around-use-of-ecMsg~803dc26.patch (SOFTWARE-6151)

* Thu May 15 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.2-1.3
- Add 0010-Correct-concurrency-and-state-tracking-around-Redriv~86d48f1.patch (SOFTWARE-6151)

* Wed May 14 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.2-1.2
- Add 0009-Fix-life-time-of-a-variable-used-for-signaling-that~286b8ca.patch (SOFTWARE-6151)

* Tue May 13 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.2-1.1
- Update to XRootD 5.8.2 (SOFTWARE-6151)
    - Patches added:
        - 0008-XRootD-s-xml-response-for-PROPFIND-will-now-include~aacf631.patch
    - Patches kept:
        - 0001-Allow-hostname-used-by-XRootD-to-be-overridden-by-en~7c119b0.patch
        - 0002-XrdTls-Allow-disabling-of-X.509-client-auth~18e1c81.patch
        - 0003-XrdSciTokens-Handle-multiple-authorization-token-set~ec1eb0c.patch -> 0003-XrdSciTokens-Handle-multiple-authorization-token-set~b82ddc3.patch
        - 0004-XrdHttp-Undo-HTTP-PUT-response-code-change~956b9fa.patch
        - 0005-XrdHttp-Fix-HTTP-protocol-errors-on-failure~4fb2221.patch
        - 0007-Re-engineer-concurrency-limits-for-throttles~0ef6dbc.patch -> 0006-Re-engineer-concurrency-limits-for-throttles~39fea57.patch
        - 0009-Modify-XrdThrottle-to-be-an-OSS-plugin~580a3f1.patch -> 0007-Modify-XrdThrottle-to-be-an-OSS-plugin~921fef5.patch
    - Patches dropped:
        - 0006-XrdPosix-Map-operation-timeouts-to-ETIME~9480232.patch
        - 0008-Tweak-throttle-manager-after-large-scale-testing~273c58e.patch
        - 0010-CMake-changes-for-XrdThrottle-overhaul~fe965e8.patch

* Wed Apr 30 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.1-1.5
- Patches added:
    - 0008-Tweak-throttle-manager-after-large-scale-testing~273c58e.patch
    - 0009-Modify-XrdThrottle-to-be-an-OSS-plugin~580a3f1.patch
    - 0010-CMake-changes-for-XrdThrottle-overhaul~fe965e8.patch
- Patches dropped:
    - 0007-XrdSciTokens-Automatically-add-WLCG-audiences-upon-r~92c168c.patch
- Patches kept:
    - 0008-Re-engineer-concurrency-limits-for-throttles~0ef6dbc.patch -> 0007-Re-engineer-concurrency-limits-for-throttles~0ef6dbc.patch

* Tue Apr 29 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.1-1.4
- Add 0008-Re-engineer-concurrency-limits-for-throttles~0ef6dbc.patch

* Fri Apr 18 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.1-1.3
- Drop 0008-Include-additional-XrdPfc-headers.patch

* Thu Apr 17 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.1-1.2
- Comment out 0007-XrdSciTokens-Automatically-add-WLCG-audiences-upon-r~92c168c.patch
- Add 0008-Include-additional-XrdPfc-headers.patch

* Wed Apr 16 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.1-1.1
- Update to 5.8.1 (SOFTWARE-6114)
    - Patches added:
        - 0006-XrdPosix-Map-operation-timeouts-to-ETIME~9480232.patch
        - 0007-XrdSciTokens-Automatically-add-WLCG-audiences-upon-r~92c168c.patch
    - Patches kept:
        - 0007-XrdHttp-Fix-HTTP-protocol-errors-on-failure~4fb2221.patch -> 0005-XrdHttp-Fix-HTTP-protocol-errors-on-failure~4fb2221.patch
    - Patches dropped:
        - 0005-Since-the-XrdPss-did-not-implement-the-auto-stat-pro~4c5e0ae.patch
        - 0006-XrdPss-Fix-proxy-when-using-tokens-and-crc32c~328ae18.patch

* Mon Mar 31 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.8.0-1.1
- Update to 5.8.0 (SOFTWARE-6114)
    - Patches added:
        - 0005-Since-the-XrdPss-did-not-implement-the-auto-stat-pro~4c5e0ae.patch
        - 0006-XrdPss-Fix-proxy-when-using-tokens-and-crc32c~328ae18.patch
        - 0007-XrdHttp-Fix-HTTP-protocol-errors-on-failure~4fb2221.patch
    - Patches kept:
        - 0003-XrdTls-Allow-disabling-of-X.509-client-auth~18e1c81.patch -> 0002-XrdTls-Allow-disabling-of-X.509-client-auth~18e1c81.patch
        - 0008-XrdHttp-Undo-HTTP-PUT-response-code-change~956b9fa.patch -> 0004-XrdHttp-Undo-HTTP-PUT-response-code-change~956b9fa.patch
    - Patches updated:
        - 0001-Allow-hostname-used-by-XRootD-to-be-overridden-by-en~e13587e.patch -> 0001-Allow-hostname-used-by-XRootD-to-be-overridden-by-en~7c119b0.patch
        - 0005-XrdSciTokens-Handle-multiple-authorization-token-set~a33ca13.patch -> 0003-XrdSciTokens-Handle-multiple-authorization-token-set~ec1eb0c.patch
    - Patches dropped:
        - 0002-XrdHttp-determines-the-presence-of-the-Age-header-in~092c7a5.patch
        - 0004-Add-new-filesystem-load-counter-plugin~3c1be23.patch
        - 0006-XrdHttp-Add-http.staticheader~5c6ee05.patch
        - 0007-XrdPfc-Check-for-a-null-pointer-dereference~121f60b.patch
        - 0009-Add-ResourceMonitor-and-PurgePlugin~f34a39d.patch
        - 0010-Fix-gstream-configuration-processing~bece0de.patch
        - 0011-Xrd-Fix-MacOS-poller~9704d2a.patch
        - 0012-Temporary-workaround-for-segfault-noted-in-upstream~3b485c0.patch

* Thu Mar 13 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.3-1.5
- Add:
    - 0010-Fix-gstream-configuration-processing~bece0de.patch
    - 0012-Temporary-workaround-for-segfault-noted-in-upstream~3b485c0.patch
- Re-add (with update):
    - 0011-Xrd-Fix-MacOS-poller~9704d2a.patch

* Mon Mar 10 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.3-1.4
- Fix patch file name; always build with purge plugin patch (SOFTWARE-6100)

* Tue Mar 04 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.3-1.3.purge
- Add purge plugin patch 0009-Add-ResourceMonitor-and-PurgePlugin~f34a39d.patch

* Tue Mar 04 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.3-1.3
- Add 0010-gstream-config-processing.patch (SOFTWARE-6099)

* Thu Jan 30 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.3-1.2
- Fix patch file names
- Add:
    - 0007-XrdPfc-Check-for-a-null-pointer-dereference~121f60b.patch
    - 0008-XrdHttp-Undo-HTTP-PUT-response-code-change~956b9fa.patch

* Tue Jan 28 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.3-1.1
- Update to XRootD 5.7.3 (SOFTWARE-6071)
- Drop upstreamed patches:
    - 0003-Fix-FD-leak-when-reading-file-size-from-cinfo-file-i~a219487.patch
    - 0008-XrdHttp-Set-oss.asize-if-object-size-is-known~d710312.patch
    - 0010-do_WriteSpan-Add-written-bytes-in-file-statistics~98a22ba.patch
    - 0011-Xrd-Fix-MacOS-poller~79a5439.patch
- Replace patches with updated versions:
    - 0004-Defer-client-TLS-auth-until-after-HTTP-parsing~323a16b.patch
        -> 0003-XrdTls-Allow-disabling-of-X.509-client-auth.patch~18e1c81.patch
    - 0005-Add-new-filesystem-load-counter-plugin~3c1be23.patch
        -> 0004-Add-new-filesystem-load-counter-plugin.patch~3c1be23.patch
    - 0006-XrdSciTokens-Handle-multiple-authorization-token-set~7433116.patch
        -> 0005-XrdSciTokens-Handle-multiple-authorization-token-set.patch~a33ca13.patch
    - 0007-XrdHttp-Add-http.staticheader~2175ae2.patch
        -> 0006-XrdHttp-Add-http.staticheader.patch~5c6ee05.patch

* Fri Jan 17 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.2-1.4.purge
- Add purge plugin patch 0009-Second-rebase-of-alja-purge-main-rb1-onto-master-5.7.patch
    (PelicanPlatform/xrootd #9)

* Fri Jan 17 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.2-1.4
- Two more patches from PelicanPlatform/xrootd (SOFTWARE-6063)
    - Add 0010-do_WriteSpan-Add-written-bytes-in-file-statistics.patch (PelicanPlatform/xrootd #10)
    - Add 0011-Xrd-Fix-MacOS-poller.patch (PelicanPlatform/xrootd #11)

* Wed Jan 15 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.7.2-1.3
- Use patches from PelicanPlatform/xrootd (SOFTWARE-6063)
    - Replace 1868-env-hostname-override.patch with 0001-Allow-hostname-used-by-XRootD-to-be-overridden-by-en.patch (PelicanPlatform/xrootd #1)
    - Replace 2348-cache-age-logic.patch with 0002-XrdHttp-determines-the-presence-of-the-Age-header-in.patch (PelicanPlatform/xrootd #2)
    - Replace 2395-cinfo-read-fd-leak.patch with 0003-Fix-FD-leak-when-reading-file-size-from-cinfo-file-i.patch (PelicanPlatform/xrootd #3)
    - Replace 2269-defer-client-auth.patch with 0004-Defer-client-TLS-auth-until-after-HTTP-parsing.patch (PelicanPlatform/xrootd #4)
    - Replace bbockelm-3-oss-statistics.patch with 0005-Add-new-filesystem-load-counter-plugin.patch (PelicanPlatform/xrootd #5)
    - Add 0006-XrdSciTokens-Handle-multiple-authorization-token-set.patch (PelicanPlatform/xrootd #6)
    - Add 0007-XrdHttp-Add-http.staticheader.patch (PelicanPlatform/xrootd #7)
    - Add 0008-XrdHttp-Set-oss.asize-if-object-size-is-known.patch (PelicanPlatform/xrootd #8)

* Fri Dec 20 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.2-1.2
- Add 2395-cinfo-read-fd-leak.patch (SOFTWARE-6047)

* Tue Dec 03 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.2-1.1
- Update to 5.7.2 and drop upstreamed patches (SOFTWARE-6036)
  - Drop 2300-stat-call-reduction.patch
  - Update 2348-cache-age-logic.patch
    (replace with https://github.com/bbockelm/xrootd/commit/2160a23febe1782cc3590a473209f0e74f965084)
  - Drop 2357-fix-errSocketTimeout-loop.patch
  - Drop 2363-reset-runstatus-in-redrive-thread.patch

* Wed Oct 16 2024 Matt Westphall <westphall@wisc.edu> - 5.7.1-1.4
- Add 2363-reset-runstatus-in-redrive-thread.patch (SOFTWARE-6024)

* Wed Oct 16 2024 Matt Westphall <westphall@wisc.edu> - 5.7.1-1.3
- Add 2357-fix-errSocketTimeout-loop.patch

* Thu Oct 03 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.1-1.2
- Update 2300-stat-call-reduction.patch (SOFTWARE-6003)
- Add 2348-cache-age-logic.patch (SOFTWARE-6003)

* Fri Sep 06 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.1-1.1
- Update to 5.7.1 and drop upstreamed patches (SOFTWARE-5975)

* Fri Aug 30 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.7.2
- Apply updated bbockelm-4-defer-client-auth (SOFTWARE-5968)

* Tue Aug 27 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.7.1
- Drop bbockelm-4-defer-client-auth (might be causing test failures)

* Mon Aug 26 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.7
- Add bbockelm-3-oss-statistics.patch (SOFTWARE-5967)
- Add bbockelm-4-defer-client-auth (as 3 patches) (SOFTWARE-5968);
    this adds libXrdOssStats-5.so to xrootd-server-libs

* Thu Aug 08 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.6
- Remove unrelated commits from 2300-stat-call-reduction.patch (SOFTWARE-5949)

* Wed Aug 07 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.5
- Bump to rebuild for aarch64
- Don't make the generated documentation (i.e., xrootd-doc subpackage) noarch
  because the generation results are different based on the arch of the builder.

* Mon Aug 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.3
- Add 2300-stat-call-reduction.patch (SOFTWARE-5949)

* Thu Aug 01 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.2
- Add 2303-file-pointer-leak.patch (SOFTWARE-5947)

* Tue Jul 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.7.0-1.1
- Update to 5.7.0 and merge OSG patches (SOFTWARE-5925)
    - Drop SOFTWARE-5800-pelican-url.patch (applied upstream)
    - Drop 2206-io-time-gstream-monitoring.patch (applied upstream)
    - Drop SOFTWARE-5870-only-if-cached.patch (applied upstream)
    - Drop 2262-fix-timing-on-throttle-plugin.patch (applied upstream)
    - Drop 2269-defer-or-disable-tls-client-auth-*.patch (applied upstream)

* Thu May 30 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.9-1.6
- Split 2269-defer-or-disable-tls-client-auth.patch into 3 patches
  and re-do its conflict resolution (SOFTWARE-5876)

* Mon May 20 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.9-1.4
- Add SOFTWARE-5870-only-if-cached.patch (SOFTWARE-5870)
- Add 2262-fix-timing-on-throttle-plugin.patch (SOFTWARE-5873, SOFTWARE-5875)
- Add 2269-defer-or-disable-tls-client-auth.patch (SOFTWARE-5876)

* Wed May 01 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.9-1.3
- Actually add 2206-io-time-gstream-monitoring.patch (SOFTWARE-5850)

* Wed Apr 10 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.9-1.2
- Add 2206-io-time-gstream-monitoring.patch (SOFTWARE-5850)

* Sun Mar 17 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.9-1.1
- Update to 5.6.9 and merge OSG patches (SOFTWARE-5839)

* Fri Feb 23 2024 Matt Westphall <westphall@wisc.edu> - 5.6.8-1.1
- Initial OSG release of upstream 5.6.8-1

* Mon Feb 12 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.7-1.2
- Bump to rebuild

* Tue Feb 6 2024 Matt Westphall <westphall@wisc.edu> - 5.6.7-1.1
- OSG release of upstream 5.6.7

* Tue Feb 06 2024 Guilherme Amadio <amadio@cern.ch> - 5.6.7-1
- XRootD 5.6.7

* Fri Jan 26 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.6-1.1
- Update to 5.6.6 (SOFTWARE-5799)
- Add patch for pelican:// URL support (SOFTWARE-5800)

* Mon Dec 11 2023 Matt Westphall <westphall@wisc.edu> - 5.6.4-1.1
- Initial OSG release of upstream 5.6.4-1

* Wed Nov 29 2023 Matt Westphall <westphall@wisc.edu> - 5.6.3-1.4
- Add 2127-Switch-from-using-a-cert-file-to-a-cert-chain-file.patch (SOFTWARE-5763)

* Mon Nov 13 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.3-1.3
- Add 2118-HTTP-Initialize-SecEntity.addrInfo.patch (SOFTWARE-5748)

* Mon Oct 30 2023 Matt Westphall <westphall@wisc.edu> - 5.6.3-1.2
- Re-add removed OSG patches (SOFTWARE-5733)

* Fri Oct 27 2023 Matt Westphall <westphall@wisc.edu> - 5.6.3-1.1
- Initial OSG release of upstream 5.6.3-1 (SOFTWARE-5733)

* Thu Oct 26 2023 Matt Westphall <westphall@wisc.edu> - 5.6.2-2.5
- Apply patches for supporting chunked PUT requests from devel (SOFTWARE-5733)

* Tue Sep 19 2023 Matt Westphall <westphall@wisc.edu> - 5.6.2-2.2
- Update to 5.6.2-2 from upstream

* Mon Aug 14 2023 Matt Westphall <westphall@wisc.edu> - 5.6.1-1.2
- Add patch for PR 2059: Add back parsing of Transfer-Encoding header (SOFTWARE-5623)
- Add patch for PR 2064: Fix logic error in user mapping (SOFTWARE-5623)

* Mon Jul 17 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.6.1-1.1
- Update to 5.6.1-1 from upstream and merge OSG changes (SOFTWARE-5623)
  - Drop 2026-Switch-to-a-fixed-set-of-DH-parameters-compatible-with-older-OpenSSL.patch (upstreamed)

* Mon Jun 12 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.5-1.2
- Add 2026-Switch-to-a-fixed-set-of-DH-parameters-compatible-with-older-OpenSSL.patch (SOFTWARE-5594)
  for compatibility between EL7 clients and EL9 servers
- Drop debugging patches

* Wed May 10 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.5-1.1
- Update to 5.5.5-1 from upstream and merge OSG changes (SOFTWARE-5567)

* Tue Mar 28 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.4-1.1
- Update to 5.5.4-1 from upstream and merge OSG changes (SOFTWARE-5539)
  - Drop 1918-Fix-direct-read-for-PFC.patch (upstreamed)
  - Drop 1920-XrdHttp-Fix-byte-range-requests.patch (upstreamed)

* Thu Mar 09 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.3-1.3
- Build xrdcl-http (SOFTWARE-5518)

* Tue Feb 21 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.3-1.2
- Update to 5.5.3-1 from upstream and merge OSG patches (SOFTWARE-5436):
  - Drop 1826-HTTP-TPC-PULL.patch (upstreamed)
  - Drop voms-mapfile-handle-missing-role.patch (upstreamed)
- Add 1918-Fix-direct-read-for-PFC.patch
- Add 1920-XrdHttp-Fix-byte-range-requests.patch
- Disable compat build on EL9

* Wed Dec 28 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.1-1.13
- Replace SOFTWARE-5418.redirector-hostnames.patch with an updated 1868-env-hostname-override.patch (SOFTWARE-5414/SOFTWARE-5418)

* Tue Dec 27 2022 Carl Edquist <edquist@cs.wisc.edu> - 5.5.1-1.12
- Another patch update from Brian B (SOFTWARE-5414)

* Thu Dec 22 2022 Brian Lin <blin@cs.wisc.edu> - 5.5.1-1.11
- Further updates to the redirector hostname patch (SOFTWARE-5418.redirector-hostnames.patch) (SOFTWARE-5418)
- Drop 1868-env-hostname-override.patch, it is included in the above patch.

* Wed Dec 21 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.1-1.10
- Turn off the debug build.
- Add 0002-DEBUG-Catch-and-log-exception-launching-voms-mapfile.patch

* Tue Dec 20 2022 Brian Lin <blin@cs.wisc.edu> - 5.5.1-1.9.dbg
- Update patch to override the IP address with the hostname at the
  redirector (SOFTWARE-5418)

* Mon Dec 19 2022 Brian Lin <blin@cs.wisc.edu> - 5.5.1-1.8.dbg
- Add patch to override the IP address with the hostname at the
  redirector

* Sun Dec 18 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.1-1.7.dbg
- Add DEBUG-Add-some-debug-lines-to-XrdVomsMapfile.patch and do a debug build.

* Thu Dec 15 2022 Carl Edquist <edquist@cs.wisc.edu> - 5.5.1-1.6
- Add 1868-env-hostname-override.patch (SOFTWARE-5414)

* Wed Nov 16 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.1-1.5
- Add voms-mapfile-handle-missing-role.patch

* Fri Nov 11 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.1-1.4
- Drop patch reverting https://github.com/xrootd/xrootd/pull/1801;
  instead add 1826-HTTP-TPC-PULL.patch which should fix the issue

* Thu Nov 03 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.1-1.3
- Add logging patch (https://github.com/xrootd/xrootd/pull/1819)
- Add patch reverting https://github.com/xrootd/xrootd/pull/1801

* Thu Oct 20 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.1-1.2
- Build from 5.5.1 full release (SOFTWARE-5328)

* Tue Aug 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 5.5.1-1.1
- Build from 5.5.0 (SOFTWARE-5275)

* Thu Aug 18 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.0-0.rc3.1
- Build from 5.5.0-rc3 (SOFTWARE-5275)

* Thu Aug 11 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.0-0.rc2.1
- Build from 5.5.0-rc2 (SOFTWARE-5275)

* Tue Aug 02 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.0-0.rc1.1
- Build from 5.5.0-rc1 (SOFTWARE-5275)
  - Remove upstreamed patch PR-1644-scitokens_logging.patch

* Mon Jun 20 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.3-1.2
- Add patch to backport https://github.com/xrootd/xrootd/pull/1644 ("Populate XrdSciTokens with more detailed log messages")

* Thu Jun 09 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.3-1.1
- Build from 5.4.3 and add OSG changes (SOFTWARE-5160)

* Thu Jun 02 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.3-0.rc4.1
- Build from 5.4.3-rc4 and add OSG changes (SOFTWARE-5160)

* Thu May 12 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.3-0.rc3.1
- Build from 5.4.3-rc3 and add OSG changes (SOFTWARE-5160)

* Wed May 11 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.3-0.rc2.1
- Build from 5.4.3-rc2 and add OSG changes (SOFTWARE-5160)

* Tue May 10 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.3-0.rc1.2
- Provide python3-xrootd on EL7

* Mon May 09 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.3-0.rc1.1
- Build from 5.4.3-rc1 and add OSG changes (SOFTWARE-5160)
- Remove xrootd-multiuser < 0.6.0 conflict (SOFTWARE-5170)

* Fri Mar 11 2022 Brian Lin <blin@cs.wisc.edu> - 5.4.2-1.1
- Move VOMS mapfile support to the source (SOFTWARE-4870)
- Fix HTTP DN hashing
- Add new throttling config for max open files and active connections

* Thu Mar 03 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.2-1
- Update to 5.4.2 and merge OSG changes (SOFTWARE-5072, SOFTWARE-5073)
- Update SOFTWARE-4870.voms-mapfile.patch

* Wed Feb 23 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.1-1
- Update to 5.4.1 and merge OSG changes (SOFTWARE-4998, SOFTWARE-4999)

* Fri Feb 18 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.1-0.rc2.osg
- Update to 5.4.1rc2 and merge OSG changes (SOFTWARE-4998, SOFTWARE-4999)
- Update SOFTWARE-4870.voms-mapfile.patch

* Tue Dec 14 2021 Brian Lin <blin@cs.wisc.edu> - 5.4.0-1.1
- Add the ability to read from a voms-mapfile (SOFTWARE-4870)

* Fri Dec 10 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.4.0-1
- Update to 5.4.0 and merge OSG changes (SOFTWARE-4898, SOFTWARE-4899)

* Tue Nov 30 2021 Brian Lin <blin@cs.wisc.edu> - 5.3.4-1
- Update to 5.3.4 and merge OSG changes (SOFTWARE-4903, SOFTWARE-4904)

* Wed Nov 24 2021 Matyas Selmeci <matyas@cs.wisc.edu> - 5.3.4-0.rc2
- Update to 5.3.4 RC2 and merge OSG changes (SOFTWARE-4903, SOFTWARE-4904)

* Wed Nov 17 2021 Brian Lin <blin@cs.wisc.edu> - 5.3.4-0.rc1
- Update to 5.3.4 RC1 and merge OSG changes (SOFTWARE-4903, SOFTWARE-4904)

* Mon Nov 15 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.3.3-1.1
- Update to 5.3.3 and merge OSG changes (SOFTWARE-4903, SOFTWARE-4904)

* Thu Oct 28 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.3.2-1.1
- Update to 5.3.2 and merge OSG changes (SOFTWARE-4871, SOFTWARE-4872)

* Mon Aug 02 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.3.1-1.1
- Update to 5.3.1 and merge OSG changes (SOFTWARE-4714)

* Fri Jul 09 2021 Carl Edquist <edquist@cs.wisc.edu> - 5.3.0-1.1
- Update to 5.3.0 and merge OSG changes (SOFTWARE-4688)

* Tue Jul 06 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.3.0-0.rc4.1.osg
- Update to 5.3.0rc4 and merge OSG changes (SOFTWARE-4688)

* Thu May 20 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.2.0-1.1.osg
- Final 5.2.0 + OSG additions (SOFTWARE-4593)

* Wed May 19 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.2.0-0.2.1.osg
- Update to 5.2.0rc2 and merge OSG changes (SOFTWARE-4593)

* Wed Mar 31 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.1-1.3.osg
- Conflict with xrootd-multiuser < 0.6 (known to be broken) (SOFTWARE-4557)

* Wed Mar 03 2021 Carl Edquist <edquist@cs.wisc.edu> - 5.1.0-1.1.osg
- Final 5.1.0 + OSG additions (SOFTWARE-4356)

* Wed Feb 10 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-0.rc7.1.osg
- Rebuild for rc7 (SOFTWARE-4356)

* Mon Feb 01 2021 Edgar Fajardo <emfajard@ucsd.edu> - 5.1.0-0.rc6.1.osg
- Rebuild for rc6 (SOFTWARE-4356)

* Mon Jan 18 2021 Edgar Fajardo <emfajard@ucsd.edu> - 5.1.0-0.rc5.1.osg
- Rebuild to rc5

* Mon Dec 21 2020 Edgar Fajardo <emfajard@ucsd.edu> - 5.1.0-0.rc4.1.osg
- Rebuild to RC4
- Remove patch Fix-typo-XrdAccAuthorizeObjectAdd-XrdAccAuthorizeObj.paatch
- Remove patch Adding-ObjAdd-to-list-of-scitokens-functions-exporte.patch
- Remove patch Rename-XrdAccAuthorizeObjectAdd-to-XrdAccAuthorizeOb.patch

* Tue Dec 15 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-0.rc3.5.osg
- Add Fix-typo-XrdAccAuthorizeObjectAdd-XrdAccAuthorizeObj.patch from https://github.com/xrootd/xrootd/commit/bf5aa963185c62228b93312dd0517ba1b1f43e52
- Add Adding-ObjAdd-to-list-of-scitokens-functions-exporte.patch  from https://github.com/xrootd/xrootd/pull/1363

* Mon Dec 14 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-0.rc3.2.osg
- Update to upstream rc3  (SOFTWARE-4356)
- Use 4.12.6 for the compat package  (SOFTWARE-4247)
- Add Rename-XrdAccAuthorizeObjectAdd-to-XrdAccAuthorizeOb.patch from https://github.com/xrootd/xrootd/pull/1361

* Wed Dec 09 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-0.rc1.2.osg
- Build xrootd-scitokens and xrootd-compat again  (SOFTWARE-4356)
- Use 4.12.5 for the compat package  (SOFTWARE-4247)

* Thu Oct 15 2020 Michal Simon <michal.simon@cern.ch> - 5.0.2-1
- Introduce xrootd-scitokens package

* Wed May 27 2020 Michal Simon <michal.simon@cern.ch> - 4.12.2-1
- Remove xrootd-voms-devel

* Fri Apr 17 2020 Michal Simon <michal.simon@cern.ch> - 4.12.0-1
- Introduce xrootd-voms and xrootd-voms-devel packages

* Mon Sep 02 2019 Michal Simon <michal.simon@cern.ch> - 4.10.1-1
- Move xrdmapc to client package

* Fri Aug 30 2019 Michal Simon <michal.simon@cern.ch> - 5.0.0
- Remove XRootD 3.x.x compat package

* Wed Apr 17 2019 Michal Simon <michal.simon@cern.ch> - 4.10.0-1
- Create add xrdcl-http package

* Tue Jan 08 2019 Edgar Fajardo <emfajard@ucsd.edu>
- Create config dir /etc/xrootd/config.d

* Tue May 08 2018 Michal Simon <michal.simon@cern.ch> 
- Make python3 sub-package optional

* Fri Nov 10 2017 Michal Simon <michal.simon@cern.ch> - 1:4.8.0-1
- Add python3 sub-package
- Rename python sub-package

* Tue Dec 13 2016 Gerardo Ganis <gerardo.ganis@cern.ch>
- Add xrdgsitest to xrootd-client-devel

* Mon Mar 16 2015 Lukasz Janyst <ljanyst@cern.ch>
- create the python package

* Wed Mar 11 2015 Lukasz Janyst <ljanyst@cern.ch>
- create the xrootd-ceph package

* Thu Oct 30 2014 Lukasz Janyst <ljanyst@cern.ch>
- update for 4.1 and introduce 3.3.6 compat packages

* Thu Aug 28 2014 Lukasz Janyst <ljanyst@cern.ch>
- add support for systemd

* Wed Aug 27 2014 Lukasz Janyst <ljanyst@cern.ch>
- use generic selinux policy build mechanisms

* Tue Apr 01 2014 Lukasz Janyst <ljanyst@cern.ch>
- correct the license field (LGPLv3+)
- rename to xrootd4
- add 'conflicts' statements
- remove 'provides' and 'obsoletes'

* Mon Mar 31 2014 Lukasz Janyst <ljanyst@cern.ch>
- Add selinux policy

* Fri Jan 24 2014 Lukasz Janyst <ljanyst@cern.ch>
- Import XrdHttp

* Fri Jun 7 2013 Lukasz Janyst <ljanyst@cern.ch>
- adopt the EPEL RPM layout by Mattias Ellert

* Tue Apr 2 2013 Lukasz Janyst <ljanyst@cern.ch>
- remove perl

* Thu Nov 1 2012 Justin Salmon <jsalmon@cern.ch>
- add tests package

* Fri Oct 21 2011 Lukasz Janyst <ljanyst@cern.ch> 3.1.0-1
- bump the version to 3.1.0

* Mon Apr 11 2011 Lukasz Janyst <ljanyst@cern.ch> 3.0.3-1
- the first RPM release - version 3.0.3
- the detailed release notes are available at:
  http://xrootd.org/download/ReleaseNotes.html
