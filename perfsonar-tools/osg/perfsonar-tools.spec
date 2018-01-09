%define relnum 1
%define toolkit_config_base /etc/perfsonar/toolkit/default_service_configs

Version:        4.0.1
Name:           perfsonar-tools
Summary:        perfSONAR active measurement tools
Release:        %{relnum}.3%{?dist}
License:        Distributable, see LICENSE
Group:          Applications/Communications
URL:            http://www.perfsonar.net/
BuildArch:      noarch

Requires:       bwctl-client    
Requires:       bwctl-server   
Requires:       owamp-client   
Requires:       owamp-server    
Requires:       nuttcp
Requires:       iperf
Requires:       iperf3
Requires:       traceroute
Requires:       iputils
Requires:       ntp
Obsoletes:      perfSONAR-Bundles-Tools
Provides:       perfSONAR-Bundles-Tools

%description
The basic command-line measurement tools used by perfSONAR for on-demand tests.

%files
%defattr(0644,perfsonar,perfsonar,0755)

%changelog
* Fri Jan 5 2018 efajardo@physics.ucsd.edu - 4.0.1-1.3
- Releasing just the personar-tools subpackage on osg (SOFTWARE-2686)

* Mon Jul 14 2015 andy@es.net
- common bundle
* Mon Jul 06 2015 adelvaux@man.poznan.pl
- Tools bundle
* Wed Mar 25 2015 sowmya@es.net
- Core bundle
* Tue Mar 24 2015 sowmya@es.net
- Testpoint and CentralManagement bundle
