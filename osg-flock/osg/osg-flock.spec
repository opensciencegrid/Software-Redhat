Name:      osg-flock
Version:   1.0
Release:   1%{?dist}
Summary:   OSG configurations for a flocking host

Group:     applications/grid
License:   Apache 2.0
URL:       https://support.opensciencegrid.org/support/solutions/articles/12000030368-submit-node-flocking-to-osg#gratia-probe-configuration

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: osg-ca-certs
Requires: gratia-probe-glideinwms
Requires: fetch-crl
Requires: condor

Source0: 80-osg-flocking.conf
Source1: ProbeConfig 

%description
%{summary}

%prep

%build

%install
rm -fr $RPM_BUILD_ROOT

# Install condor configuration
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d
install -m 644 %{SOURCE0} %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d


# Install gratia configuration
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gratia/condor/
install -m 644 %{SOURCE0} %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/gratia/condor

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%config(noreplace) %{_sysconfdir}/condor/config.d/99_osg_flock.conf


%changelog
* Fri Sep 07 2018 Suchandra Thapa <ssthapa@uchicago.edu> 1.0-1
- Initial meta package based in part on osg-condor-flock rpms

