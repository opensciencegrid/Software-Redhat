Summary: XRootD Monitoring Shoveler
Name: xrootd-monitoring-shoveler
Version: 1.1.2
Release: 3%{?dist}
License: ASL 2.0
URL: https://github.com/opensciencegrid/xrootd-monitoring-shoveler

# Pre-compiled go binaries
Source0: %{name}_%{version}_Linux_x86_64.tar.gz
ExclusiveArch: x86_64
Source1: %{name}.service
Source2: config.yaml
Source3: dependency-licenses.txt

# go compiler doesn't generate build id files by default.
# We also don't have them if we're using a pre-compiled binary.
%global _missing_build_ids_terminate_build 0
# Making debuginfo package dies on el8 due to lack of build id
%global debug_package %{nil}

%description
This shoveler gathers UDP messages and sends them to a message bus.
This shoveling is used to convert unreliable UDP to reliable message bus.

%prep
%setup -q -n %{name}_%{version}_Linux_x86_64
cp %{SOURCE3} .

%build
exit 0

%install
install -m 755 -d $RPM_BUILD_ROOT/%{_bindir}/
install -m 755 %{name} $RPM_BUILD_ROOT/%{_bindir}/
install -m 755 createtoken $RPM_BUILD_ROOT/%{_bindir}/

install -m 755 -d $RPM_BUILD_ROOT/%{_unitdir}/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/

install -m 755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/

install -m 755 -d $RPM_BUILD_ROOT/%_localstatedir/spool/shoveler-queue

%files
%{_bindir}/%{name}
%{_bindir}/createtoken
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}/config.yaml
%dir %_localstatedir/spool/shoveler-queue
%doc README.md
%doc LICENSE.txt
%doc dependency-licenses.txt

%changelog
* Thu Oct 10 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1.2-3
- Add ExclusiveArch: x86_64 since we're repackaging a compiled binary

* Thu Feb 16 2023 Carl Edquist <edquist@cs.wisc.edu> - 1.1.2-2
- Bump to rebuild for RPM GPG key (SOFTWARE-5457)

* Wed Jun 22 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.1.2-1
- Update to v1.1.2 (SOFTWARE-5235)

* Fri Mar 11 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.0.0-1
- Initial version

