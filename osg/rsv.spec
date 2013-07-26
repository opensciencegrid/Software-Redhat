
Name:      rsv
Summary:   RSV Meta Package
Version:   3.7.8
Release:   1%{?dist}
License:   Apache 2.0
Group:     Applications/Monitoring
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV
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

%description
%{summary}

%install
# No files to install or directories to make

%clean
rm -rf $RPM_BUILD_ROOT

%files
# No files since this is a meta package

%changelog
* Fri Jul 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.7.8-1
- Set version to 3.7.8

* Thu Oct 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> 3.7.7-1
- Set version to 3.7.7

* Thu Aug 23 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.6-1
- Set version to 3.7.6

* Wed Jul 04 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.4-1
- Set version to 3.7.4

* Mon Jun 25 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.2-1
- Set version to 3.7.2

* Mon Apr 23 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.0-1
- Set version to 3.7.0

* Fri Apr 13 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.7.0r1-1
- Set version to 3.7.0r1

* Fri Jan 06 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.7-2
- Added dependency on voms-clients

* Wed Dec 28 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.7-1
- No changes, bumped due to changes in rsv-metrics and rsv-core.

* Thu Sep 08 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.5-3
- Added dependency on grid-certificates

* Thu Sep 08 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.5-2
- Added dependencies on osg-configure and osg-configure-rsv

* Thu Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0
- Created an initial RSV meta package
