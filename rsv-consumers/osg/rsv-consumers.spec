
Name:      rsv-consumers
Version:   3.7.10
Release:   1%{?dist}
Summary:   RSV Consumers Infrastructure

Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: gratia-probe-metric
Requires: httpd

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

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

make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

# This package owns this directory and everything in it
%{_libexecdir}/rsv/consumers/

%config %{_sysconfdir}/rsv/meta/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/rsv-nagios.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-consumers

%config %{_sysconfdir}/httpd/conf.d/rsv.conf
%config %{_datadir}/osg/www.d/rsv.site

%attr(-,rsv,rsv) %{_datadir}/rsv
%attr(-,rsv,rsv) %{_datadir}/rsv/www
%attr(-,rsv,rsv) %{_datadir}/rsv/www/index.html
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/consumers

%changelog
* Fri Sep 20 2013  <edquist@cs.wisc.edu> - 3.7.10-1
- Updated to 3.7.10
- SOFTWARE-1170 - fix PLUGIN_HOST for nagios-consumer

* Mon Aug 26 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.7.9-1
- Updated to 3.7.9
- SOFTWARE-1048 - better HTCondor-CE support
- SOFTWARE-819 - metric argument handling bugfixes

* Fri Jul 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.7.8-1
- Updated to 3.7.8

* Thu Oct 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> 3.7.7-1
- Updated to 3.7.7

* Tue Jul 24 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu>
- Updated to 3.7.5
- SOFTWARE-712 - Replace newlines in Nagios URL with spaces

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
- Implemented nagios-consumer for OSG 3.  Incorporated rsv2nagios.py and
  rsv2nsca.py in the new consumer.
- Rewrote html-consumer and gratia-consumer to share common code with
  nagios-consumer
- SOFTWARE-519 - fixed a bug where a consumer could crash if the timestamp
  field in the record is empty.

* Fri Apr 13 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.0r1-1
- Update to 3.7.0r1

* Tue Feb 21 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.9-2
- Removed %ghost from %{_datadir}/rsv/www/index.html since that was incorrect.

* Tue Feb 21 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.9-1
- Added a sample index.html page to display before the html-consumer runs.

* Wed Dec 28 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.7-1
- No changes, bumped due to changes in rsv-metrics and rsv-core.

* Thu Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Creating a first RPM for rsv-consumers
