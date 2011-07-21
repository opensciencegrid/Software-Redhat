
Name:      rsv-metrics
Version:   3.4.1
Release:   1%{?dist}
Summary:   RSV metrics

Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  mock
Requires:  rpm-build
Requires:  createrepo

# Some of the "old" RSV probes rely on Date::Manip.  We intend to rewrite
# these probes so this dependency can probably go away at some point.
Requires:  perl(Date::Manip)

%description
%{summary}


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


%clean
#rmdir %{_sysconfdir}/rsv/meta/metrics
#rmdir %{_sysconfdir}/rsv/metrics
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

# This package owns these directories and everything in them
%{_libexecdir}/rsv/probes/
%{_libexecdir}/rsv/metrics/

%config %{_sysconfdir}/rsv/meta/metrics/*
%config(noreplace) %{_sysconfdir}/rsv/metrics/*


%changelog
* Wed Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Created an initial rsv-metrics RPM
