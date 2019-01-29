Name:           vo-client
Version:        85
Release:        2%{?dist}
Summary:        Contains vomses file for use with user authentication

Group:          System Environment/Base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildArch:      noarch

Requires: grid-certificates >= 7

Source0:        %{name}-%{version}.tar.gz

# See
# https://opensciencegrid.github.io/technology/software/create-vo-client/
# for instructions


%description
%{summary}

%package lcmaps-voms
Summary:        Provides a voms-mapfile-default file, mapping VOMS FQANs to Unix users suitable for use by the LCMAPS VOMS plugin
Group:          system environment/base
Requires:       %{name} = %{version}-%{release}

%description lcmaps-voms
%{summary}

%package dcache
Summary:        Provides a grid-vorolemap file for use by dCache, similar to voms-mapfile-default
Group:          system environment/base
Requires:       %{name} = %{version}-%{release}

%description dcache
%{summary}


%prep
%setup

%build
make

%install
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -d $RPM_BUILD_ROOT/%{_datadir}/osg/
mv vomses $RPM_BUILD_ROOT/%{_sysconfdir}/
mv voms-mapfile-default $RPM_BUILD_ROOT/%{_datadir}/osg/
mv grid-vorolemap $RPM_BUILD_ROOT/%{_datadir}/osg/

chmod 644 $RPM_BUILD_ROOT/%{_sysconfdir}/vomses
chmod 644 $RPM_BUILD_ROOT/%{_datadir}/osg/voms-mapfile-default
chmod 644 $RPM_BUILD_ROOT/%{_datadir}/osg/grid-vorolemap

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/
mv vomsdir $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/
find $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir -type f -exec chmod 644 {} \;
find $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir -type d -exec chmod 755 {} \;

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/vomses
%config(noreplace) %{_sysconfdir}/grid-security/vomsdir

%files lcmaps-voms
%defattr(-,root,root,-)
%{_datadir}/osg/voms-mapfile-default

%files dcache
%defattr(-,root,root,-)
%config(noreplace) %{_datadir}/osg/grid-vorolemap

%changelog
* Fri Jan 25 2019 Carl Edquist <edquist@cs.wisc.edu> - 85-2
- Drop osg-gums-config and edgmkgridmap subpackages (SOFTWARE-3542)
- Clean up build process

* Mon Dec 17 2018 Carl Edquist <edquist@cs.wisc.edu> - 85-1
- Update INFN CA DN
- Add backup VOMS server for enmr.eu and glast.org (SOFTWARE-3513)

* Mon Oct 01 2018 Carl Edquist <edquist@cs.wisc.edu> - 84-1
- Add dteam VO (SOFTWARE-3426)

* Mon Sep 10 2018 Carl Edquist <edquist@cs.wisc.edu> - 83-1
- Update LSC and vomses entries for SuperCDMS and LSST (SOFTWARE-3402)

* Tue Aug 21 2018 Carl Edquist <edquist@cs.wisc.edu> - 81-1
- Drop '/*' and '/Capability=...' for grid-vorolemap (SOFTWARE-3222)

* Thu Jul 19 2018 Carl Edquist <edquist@cs.wisc.edu> - 80-1
- Add dcache subpackage with /usr/share/osg/grid-vorolemap (SOFTWARE-3222)

* Fri May 04 2018 Carl Edquist <edquist@cs.wisc.edu> - 79-1
- Add new InCommon VOMS cert for OSG (SOFTWARE-3248)

* Fri Mar 30 2018 Carl Edquist <edquist@cs.wisc.edu> - 78-1
- Add manual mapfile generator script
- Handle matchFQAN=vorole in voms-mapfile generator (SOFTWARE-3183)
- Atlas VO updates (SOFTWARE-3183)

* Fri Feb 16 2018 Carl Edquist <edquist@cs.wisc.edu> - 77-2
- Add dependency for lcmaps-voms on the main vo-client package (SOFTWARE-3137)

* Mon Dec 04 2017 Carl Edquist <edquist@cs.wisc.edu> - 77-1
- Update to vo-client 77
  - Remove voms1.egee.cesnet.cz (auger) VOMS server (SOFTWARE-3042)

* Mon Oct 30 2017 Carl Edquist <edquist@cs.wisc.edu> - 76-1
- Update to vo-client 76
  - Drop redundant geant4-lcgadmin objects (SOFTWARE-2921)
  - Additional snoplus voms servers (SOFTWARE-2965)

