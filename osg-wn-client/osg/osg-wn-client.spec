Name:      osg-wn-client
Summary:   OSG Worker-Node Client
Version:   23
Release:   1%{?dist}
License:   Apache 2.0
URL:       http://www.opensciencegrid.org
BuildArch: noarch


Requires: /usr/bin/xrdcp
Requires: /usr/bin/curl
Requires: /usr/bin/ldapsearch
Requires: /usr/bin/wget
Requires: grid-certificates >= 7
Requires: fetch-crl
Requires: osg-system-profiler
Requires: stashcp
Requires: vo-client
Requires: voms-clients-cpp

Requires: gfal2
Requires: python3-gfal2-util
Requires: gfal2-plugin-http
Requires: gfal2-plugin-file
Requires: gfal2-plugin-xrootd

%description
%{summary}

%install

mkdir -p $RPM_BUILD_ROOT%{_prefix}/etc/
cat > $RPM_BUILD_ROOT%{_prefix}/etc/globus-user-env.sh << EOF
#!/bin/sh

# This file is expected by gLite jobs because GLOBUS_LOCATION 
# defaults to /usr, and they're looking for 
# $GLOBUS_LOCATION/etc/globus-user-env.sh. It doesn't need to have
# anything, it just needs to be there. 

EOF

%files
%config(noreplace) %{_prefix}/etc/globus-user-env.sh

%changelog
* Fri Sep 8 2023 Matt Westphall <westphall@wisc.edu> - 23-1
- Bump version for OSG 23

* Thu Feb 16 2023 Carl Edquist <edquist@cs.wisc.edu> - 3.6-6
- Bump to rebuild for RPM GPG key (SOFTWARE-5457)

* Fri May 06 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.6-5
- Add stashcp and voms-clients-cpp (SOFTWARE-5171)

* Wed Sep 22 2021 Carl Edquist <edquist@cs.wisc.edu> - 3.6-4
- Change gfal2-util requirement to python3-gfal2-util (SOFTWARE-4826)

* Fri Feb 26 2021 Brian Lin <blin@cs.wisc.edu> - 3.6-3
- Remove remaining packages bringing in Globus dependencies (SOFTWARE-4487)

* Fri Feb 26 2021 Brian Lin <blin@cs.wisc.edu> - 3.6-2
- Remove old CGSI-gSOAP requirement (SOFTWARE-4487)

* Wed Feb 17 2021 Carl Edquist <edquist@cs.wisc.edu> - 3.6-1
- Drop GSI/GridFTP requirements for OSG 3.6 (SOFTWARE-4487)

* Thu Apr 23 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5-4
- Don't require fts-client on EL8, it's not available (SOFTWARE-4050)

* Fri Aug 02 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-1
- Bump version to 3.5 (SOFTWARE-3761)

* Wed Dec 12 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 3.4-5
- Add stashcache-client (SOFTWARE-3472)

* Mon Jan 8 2018 Edgar Fajardo <emfajard@ucsd.edu> 3.4-4
- Dropping osg-version requirements (SOFTWARE-2917)

* Tue Nov 14 2017 Edgar Fajardo <emfajard@ucsd.edu> 3.4-3
- Adding gfal2-http (SOFTWARE-2191)

* Thu May 25 2017 Edgar Fajardo <emfajard@ucsd.edu> 3.4-1
- Droping java dependencies  (SOFTWARE-2676)
- Bumping version number 

* Tue May 23 2017 Edgar Fajardo <emfajard@ucsd.edu> 3.3-8
- Drop the setup.sh script no longer necessary in 3.4 (SOFTWARE-2676)
- Drop the glexec subpackages since glexec is dropped in 3.4

* Thu Apr 13 2017 Edgar Fajrdo <emfajard@ucsd.edu> 3.3-7
- Added gsi-openssh-clients (SOFTWARE-2657)

* Mon Oct 31 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-6
- Deprecate /etc/osg/wn-client/setup.sh and setup.csh (SOFTWARE-1977)

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-5
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Fri Jun 19 2015 Jose Caballero <jcaballero@bnl.gov> 3.3-4
- Added dependency to /usr/bin/xrdcp 

