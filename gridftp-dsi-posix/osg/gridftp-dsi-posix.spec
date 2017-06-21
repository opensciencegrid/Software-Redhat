Name:           gridftp-dsi-posix
Version:        1.4
Release:        1%{?dist}
Summary:        DSI library and POSIX preload
Group:          System Environment/Daemons
License:        Stanford (modified BSD with advert clause)
URL:            https://github.com/wyang007/gridftp_dsi_posix

Source0:        %{name}-%{version}.tar.gz
Source1:        gridftp-xrootd.conf
Source2:        globus-gridftp-server-plugin.osg-sysconfig
Source3:        gridftp-xrootd.osg-extensions.conf

BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  globus-common-devel globus-gridftp-server-devel zlib-devel

Obsoletes: xrootd-dsi < 3.0.5
Provides: xrootd-dsi

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
* Wed Jun 21 2017 Brian Lin <blin@cs.wisc.edu> - 1.4-1
- Add support to GLOBUS_GFS_CMD_SITE_RDEL
- Add GRIDFTP_APPEND_XROOTD_CGI hook (environment variable) to support Xrootd space token.
- Renamed xrootd-dsi packaging to reflect upstream
