Name:           osg-se-bestman
Summary:        OSG BeStMan Storage Element package for RPM distribution
Version:        3.2
Release:        1%{?dist}
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# from VDT
Requires: osg-version
Requires: osg-system-profiler
Requires: bestman2-server
Requires: bestman2-client
Requires: bestman2-tester
Requires: edg-mkgridmap
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
# From osg-gridftp meta package
Requires: globus-gridftp-server-progs
Requires: vo-client
Requires: grid-certificates >= 7
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
* Fri Jul 17 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.2-1
- Require grid-certificates >= 7 (SOFTWARE-1883)
- Change version number to match release series

* Thu Apr 04 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-9
- Remove java dependency

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-8
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

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
