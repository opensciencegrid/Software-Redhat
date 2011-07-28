Name:      osg-voms
Summary:   OSG VOMS 
Version:   3.0.0
Release:   1
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#from vdt
Requires: voms-admin-server
Requires: voms-admin-client
#
Requires: mysql-server
#from epel
Requires: voms-server
Requires: voms-mysql-plugin
#from vdt
Requires: voms-admin-server
Requires: voms-admin-client

%description
%{summary}
meta package to install voms-admin and voms-core packages


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files



%changelog
* Thu Jul 28 2011 Tanya Levshina <tlevshin.fnal.gov> 
- Created an initial osg-voms RPM.

