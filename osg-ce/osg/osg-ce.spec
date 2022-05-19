%global htcce osg-htcondor-ce
%global basece osg-base-ce
%global osgce osg-ce

Name:      osg-ce
Summary:   OSG Compute Element
Version:   3.5
Release:   7%{?dist}
License:   Apache 2.0
URL:       http://www.opensciencegrid.org

Source0: 01-blahp-location.conf
Source1: 03-gratia-cleanup.conf
Source2: 51-gratia.conf
Source3: 03-osg-ce-collector.conf

Requires: grid-certificates >= 7

Requires: fetch-crl
Requires: osg-system-profiler
Requires: vo-client

Requires: vo-client-lcmaps-voms

Requires: osg-configure >= 1.0.57
Requires: osg-configure-ce
Requires: osg-configure-gip
Requires: osg-configure-gratia
Requires: osg-configure-misc
Requires: osg-configure-squid
Requires: frontier-squid
Requires: osg-scitokens-mapfile

Requires: osg-configure-infoservices

# Require the Globus-LCMAPS plugin for authZ
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)

# Added provides version for 3.4 (SOFTWARE-2768) can probably be removed in 3.5
Obsoletes: %{basece} < 3.4-3
Provides: %{basece} = %{version}-%{release}
Obsoletes: %{htcce} < 3.4-3
Provides: %{htcce} = %{version}-%{release}
Requires: htcondor-ce


%description
%{summary}

%post

%package condor
Summary: Condor meta-package for the OSG-CE

Requires: %{osgce} = %{version}-%{release}
Requires: gratia-probe-condor
Requires: osg-configure-condor

# Added provides version for 3.4 (SOFTWARE-2768)                                                                                                            
Obsoletes: %{basece}-condor < 3.4-3
Provides: %{basece}-condor = %{version}-%{release}
Obsoletes: %{htcce}-condor < 3.4-3
Provides: %{htcce}-condor = %{version}-%{release}

Requires: htcondor-ce
Requires: htcondor-ce-condor



%description condor
%{summary}


%package pbs
Summary: PBS meta-package for the OSG-CE

Requires: %{osgce} = %{version}-%{release}
Requires: gratia-probe-pbs-lsf
Requires: osg-configure-pbs

# Added provides version for 3.4 (SOFTWARE-2768)                                                                        
Obsoletes: %{basece}-pbs < 3.4-3
Provides: %{basece}-pbs = %{version}-%{release}
Obsoletes: %{htcce}-pbs < 3.4-3
Provides: %{htcce}-pbs = %{version}-%{release}

Requires: htcondor-ce
Requires: htcondor-ce-pbs

%description pbs
%{summary}


%package lsf
Summary: LSF meta-package for the OSG-CE

Requires: %{osgce} = %{version}-%{release}
Requires: gratia-probe-pbs-lsf
Requires: osg-configure-lsf

# Added provides version for 3.4 (SOFTWARE-2768)                                                                                                            
Obsoletes: %{basece}-lsf < 3.4-3
Provides: %{basece}-lsf = %{version}-%{release}
Obsoletes: %{htcce}-lsf < 3.4-3
Provides: %{htcce}-lsf = %{version}-%{release}

Requires: htcondor-ce
Requires: htcondor-ce-lsf

%description lsf
%{summary}


%package sge
Summary: SGE meta-package for the OSG-CE

Requires: %{osgce} = %{version}-%{release}
Requires: gratia-probe-sge
Requires: osg-configure-sge

# Added provides version for 3.4 (SOFTWARE-2768)                                                                                                             
Obsoletes: %{basece}-sge < 3.4-3
Provides: %{basece}-sge = %{version}-%{release}
Obsoletes: %{htcce}-sge < 3.4-3
Provides: %{htcce}-sge = %{version}-%{release}

Requires: htcondor-ce
Requires: htcondor-ce-sge

%description sge
%{summary}

%package slurm
Summary: SLURM meta-package for the OSG-CE

Requires: %{osgce} = %{version}-%{release}
Requires: gratia-probe-slurm
Requires: osg-configure-slurm

# Added provides version for 3.4 (SOFTWARE-2768)                                                                                                            
Obsoletes: %{basece}-slurm < 3.4-3
Provides: %{basece}-slurm = %{version}-%{release}
Obsoletes: %{htcce}-slurm < 3.4-3
Provides: %{htcce}-slurm = %{version}-%{release}

Requires: htcondor-ce
Requires: htcondor-ce-slurm

%description slurm
%{summary}

%package bosco
Summary: Bosco meta-package for the HTCondor-CE OSG-CE

Requires: %{osgce} = %{version}-%{release}
Requires: gratia-probe-htcondor-ce
Requires: osg-configure-bosco
# Added for scripts to manage remote WN tarball, CA, and CRL
# installations (SOFTWARE-3582)
Requires: hosted-ce-tools

