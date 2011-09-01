Name:      osg-ce
Summary:   OSG Compute Element 
Version:   3.0.0
Release:   10
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

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
Requires: gip
Requires: osg-info-services
Requires: gums-client
Requires: edg-mkgridmap
Requires: osg-site-verify

# For the CE authz
Requires: lcmaps-plugins-gums
Requires: lcmaps-plugins-verify-proxy
Requires: lcmaps-plugins-basic
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

%description condor
%{summary}

%package pbs
Group: Grid
Summary: PBS meta-package for the OSG-CE
Requires: gratia-probe-pbs-lsf
Requires: globus-gram-job-manager-setup-pbs

%description pbs
%{summary}

%package lsf
Group: Grid
Summary: LSF meta-package for the OSG-CE
Requires: gratia-probe-pbs-lsf
Requires: globus-gram-job-manager-setup-lsf

%description lsf
%{summary}

%package sge
Group: Grid
Summary: SGE meta-package for the OSG-CE
Requires: gratia-probe-sge
Requires: globus-gram-job-manager-setup-sge

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

