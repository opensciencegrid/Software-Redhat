Name:           osg-condor-flock
Version:        2.2
Release:        1%{?dist}
Summary:        Condor configuration to flock to OSG Submitters

Group:          applications/grid
License:        Apache 2.0
URL:            https://twiki.grid.iu.edu/bin/view/CampusGrids
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       condor
Requires:       gratia-probe-condor
Requires:       grid-certificates

BuildArch:      noarch

Source0:        98_flock_hosts.conf
Source1:        99_osg_flock.conf
Source2:        README

%description
%{summary}

%prep


%build


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d
install -m 644 %{SOURCE0} %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d

install -d $RPM_BUILD_ROOT/%{_docdir}/osg-condor-flock
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_docdir}/osg-condor-flock

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/condor/config.d/98_flock_hosts.conf
%config(noreplace) %{_sysconfdir}/condor/config.d/99_osg_flock.conf
%doc %{_docdir}/osg-condor-flock/README



%changelog
* Thu Jan 10 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 2.2-1
- Removing claimtobe from the default authentication methods

* Tue Jan 08 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 2.1-1
- Updating OSG-XSEDE DN and making it defualt

* Wed May 30 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 2.0-2
- Fixing GSI_DAEMON_NAME

* Tue May 29 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 2.0-1
- Adding osg-xsede submit host

* Wed Nov 09 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-8
- Fixing DEAMON_NAME to GSI_DAEMON_NAME and SEC_*

* Wed Nov 09 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-7
- Fixed typo in 99_osg_flock.conf

* Wed Sep 28 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-6
- Added gratia configuration into the condor configuration

* Wed Sep 28 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-5
- Adding Campus Factory configurations

* Wed Sep 07 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-4
- Changed the default flocking host to ENGAGE_RENCI
- Added documentation URL to README

* Tue Aug 30 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-3
- Changed DN for engage submit host

* Tue Aug 30 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-2
- Made changes to conf files after testing
- Added grid-certificates requirement

* Mon Aug 22 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-1
- Initial build

