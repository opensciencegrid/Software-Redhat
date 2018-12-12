Summary: StashCache client tools
Name: stashcache-client
Version: 5.2.0
Release: 1%{?dist}
License: Apache 2.0
Url: https://github.com/opensciencegrid/StashCache
BuildArch: noarch
Source0: StashCache-%{version}.tar.gz
Source1: README-caches
Requires: curl
Requires: xrootd-client
Provides: stashcp = %{version}-%{release}

%description
stashcp allows users to copy files out of the OSG StashCache data federation.

%prep
%setup -qn StashCache-%{version}

%install
install -D bin/stashcp %{buildroot}%{_bindir}/stashcp
install -D -m 0644 bin/caches.json %{buildroot}%{_datarootdir}/stashcache/caches.json
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datarootdir}/stashcache/README-caches

%files
%{_bindir}/stashcp
%{_datarootdir}/stashcache/caches.json
%{_datarootdir}/stashcache/README-caches

%changelog
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

# vim:ft=spec
