%global htcce osg-htcondor-ce
%global basece osg-base-ce

Name:      osg-ce
Summary:   OSG Compute Element
Version:   3.3
Release:   10%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: %{htcce} = %{version}-%{release}


%description
%{summary}

%post


###############################################################################
# Base subpackages
###############################################################################
%package -n %{basece}
Group: Grid
Summary: Meta-package of gateway-independent components of the OSG CE
Requires: globus-gridftp-server-progs
Requires: osg-version
Requires: grid-certificates >= 7

# former osg-client requirements (minus networking stuff)
Requires: globus-common-progs
Requires: globus-gsi-cert-utils-progs
Requires: gsi-openssh-clients
Requires: osg-cert-scripts
Requires: osg-system-profiler
Requires: osg-version
Requires: osg-wn-client
Requires: vo-client

Requires: osg-info-services
Requires: osg-vo-map
Requires: gip

%if 0%{?rhel} < 7
Requires: gums-client
%endif

Requires: edg-mkgridmap
Requires: gratia-probe-gridftp-transfer
Requires: osg-cleanup
Requires: osg-configure >= 1.0.57
Requires: osg-configure-ce
Requires: osg-configure-gip
Requires: osg-configure-gratia
Requires: osg-configure-managedfork
Requires: osg-configure-misc
Requires: osg-configure-network
Requires: osg-configure-squid
Requires: frontier-squid

# New in 3.2:
Requires: osg-configure-infoservices

# The following is required for the RSV Gratia probes to work.
Requires: perl(Date::Manip)

# For the CE authz
%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif

%description -n %{basece}
%{summary}


%package -n %{basece}-condor
Group: Grid
Summary: Gateway-less Condor meta-package for OSG-CE

Requires: %{basece} = %{version}-%{release}
Requires: gratia-probe-condor
Requires: osg-configure-condor

%description -n %{basece}-condor
%{summary}


%package -n %{basece}-pbs
Group: Grid
Summary: Gateway-less PBS meta-package for OSG-CE

Requires: %{basece} = %{version}-%{release}
Requires: gratia-probe-pbs-lsf
Requires: osg-configure-pbs

%description -n %{basece}-pbs
%{summary}


%package -n %{basece}-lsf
Group: Grid
Summary: Gateway-less LSF meta-package for OSG-CE

Requires: %{basece} = %{version}-%{release}
Requires: gratia-probe-pbs-lsf
Requires: osg-configure-lsf

%description -n %{basece}-lsf
%{summary}


%package -n %{basece}-sge
Group: Grid
Summary: Gateway-less SGE meta-package for OSG-CE

Requires: %{basece} = %{version}-%{release}
Requires: gratia-probe-sge
Requires: osg-configure-sge

%description -n %{basece}-sge
%{summary}

%package -n %{basece}-slurm
Group: Grid
Summary: Gateway-less SLURM meta-package for OSG-CE

Requires: %{basece} = %{version}-%{release}
Requires: gratia-probe-slurm
Requires: osg-configure-slurm

%description -n %{basece}-slurm
%{summary}

%package -n %{basece}-bosco
Group: Grid
Summary: Gateway-less BOSCO meta-package for OSG-CE

Requires: %{basece} = %{version}-%{release}
Requires: gratia-probe-htcondor-ce
Requires: osg-configure-bosco

%description -n %{basece}-bosco
%{summary}



###############################################################################
# HTCondor-CE subpackages
###############################################################################
%package -n %{htcce}
Group: Grid
Summary: OSG Compute Element (HTCondor-CE-only)

Requires: %{basece} = %{version}-%{release}
Requires: htcondor-ce

%description -n %{htcce}
%{summary}


%package -n %{htcce}-condor
Group: Grid
Summary: Condor meta-package for the HTCondor-CE OSG-CE

Requires: %{htcce} = %{version}-%{release}
Requires: %{basece}-condor = %{version}-%{release}
Requires: htcondor-ce-condor

%description -n %{htcce}-condor
%{summary}


%package -n %{htcce}-pbs
Group: Grid
Summary: PBS meta-package for the HTCondor-CE OSG-CE
Requires: %{htcce} = %{version}-%{release}
Requires: %{basece}-pbs = %{version}-%{release}
Requires: htcondor-ce-pbs

%description -n %{htcce}-pbs
%{summary}

%package -n %{htcce}-lsf
Group: Grid
Summary: LSF meta-package for the HTCondor-CE OSG-CE
Requires: %{htcce} = %{version}-%{release}
Requires: %{basece}-lsf = %{version}-%{release}
Requires: htcondor-ce-lsf

%description -n %{htcce}-lsf
%{summary}

%package -n %{htcce}-sge
Group: Grid
Summary: SGE meta-package for the HTCondor-CE OSG-CE
Requires: %{htcce} = %{version}-%{release}
Requires: %{basece}-sge = %{version}-%{release}
Requires: htcondor-ce-sge

%description -n %{htcce}-sge
%{summary}

%package -n %{htcce}-slurm
Group: Grid
Summary: SLURM meta-package for the HTCondor-CE OSG-CE
Requires: %{htcce} = %{version}-%{release}
Requires: %{basece}-slurm = %{version}-%{release}
Requires: htcondor-ce-pbs

%description -n %{htcce}-slurm
%{summary}

%package -n %{htcce}-bosco
Group: Grid
Summary: Bosco meta-package for the HTCondor-CE OSG-CE
Requires: %{htcce} = %{version}-%{release}
Requires: %{basece}-bosco = %{version}-%{release}
Requires: condor-bosco
Requires: htcondor-ce-bosco

%description -n %{htcce}-bosco
%{summary}



###############################################################################
# Main (both HTCondor-CE and GRAM-CE) subpackages
###############################################################################
%package condor
Group: Grid
Summary: Condor meta-package for the OSG-CE

Requires: %{name} = %{version}-%{release}
Requires: %{htcce}-condor = %{version}-%{release}

%description condor
%{summary}

%package pbs
Group: Grid
Summary: PBS meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: %{htcce}-pbs = %{version}-%{release}

%description pbs
%{summary}

%package lsf
Group: Grid
Summary: LSF meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: %{htcce}-lsf = %{version}-%{release}

%description lsf
%{summary}

%package sge
Group: Grid
Summary: SGE meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: %{htcce}-sge = %{version}-%{release}

%description sge
%{summary}

%package slurm
Group: Grid
Summary: Slurm meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: %{htcce}-slurm = %{version}-%{release}

%description slurm
%{summary}

%package bosco
Group: Grid
Summary: Bosco meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: %{htcce}-bosco = %{version}-%{release}

%description bosco
%{summary}



%build
exit 0

%install
exit 0

%clean
exit 0


%files -n %{basece}
%files -n %{basece}-condor
%files -n %{basece}-pbs
%files -n %{basece}-lsf
%files -n %{basece}-sge
%files -n %{basece}-slurm
%files -n %{basece}-bosco
%files -n %{htcce}
%files -n %{htcce}-condor
%files -n %{htcce}-pbs
%files -n %{htcce}-lsf
%files -n %{htcce}-sge
%files -n %{htcce}-slurm
%files -n %{htcce}-bosco
%files
%files condor
%files pbs
%files lsf
%files sge
%files slurm
%files bosco

%changelog
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