# Added provides version for 3.4 (SOFTWARE-2768)                                                                                                            
Obsoletes: %{basece}-bosco < 3.4-3
Provides: %{basece}-bosco = %{version}-%{release}
Obsoletes: %{htcce}-bosco < 3.4-3
Provides: %{htcce}-bosco = %{version}-%{release}

Requires: htcondor-ce
Requires: htcondor-ce-bosco

%description bosco
%{summary}


%build
exit 0

%install
install -m 755         -d $RPM_BUILD_ROOT/%{_datadir}/condor-ce/config.d
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/%{_datadir}/condor-ce/config.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/condor-ce/config.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/condor-ce/config.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/condor-ce/config.d


%files
# TODO: Drop the OSG-blahp config when the OSG and HTCondor blahps are merged
# https://htcondor-wiki.cs.wisc.edu/index.cgi/tktview?tn=5102,86
%{_datadir}/condor-ce/config.d/01-blahp-location.conf
%{_datadir}/condor-ce/config.d/03-gratia-cleanup.conf
%{_datadir}/condor-ce/config.d/03-osg-ce-collector.conf

%files condor
%files pbs
%files lsf
%files sge
%files slurm

%files bosco
%{_datadir}/condor-ce/config.d/51-gratia.conf

%changelog
* Mon Apr 19 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5-7
- Require osg-scitokens-mapfile (SOFTWARE-4574)

* Tue Feb 02 2021 Brian Lin <blin@cs.wisc.edu> - 3.5-6
- Add explicit htcondor-ce requirement to sub-packages (SOFTWARE-4456)

* Wed Apr 01 2020 Carl Edquist <edquist@cs.wisc.edu> - 3.5-5
- Add SCHEDD_CRON_GRATIA_ARGS to 51-gratia.conf (SOFTWARE-3973)
- Move 51-gratia.conf to bosco subpackage

* Wed Jan 08 2020 Brian Lin <blin@cs.wisc.edu> - 3.5-4
- Set the central collector in the default osg-ce configuration (SOFTWARE-3382)

* Wed Nov 20 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-3
- Add schedd cron config for gratia probe (SOFTWARE-3841)
- Drop ansible requirement (SOFTWARE-3920)

* Fri Sep 06 2019 Brian Lin <blin@cs.wisc.edu> - 3.5-2
- Add Blahp location and Gratia cleanup configuration (SOFTWARE-3813)
- Remove deprecated and 32-bit requirements
- Add Ansible requirement (SOFTWARE-3813)
- Add tools that automatically update WN tarball, CAs, and CRLs on the
remote head node (SOFTWARE-3582)

* Fri Aug 02 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-1
- Removing osg-vo-map requirement for OSG 3.5 (SOFTWARE-3761)

* Mon Jan 8 2018 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-4
- Removing osg-version requirements (SOFTWARE-2917)

* Tue Jul 11 2017 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-3
- Merged osg-base-ce and osg-htcondor-ce into only one subpackages (SOFTWARE-2768)
- Remove the osg-base-ce package

* Mon May 22 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-2
- Add OSG VOMS mapfile to osg-ce (SOFTWARE-2702)
- Drop osg-cert-scripts DOE grids interface

* Mon May 01 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-1
- Drop GridFTP (SOFTWARE-2633)
- Drop client tools (SOFTWARE-2650)
- Drop GUMS and edg-mkgridmap (SOFTWARE-2482, SOFTWARE-2600)
- Drop GRAM-related osg-configure modules (SOFTWARE-2705)

* Tue Mar 28 2017 Edgar Fajardo <efajardo@physics.ucsd.edu> - 3.3-12
- Removed the requirements of gip, osg-info-services and osg-cleanup (SOFTWARE-2585)

* Thu Mar 02 2017 Brian Lin <blin@cs.wisc.edu> - 3.3-11
- Require htcondor-ce-slurm for osg-htcondor-ce-slurm

* Fri Dec 23 2016 Derek Weitzel <dweitzel@cse.unl.edu> - 3.3-10
- Conditionally turn of gums-client dependency for rhel7

* Wed Aug 03 2016 Derek Weitzel <dweitzel@cse.unl.edu> - 3.3.9
- Add gratia-probe-htcondor-ce to requirements for osg-ce-bosco (SOFTWARE-2543)

* Wed Aug 03 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3.8
- Add gums-client back to EL7 (SOFTWARE-2418); clipped version no longer needed

* Mon Jun 27 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-7
- Require htcondor-ce-bosco in bosco CE subpackages (SOFTWARE-2373)

* Thu Apr 14 2016 Edgar Fajardo <efajardo@physics.ucsd.edu> - 3.3-6
- Removed the gram components from the subpackages (SOFTWARE-2278)

* Fri Mar 25 2016 Derek Weitzel <dweitzel@cse.unl.edu> - 3.3-5
- Adding bosco CE package