* Fri Sep 08 2017 Carl Edquist <edquist@cs.wisc.edu> - 75-1
- Update to vo-client 75
  - Add CMS wildcard to default map file (SOFTWARE-2852)

* Fri Jun 09 2017 Carl Edquist <edquist@cs.wisc.edu> - 74-1
- Update to vo-client 74 (SOFTWARE-2765)
  - Fix the edg-mkgridmap entries for project8 and miniclean (SOFTWARE-2727)
  - Add new VOMS entry for CIGI (SOFTWARE-2712)
    - https://ticket.opensciencegrid.org/33374
  - Add LIGO entry to GUMS template (SOFTWARE-2762)
  - Fix vo-client ATLAS mappings (SOFTWARE-2753)

* Wed Apr 26 2017 Carl Edquist <edquist@cs.wisc.edu> - 73-1
- Update to vo-client 73 (SOFTWARE-2710)
  - Update edg-mkgridmap CDF entry to match vomses #13
  - Remove LIGO server from GUMS template #14
  - Remove unused CDF glidecaf settings #15
    - https://ticket.opensciencegrid.org/33395
  - drop /production role for des vomsUserGroup #17 (SOFTWARE-2350)
  - Update default CMS mappings #18 (SOFTWARE-2691)
    - https://ticket.opensciencegrid.org/33396#1491658593
  - Update default Fermilab / FIFE mappings #19 (SOFTWARE-2690)
    - https://ticket.opensciencegrid.org/33395#1491839472

* Wed Mar 22 2017 Carl Edquist <edquist@cs.wisc.edu> - 72-2
- Update changelog for 72-1 build (SOFTWARE-2643)

* Mon Mar 20 2017 Carl Edquist <edquist@cs.wisc.edu> - 72-1
- Update to vo-client 72 (SOFTWARE-2643)
  - Remove NYSGRID, CSIU, & OSGEDU VOs
  - Add voms.grid.iu.edu voms server for OSG VO

* Wed Mar 01 2017 Carl Edquist <edquist@cs.wisc.edu> - 71-4
- Keep FNAL (non-INFN.IT) CDF voms servers (SOFTWARE-2612)

* Thu Feb 23 2017 Carl Edquist <edquist@cs.wisc.edu> - 71-3
- Include vo-client-lcmaps-voms sub-package with voms-mapfile-default
  for use by the LCMAPS VOMS plugin (SOFTWARE-2609, SOFTWARE-2563)

* Mon Feb 20 2017 Carl Edquist <edquist@cs.wisc.edu> - 71-2
- Remove dependent objects for cdf, cdf1 voms servers (SOFTWARE-2612)

* Fri Feb 17 2017 Carl Edquist <edquist@cs.wisc.edu> - 71-1
- Update to vo-client 71 (SOFTWARE-2612)
  - Remove cdf, cdf1 voms servers

* Wed Jan 18 2017 Carl Edquist <edquist@cs.wisc.edu> - 70-1
- Update to vo-client 70 (SOFTWARE-2567)
  - Remove MCDRD VO

* Wed Oct 05 2016 Carl Edquist <edquist@cs.wisc.edu> - 69-1
- Update to vo-client 69 (SOFTWARE-2473)
  - Removed LBNE
  - Removed CDF INFN
  - Added MINICLEAN

* Wed Sep 07 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 68-2
- Update to vo-client 68 (SOFTWARE-2445)
  - Added project8

* Mon Jul 25 2016 Carl Edquist <edquist@cs.wisc.edu> - 67-1
- Corrected edg-mkgridmap.config for ILC (SOFTWARE-2402)

* Wed May 04 2016 Carl Edquist <edquist@cs.wisc.edu> - 66-1
- Update to vo-client 66 (SOFTWARE-2316)
  - LZ, DREAM, CIGI, SURAGRID Update to CILogon
  - OSG IU VOMS Removal
  - COMPBIOGRID Removal
  - NEES VO Removal

* Fri Apr 01 2016 Carl Edquist <edquist@cs.wisc.edu> - 65-2
- Update DN/CA for osg/voms1.opensciencegrid.org (SOFTWARE-2265)

