
Name:      rsv-metrics
Version:   3.7.7
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
Requires: fetch-crl

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
* Thu Oct 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> 3.7.7-1
- SOFTWARE-807 - Fixed bug in srmcp metric when the SE host and machine being probed are the same 
- SOFTWARE-762 - Fixed incorrect hash reporting in crl-freshness probe
- Increased default time after which missing CA cert warnings become errors
- Various other bugfixes

* Thu Aug 23 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.6-1
- Fixed service type of GridFTP metric (OSG-GridFTP -> GridFTP)

* Wed Aug 15 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.5-2
- Added dependency on fetch-crl

* Wed Aug 08 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.5-1
- Updated to 3.7.5
- Increase default error hours thresholdfrom 3 to 8  in cacert-verify-probe

* Wed Jul 04 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.4-1
- Updated to 3.7.4
- SOFTWARE-706 - Remove global logrotate declarations
- SOFTWARE-707 - Fix bug in 3.7.2 that crashes when using a user proxy

* Mon Jun 25 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.2-1
- Updated to 3.7.2
- SOFTWARE-701 - Disable CondorG emails to rsv account
- SOFTWARE-702 - Recreate /var/tmp/rsv if it is deleted

* Wed Jun 13 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.1-1
- Update to 3.7.1
- SOFTWARE-666 - Update RSV to use Python subprocess module
- SOFTWARE-632 - Improve RSV error messages from the OSG directories probe
- SOFTWARE-454 - Add --test option which is the same as --run but does not generate records
- SOFTWARE-453 - Allow --host to be specified with --on/--off to turn on/off all metrics enabled on a host 

* Mon Apr 23 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.0-1
- Update to 3.7.0
- SOFTWARE-600 - fix a bug in Gratia condor probe that prevents finding
  condor_config_val when Condor is installed in a non-standard location.
- SOFTWARE-595 - changed the status of the local certificate checks to be a
  WARNING when the cert validity is 168>validity>24 hours.
- Removed org.osg.batch.* metrics along with some other code that was not ported
  to OSG 3

* Fri Apr 13 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.0r1-1
- Update to 3.7.0r1

* Mon Feb 6 2012 Doug Strain <dstrain@fnal.gov> 3.6.10-1
- Fixed srm-ping-probe to work with bestman syntax not dcache syntax

* Mon Jan 30 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.9-1
- Removed broken symlinks for info-service-probe

* Tue Jan 24 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.8-1
- Updated srmcp probe to give a warning if srm-rm fails.

* Wed Dec 28 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.7-1
- Aesthetic changes - improved the output of some probes.

* Tue Nov 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> 3.6.6-1
- osg-version probe interval changed from daily to hourly

* Thu Nov 17 2011 Matyas Selmeci <matyas@cs.wisc.edu> 3.6.5-1
- Updated osg-version probe to use the osg-version package

* Wed Nov 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> 3.6.4-1
- Gratia metrics fixes

* Thu Nov 03 2011 Matyas Selmeci <matyas@cs.wisc.edu> 3.6.3-1
- ReSS metrics updated to brief format.
- SRM metrics updated to brief format.
- CA dir lookup more robust.

* Wed Oct 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.2-1
- Fixed a problem in probe default arguments.

* Wed Oct 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.1-1
- Update for CA and CRL probes.

* Tue Oct 25 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.0-1
- Fixed problems in SRM metrics.  Fixed bug in gridftp metric.

* Wed Oct 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> 3.5.8-1
- Added yum-check-update metric

* Wed Oct 19 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.5.7-1
- Update for CA and CRL probes.

* Tue Oct 18 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.5.6-1
- Update for CA and CRL probes.

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
