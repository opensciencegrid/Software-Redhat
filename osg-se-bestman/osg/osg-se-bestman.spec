Name:           osg-se-bestman
Summary:        OSG BeStMan Storage Element package for RPM distribution
Version:        3.0.0
Release:        7%{?dist}
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# from VDT
Requires: osg-version
Requires: osg-system-profiler
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



%description
This is a meta-package for the BeStMan (Berkeley Storage Manager)
with underlying gridFTP and related packages.  This will
also install lcas/lcmaps plugins for gums integration.
Utilities such as fetch-crl, client tools, bestman2 tester,
and edg-mkgridmap are included for convenience.

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-7
- Added dependencies on osg-version and osg-system-profiler

* Wed Sep 28 2011 Doug Strain <dstrain@fnal.gov> - 3.0.0-6
-Getting rid of noarch since this has liblcas arch-sepcific deps

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-5
Another update to get Requires right for 32-bit modules

* Wed Aug 31 2011 Doug Strain <dstrain@fnal.gov> - 3.0.0-4
- Fixed package dependencies to use same as osg-gridftp

* Thu Aug 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-3
- Require virtual dep grid-certificates, not actual package osg-ca-certs.

* Wed Jul 20 2011 Alex Sim <asim@lbl.gov>
- Created an initial osg-se-bestman RPM