* Tue Feb 16 2016 Brian Lin <blin@cs.wisc.edu> - 3.3-4
- Drop globus SLURM jobmanager requirement

* Thu Jul 16 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-3
- Drop lfc-client, osg-site-verify, osg-site-web-page deps
- Replace osg-client dep with its contents (minus networking stuff)

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue Apr 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-9_clipped
- Create clipped version for el7

* Tue Mar 10 2015 Brian Lin <blin@cs.wisc.edu> 3.2-8
- Drop batch system requirements (SOFTWARE-1796)

* Fri Feb 20 2015 Brian Lin <blin@cs.wisc.edu> 3.2-7
- Add SLURM metapackage

* Wed Nov 26 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-6
- Have pbs and sge metapackages install their respective batch systems (SOFTWARE-1701)

* Wed Jul 30 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-5
- Have main osg-ce packages install both HTCondor-CE and GRAM (SOFTWARE-1559)

* Tue Jul 29 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-4
- Require osg-configure >= 1.0.57 (SOFTWARE-1552)

* Mon Jul 28 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-3
- Add htcondor-ce metapackages (SOFTWARE-1552)

* Mon Feb 24 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2-1
- Replace osg-configure-cemon dependency with osg-configure-infoservices on OSG 3.2 (SOFTWARE-1276)
- Change version to match release series

* Thu Oct 17 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-35
- Remove glite-ce-monitor dependency

* Thu Sep 05 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-34
- Re-add dependency on frontier-squid, which somehow got lost in the merge

* Tue Aug 27 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-33
- Merged changes in trunk

* Thu Aug 22 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-32
- Add dependency on frontier-squid

* Wed Apr 03 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-31
- Update to remove java requirement since it's brought in by osg-client -> osg-wn-client

* Fri Apr 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-30
- Restored gums dependency on el6.

* Mon Mar 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-29
- Removed gums dependency on el6 since it's not ready yet.

* Wed Feb 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-27
- Add dependency on the new gratia-probe-gram sub-package, which contains the perl modules for GRAM/Gratia integration.

* Mon Jan 30 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> - 3.0.0-26
- Added dependency on osg-configure-network

* Fri Jan 20 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> - 3.0.0-25
- Added dependency on osg-cleanup

* Wed Nov 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-24
- Added dependency on perl(Date::Manip), for the Gratia RSV probes.

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-23
- Added dependency on osg-version

* Fri Nov 11 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-22
- Added dependencies so the Globus gatekeeper and GRAM job manager are always installed. 

* Mon Nov 7 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-21
- Added dependency on gratia-probe-gridftp-transfer since we ship the GridFTP
  server. 

* Thu Nov 3 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-20
- Removed dependency on syslog-ng, which shouldn't have been there. 

* Tue Oct 25 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-19
- Add post install scriplet to fork "jobmanager" to be jobmanager-fork-poll

* Tue Oct 11 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-18
- Fixed dependencies for PBS, LSF, and SGE

* Mon Oct 10 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-17
- Added dependencies on glite-ce-monitor and osg-info-services

* Mon Sep 26 2011 Alain Roy (roy@cs.wisc.edu> - 3.0.0-16
- Move some of the osg-configure-* packages into the proper subpackages. 

* Fri Sep 23 2011 Suchandra Thapa (sthapa@ci.uchicago.edu) - 3.0.0-15
- Updated dependencies to bring in more osg-configure-* packages.

* Thu Sep 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-14
- Added Requires to prefer globus-gram-job-manager-fork-setup-poll over
  -setup-seg, since we haven't been able to get the latter working yet.

* Mon Sep 12 2011 Alain Roy <roy@cs.wisc.edu > 3.0.0-13
  Added dependency on grid-certificates

* Thu Sep 08 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-12
- Added dependencies from the pbs/lsf/sge sub packages on osg-ce. 

* Thu Sep 01 2011 Dave Dykstra <dwd@fnal.gov> - 3.0.0-11
- Removed lcmaps-plugins-* requires.  A couple of them were now wrong,
  and in any case they are pulled in by the lcmaps package which is
  pulled in by lcas-lcmaps-gt4-interface.

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-10
- Do not mark this as a noarch package, as we depend directly on a arch-specific RPM.

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-9
Another update to get Requires right for 32-bit modules

* Tue Aug 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-8
Fix requirements for lcas-lcmaps-gt4-interface.

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-7
- Update dependencies to point at new-style GRAM jobmanager names.

* Sun Aug 07 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-6
- Add dependency on site-verify

* Thu Aug 04 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-5
Added dependency on edg-mkgridmap

* Thu Aug 04 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-4
- Add gums-client as a CE dependency.

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-3
- Add in the information services items.

* Thu Jul 28 2011 Brian Bockelman <bbockelm@cse.unl.edu>
- Updated RPM dependency.

* Wed Jul 20 2011 Tanya Levshina <tlevshin.fnal.gov>
- Created an initial osg-ce RPM.

