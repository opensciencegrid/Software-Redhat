Name:      osg-gridftp
Summary:   Standalone OSG GridFTP w/lcmaps gums client
Version:   3.0.0
Release:   7
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: osg-version
Requires: osg-system-profiler
Requires: globus-gridftp-server-progs
Requires: vo-client
Requires: grid-certificates
Requires: gratia-probe-gridftp-transfer
Requires: gums-client
Requires: fetch-crl
#This is probably not needed
#Requires: edg-mkgridmap


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

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
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

