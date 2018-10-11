Summary: StashCache copy client
Name: stashcp
Version: 5.1.0
Release: 1%{?dist}
License: Apache 2.0
Url: https://github.com/opensciencegrid/StashCache
Source0: StashCache-%{version}.tar.gz
Requires: curl
Requires: xrootd-client

%description
stashcp allows users to copy files out of the OSG StashCache data federation.



%prep
# %%setup quick reference:
#   -a N        Unpack source N after cd
#   -b N        Unpack source N before cd
#   -c          Create and cd to dir before unpacking
#   -D          Do not delete dir before unpacking
#   -n DIR      Name of extract dir (instead of NAME-VERSION)
#   -T          Do not autounpack Source0

%setup -n StashCache-%{version}



%install
install -D bin/stashcp %{buildroot}%{_bindir}/stashcp



%files
%{_bindir}/stashcp






%changelog
* Thu Oct 11 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-1
- Initial packaging


# vim:ft=spec
