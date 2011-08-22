Name:           osg-condor-flock
Version:        1.0
Release:        1%{?dist}
Summary:        Condor configuration to flock to OSG Submitters

Group:          applications/grid
License:        Apache 2.0
URL:            https://twiki.grid.iu.edu/bin/view/CampusGrids
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       condor
Requires:       gratia-probe-condor


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
install -m 644 98_flock_hosts.conf 99_osg_flock.conf $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d

install -d $RPM_BUILD_ROOT/%{_docdir}/osg-condor-flock
install -m 644 README $RPM_BUILD_ROOT/%{_docdir}/osg-condor-flock

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/condor/config.d/98_flock_hosts.conf
%config(noreplace) %{_sysconfdir}/condor/config.d/99_osg_flock.conf
%doc %{_docdir}/osg-condor-flock/README



%changelog
* Mon Aug 22 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-1
- Initial build

