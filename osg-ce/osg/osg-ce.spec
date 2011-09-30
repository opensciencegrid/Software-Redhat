Name:      osg-ce
Summary:   OSG Compute Element 
Version:   3.0.0
Release:   16
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: grid-certificates
Requires: java-1.6.0-sun-compat
Requires: globus-gridftp-server-progs 
Requires: osg-client
Requires: syslog-ng
Requires: lfc-client
#Requires: Job-Environment
Requires: osg-vo-map
Requires: vo-client
#Requires: cemon-server
#Requires: osg-site-verify
Requires: osg-site-web-page
Requires: globus-gram-job-manager-fork
Requires: globus-gram-job-manager-fork-setup-poll
Requires: gip
Requires: osg-info-services
Requires: gums-client
Requires: edg-mkgridmap
Requires: osg-site-verify
Requires: osg-system-profiler
Requires: osg-configure
Requires: osg-configure-ce
Requires: osg-configure-cemon
Requires: osg-configure-gip
Requires: osg-configure-gratia
Requires: osg-configure-managedfork
Requires: osg-configure-misc
Requires: osg-configure-squid

# For the CE authz
%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif

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
Requires: globus-gram-job-manager-setup-pbs
Requires: osg-configure-pbs

%description pbs
%{summary}

%package lsf
Group: Grid
Summary: LSF meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: gratia-probe-pbs-lsf
Requires: globus-gram-job-manager-setup-lsf
Requires: osg-configure-lsf

%description lsf
%{summary}

%package sge
Group: Grid
Summary: SGE meta-package for the OSG-CE
Requires: %{name} = %{version}-%{release}
Requires: gratia-probe-sge
Requires: globus-gram-job-manager-setup-sge
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

