
Name:      osg-client
Summary:   OSG Client
Version:   3.0.0
Release:   2
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: osg-wn-client
Requires: ndt
Requires: condor
Requires: bwctl
Requires: gsissh
Requires: nmap
Requires: lcg-info
Requires: lcg-infosites
Requires: npad-client
Requires: osg-discovery
Requires: owamp
Requires: ppdg-cert-scripts

%description
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/osg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{_sysconfdir}/osg

%changelog
* Thu Jul 14 2011 Derek Weitzel <dweitzel@cse.unl.edu> 3.0.0-2
- Changed name of gsiopenssh to gsissh

* Wed Jul  6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.0.0-1
- Created an initial osg-client RPM based on Alains list of deps.

