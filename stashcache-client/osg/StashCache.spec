Summary: StashCache client tools
Name: stashcache-client
Version: 5.5.0
Release: 3%{?dist}
License: Apache 2.0
Url: https://github.com/opensciencegrid/StashCache
BuildArch: noarch
Source0: StashCache-%{version}.tar.gz
Source1: README-caches
BuildRequires: python2-setuptools
Requires: python2-setuptools
Requires: curl
Requires: xrootd-client
Provides: stashcp = %{version}-%{release}

%if 0%{?rhel} >= 8
%define __python /usr/bin/python2
%endif

%description
stashcp allows users to copy files out of the OSG StashCache data federation.

%prep
%autosetup -n StashCache-%{version}

%build
%py2_build

%install
%py2_install
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datarootdir}/stashcache/README-caches

%files
%{python2_sitelib}/*
%{_bindir}/stashcp
%{_datarootdir}/stashcache/caches.json
%{_datarootdir}/stashcache/README-caches

%changelog
* Thu Apr 23 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.0-3
- Build for EL 8 (SOFTWARE-4050)

* Fri Oct 11 2019 Diego Davila <didavila@ucsd.edu> - 5.5.0-2
- Adding "Requires: python2-setuptools" (SOFTWARE-3799)

* Wed Oct 2 2019 Diego Davila <didavila@ucsd.edu> - 5.5.0-1
- Update to 5.5.0
- Use python macros to install

* Wed Dec 12 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.2.0-1
- Update to 5.2.0

* Tue Dec 04 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-5
- Fix crash when we can't look up any caches with GeoIP

* Tue Oct 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-4
- Make a failure when querying the origin for the file size not fatal

* Tue Oct 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-3
- Rename to stashcache-client
- Add readme file for caches.json

* Fri Oct 12 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-2
- Package caches.json

* Thu Oct 11 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-1
- Initial packaging

