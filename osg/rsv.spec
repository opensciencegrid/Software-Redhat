Name:      rsv
Summary:   RSV Meta Package
Version:   3.7.15
Release:   1%{?dist}
License:   Apache 2.0
Group:     Applications/Monitoring
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: condor-cron
Requires: rsv-consumers
Requires: rsv-core
Requires: rsv-metrics
Requires: osg-configure
Requires: osg-configure-rsv
Requires: grid-certificates
Requires: voms-clients

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}


%package consumers
Summary:  RSV Consumers Infrastructure
Group:     Applications/Monitoring
Requires: gratia-probe-metric
Requires: httpd

%description consumers
%{summary}


%package core
Summary: RSV Core Infrastructure
Group:     Applications/Monitoring
Requires: /usr/bin/grid-proxy-info
Requires: /usr/bin/globus-job-run

# We require globus-common-progs to work around a missing dependency 
# in the globus-gram-client-tools RPM (which provides globus-job-run)
# In the future, we should be able to remove this
Requires: globus-common-progs

# We use shar files for globus-job-run
Requires: sharutils

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description core
%{summary}




%package metrics
Summary: RSV Metrics
Group:     Applications/Monitoring
Provides: perl(RSVMetric)
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
# No longer required
# Requires: fetch-crl

%description metrics
%{summary}



%prep
%setup -q


%install
rm -rf $RPM_BUILD_ROOT
for subpackage in rsv-core rsv-consumers rsv-metrics; do
    make -C $subpackage install DESTDIR=$RPM_BUILD_ROOT
done


%clean
rm -rf $RPM_BUILD_ROOT


# Adding -m to the useradd command doesn't make the directory so force it
%global make_rsv_user_group \
    [ -e /var/rsv ] || mkdir -p /var/rsv \
    getent group rsv >/dev/null || groupadd -r rsv \
    getent passwd rsv >/dev/null || useradd -r -g rsv -d /var/rsv -s /bin/sh -c "RSV monitoring" rsv \
    chown rsv:rsv /var/rsv


%pre consumers
%make_rsv_user_group


%pre core
%make_rsv_user_group


%pre metrics
%make_rsv_user_group



%post core
/sbin/chkconfig --add rsv
/sbin/ldconfig

%preun core
if [ $1 = 0 ]; then
  /sbin/service rsv stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del rsv
fi

%postun core
if [ "$1" -ge "1" ]; then
  /sbin/service rsv restart >/dev/null 2>&1 || :
fi
/sbin/ldconfig


%files
# Meta-package

%files consumers
%defattr(-,root,root,-)

# This package owns this directory and everything in it
%{_libexecdir}/rsv/consumers/

%config %{_sysconfdir}/rsv/meta/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/rsv-nagios.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-consumers

%config %{_sysconfdir}/httpd/conf.d/rsv.conf
%config %{_datadir}/osg/www.d/rsv.site

%attr(-,rsv,rsv) %dir %{_datadir}/rsv
%attr(-,rsv,rsv) %dir %{_datadir}/rsv/www
%attr(-,rsv,rsv) %{_datadir}/rsv/www/index.html
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/consumers




%files core
%defattr(-,root,root,-)

%dir %attr(-,rsv,rsv) %{_localstatedir}/log/rsv
%attr(-,rsv,rsv) %{_localstatedir}/tmp/rsv

%{_bindir}/rsv-control
%{_libexecdir}/rsv/misc/

%{_initrddir}/rsv

%config(noreplace) %{_sysconfdir}/rsv/consumers.conf
%config(noreplace) %{_sysconfdir}/rsv/rsv.conf

