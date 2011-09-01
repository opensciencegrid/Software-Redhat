Name:           xrootd-dsi
Version:        3.0.4
Release:        3
Summary:        xrootd DSI library and POSIX preload
Group:          System Environment/Daemons
License:        Stanford (modified BSD with advert clause)
URL:            http://xrootd.org/

Source:        xrootd-dsi.tar.gz
Patch0:        xrootd-dsi.patch

BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires: globus-common-devel globus-gridftp-server-devel zlib-devel
Requires: xrootd-client xrootd-libs 
#Hold off on these for now
#vdt-compat globus-base-data-server

%description
DSI module and POSIX preload libraries for Xrootd

%prep
%setup -q -n %{name}
%patch0 -p1

%build

make

%install

mkdir -p $RPM_BUILD_ROOT/opt/vdt/setup.d
install -m 755 xrootd-gsiftp.sh $RPM_BUILD_ROOT/opt/vdt/setup.d/xrootd-gsiftp.sh

%ifarch x86_64
mkdir -p $RPM_BUILD_ROOT/usr/lib64
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/usr/lib64/libglobus_gridftp_server_posix.so
%endif
%ifarch i386
mkdir -p $RPM_BUILD_ROOT/usr/lib
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/usr/lib/libglobus_gridftp_server_posix.so
%endif

%files

/opt/vdt/setup.d
/opt/vdt/setup.d/xrootd-gsiftp.sh

%ifarch x86_64
/usr/lib64/libglobus_gridftp_server_posix.so
%endif

%ifarch i386
/usr/lib/libglobus_gridftp_server_posix.so
%endif


%changelog
* Tue Aug 16 2011 Doug Strain <dstrain@fnal.gov> 3.0.4-2
- Modified package to use epel libraries and header files.
- Now uses FHS locations

* Mon Jun 14 2011 Doug Strain <dstrain@fnal.gov> 3.0.4
- Created package for xrootd-dsi
