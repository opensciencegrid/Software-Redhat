Name:           xrootd-dsi
Version:        3.0.4
Release:        1
Summary:        xrootd DSI library and POSIX preload
Group:          System Environment/Daemons
License:        Stanford (modified BSD with advert clause)
URL:            http://xrootd.org/

Source:        xrootd-dsi.tar.gz

BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires: globus-core globus-base-essentials globus-base-sdk gcc
Requires: xrootd-client xrootd-libs vdt-compat globus-base-data-server

%description
DSI module and POSIX preload libraries for Xrootd

%prep
%setup -q -n %{name}

%build

%ifarch x86_64
export FLAVOR='gcc64dbg'
%endif
%ifarch i386
export FLAVOR='gcc32dbg'
%endif
export GLOBUS_LOCATION=/opt/vdt/globus
export GPT_LOCATION=/opt/vdt/gpt
export GPT_INSTALL_LOCATION=/opt/vdt/globus
/opt/vdt/gpt/sbin/gpt-build -force -nosrc $FLAVOR
/opt/vdt/globus/bin/globus-makefile-header --flavor=$FLAVOR > makefile_header
make

%install

mkdir -p $RPM_BUILD_ROOT/opt/vdt/setup.d
mkdir -p $RPM_BUILD_ROOT/opt/vdt/globus/lib
install -m 755 xrootd-gsiftp.sh $RPM_BUILD_ROOT/opt/vdt/setup.d/xrootd-gsiftp.sh

%ifarch x86_64
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/opt/vdt/globus/lib/libglobus_gridftp_server_posix_gcc64dbg.so
%endif
%ifarch i386
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/opt/vdt/globus/lib/libglobus_gridftp_server_posix_gcc32dbg.so
%endif

%files

/opt/vdt/setup.d
/opt/vdt/setup.d/xrootd-gsiftp.sh

%ifarch x86_64
/opt/vdt/globus/lib/libglobus_gridftp_server_posix_gcc64dbg.so
%endif

%ifarch i386
/opt/vdt/globus/lib/libglobus_gridftp_server_posix_gcc32dbg.so
%endif


%changelog
* Mon Jun 14 2011 Doug Strain <dstrain@fnal.gov> 3.0.4
Created package for xrootd-dsi
