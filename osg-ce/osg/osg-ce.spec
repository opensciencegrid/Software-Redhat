Name:      osg-ce
Summary:   OSG Compute Element 
Version:   3.0.0
Release:   3
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

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
Requires: globus-gram-job-manager-setup-fork
Requires: gip
Requires: osg-info-services

# For the CE authz
Requires: lcmaps-plugins-gums
Requires: lcmaps-plugins-verify-proxy
Requires: lcmaps-plugins-basic
Requires: lcas-lcmaps-gt4-interface

%description
%{summary}

%package condor
Group: Grid
Summary: Condor meta-package for the OSG-CE

Requires: %{name} = %{version}-%{release}
Requires: condor
Requires: gratia-probe-condor
Requires: globus-gram-job-manager-setup-condor

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
* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-3
- Add in the information services items.

* Thu Jul 28 2011 Brian Bockelman <bbockelm@cse.unl.edu>
- Updated RPM dependency.

* Wed Jul 21 2011 Tanya Levshina <tlevshin.fnal.gov> 
- Created an initial osg-ce RPM.

