Name:      osg-client
Summary:   OSG Client
Version:   3.0.0
Release:   22%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: osg-version
Requires: osg-wn-client
Requires: ndt-client
Requires: bwctl-client
Requires: gsi-openssh-clients
Requires: lcg-info
Requires: lcg-infosites
# No npad for now, because it installs server by default. Re-add later?
#Requires: npad

# Don't require osg-discovery for el6, not working...
%if 0%{?el6}
%else
Requires: osg-discovery
%endif

Requires: owamp-client
Requires: osg-cert-scripts
Requires: vo-client
Requires: globus-gram-client-tools
# Needed by globus-gram-client-tools, but missing dependency
Requires: globus-common-progs 
Requires: globus-gsi-cert-utils-progs
Requires: osg-system-profiler

%description
%{summary}

%package condor
Group: Grid
Summary:  OSG Client with Condor

Requires: %{name} = %{version}-%{release}
Requires: condor

%description condor
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/osg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{_sysconfdir}/osg

%files condor

%changelog
* Thu Jun 19 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 3.0.0-22
- Updated to remove the nmap requirement.

* Wed Apr 03 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-20
- Update to remove java requirement since it's brought in by osg-wn-client

* Thu Aug 30 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-19
- AlsocChanged dependency on ndt to ndt-client so we do not 
  install the server

* Thu Aug 23 2012 Alain Roy <roy@cs.wisc.edu> - 3.0.0-18
- Changed dependency on bwctl to bwctl-client so we do not 
  install the server

* Fri Feb 24 2012 Alain Roy <roy@cs.wisc.edu> - 3.0.0-17
- Fixed gsi-openssh dependency to get the client tools

* Fri Feb 17 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-16
- Removing osg-discovery for el6 (for real this time).

* Fri Feb 17 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-15
- Removing osg-discovery for el6.

* Fri Nov 18 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-14
- Added dependency on globus-common-progrs, as workaround for missing 
  dependency in globus-gram-client-tools. 

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-13
- Added dependency on osg-version

* Mon Oct 31 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-12
- Added dependency on globus-gsi-cert-utils-progs, to get grid-cert-info 
  installed by default. 

* Mon Oct 24 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-11
- Removed npad because it installs a server by default, which it inappropriate 
  for a client install

* Thu Sep 8 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-10
- Added condor subpackage so people can choose to install without Condor dependency

* Thu Sep 08 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-9 
- gsissh renamed to gsi-openssh

* Mon Aug 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-8
- Removed the osg-voms-compat package as a dependency.

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-7
- Added osg-voms-compat to list of requires

* Fri Jul 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-6
- Added globus-gram-client-tools for globus-job-* tools.

* Fri Jul 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-5
- Added the vo-client to requires.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-4
- Force Oracle JDK for this meta-package.

* Thu Jul 14 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0.0-3
- Changed npad-client to just npad.  no client package

* Thu Jul 14 2011 Derek Weitzel <dweitzel@cse.unl.edu> 3.0.0-2
- Changed name of gsiopenssh to gsissh

* Wed Jul  6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.0.0-1
- Created an initial osg-client RPM based on Alains list of deps.

