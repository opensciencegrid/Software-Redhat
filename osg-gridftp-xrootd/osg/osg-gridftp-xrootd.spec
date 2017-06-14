Name:           osg-gridftp-xrootd
Summary:        OSG GridFTP XRootd Storage Element package
Version:        3.4
Release:        1%{?dist}
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# from VDT
Requires: osg-version
Requires: osg-system-profiler
Requires: fetch-crl
# From osg-gridftp meta package
Requires: globus-gridftp-server-progs
Requires: vo-client
Requires: grid-certificates >= 7
Requires: gratia-probe-gridftp-transfer
%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif

#Xrootd stuff
Requires: xrootd-dsi
Requires: xrootd-fuse >= 1:4.1.0
Requires: gratia-probe-xrootd-transfer >= 1.17.0-1
Requires: gratia-probe-xrootd-storage


%description
This is a meta-package for the BeStMan (Berkeley Storage Manager)
with underlying xrootd storage element using fuse/dsi module.

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Tue May 23 2017 Brian Lin <blin@cs.wisc.edu> 3.4-1
- Rebuild for OSG 3.4

* Thu Aug 25 2016 Carl Edquist <edquist@cs.wisc.edu> - 3.3-3
- drop gums-client dependency (SOFTWARE-2398)
- remove rhel5-specific macros (OSG-3.2 EOL)

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue Mar 31 2015 Edgar Fajardo <emfajard@ucsd.edu> - 3.0.0-6
- Removed the xroot4-fuse for xrootd-fuse and version

* Tue Aug 12 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-5
- Update xrootd-fuse requirement to xrootd4-fuse

* Thu Apr 04 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-4
- Remove java dependency.

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-3
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-2
- Added dependencies on osg-version and osg-system-profiler

* Fri Oct 21 2011 Doug Strain <dstrain@fnal.gov> - 3.0.0-1
- Initial creation of osg-gridftp-xrootd meta package
- Needed for Xrootd installation with multiple GridFTP

