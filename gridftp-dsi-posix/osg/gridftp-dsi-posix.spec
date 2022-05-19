%if 0%{?el8}
%global __debug_install_post %{nil}
%global debug_package %{nil}
%endif

Name:           gridftp-dsi-posix
Epoch:          1
Version:        1.4
Release:        3%{?dist}
Summary:        DSI library and POSIX preload
License:        Stanford (modified BSD with advert clause)
URL:            https://github.com/wyang007/gridftp_dsi_posix

Source0:        %{name}-%{version}.tar.gz
Source1:        gridftp-xrootd.conf
Source2:        globus-gridftp-server-plugin.osg-sysconfig
Source3:        gridftp-xrootd.osg-extensions.conf

BuildRequires:  globus-common-devel globus-gridftp-server-devel zlib-devel

Obsoletes: xrootd-dsi < 3.0.5
Provides: xrootd-dsi = %{epoch}:%{version}
Provides: xrootd-dsi%{_isa} = %{epoch}:%{version}

Requires: xrootd-client >= 1:4.0.0
Requires: xrootd-libs >= 1:4.0.0

Requires: globus-gridftp-server-progs >= 6.14-2
Requires: globus-gridftp-osg-extensions

Conflicts: gridftp-hdfs

%description
DSI module and POSIX preload libraries

%prep
%setup -q

%build

make

%install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-dsi-posix
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-dsi-posix/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-dsi-posix/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/osg/sysconfig
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/osg/sysconfig/globus-gridftp-server-plugin
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
touch $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gridftp-dsi-posix

%ifarch x86_64
sed -i 's/XROOTDLIB=\/usr\/lib/XROOTDLIB=\/usr\/lib64/' $RPM_BUILD_ROOT%{_datadir}/osg/sysconfig/globus-gridftp-server-plugin
%endif

mkdir -p $RPM_BUILD_ROOT%{_libdir}
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT%{_libdir}

%files
%config(noreplace) %{_sysconfdir}/sysconfig/gridftp-dsi-posix
%{_sysconfdir}/gridftp-dsi-posix/gridftp-xrootd.conf
%{_sysconfdir}/gridftp-dsi-posix/gridftp-xrootd.osg-extensions.conf
%{_datarootdir}/osg/sysconfig/globus-gridftp-server-plugin
%{_libdir}/libglobus_gridftp_server_posix.so

%changelog
* Wed Apr 07 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1:1.4-3
- Packaging changes for EL8 (SOFTWARE-4231):
    - Apparently %{_isa} is not allowed in Obsoletes clauses on EL8; package names only
    - Disable debuginfo package generator since it doesn't find any files

* Thu Jun 22 2017 Brian Lin <blin@cs.wisc.edu> - 1:1.4-2
- Added architecture-specific provides for xrootd-dsi
- Refer to gridftp-dsi-posix paths in globus-gridftp-server-plugin

* Wed Jun 21 2017 Brian Lin <blin@cs.wisc.edu> - 1.4-1
- Add support to GLOBUS_GFS_CMD_SITE_RDEL
- Add GRIDFTP_APPEND_XROOTD_CGI hook (environment variable) to support Xrootd space token.
- Renamed xrootd-dsi packaging to reflect upstream