* Thu Mar 31 2016 Carl Edquist <edquist@cs.wisc.edu> - 65-1
- Update to vo-client 65 (SOFTWARE-2265)
  - Added SuperCDMS VO
  - Update HCC & GLOW DNs
  - Update 11 voms1.fnal.gov DNs

* Mon Feb 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 64-1
- Update to vo-client 64 (SOFTWARE-2218)
  - New VOMS servers DNs for DOSAR, SBGrid, NYSGRID

* Fri Jan 29 2016 Carl Edquist <edquist@cs.wisc.edu> - 63-1
- Update to vo-client 63 (SOFTWARE-2186)
  - Drop UC3 and osgcrossce VOs
  - Transition OSG VO to CILogon OSG CA
  - Change DN of VOMS servers for Star, Gluex, MIS, & osgedu VOs

* Mon Jan 11 2016 Carl Edquist <edquist@cs.wisc.edu> - 62-2
- Update FNAL VOMS Server CA (SOFTWARE-2154)

* Wed Jan 06 2016 Carl Edquist <edquist@cs.wisc.edu> - 62-1
- Update to vo-client 62 (SOFTWARE-2154)
  - Update FNAL VOMS Server DN
  - Drop LIGO VO

* Fri Aug 07 2015 Carl Edquist <edquist@cs.wisc.edu> - 61-1
- Update to vo-client 61 (SOFTWARE-1993)
  - Added DUNE VO

* Tue Jul 07 2015 Carl Edquist <edquist@cs.wisc.edu> - 60-1
- Update to vo-client 60 (SOFTWARE-1967)
  - Added LZ VO

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 59-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Fri May 15 2015 Carl Edquist <edquist@cs.wisc.edu> - 59-1
- Update to vo-client 59 (SOFTWARE-1747)
  - Restructured/removed various Fermilab entries from gums template
  - Removed ATLAS VOMS server vo.racf.bnl.gov
  - Removed GPN, Superbvo VOs
  - Updated nysgrid VOMS address to NYSGRID

* Thu Dec 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 58-3
- Fix https:/// in url (SOFTWARE-1711)

* Thu Dec 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 58-2
- Bring .lsc files up to date (SOFTWARE-1711)

* Wed Dec 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 58-1
- Update to vo-client 58 (SOFTWARE-1711)
  - Added Fermilab Analysis Role
  - Removed all old CERN VOMS addresses
  - Replaced old {lcg-,}voms.cern.ch with {lcg-,}voms2.cern.ch

* Thu Nov 06 2014 Carl Edquist <edquist@cs.wisc.edu> - 57-1
- Update to vo-client 57 (SOFTWARE-1657)
  - Switched voms.cern.ch to voms2.cern.ch
  - Vomses additions for atlas, cms, alice, ops, geant4

* Mon Aug 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 56-1
- Update to vo-client 56 (SOFTWARE-1562)
  - Remove I2U2 VO
  - Remove (lcg-)voms2.cern.ch servers for atlas & cms

* Tue Jul 01 2014 Carl Edquist <edquist@cs.wisc.edu> - 55-1
- Update to vo-client 55 (SOFTWARE-1528)
  - Add snoplus.snolab.ca VO
  - Remove Engage VO
  - Cleanup:
    - Update all outdated LSC files (including dosar)
    - Fix DN mismatches in vomses
    - Remove old LSC files no longer in vomses

* Fri May 23 2014 Carl Edquist <edquist@cs.wisc.edu> - 54-1
- Update to vo-client 54 (SOFTWARE-1491)
  - Add missing LSC files for voms2.cern.ch and lcg-voms2.cern.ch

* Thu May 08 2014 Carl Edquist <edquist@cs.wisc.edu> - 53-1
- Update to vo-client 53 (SOFTWARE-1473)
  - Modify CMS VOMS Address in GUMS Template
  - Modify ILC VOMS Address in GUMS Template and vomses file
  - Modify CompBioGrid vomses entry

* Mon Feb 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 52-1
- Update to vo-client 52 (SOFTWARE-1444)
  - Add New Sub-VOs Lariat, Gendetrd, Lar1, and Okra
  - New stanzas for Production Analysis and Glidein roles in gums template
  - New VOMS Servers at CERN
  - Removed Dayabay VO

