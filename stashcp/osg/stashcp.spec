Summary: StashCache/OSDF client
Name: stashcp
Version: 6.8.0
Release: 1%{?dist}
License: ASL 2.0
Url: https://github.com/opensciencegrid/stashcp
# Pre-compiled binary
Source0: %{name}_%{version}_Linux_x86_64.tar.gz
Source1: 10-stash-plugin.config
ExclusiveArch: x86_64
Obsoletes: stashcache-client < 6.4.0
Provides: stashcache-client = %{version}-%{release}

# go compiler doesn't generate build id files by default.  We also don't have them
# if we're using a pre-compiled binary.
%global _missing_build_ids_terminate_build 0
# Making debuginfo package dies on el8 due to lack of build id
%global debug_package %{nil}


%description
%{summary}

%package -n condor-stash-plugin
Summary: stash_plugin
Requires: condor

%description -n condor-stash-plugin
stash plugin for HTCondor


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
install -m 0644 %{SOURCE1} %{buildroot}/etc/condor/config.d/10-stash-plugin.config

%files
%{_bindir}/stashcp
%doc LICENSE.txt
%doc README.md

%files -n condor-stash-plugin
/usr/libexec/condor/stash_plugin
%config(noreplace) /etc/condor/config.d/10-stash-plugin.config
%doc LICENSE.txt
%doc README.md

%changelog
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
