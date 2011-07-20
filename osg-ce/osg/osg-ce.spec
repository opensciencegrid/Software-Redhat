Name:      osg-ce
Summary:   OSG Compute Element 
Version:   3.0.0
Release:   1
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#from epel
Requires: java-1.6.0-sun-compat
Requires: globus-gridftp-server-progs 
Requires: voms-clients 
Requires: uberftp 
Requires: myproxy
Requires: syslog-ng
Requires: wget
Requires: myproxy
#from vdt
Requires: lcg-utils
Requires: lfc-client
Requires: dcache-srmclient
Requires: bestman2-client
Requires: ndt 
Requires: /usr/bin/uberftp
Requires: /usr/bin/wget
Requires: /usr/bin/ldapsearch
Requires: osg-ca-certs
Requires: fetch-crl
Requires: npad
Requires: owamp
Requires: bwctl
#Requires: gums-client
#Requires: prima 
#Requires: pegasus-worker 
#Requires: Job-Environment
#Requires: MonaLisa
#Requires: osg-vo-map
#Requires: osg-rsv 
#Requires: gratia-metric-probe
#Requires: cemon-server
#Requires: osg-site-verify
#Requires: osg-site-web-page

%description
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files



%changelog
* Wed Jul  21 2011 Tanya Levshina <tlevshin.fnal.gov> 
- Created an initial osg-ce RPM.

