Summary: OSDF client programs
Name: osdf-client
Version: 6.10.1
Release: 1%{?dist}
License: ASL 2.0
Url: https://github.com/htcondor/osdf-client
# Pre-compiled binary
Source0: https://github.com/htcondor/%{name}/releases/download/v%{version}/%{name}_Linux_x86_64.tar.gz
Source1: https://github.com/htcondor/%{name}/blob/v%{version}/resources/10-stash-plugin.conf
ExclusiveArch: x86_64

# go compiler doesn't generate build id files by default.  We also don't have them
# if we're using a pre-compiled binary.
%global _missing_build_ids_terminate_build 0
# Making debuginfo package dies on el8 due to lack of build id
%global debug_package %{nil}


%description
%{summary}

%package -n stashcp
Summary: Stash/OSDF command-line copy client
Obsoletes: stashcache-client < 6.4.0
Provides: stashcache-client = %{version}-%{release}

%description -n stashcp
Stash/OSDF command-line copy client

%package -n condor-stash-plugin
Summary: stash_plugin
Requires: condor

%description -n condor-stash-plugin
Stash/OSDF plugin for HTCondor


%prep
%setup -c -n stashcp

%build
exit 0

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 stashcp %{buildroot}%{_bindir}/stashcp
mkdir -p %{buildroot}/usr/libexec/condor
install -m 0755 stash_plugin %{buildroot}/usr/libexec/condor/stash_plugin
mkdir -p %{buildroot}/etc/condor/config.d
install -m 0644 %{SOURCE1} %{buildroot}/etc/condor/config.d/10-stash-plugin.conf

%files -n stashcp
%{_bindir}/stashcp
%doc LICENSE.txt
%doc README.md

%files -n condor-stash-plugin
/usr/libexec/condor/stash_plugin
%config(noreplace) /etc/condor/config.d/10-stash-plugin.conf
%doc LICENSE.txt
%doc README.md

%changelog
* Thu Apr 13 2023 Brian Lin <blin@cs.wisc.edu> - 6.10.1-1
- Cache keys in memory outside Linux
- Fix token find

* Thu Mar 09 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.10.0-1
- Update to 6.10.0 (SOFTWARE-5517)

* Wed Jan 25 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.9.5-1
- Update to 6.9.5 (SOFTWARE-5372)

* Fri Jan 06 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.9.4-2
- Fix broken 10-stash-plugin.conf (SOFTWARE-5372)

* Wed Jan 04 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.9.4-1
- Update to 6.9.4 (SOFTWARE-5372)

* Mon Oct 10 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.9.2-2
- Take new 10-stash-plugin.conf file from upstream (SOFTWARE-5350)
  (replace 10-stash-plugin.config with it, for consistency with upstream)

* Mon Oct 10 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.9.2-1
- Update to 6.9.2, rename to osdf-client, change upstream to htcondor/osdf-client (SOFTWARE-5350)

* Mon Aug 15 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.8.1-1
- Update to 6.8.1 (SOFTWARE-5284)

* Mon Aug 08 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.8.0-1
- Update to 6.8.0 (SOFTWARE-5284)

* Fri May 06 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.7.5-1
- Update to 6.7.5 (SOFTWARE-5101)

* Mon Mar 07 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.6.0-1
- Update to 6.6.0 (SOFTWARE-4887)

* Mon Jan 10 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.5.3-1
- Update to 6.5.3 (SOFTWARE-4887)

* Fri Jan 07 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.5.1-1
- Initial, binary-only packaging (SOFTWARE-4887)

# vim:ft=spec
