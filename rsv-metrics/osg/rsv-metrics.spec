
Name:      rsv-metrics
Version:   3.5.5
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

Requires: /usr/bin/grid-proxy-info
Requires: /usr/bin/globus-job-run
Requires: /usr/bin/globusrun
Requires: /usr/bin/globus-url-copy
Requires: uberftp
Requires: bestman2-client
Requires: /usr/bin/ldapsearch
Requires: logrotate

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
install -d $RPM_BUILD_ROOT%{_libexecdir}/rsv
cp -r libexec/probes $RPM_BUILD_ROOT%{_libexecdir}/rsv/
cp -r libexec/metrics $RPM_BUILD_ROOT%{_libexecdir}/rsv/

# Install configuration
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta
cp -r etc/meta/metrics $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta/
cp -r etc/metrics $RPM_BUILD_ROOT%{_sysconfdir}/rsv/

# Install helper files
install -d $RPM_BUILD_ROOT%{_datadir}/rsv/
cp -r usr/share/rsv/probe-helper-files $RPM_BUILD_ROOT%{_datadir}/rsv/

# Area for records awaiting processing
install -d $RPM_BUILD_ROOT%{_localstatedir}/spool/rsv

# Create the logging directories
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/rsv/metrics
ln -s metrics $RPM_BUILD_ROOT%{_localstatedir}/log/rsv/probes

# Put log rotation in place
install -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 logrotate/rsv-metrics.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/rsv-metrics

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
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-metrics

# Metric records will be placed in spool
%attr(-,rsv,rsv) %{_localstatedir}/spool/rsv
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/metrics
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/probes

%changelog
* Wed Oct 05 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.5.3-1
- Updated for CA metric.

* Tue Oct 04 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.5.2-1
- Added CA and CRL metrics which are not yet full functional.

* Thu Sep 15 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.8-1
- Added log rotation and more

* Fri Sep 09 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.5-3
- Further sorting through dependencies

* Thu Sep 08 2011 Doug Strain <dstrain@fnal.gov> 3.4.5-2
- Fixed some of the requires lines for bestman2-client

* Wed Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Created an initial rsv-metrics RPM
