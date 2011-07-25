Summary: Process tracking plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-glexec-tracking
Version: 0.0.5
Release: 1%{?dist}
License: EGEE Middleware and ASL and Fermitools
Group: System Environment/Libraries
# The tarball was created from CVS using the following commands:
# cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only export -d lcmaps-plugins-glexec-tracking-0.0.5 -r lcmaps-plugins-glexec-tracking_R_0_0_5 privilege/lcmaps-plugins-glexec-tracking
# tar zcf lcmaps-plugins-glexec-tracking/0.0.5/lcmaps-plugins-glexec-tracking-0.0.5.tar.gz lcmaps-plugins-glexec-tracking-0.0.5/
Source0: %{name}-%{version}.tar.gz
Patch0: glexec_location.patch
BuildRequires: lcmaps-interface
BuildRequires: libtool automake autoconf
Requires: /usr/sbin/condor_procd
Requires: /usr/sbin/gidd_alloc
Requires: /usr/sbin/procd_ctl
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This plugin utilizes the Condor procd to track the processes spawned
by glexec.

%prep
%setup -q -a0

pushd src/glexec-tracking
%patch0 -p0
popd


%build
./bootstrap
%configure --disable-static --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
mv $RPM_BUILD_ROOT/%{_libdir}/lcmaps $RPM_BUILD_ROOT/%{_libdir}/modules
ln -s liblcmaps_glexec_tracking.so $RPM_BUILD_ROOT/%{_libdir}/modules/liblcmaps_glexec_tracking.so.0
ln -s liblcmaps_glexec_tracking.so.0 $RPM_BUILD_ROOT/%{_libdir}/modules/liblcmaps_glexec_tracking.so.0.0.0
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/modules/lcmaps_glexec_tracking.mod
%{_libdir}/modules/liblcmaps_glexec_tracking.so
%{_libdir}/modules/liblcmaps_glexec_tracking.so.0
%{_libdir}/modules/liblcmaps_glexec_tracking.so.0.0.0
%{_sbindir}/glexec_monitor

%changelog
* Mon Jul 18 2011 Dave Dykstra <dwd@fnal.gov> 0.0.5-1
- Based on CVS with glexec-tracking name
- Make -procdir option default to '/usr', and if default is taken
  find procd_ctl in bin instead of sbin.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.4-2
- Include glexec_monitor in package.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.4-1
- Initial build.
