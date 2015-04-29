Name:      osg-gridftp
Summary:   Standalone OSG GridFTP w/lcmaps gums client
Version:   3.3
%if 0%{?el7}
%define release_suffix _clipped
%endif
Release:   1%{?release_suffix}%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Source1: udt-%{name}.conf

Requires: osg-version
Requires: osg-system-profiler
Requires: globus-gridftp-server-progs
Requires: vo-client
Requires: grid-certificates
Requires: gratia-probe-gridftp-transfer
%if ! 0%{?el7}
Requires: gums-client
%endif
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
#This is probably not needed
#Requires: edg-mkgridmap

%if 0%{?rhel} >= 6
Requires: globus-xio-udt-driver
%endif

%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif

# This should also pull in lcas, lcmaps, and various plugins
# (basic, proxy verify, posix, etc)

%description
This is a meta package for a standalone GridFTP server with 
gums support through lcmaps plugin and vo-client.

%build

%install
%if 0%{?rhel} >= 6
mkdir -p %{buildroot}%{_sysconfdir}/gridftp.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/gridftp.d/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%if 0%{?rhel} >= 6
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/gridftp.d/udt-%{name}.conf
%endif


%changelog
* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue Apr 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-11_clipped
- Create clipped version for el7

* Thu Mar 13 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-9
- Add globus-xio-udt-driver dependency for el6, and enable by default in
  /etc/gridftp.d/ (SOFTWARE-1412)

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-8
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-7
- Added dependencies on osg-version and osg-system-profiler

* Fri Nov 3 2011 Doug Strain <dstrain.fnal.gov> - 3.0.0-6
- Added fetch-crl to the requirements

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-5
- Do not mark this as a noarch package, as we depend directly on a arch-specific RPM.

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-4
Another update to get Requires right for 32-bit modules

* Fri Aug 26 2011 Doug Strain <dstrain.fnal.gov> 
- Created an initial gridftp-standalone meta package RPM.

