
Summary: Client tools for OSG Topology
Name: topology-client
Version: 1.22.0
Release: 2%{?dist}
Source: topology-%{version}.tar.gz
License: Apache 2.0
BuildArch: noarch
Url: https://github.com/opensciencegrid/topology/
BuildRequires: unzip
BuildRequires: python3-requests
%if 0%{?el8}
BuildRequires: python3-gnupg
Requires: python3-gnupg
%endif
# obtained via `python3 -m pip download python-gnupg`
Source1: https://vdt.cs.wisc.edu/upstream/topology-client/python-deps/python_gnupg-0.4.8-py2.py3-none-any.whl
Patch0: Find-local-install-of-python-gnupg.patch

Requires: python3-requests

%define __python /usr/bin/python3
BuildRequires: python3-devel
BuildRequires: %__python

%description
Client tools that interact with OSG Topology data


%package -n topology-cacher
Summary: A utility for periodically downloading OSG Topology data

%description -n topology-cacher
A utility for periodically downloading OSG Topology data.


%prep
%setup -q -n topology-%{version}
%if 0%{?el7}
%patch0 -p1
%endif

%install
install -D -m 0755 bin/osg-notify %{buildroot}/%{_bindir}/osg-notify
install -D -m 0644 src/net_name_addr_utils.py  %{buildroot}/%{python_sitelib}/net_name_addr_utils.py
install -D -m 0644 src/topology_utils.py %{buildroot}/%{python_sitelib}/topology_utils.py
install -D -m 0755 src/topology_cacher.py %{buildroot}/%{python_sitelib}/topology_cacher.py
install -D -m 0644 topology-cacher.cron %{buildroot}/etc/cron.d/topology-cacher.cron
%if 0%{?el7}
    unzip %{SOURCE1}
    install -D -m 0644 gnupg.py %{buildroot}/usr/lib/topology-client/gnupg.py
%endif

%files
%{_bindir}/osg-notify
%{python_sitelib}/net_name_addr_utils.py*
%{python_sitelib}/topology_utils.py*
%{python_sitelib}/__pycache__/net_name_addr_utils*
%{python_sitelib}/__pycache__/topology_utils*
%if 0%{?el7}
    /usr/lib/topology-client/*
%endif

%files -n topology-cacher
%{python_sitelib}/topology_cacher.py*
%{python_sitelib}/__pycache__/topology_cacher*
%config(noreplace) /etc/cron.d/topology-cacher.cron


%changelog
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.22.0-2
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Wed Oct 5 2022 Brian Lin <blin@cs.wisc.ed> 1.22.0-1
- Fix UnboundLocalError when sending unsigned messages (SOFTWARE-4538)
- Replace opensciencegridrid references with osg-htc in osg-notify (SOFTWARE-5305)

* Wed Mar 16 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 1.8.0-0.3
- Fix path for python3-gnupg on EL7 (SOFTWARE-5079)

* Mon Mar 07 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 1.8.0-0.2
- Update Python dependencies

* Mon Aug 16 2021 Mátyás Selmeci <matyas@cs.wisc.edu> 1.8.0-0.1
- Add topology-cacher (SOFTWARE-4704)

* Thu Mar 18 2021 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4.6-1
- Fix crash when writing unsigned messages (SOFTWARE-4538)

* Wed Jan 27 2021 Brian Lin <blin@cs.wisc.edu> 1.2.0-1
- Fix 'From' address for security announcements (SOFTWARE-4349)

* Tue Dec 10 2019 Diego Davila <didavila@ucsd.edu> 1.1.0-1
- Replace smart quotes and dashes with their ASCII equivalent (SOFTWARE-3893)

* Tue Oct 15 2019 Diego Davila <didavila@ucsd.edu> 1.0.0-1
- Initial
