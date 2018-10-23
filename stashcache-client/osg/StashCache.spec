Summary: StashCache client tools
Name: stashcache-client
Version: 5.1.0
Release: 2%{?dist}
License: Apache 2.0
Url: https://github.com/opensciencegrid/StashCache
BuildArch: noarch
Source0: StashCache-%{version}.tar.gz
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

%files
%{_bindir}/stashcp
%{_datarootdir}/stashcache/caches.json

%changelog
* Tue Oct 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-2
- Package caches.json

* Thu Oct 11 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-1
- Initial packaging

# vim:ft=spec
