Name:           xrootd-dsi
Version:        3.0.4
Release:        7
Summary:        xrootd DSI library and POSIX preload
Group:          System Environment/Daemons
License:        Stanford (modified BSD with advert clause)
URL:            http://xrootd.org/

Source0:        xrootd-dsi.tar.gz
Source1:        gridftp-xrootd.conf
Source2:        xrootd-dsi-environment
Patch0:        xrootd-dsi.patch

BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires: globus-common-devel globus-gridftp-server-devel zlib-devel
Requires: xrootd-client xrootd-libs 
#Hold off on these for now
#vdt-compat globus-base-data-server
Conflicts: gridftp-hdfs

%description
DSI module and POSIX preload libraries for Xrootd

%prep
%setup -q -n %{name}
%patch0 -p1

%build

make

%install

#This script is no longer needed.  Variables added in gridftp package
#mkdir -p $RPM_BUILD_ROOT/opt/vdt/setup.d
#install -m 755 xrootd-gsiftp.sh $RPM_BUILD_ROOT/opt/vdt/setup.d/xrootd-gsiftp.sh

mkdir -p $RPM_BUILD_ROOT/etc/xrootd-dsi
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig/gridftp.conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/xrootd-dsi
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/gridftp.conf.d

%ifarch x86_64
mkdir -p $RPM_BUILD_ROOT/usr/lib64
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/usr/lib64/libglobus_gridftp_server_posix.so
sed -i 's/XROOTDLIB=\/usr\/lib/XROOTDLIB=\/usr\/lib64/' $RPM_BUILD_ROOT/etc/sysconfig/gridftp.conf.d/xrootd-dsi-environment
%endif
%ifarch i386
mkdir -p $RPM_BUILD_ROOT/usr/lib
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/usr/lib/libglobus_gridftp_server_posix.so
%endif

%files
/etc/xrootd-dsi/gridftp-xrootd.conf
/etc/sysconfig/gridftp.conf.d/xrootd-dsi-environment

%ifarch x86_64
/usr/lib64/libglobus_gridftp_server_posix.so
%endif

%ifarch i386
/usr/lib/libglobus_gridftp_server_posix.so
%endif


%changelog
* Tue Oct 11 2011 Doug Strain <dstrain@fnal.gov> 3.0.4-7
- Putting conf variables in gridftp.conf.d

* Fri Sep 30 2011 Jeff Dost <jdost@ucsd.edu> - 3.0.4-6
- Add Conflicts line to block if gridftp-hdfs is installed

* Thu Sep 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.4-5
Rebuild against updated Globus libraries

* Thu Sep 1 2011 Doug Strain <dstrain@fnal.gov> 3.0.4-4
- Fixed build for Globus 5.2 and got rid of setup.sh script.

* Tue Aug 16 2011 Doug Strain <dstrain@fnal.gov> 3.0.4-2
- Modified package to use epel libraries and header files.
- Now uses FHS locations

* Mon Jun 14 2011 Doug Strain <dstrain@fnal.gov> 3.0.4
- Created package for xrootd-dsi