%{python_sitelib}/rsv/*

%{_mandir}/man1/rsv-control.1*


%files metrics
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
* Mon Mar 24 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.7.15-1
- SOFTWARE-1198 - Fix HTCondor-CE RSV metric org.osg.globus.gram-authentication
- SOFTWARE-1388 - Deprecated "[allmetrics args]" config section

* Mon Jan 27 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.7.14-1
- SOFTWARE-1336 - additional warnings for gratia probe
- SOFTWARE-1358 - patch to support zabbix consumer

* Tue Nov 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.7.13-2
- Bumb release to rebuild for koji issue

* Tue Nov 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.7.13-1
- SOFTWARE-1147 - Create local version of Java RSV probe
- SOFTWARE-1195 - Add rsv-profiler check for actual UID/GID of cndrcron user
- SOFTWARE-1199 - RSV: Fix --gatekeeper-type option for local tests
- SOFTWARE-1309 - handle missing java/javac commands in java-version-probe

* Mon Nov 11 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.7.12-1
- SOFTWARE-1281 - use 1024-bit proxies

* Fri Oct 04 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.7.11-1
- SOFTWARE-1210 - combine RSV builds

* Fri Sep 20 2013  <edquist@cs.wisc.edu> - 3.7.10-1
- SOFTWARE-1170 - fix PLUGIN_HOST for nagios-consumer

* Mon Aug 26 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.7.9-1
- SOFTWARE-1048 - better HTCondor-CE support
- SOFTWARE-819 - metric argument handling bugfixes

* Fri Jul 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.7.8-1
- rsv-core:
    - SOFTWARE-783 - Allow timeout or job-timeout options in probe meta files
    - SOFTWARE-1116 - Add additional condor-cron config files to rsv-profiler output
- rsv-metrics:
    - SOFTWARE-563 - have gratia probe distinguish between certinfo and probe files
    - SOFTWARE-775 - better diagnostics for crl-expiry errors
    - SOFTWARE-783 - change custom 'timeout' option in pigeon probe to 'job-timeout'
    - SOFTWARE-1125 - make Java version probe only run every 6 hours

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.7.7-2
- rsv-metrics:
    - Remove fetch-crl requirement.

* Thu Oct 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> 3.7.7-1
- rsv-metrics:
    - SOFTWARE-807 - Fixed bug in srmcp metric when the SE host and machine being probed are the same 
    - SOFTWARE-762 - Fixed incorrect hash reporting in crl-freshness probe
    - Increased default time after which missing CA cert warnings become errors
    - Various other bugfixes

* Thu Aug 23 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.6-1
- rsv-metrics:
    - Fixed service type of GridFTP metric (OSG-GridFTP -> GridFTP)

* Wed Aug 15 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.5-2
- rsv-metrics:
    - Added dependency on fetch-crl

* Thu Jul 05 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.5-1
- rsv-core:
    - TECHNOLOGY-20 - Added Condor-CE support to RSV
- rsv-consumers:
    - SOFTWARE-712 - Replace newlines in Nagios URL with spaces
- rsv-metrics:
    - Increase default error hours thresholdfrom 3 to 8  in cacert-verify-probe

* Wed Jul 04 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.4-1
- SOFTWARE-706 - Remove global logrotate declarations
- SOFTWARE-707 - Fix bug in 3.7.2 that crashes when using a user proxy

* Mon Jun 25 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.3-1
- rsv-core:
    - Fixed bugs in how subprocess module is used

* Mon Jun 25 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.2-1
- SOFTWARE-701 - Disable CondorG emails to rsv account
- SOFTWARE-702 - Recreate /var/tmp/rsv if it is deleted

* Wed Jun 13 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.1-1
- SOFTWARE-666 - Update RSV to use Python subprocess module
- SOFTWARE-632 - Improve RSV error messages from the OSG directories probe
- SOFTWARE-454 - Add --test option which is the same as --run but does not generate records
- SOFTWARE-453 - Allow --host to be specified with --on/--off to turn on/off all metrics enabled on a host 

* Mon Apr 23 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.0-1
- rsv-core:
    - SOFTWARE-618 - implemented support for using legacy Globus proxies
    - SOFTWARE-530 - added metric configuration knob to skip ping checks
- rsv-consumers:
    - Implemented nagios-consumer for OSG 3.  Incorporated rsv2nagios.py and
      rsv2nsca.py in the new consumer.
    - Rewrote html-consumer and gratia-consumer to share common code with
      nagios-consumer
    - SOFTWARE-519 - fixed a bug where a consumer could crash if the timestamp
      field in the record is empty.
- rsv-metrics:
    - SOFTWARE-600 - fix a bug in Gratia condor probe that prevents finding
      condor_config_val when Condor is installed in a non-standard location.
    - SOFTWARE-595 - changed the status of the local certificate checks to be a
      WARNING when the cert validity is 168>validity>24 hours.
    - Removed org.osg.batch.* metrics along with some other code that was not ported
      to OSG 3

* Fri Apr 13 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.0r1-1
- Updated to 3.7.0r1

* Tue Feb 21 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-consumers-3.6.9-2
- rsv-consumers:
    - Removed %ghost from %{_datadir}/rsv/www/index.html since that was incorrect.

* Mon Feb 21 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-consumers-3.6.9-1
- rsv-consumers:
    - Added a sample index.html page to display before the html-consumer runs.

* Mon Feb 06 2012 Doug Strain <dstrain@fnal.gov> rsv-metrics-3.6.10-1
- rsv-metrics:
    - Fixed srm-ping-probe to work with bestman syntax not dcache syntax

* Fri Feb 03 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-core-3.6.8-4
- rsv-core:
    - Fix ownership of /var/rsv

* Fri Feb 03 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-core-3.6.8-3
- rsv-core:
    - mkdir /var/rsv since -m option to useradd does not seem to work

* Thu Feb 02 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-core-3.6.8-2
- rsv-core:
    - Use '%{localstatedir}/tmp' instead of %{_tmppath} when creating directories
    - Add -m option when running useradd to make rsv user

* Mon Jan 30 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.6.9-1
- rsv-metrics:
    - Removed broken symlinks for info-service-probe

* Tue Jan 24 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.6.8-1
- rsv-metrics:
    - Updated srmcp probe to give a warning if srm-rm fails.

* Fri Jan 06 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-3.6.7-2
- Added dependency on voms-clients

* Fri Dec 30 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-core-3.6.8-1
- rsv-core:
    - Bug fix for passing arguments on command line

* Wed Dec 28 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.7-1
- rsv-core:
    - Added the ability to pass metric arguments on the command line.
    - Fixed a bug in listing of probes with cron times. (JIRA 432)
    - Improved error if uudecode is missing on remote CE.
    - Other minor bug fixes.
- rsv-metrics:
    - Aesthetic changes - improved the output of some probes.

* Wed Dec 07 2011 Alain Roy <roy@cs.wisc.edu> rsv-core-3.6.6-2
- rsv-core:
    - Added dependency on globus-common-progs

* Tue Nov 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> rsv-metrics-3.6.6-1
- rsv-metrics:
    - osg-version probe interval changed from daily to hourly

* Thu Nov 17 2011 Matyas Selmeci <matyas@cs.wisc.edu> rsv-metrics-3.6.5-1
- rsv-metrics:
    - Updated osg-version probe to use the osg-version package

* Wed Nov 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> rsv-metrics-3.6.4-1
- rsv-metrics:
    - Gratia metrics fixes

* Thu Nov 03 2011 Matyas Selmeci <matyas@cs.wisc.edu> rsv-metrics-3.6.3-1
- rsv-metrics:
    - ReSS metrics updated to brief format.
    - SRM metrics updated to brief format.
    - CA dir lookup more robust.

* Wed Oct 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.6.2-1
- rsv-metrics:
    - Fixed a problem in probe default arguments.

* Wed Oct 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.6.1-1
- rsv-metrics:
    - Update for CA and CRL probes.

* Tue Oct 25 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.6.0-1
- rsv-metrics:
    - Fixed problems in SRM metrics.  Fixed bug in gridftp metric.

* Thu Oct 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-core-3.5.9-1
- rsv-core:
    - Re-implemented globus-job-run submission (as a backup for Condor-G)

* Wed Oct 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> rsv-metrics-3.5.8-1
- rsv-metrics:
    - Added yum-check-update metric

* Wed Oct 19 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.5.7-1
- rsv-metrics:
    - Update for CA and CRL probes.

* Tue Oct 18 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.5.6-1
- rsv-metrics:
    - Update for CA and CRL probes.

* Wed Oct 05 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.5.3-1
- rsv-core:
    - rsv-control wrapper now uses system python
- rsv-metrics:
    - Updated for CA metric.

* Tue Oct 04 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.5.2-1
- rsv-metrics:
    - Added CA and CRL metrics which are not yet full functional.

* Thu Sep 15 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.4.8-1
- rsv-metrics:
    - Added log rotation and more

* Fri Sep 09 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-metrics-3.4.5-3
- rsv-metrics:
    - Further sorting through dependencies

* Thu Sep 08 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-3.4.5-3
- Added dependency on grid-certificates

* Thu Sep 08 2011 Doug Strain <dstrain@fnal.gov> rsv-metrics-3.4.5-2
- Fixed some of the requires lines for bestman2-client

* Thu Sep 08 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> rsv-3.4.5-2
- Added dependencies on osg-configure and osg-configure-rsv

* Thu Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0
- Created initial packages
