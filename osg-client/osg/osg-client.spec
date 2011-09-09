
Name:      osg-client
Summary:   OSG Client
Version:   3.0.0
Release:   10
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: java-1.6.0-sun-compat
Requires: osg-wn-client
Requires: ndt
Requires: bwctl
Requires: gsissh
Requires: nmap
Requires: lcg-info
Requires: lcg-infosites
Requires: npad
Requires: osg-discovery
Requires: owamp-client
Requires: osg-cert-scripts
Requires: vo-client
Requires: globus-gram-client-tools
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