* Mon Feb 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 51-1
- Update to vo-client 51 (SOFTWARE-1372)
  - VOs hosted by Fermilab VOMS server transitioned to DigiCert certificates
  - voms.fnal.gov was replaced by voms1/2.fnal.gov
  - voms.opensciencegrid.org replaced by voms1/2.opensciencegrid.org
  - Reference to GOC VOMS server corrected in gums template
  - SBGrid LSC file updated for new DigiCert certificate

* Fri Jan 10 2014 Carl Edquist <edquist@cs.wisc.edu> - 50-2
- Remove trailing slash from atlas/ in edg-mkgridmap.conf (SOFTWARE-1344)

* Tue Jan 07 2014 Carl Edquist <edquist@cs.wisc.edu> - 50-1
- Update to vo-client 50 (SOFTWARE-1344)
  - Add vo.cta.in2p3.fr VO
  - Add xenon-biggrid.nl VO
  - OSGCrossCE Configuration Change

* Wed Nov 06 2013 Carl Edquist <edquist@cs.wisc.edu> - 49-1
- Update to vo-client 49 (SOFTWARE-1248)

* Fri Oct 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 48-1
- Update to vo-client 48 (SOFTWARE-1216)

* Tue Sep 03 2013 Brian Lin <blin@cs.wisc.edu> - 47-1
- Updated to vo-client 47:
  - Add OSG Cross CE VO
  - Change SBGrid VOMS Certificate
  - Change GLOW VOMS Certificate

* Fri Aug 02 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 46-1
- Updated to vo-client 46:
  - Remove NWICG VO
  - Add ENMR VO
  - Add Darkside VO
  - Change VOMS URL for NYSGRID
  - Add production role for Belle VO

* Tue Jul 02 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 45-1
- Updated to vo-client v45:
  - Add GLAST VO
  - Add Auger VO
  - Remove NEBioGrid VO

* Fri Mar 29 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 44-1
- Updated to vo-client v44.

* Thu Nov 01 2012 Tim Cartwright <cat@cs.wisc.edu> - 43-2
- Swapped in the gums.config.template file from John Weigand (see SOFTWARE-824).

* Tue Oct 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 43-1
- Updated to vo-client v43.

* Tue Jul 17 2012 Alain Roy <roy@cs.wisc.edu> - 42-2
- Fixed LSC file for OSG VO.

* Mon Jun 18 2012 Alain Roy <roy@cs.wisc.edu> - 42-1
- Updated to vo-client v42. Fixed LSST GUMS template and added COUPP sub-vo.

* Tue Apr 24 2012 Alain Roy <roy@cs.wisc.edu> - 41-3
- Adjusted VOMS server URLs for default GUMS config to work with latest GUMS.

* Mon Apr 23 2012 Alain Roy <roy@cs.wisc.edu> - 41-2
- Fixed LSST URL

* Wed Apr 18 2012 Alain Roy <roy@cs.wisc.edu> - 41-1
- Updated to match GOC's new v41 release.
- Added lsst
- Updated VOMS hostname for Alice

* Wed Mar 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 40-4
- osg-edg-mkgridmap-config renamed back to vo-client-edgmkgridmap to solve yum dependency resolution issues.

* Wed Mar 07 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 40-3
- Rename vo-client-edgmkgridmap to osg-edg-mkgridmap-config; remove vo-client dependency
- Add osg-gums-config

* Thu Nov 10 2011 Alain Roy <roy@cs.wisc.edu> - 40-2
- Fixed LSC file for LIGO

* Thu Oct 27 2011 Alain Roy <roy@cs.wisc.edu> - 40-1
- Updated to version 40 of the vo-client. Adds lbne & alice

* Wed Aug 10 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 38-8
- Depend on virtual dependency grid-certificates, not specific package.

* Wed Aug 03 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-7
- Fixed engage's lsc file

* Fri Jul 22 2011 Igor Sfiligoi <isfiligoi@ucsd.edu> - 38-6
- Change RPM to extract directly from the upstream tarball
- Expect the vomsdir to be in the upstream tarball

* Thu Jul 21 2011 Neha Sharma <neha@fnal.gov> - 38-5
- Modified the directory structure. Only needs files at top level

* Wed Jul 20 2011 Neha Sharma <neha@fnal.gov> - 38-4
- Added vo-client-edgmkgridmap

* Tue Jul 19 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-3
- Removed vdt-make-vomsdir.  It now has it's own rpm

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-2
- Added vdt-make-vomsdir and cleaned up packaging

* Fri Jul 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-1
- Initial build of vo-client


