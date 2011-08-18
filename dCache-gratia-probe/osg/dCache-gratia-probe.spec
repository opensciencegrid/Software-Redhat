Name:      dCache-gratia-probe 
Summary:   dCache-gratia-probe
Version:   3.0.0
Release:   1
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#from vdt
Requires: gratia-probe-dCache-transfer 
Requires: gratia-probe-dCache-storage
Requires: osg-ca-certs
Requires: osg-vo-map
Requires: gums-client 
#from epel
Requires: fetch-crl 

%description
%{summary}
meta package to install gratia-probe-dCache-transfer and gratia-probe-dCache-storage packages


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files



%changelog

* Thu Aug 18 2011 Tanya Levshina <tlevshin.fnal.gov> 
- Created an initial dCache-gratia-probe RPM.

