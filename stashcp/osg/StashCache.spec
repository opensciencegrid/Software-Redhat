Summary: StashCache copy client
Name: stashcp
Version: 5.1.0
Release: 1%{?dist}
License: Apache 2.0
Group: Grid
Url: https://github.com/opensciencegrid/StashCache
BuildArch: noarch
Source0: StashCache-%{version}.tar.gz
Requires: curl
Requires: xrootd-client

%description
stashcp allows users to copy files out of the OSG StashCache data federation.

%prep
%setup -n StashCache-%{version}

%install
install -D bin/stashcp %{buildroot}%{_bindir}/stashcp

%files
%{_bindir}/stashcp

%changelog
* Thu Oct 11 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-1
- Initial packaging

# vim:ft=spec