* Wed Jun 10 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-3
- Explicitly require the C++ version of the voms clients

* Thu Apr 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-2
- Remove requirements dropped from 3.3
- Remove conditionals for el5
- Remove _clipped version -- el7 now supports everything el6 does

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue Apr 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-31_clipped
- Use fts-client instead of glite-fts-client for el7

* Mon Mar 09 2015 Brian Lin <blin@cs.wisc.edu> 3.0.0-30
- Explicitly require voms-clients

* Wed Feb 25 2015 Brian Lin <blin@cs.wisc.edu> 3.0.0-29
- Bring in gfal2-plugin-file (SOFTWARE-1799)

* Tue Nov 11 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-28_clipped
- Bring in dcache-srmclient on EL7
- Include java-devel on EL7

* Tue Oct 07 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-27_clipped
- Bring in glite-fts-client on EL7

* Tue Oct 07 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-26
- Require CGSI-gSOAP >= 1.3.6 for gfal2-plugin-srm (SOFTWARE-1603)

* Tue Oct 07 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-25
- Bring in gfal2-plugin-xrootd too, now built against xrootd4 (SOFTWARE-1603)

* Thu Oct 02 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-24
- Bring in GFAL2 tools (SOFTWARE-1603)

* Wed Sep 17 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-23_clipped
- Create clipped release for EL7 containing only the packages that we were able to build (SOFTWARE-1604)

* Tue Apr 01 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-22
- Ship with UDT driver plugin (SOFTWARE-1443)

* Tue Mar 25 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-20
- Update lcg-utils requirement to lcg-util (SOFTWARE-1373)

* Wed Apr 03 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-19.osg
- Update to require java7-devel and jpackage-utils

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-18.osg
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Fri Jan 03 2013 Dave Dykstra <dwd@fnal.gov> - 3.0.0-17.osg
- Added mkgltempdir as osg-wn-client-glexec requirement

* Wed Jul 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-16.osg
- Add explicit dependency on globus-gass-copy-progs (for globus-url-copy)

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> - 3.0.0-15.osg
- Rebuild after merging to trunk

* Mon Feb 27 2012 Dave Dykstra <dwd@fnal.gov> - 3.0.0-14.osg
- Added glexec-wrapper-scripts requirement on glexec

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-13
- Added dependency on osg-version

* Mon Oct 24 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-12
- Added dependency on on lfc-python (Needed by ATLAS)
- Added /usr/etc/globus-user-env.sh, which is needed by 
  gLite jobs.

* Tue Oct 11 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-11
- Added setup.csh to match setup.sh, just in case someone
  needs it.

* Mon Aug 22 2011 Dave Dykstra <dwd@fnal.gov> - 3.0.0-10
- Remove lcmaps-plugins-glexec-tracking from osg-wn-client-glexec
  Requires because it has been moved down to glexec instead

* Mon Aug 22 2011 Dave Dykstra <dwd@fnal.gov> - 3.0.0-9
- Remove redundant Requires from osg-wn-client-glexec which were
  already Required by lcmaps (which is Required by glexec).
- Added gratia-probe-glexec as Required by osg-wn-client-glexec

* Thu Aug 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-8
- Require virtual dep grid-certificates, not actual package osg-ca-certs.

* Thu Aug 04 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-7
- Added vo-client to dependencies

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-6
- Correct plugin names in the glexec meta-package.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-5
Update to reflect current plugin names.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-4
Add glexec sub-package.

* Thu Jul 14 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-3
- Added dcap-tunnel-gsi to list of dependencies

* Fri Jul 08 2011 Derek Weitzel <dweitzel@cse.unl.edu> 3.0.0-2
- Added fetch-crl dependency

* Wed Jul  6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.0.0-1
- Bump to correct version number.
- Add osg-ca-certs to the requires.
- Re-added the pegasus worker node client.

* Fri Jul  1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.0-1
- Created an initial osg-wn-client RPM.
- Not all deps actually exist: just giving us a target to strive for.

