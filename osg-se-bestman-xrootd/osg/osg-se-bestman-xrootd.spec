Name:           osg-se-bestman-xrootd
Summary:        OSG BeStMan XRootd Storage Element package
Version:        3.0.0
Release:        1
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome
BuildArch:      noarch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# from VDT
Requires: java-1.6.0-sun-compat
Requires: bestman2-server
Requires: bestman2-client
Requires: bestman2-tester
Requires: edg-mkgridmap
Requires: fetch-crl
# From osg-gridftp meta package
Requires: globus-gridftp-server-progs
Requires: vo-client
Requires: grid-certificates
Requires: gratia-probe-gridftp-transfer
Requires: gums-client
%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif

#Xrootd stuff
Requires: xrootd-dsi
Requires: xrootd-fuse
Requires: gratia-xrootd-transfer-probe
Requires: gratia-xrootd-storage-probe


%description
This is a meta-package for the BeStMan (Berkeley Storage Manager)
with underlying xrootd storage element using fuse/dsi module.

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Thu Sep 1 2011 Doug Strain <dstrain@fnal.gov> - 3.0.0-1
- Initial creation of osg-se-bestman-xrootd meta package
