Summary: Process tracking plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-glexec-tracking
Version: 0.0.4
Release: 1%{?dist}
License: Unknown
Group: System Environment/Libraries
# The tarball was created from CVS using the following commands:
# cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only export -d lcmaps-plugins-glexec-tracking-0.0.4 -r glite-security-lcas-plugins-tracking_R_0_0_4 privilege/glite-security-lcmaps-plugins-tracking
# tar zcf lcmaps-plugins-glexec-tracking-0.0.4.tar.gz lcmaps-plugins-glexec-tracking-0.0.4/
Source0: %{name}-%{version}.tar.gz
# This tarball was created from HEAD on 15 July 2011
# cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only export -r HEAD -d glexec_monitor privilege/glexec-osg/contrib/glexec_monitor
# tar zcf glexec_monitor.tar.gz glexec_monitor
Source1: glexec_monitor.tar.gz

Patch0: fedora_file_locations.patch
BuildRequires: lcmaps-interface
BuildRequires: libtool automake autoconf
BuildRequires:  glite-build-common-cpp
Requires: /usr/sbin/condor_procd
Requires: /usr/sbin/gidd_alloc
Requires: /usr/sbin/procd_ctl
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This plugin utilizes the Condor procd to track the processes spawned
by glexec.

%prep
%setup -q -a1

%patch0 -p0

%build
./bootstrap
%configure --disable-static --with-glite-location=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
cp glexec_monitor/glexec_monitor $RPM_BUILD_ROOT%{_sbindir}/glexec_monitor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/modules/lcmaps_tracking.mod
%{_libdir}/modules/liblcmaps_tracking.so
%{_libdir}/modules/liblcmaps_tracking.so.0
%{_libdir}/modules/liblcmaps_tracking.so.0.0.0
%{_sbindir}/glexec_monitor

%changelog
* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.4-2
- Include glexec_monitor in package.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.4-1
- Initial build.


