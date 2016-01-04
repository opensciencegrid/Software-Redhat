Name:      rsv-perfsonar
Version:   1.1.2
Release:   1%{?dist}
Summary:   RSV Metrics to monitor pefsonar
Packager:  OSG-Software
Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: rsv
# Still needs esmond rpm to bring the python 2.7
Requires: esmond
#This requirements to publish data to the CERN message brokers
Requires: stompclt
Requires: python-simplevisor
# This is for /sbin/service                                                                                                                                  
Requires(preun): initscripts


%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
Requires: python-simplejson
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}

%prep
#%setup -n trunk
#%setup -n %{name}
%setup -n %{version}

%install
rm -fr $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README
%defattr(-,root,root,-)
%{_libexecdir}/rsv/probes/perfsonar-simple-local-probe
%{_libexecdir}/rsv/probes/network-monitoring-local-probe
%{_libexecdir}/rsv/probes/worker-scripts/esmond*
%{_libexecdir}/rsv/metrics/org.osg.general.perfsonar-simple
%{_libexecdir}/rsv/metrics/org.osg.local.network-monitoring-local
%config %{_sysconfdir}/condor-cron/config.d/50-rsv-perfsonar.config
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.general.perfsonar-simple.meta
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.local.network-monitoring-local.meta
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.general.perfsonar-simple.conf
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.local.network-monitoring-local.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-perfsonar-metrics
%config(noreplace) %{_sysconfdir}/rsv/stompclt/default.conf
%config(noreplace) %{_sysconfdir}/rsv/stompclt/simplevisor.cfg
%attr(-,rsv,rsv)  %{_sysconfdir}/rsv
%attr(-,rsv,rsv)  %{_localstatedir}/run/rsv-perfsonar/
# For the virtual enviroment of the python2.7 for the probes
%attr(-,rsv,rsv)  %{_localstatedir}/rsv/
%attr(-,rsv,rsv)  %{_localstatedir}/rsv/localenv
# for the simplevisor init script
%{_initrddir}/simplevisor

%post -p /bin/bash
mkdir /var/rsv/localenv                                                                                                                                    
source /opt/rh/python27/enable                                                                                                                               
/opt/rh/python27/root/usr/bin/virtualenv --prompt="(esmondup)" /var/rsv/localenv                                                                            
. /var/rsv/localenv/bin/activate
pip install esmond-client --upgrade                                                                                                                          
pip install requesocks --upgrade
pip install dirq --upgrade
pip install messaging  --upgrade                                                                                                                            



%changelog
* Mon Jan 1 2016 <efajardo@physics.ucsd.edu> 1.1.2-1
- Improved error handling and warning messages
- Removed the creation of some symlinks since rsv does that now

* Thu Oct 29 2015 <efajardo@physics.ucsd.edu> 1.1.1-1
- Fixed bug on probes ussing SSL only for metadata and not for data

* Thu Oct 22 2015 <efajardo@physics.ucsd.edu> 1.1.0-1
- Bumped to version 1.1.0 to go into the release
- Fixed the https bugs on probes not falling back to it
 
* Mon Oct 12 2015 <efajardo@physics.ucsd.edu> 1.0.26-1
- Fixed bug when the tmp directory knob was not being used

* Mon Oct 5 2015 <efajardo@physics.ucsd.edu> 1.0.25-1
- Changed the bulk posts to only posts at most 100 datapoints per event type at a time

* Fri Sep 18 2015  <efajardo@physics.ucsd.edu> 1.0.24-1
- Made the directory to write each metadata key to be configurable
- Added the initScript for the simplevisor

* Mon Sep 14 2015 <efajardo@physics.ucsd.edu> 1.0.23-1
- Each probes writes a dictionary for each meatadata key with the last timestamp of a succesfull run

* Tue Aug 25 2015  <efajardo@physics.ucsd.edu> 1.0.22-1
- All probes use the same python enviroment for efficiency

* Tue Aug 25 2015  <efajardo@physics.ucsd.edu> 1.0.21-1
- Removed changing the permission of the logs of esmond
- No longer using esmond rpm but esmond-client via pip
- Removed the pip installation for the message queue
 
* Tue Aug 4 2015 <efajardo@physics.ucsd.edu> 1.0.20-1
- Removed the sleep option since no longer needed
- Added error handling for import problems with esmond

* Mon Jul 6 2015 <efajardo@physics.ucsd.edu> 1.0.19-1
- Fixed bug when directory queue is not present

* Mon Jun 29 2015 <efajardo@physics.ucsd.edu> 1.0.18-1
- Added the support for message passing queue from Marian Babik

* Wed Jun 17 2015 <efajardo@physics.ucsd.edu> 1.0.17-1
- Add missing pactek-count-lost/sent datapoints
- Don't run multiple probes for hosts sharing same IP
 
* Mon Jun 08 2015 <efajardo@physics.ucsd.edu> 1.0.16-1
- Mark as an error packet-loss-rate when problems occurr.

* Fri May 22 2015 <efajardo@physics.ucsd.edu> 1.0.15-1
- Cannonically post input source and destination
- Changed requirement for esmond
 
