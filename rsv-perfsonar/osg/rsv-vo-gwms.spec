Name:      rsv-vo-gwms
Version:   0.0.1
Release:   1%{?dist}
Summary:   RSV metrics to test CE's from gwms factory
Packager:  OSG-Software
Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: rsv
Requires: python-condor


%description
%{summary}

%prep
%setup -n %{name}
#%setup -n %{name}-%{version}

%install
rm -fr $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README
%defattr(-,root,root,-)
%{_libexecdir}/rsv/probes/gfactory-querying-local-probe
%{_libexecdir}/rsv/metrics/org.osg.local-gfactory-querying-local
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.local-gfactory-querying-local.meta
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.local-gfactory-querying-local.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-vo-gwms-metrics
%attr(-,rsv,rsv)  %{_sysconfdir}/rsv
%attr(-,rsv,rsv)  %{_sysconfdir}/rsv/metrics

%post -p /bin/bash
# Create the html dir in the correct place
mkdir /var/www/html/rsv
chown rsv /var/www/html/rsv
rm -rf /usr/share/rsv/www
ln -s /var/www/html/rsv /usr/share/rsv/www


%changelog
* Wed Nov 14 2014 <efajardo@physics.ucsd.edu> - 0.0.1-1
- Creating a first RPM for rsv-vo-gwms
