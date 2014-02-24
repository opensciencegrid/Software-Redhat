Name:      osg-ce
Summary:   OSG Compute Element
Version:   3.2
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: osg-version
Requires: grid-certificates
Requires: globus-gridftp-server-progs 
Requires: osg-client
Requires: lfc-client
Requires: osg-info-services
Requires: osg-vo-map
Requires: vo-client
Requires: osg-site-web-page
Requires: globus-gatekeeper
Requires: globus-gram-job-manager
Requires: globus-gram-job-manager-fork
Requires: globus-gram-job-manager-fork-setup-poll
Requires: gip
Requires: gums-client
Requires: edg-mkgridmap
Requires: gratia-probe-gram
Requires: gratia-probe-gridftp-transfer
Requires: osg-site-verify
Requires: osg-system-profiler
Requires: osg-cleanup
Requires: osg-configure
Requires: osg-configure-ce
Requires: osg-configure-gip
Requires: osg-configure-gratia
Requires: osg-configure-managedfork
Requires: osg-configure-misc
Requires: osg-configure-network
Requires: osg-configure-squid
Requires: frontier-squid
Requires(post): globus-gram-job-manager-scripts >= 4

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

%post
# We always want the default jobmanager to be fork (OSG convention), so we
# force it on both install and upgrade. 
/usr/sbin/globus-gatekeeper-admin -e jobmanager-fork-poll -n jobmanager > /dev/null 2>&1 || :

%description
%{summary}

%package condor
Group: Grid
Summary: Condor meta-package for the OSG-CE

Requires: %{name} = %{version}-%{release}
Requires: condor
Requires: gratia-probe-condor
Requires: globus-gram-job-manager-condor
Requires: osg-configure-condor

%description condor
%{summary}

%package pbs
Group: Grid
Summary: PBS meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: gratia-probe-pbs-lsf
Requires: globus-gram-job-manager-pbs-setup-seg
Requires: osg-configure-pbs

%description pbs
%{summary}

%package lsf
Group: Grid
Summary: LSF meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: gratia-probe-pbs-lsf
Requires: globus-gram-job-manager-lsf-setup-seg
Requires: osg-configure-lsf

%description lsf
%{summary}

%package sge
Group: Grid
Summary: SGE meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: gratia-probe-sge
Requires: globus-gram-job-manager-sge-setup-seg
Requires: osg-configure-sge

%description sge
%{summary}

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files

%files condor
%files pbs
%files lsf
%files sge

%changelog
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

* Wed Jul 21 2011 Tanya Levshina <tlevshin.fnal.gov> 
- Created an initial osg-ce RPM.

