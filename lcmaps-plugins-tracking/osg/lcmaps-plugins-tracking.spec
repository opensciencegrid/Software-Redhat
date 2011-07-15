Summary: Process tracking plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-tracking
Version: 0.0.4
Release: 1%{?dist}
License: Unknown
Group: System Environment/Libraries
# The tarball was created from CVS using the following commands:
# cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only export -d lcmaps-plugins-tracking-0.0.4 -r glite-security-lcas-plugins-tracking_R_0_0_4 privilege/glite-security-lcmaps-plugins-tracking
# tar zcf lcmaps-plugins-tracking-0.0.4.tar.gz lcmaps-plugins-tracking-0.0.4/
Source0: %{name}-%{version}.tar.gz
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
%setup -q

%patch0 -p0

%build
./bootstrap
%configure --disable-static --with-glite-location=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/modules/lcmaps_tracking.mod
%{_libdir}/modules/liblcmaps_tracking.so.0
%{_libdir}/modules/liblcmaps_tracking.so.0.0.0
%exclude %{_libdir}/modules/*.so

%changelog
* Mon Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.4-1
- Initial build.


