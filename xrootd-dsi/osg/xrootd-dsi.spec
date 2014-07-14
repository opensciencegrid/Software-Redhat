Name:           xrootd-dsi
Version:        3.0.4
Release:        12%{?dist}
Summary:        xrootd DSI library and POSIX preload
Group:          System Environment/Daemons
License:        Stanford (modified BSD with advert clause)
URL:            http://xrootd.org/

Source0:        xrootd-dsi.tar.gz
Source1:        gridftp-xrootd.conf
Source2:        globus-gridftp-server-plugin.osg-sysconfig
Patch0:         xrootd-dsi.patch

BuildRoot:      %{_tmppath}/%{name}-root
BuildRequires: globus-common-devel globus-gridftp-server-devel zlib-devel
Requires: xrootd4-client >= 1:4.0.1
Requires: xrootd4-libs >= 1:4.0.1
Requires: globus-gridftp-server-progs >= 6.14-2
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
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/xrootd-dsi
mkdir -p $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/globus-gridftp-server-plugin

%ifarch x86_64
mkdir -p $RPM_BUILD_ROOT/usr/lib64
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/usr/lib64/libglobus_gridftp_server_posix.so
sed -i 's/XROOTDLIB=\/usr\/lib/XROOTDLIB=\/usr\/lib64/' $RPM_BUILD_ROOT/usr/share/osg/sysconfig/globus-gridftp-server-plugin
%endif
%ifarch i386
mkdir -p $RPM_BUILD_ROOT/usr/lib
install -m 644 libglobus_gridftp_server_posix.so $RPM_BUILD_ROOT/usr/lib/libglobus_gridftp_server_posix.so
%endif

%files
/etc/xrootd-dsi/gridftp-xrootd.conf
/usr/share/osg/sysconfig/globus-gridftp-server-plugin

%ifarch x86_64
/usr/lib64/libglobus_gridftp_server_posix.so
%endif

%ifarch i386
/usr/lib/libglobus_gridftp_server_posix.so
%endif


%changelog
* Mon Jul 14 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 3.0.4-12
- Rebuild against xrootd4

* Thu Apr 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.4-11
- Explicitly require xrootd 3.3.1

* Wed Apr 03 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.4-10
- Bump to rebuild against xrootd 3.3.1

* Wed Feb 20 2013 Dave Dykstra <dwd@fnal.gov> 3.0.4-9
- Move environment variables from /etc/syscconfig/gridftp.conf.d
  to /usr/share/osg/sysconfig/globus-gridftp-server-plugin

* Tue Jan 22 2013 Doug Strain <dstrain@fnal.gov> 3.0.4-8
- Rebuild for gridftp 6.14

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
