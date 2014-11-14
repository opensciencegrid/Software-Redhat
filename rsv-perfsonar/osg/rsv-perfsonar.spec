Name:      rsv-perfsonar
Version:   0.0.5
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
#The perfsonar probe libraries need it. Getting it from I2 repo for now
Requires: esmond

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
Requires: python-simplejson
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}

%prep
%setup -n %{name}

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
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.general.perfsonar-simple.meta
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.local.network-monitoring-local.meta
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.general.perfsonar-simple.conf
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.local.network-monitoring-local.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-perfsonar-metrics
%attr(-,rsv,rsv)  %{_sysconfdir}/rsv

%post -p /bin/bash
# Change the permissions for the perfsonar probes to work
# Not a big deal since they never really use the log.
chown rsv /var/log/esmond/django.log
chmod a+w /var/log/esmond/django.log
chown rsv /var/log/esmond/esmond.log
chmod a+w /var/log/esmond/esmond.log
# Create the html dir in the correct place
mkdir /var/www/html/rsv
chown rsv /var/www/html/rsv
rm -rf /usr/share/rsv/www
ln -s /var/www/html/rsv /usr/share/rsv/www


%changelog
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
