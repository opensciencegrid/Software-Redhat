Name:		xrootd-compat
Version:	3.3.6
Release:	1.1%{?dist}
Summary:	Extended ROOT file server - compat version

Group:		System Environment/Daemons
License:	LGPLv3+
URL:		http://xrootd.org/
Source0:	http://xrootd.org/download/v%{version}/xrootd-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	krb5-devel
BuildRequires:	libevent-devel
BuildRequires:	libxml2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{version}-%{release}
Requires:	xrootd-server >= 1:4.1.0
Obsoletes:	xrootd < 1:4.0.0

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

This package contains the xrootd 3.x version of the server.

%package libs
Summary:	Libraries used by xrootd servers and clients - compat version
Group:		System Environment/Libraries
#Conflicts:	xrootd-libs < 1:4.1.0

%description libs
This package contains libraries used by the xrootd servers and clients
(compat version 3.x).

%package client-libs
Summary:	Libraries used by xrootd clients - compat version
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
#Conflicts:	xrootd-client-libs < 1:4.1.0

%description client-libs
This package contains libraries used by xrootd clients (compat version 3.x).

%package server-libs
Summary:	Libraries used by xrootd servers - compat version
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{version}-%{release}
#Conflicts:	xrootd-server-libs < 1:4.1.0

%description server-libs
This package contains libraries used by xrootd servers (compat version 3.x).

%prep
%setup -q -n xrootd-%{version}

%build
mkdir build

pushd build
%cmake -DENABLE_PERL=FALSE -DENABLE_FUSE=FALSE ..
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

pushd build
make install DESTDIR=%{buildroot}
popd

# Remove server binaries not needed for compat package
rm -rf %{buildroot}%{_datadir}
rm %{buildroot}%{_bindir}/cconfig
rm %{buildroot}%{_bindir}/cns_ssi
rm %{buildroot}%{_bindir}/frm_admin
rm %{buildroot}%{_bindir}/frm_xfragent
rm %{buildroot}%{_bindir}/mpxstats
rm %{buildroot}%{_bindir}/wait41
rm %{buildroot}%{_bindir}/XrdCnsd
rm %{buildroot}%{_bindir}/xrdpwdadmin
rm %{buildroot}%{_bindir}/xrdsssadmin

# Remove client binaries not needed for compat package
rm %{buildroot}%{_bindir}/xprep
rm %{buildroot}%{_bindir}/xrd
rm %{buildroot}%{_bindir}/xrdadler32
rm %{buildroot}%{_bindir}/xrdcopy
rm %{buildroot}%{_bindir}/xrdcp
rm %{buildroot}%{_bindir}/xrdcp-old
rm %{buildroot}%{_bindir}/xrdfs
rm %{buildroot}%{_bindir}/xrdgsiproxy
rm %{buildroot}%{_bindir}/xrdstagetool

# Remove devel files not needed for compat package
rm -rf %{buildroot}%{_includedir}
rm %{buildroot}%{_libdir}/libXrdAppUtils.so
rm %{buildroot}%{_libdir}/libXrdCl.so
rm %{buildroot}%{_libdir}/libXrdClient.so
rm %{buildroot}%{_libdir}/libXrdCrypto.so
rm %{buildroot}%{_libdir}/libXrdCryptoLite.so
rm %{buildroot}%{_libdir}/libXrdFfs.so
rm %{buildroot}%{_libdir}/libXrdMain.so
rm %{buildroot}%{_libdir}/libXrdOfs.so
rm %{buildroot}%{_libdir}/libXrdPosix.so
rm %{buildroot}%{_libdir}/libXrdPosixPreload.so
rm %{buildroot}%{_libdir}/libXrdServer.so
rm %{buildroot}%{_libdir}/libXrdUtils.so

# Rename server binaries to allow parallel install
mv %{buildroot}%{_bindir}/cmsd %{buildroot}%{_bindir}/cmsd-3
mv %{buildroot}%{_bindir}/frm_purged %{buildroot}%{_bindir}/frm_purged-3
mv %{buildroot}%{_bindir}/frm_xfrd %{buildroot}%{_bindir}/frm_xfrd-3
mv %{buildroot}%{_bindir}/xrootd %{buildroot}%{_bindir}/xrootd-3

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post client-libs -p /sbin/ldconfig

%postun client-libs -p /sbin/ldconfig

%post server-libs -p /sbin/ldconfig

%postun server-libs -p /sbin/ldconfig

%files
%{_bindir}/cmsd-3
%{_bindir}/frm_purged-3
%{_bindir}/frm_xfrd-3
%{_bindir}/xrootd-3

%files libs
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

%files client-libs
%{_libdir}/libXrdCl.so.*
%{_libdir}/libXrdClient.so.*
%{_libdir}/libXrdFfs.so.*
%{_libdir}/libXrdPosix.so.*
%{_libdir}/libXrdPosixPreload.so.*

%files server-libs
%{_libdir}/libXrdBwm.so.*
%{_libdir}/libXrdOfs.so.*
%{_libdir}/libXrdPss.so.*
%{_libdir}/libXrdServer.so.*
%{_libdir}/libXrdXrootd.so.*
# Some of the libraries are used as plugins - need the .so symlink at runtime
%{_libdir}/libXrdBwm.so
%{_libdir}/libXrdPss.so
%{_libdir}/libXrdXrootd.so

%changelog
* Wed Feb 25 2015 Edgar Fajardo <emfajard@ucsd.edu> - 3.3.6-1.1
- Removed the conflicts to avoid rhel5 update failures

* Thu Nov 27 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.3.6-1
- Parallel installable compat package
