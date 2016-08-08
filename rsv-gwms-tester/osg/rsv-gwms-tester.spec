Name:      rsv-gwms-tester
Version:   1.0.3
Release:   1%{?dist}
Summary:   RSV metrics to test sites with a schedd connected to a glidein pool
Packager:  OSG-Software
Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   v%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: rsv >= 3.13
Requires: condor-python


%description
%{summary}

%prep
%setup -n %{name}-%{version}

%install
rm -fr $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README
%defattr(-,root,root,-)
%{_libexecdir}/rsv/probes/gfactory-site-query-local-probe
%{_libexecdir}/rsv/probes/dummy-vanilla-probe
%{_libexecdir}/rsv/metrics/org.osg.general.dummy-vanilla-probe
%{_libexecdir}/rsv/metrics/org.osg.local-gfactory-site-querying-local
%config %{_sysconfdir}/condor-cron/config.d/*
%config %{_sysconfdir}/rsv/meta/metrics/org.osg.local-gfactory-site-querying-local.meta
%config(noreplace) %{_sysconfdir}/rsv/metrics/org.osg.local-gfactory-site-querying-local.conf
%attr(-,rsv,rsv)  %{_sysconfdir}/rsv
%attr(-,rsv,rsv)  %{_sysconfdir}/rsv/metrics
%attr(755, -, -) %{_libexecdir}/rsv/metrics/org.osg.local-gfactory-site-querying-local
%attr(755, -, -) %{_libexecdir}/rsv/probes/gfactory-site-query-local-probe

%post -p /bin/bash


%changelog
* Mon Aug 08 2016 <efajado@physics.ucsd.edu> - 1.0.3-1
- Updated Makefile to include condor-cron configs

* Mon Aug 08 2016 <efajado@physics.ucsd.edu> - 1.0.2-1
- Updated the README for configuration instrucctions
- Added condor-cron config templates from the glideinwms schedd configs

* Mon Aug 01 2016 <efajado@physics.ucsd.edu> - 1.0.1-1
- First version of the probe