* Wed Apr 29 2015 <efajardo@physics.ucsd.edu> 1.0.14-1
- Added SSL support to query remote perfsonar hosts

* Thu Mar 26 2015 <efajardo@physics.ucsd.edu> 1.0.13-1
- Sanitized the url from the meshes to prevent the main probe from choking

* Tue Mar 3 2015 <efajardo@physics.ucsd.edu> 1.0.12-1
- Changed the way the packet-loss-rate is uploaded for increased accurancy

* Fri Feb 20 2015 <efajardo@physics.ucsd.edu> 1.0.10-1
- The code changes for increased debugging and packet loss rate did not make it to 1.0.9

* Thu Feb 19 2015 <efajardo@physics.ucsd.edu> 1.0.9-1
- New way of uploading packet loss rate
- Efficency tweaks provided by Brian B.

* Fri Feb 13 2015 <efajardo@physics.ucsd.edu> 1.0.8-1
- Updated requirement for esmond. To bug fix posting double values for throughput
- Stopped checking for old keys to gain efficiency

* Mon Feb 09 2015 <efajardo@physics.ucsd.edu> 1.0.7-1
- Fix to prevent duplicate entries by storing original metada key

* Tue Feb 03 2015 <efajardo@physics.ucsd.edu> 1.0.6-1
- Included Andrew Lake's fix for uploading the summaries
- Changed the required esmond version

* Thu Jan 22 2015 <efajardo@physics.ucsd.edu> 1.0.5-1
- Fixed bug when uploading summaries

* Mon Jan 20 2015 <efajardo@physics.ucsd.edu> 1.0.4-1
- Added the config option for the allowedEvents

* Wed Jan 14 2015 <efajardo@physics.ucsd.edu> 1.0.3-1
- Fixed bug in last version that prevented event types to be added to the post

* Mon Jan 12 2015 <efajardo@physics.ucsd.edu> 1.0.2-1
- Improved memmory footprint of the probes

* Thu Jan 8 2015 <efajardo@physics.ucsd.edu> - 1.0.1-2
- Fix requesocks library installation

* Thu Jan 8 2015 <efajardo@physics.ucsd.edu> - 1.0.1-1
- Added the socsk5 proxy requirement for accessing sites in the LHCOne
- Added the installation fo the requesocks library

* Thu Dec 18 2014 <efajardo@physics.ucsd.edu> - 1.0.0-1
- Bumped to first production version
- Code is basically same as 0.0.12

* Tue Dec 16 2014 <efajardo@physics.ucsd.edu> - 0.0.12-1
- Added the option to dynamically adjust the start query time on the perf boxes
- Only certain type of events are uploaded (the ones that are usefull)

* Thu Dec 11 2014 <efajardo@physics.ucsd.edu> - 0.0.11-1
- Added the feature of omiting uploading summaries
- Upgraded suggested configuration options

* Mon Dec 8 2014 <efajardo@physics.ucsd.edu> - 0.0.10-1
- Fixed bug when reading data
- Added soft time out and warning for the probes
- Added the option to debug for more content
- Added timestamps in the logs

* Thu Nov 20 2014 <efajardo@physics.ucsd.edu> - 0.0.9-1
- Using EventBulk to increase efficiency in posting

* Tue Nov 18 2014 <efajardo@physics.ucsd.edu> - 0.0.8-1
- Increased efficiency on enabling and disabling dummy probes

* Tue Nov 18 2014 <efajardo@physics.ucsd.edu> - 0.0.7-1
- Increased the efficiency on posting and reading data

* Mon Nov 17 2014 <efajardo@physics.ucsd.edu> - 0.0.6-1
- Added the option for a super mesh as a json url that contains other meshes

* Fri Nov 14 2014  <efajardo@physics.ucsd.edu> - 0.0.5-1
- Now uploading of packet-loss-rate as a fraction not float

* Tue Nov 4 2014  <efajardo@physics.ucsd.edu> - 0.0.4-1
- Added sleep time for the probe.
- Added the start knob to fix some issues.

* Tue Sep 23 2014 <efajardo@physics.ucsd.edu> - 0.0.3-1
- Added support for multiple meshes
- Added the key, username and goc_url to be configurable

* Fri Sep 05 2014 <efajardo@physics.ucsd.edu> - 0.0.2-1
- The rsv master probe now turns on the dummy probes

* Thu Sep 04 2014 <efajardo@physics.ucsd.edu> - 0.0.1-5
- Corrected the permission on the django.log

* Thu Sep 04 2014 <efajardo@physics.ucsd.edu> - 0.0.1-4
- Added the post section to deal with some file permission changes
- Added the softlinking to the standard http location

* Thu Sep 04 2014 <efajardo@physics.ucsd.edu> - 0.0.1-3
- Removed the different rsv* requirements and added rsv.

* Wed Sep 03 2014 <efajardo@physics.ucsd.edu> - 0.0.1-2
- Removed the log from the rsv log from the files not to collide with the rsv-metrics

* Fri Aug 29 2014  <efajardo@physics.ucsd.edu> - 0.0.1-1
- Creating a first RPM for rsv-perfsonar
