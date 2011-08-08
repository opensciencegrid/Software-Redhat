
Name:      rsv-metrics
Version:   3.4.3
Release:   1%{?dist}
Summary:   RSV metrics

Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

Provides: perl(RSVMetric)

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

# Some of the "old" RSV probes rely on Date::Manip.  We intend to rewrite
# these probes so this dependency can probably go away at some point.
Requires:  perl(Date::Manip)

# TODO - add the following dependencies once we know their RPM names
Requires: /usr/bin/grid-proxy-info
Requires: /usr/bin/globus-job-run
Requires: /usr/bin/globusrun
Requires: /usr/bin/globus-url-copy
Requires: /usr/bin/uberftp
Requires: /usr/bin/srm-ping
Requires: /usr/bin/srm-copy
Requires: /usr/bin/srm-ls
Requires: /usr/bin/srm-rm
#package('Globus-Base-RM-Client')
#package('SRM-Client-Fermi')
#package('Dccp')
#package('Gratia-Metric-Probe')
#package('OpenLDAP')

# Requested by Doug Strain for his new storage metrics 2010-10
#package('SRM-Client-LBNL')
#package('SRM-Tester-LBNL')
#package('OSG-Discovery')
#package('UberFTP')

%description
%{summary}


%pre
# Create the rsv user/group
getent group rsv >/dev/null || groupadd -r rsv
getent passwd rsv >/dev/null || useradd -r -g rsv -d /var/rsv -s /bin/sh -c "RSV monitoring" rsv


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Install executables
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/rsv
cp -r libexec/probes $RPM_BUILD_ROOT%{_libexecdir}/rsv/
cp -r libexec/metrics $RPM_BUILD_ROOT%{_libexecdir}/rsv/

# Install configuration
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta
cp -r etc/meta/metrics $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta/
cp -r etc/metrics $RPM_BUILD_ROOT%{_sysconfdir}/rsv/

# Install helper files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/rsv/
cp -r usr/share/rsv/probe-helper-files $RPM_BUILD_ROOT%{_datadir}/rsv/

# Area for records awaiting processing
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/spool/rsv

# Create the logging directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/rsv/metrics
ln -s metrics $RPM_BUILD_ROOT%{_localstatedir}/log/rsv/probes

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

# This package owns these directories and everything in them
%{_libexecdir}/rsv/probes/
%{_libexecdir}/rsv/metrics/
%{_datadir}/rsv/probe-helper-files/

%config %{_sysconfdir}/rsv/meta/metrics/*
%config(noreplace) %{_sysconfdir}/rsv/metrics/*

# Metric records will be placed in spool
%attr(-,rsv,rsv) %{_localstatedir}/spool/rsv
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/metrics
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/probes

%changelog
* Wed Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Created an initial rsv-metrics RPM
