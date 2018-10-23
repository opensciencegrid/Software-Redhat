Summary: StashCache client tools
Name: stashcache-client
Version: 5.1.0
Release: 3%{?dist}
License: Apache 2.0
Url: https://github.com/opensciencegrid/StashCache
BuildArch: noarch
Source0: StashCache-%{version}.tar.gz
Source1: README-caches
Patch0: Also-look-for-caches.json-in-etc-stashcache-and-usr-.patch
Requires: curl
Requires: xrootd-client
Provides: stashcp = %{version}-%{release}

%description
stashcp allows users to copy files out of the OSG StashCache data federation.

%prep
%setup -qn StashCache-%{version}
%patch0 -p1

%install
install -D bin/stashcp %{buildroot}%{_bindir}/stashcp
install -D -m 0644 bin/caches.json %{buildroot}%{_datarootdir}/stashcache/caches.json
install -D -m 0644 %{SOURCE1} %{buildroot}%{_datarootdir}/stashcache/README-caches

%files
%{_bindir}/stashcp
%{_datarootdir}/stashcache/caches.json
%{_datarootdir}/stashcache/README-caches

%changelog
* Tue Oct 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-3
- Rename to stashcache-client
- Add readme file for caches.json

* Fri Oct 12 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-2
- Package caches.json

* Thu Oct 11 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-1
- Initial packaging

# vim:ft=spec
