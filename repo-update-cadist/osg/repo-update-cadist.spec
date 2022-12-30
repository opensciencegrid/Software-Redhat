Name:      repo-update-cadist
Summary:   repo-update-cadist
Version:   1.1.4
Release:   1.1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       https://github.com/opensciencegrid/repo-update-cadist
BuildArch: noarch
Requires: subversion
Requires: wget
Requires: yum-utils

Source0:   %{name}-%{version}.tar.gz

%description
%{summary}

%prep
%setup

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -pm 755 %{name}  $RPM_BUILD_ROOT%{_bindir}/
%if 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 %{name}.service $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 %{name}.timer $RPM_BUILD_ROOT%{_unitdir}
%else
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
install -pm 644 %{name}.cron  $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
%endif

%files
%{_bindir}/%{name}
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer
%else
%config(noreplace) %{_sysconfdir}/cron.d/%{name}.cron
%endif

%changelog
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.1.4-1.1
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Tue Feb 02 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.1.4-1
- Fix path to OSG tarball in IGTF INDEX.html (SOFTWARE-4394)

* Thu Jul 30 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.1.2-1
- Stop fixing broken CA bundle tarball links in INDEX.html (SOFTWARE-3874)

* Thu May 07 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.1.1-1
- Fix broken CA bundle tarball links in INDEX.html files (SOFTWARE-4091)

* Thu May 07 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.1.0-1
- Generate tarball & artifacts from binary rpms (SOFTWARE-4091)

* Mon Jul 01 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.4-1
- Stop checking gpg sig (SOFTWARE-3555)

* Fri Apr 27 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.0.3-1
- Add systemd service/timer and locking to cron job (SOFTWARE-3234)
- Only run service hourly (SOFTWARE-3238)

* Tue Apr 17 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.2-1
- Fix comment in cron job

* Tue Apr 17 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.1-1
- Add cron job
- Add dependencies

* Tue Mar 06 2018 Edgar Fajardo <efajardo@physics.ucsd.edu> 1.0.0-2
- Clean and buildroot sections removed

* Mon Mar 05 2018 Edgar Fajardo <efajardo@physics.ucsd.edu> 1.0.0-1
- First RPM 1.0.0 (SOFTWARE-3102)
