Summary: OSG VMU test scripts
Name: vm-test-runs
Version: 1.1
Release: 1.1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: Apache 2.0
BuildArch: noarch
Url: https://github.com/opensciencegrid/vm-test-runs/

%{?systemd_requires}

Requires: libguestfs-tools
Requires: git

%description
Tools for running OSG VMU tests in the CHTC

%pre
getent group osgtest >/dev/null || groupadd -r osgtest
getent passwd osgtest >/dev/null || \
  useradd -g osgtest -m -s /sbin/nologin \
    -c "for automated OSG nightly tests" osgtest
exit 0

%prep
%setup -q

%install
mkdir -p %{buildroot}/osgtest/runs

install -D -m 0644 rpm/osg-nightly-tests.service %{buildroot}/%{_unitdir}/osg-nightly-tests.service
install -D -m 0644 rpm/osg-nightly-tests.timer %{buildroot}/%{_unitdir}/osg-nightly-tests.timer
install -D -m 0644 rpm/vm-test-cleanup.service %{buildroot}/%{_unitdir}/vm-test-cleanup.service
install -D -m 0644 rpm/vm-test-cleanup.timer %{buildroot}/%{_unitdir}/vm-test-cleanup.timer

install -D -m 0755 bin/compare-rpm-versions %{buildroot}/%{_bindir}/compare-rpm-versions
install -D -m 0755 bin/list-rpm-versions %{buildroot}/%{_bindir}/list-rpm-versions
install -D -m 0755 bin/osg-run-tests %{buildroot}/%{_bindir}/osg-run-tests
install -D -m 0755 bin/vm-test-cleanup %{buildroot}/%{_bindir}/vm-test-cleanup

install -D vmu.css %{buildroot}/%{_localstatedir}/www/html/vmu.css

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post osg-nightly-tests.service osg-nightly-tests.timer vm-test-cleanup.service vm-test-cleanup.timer

%preun
%systemd_preun osg-nightly-tests.service osg-nightly-tests.timer vm-test-cleanup.service vm-test-cleanup.timer

%postun
%systemd_postun_with_restart osg-nightly-tests.service osg-nightly-tests.timer vm-test-cleanup.service vm-test-cleanup.timer

%files
%attr(1777,root,root) %dir /osgtest/runs

%{_bindir}/compare-rpm-versions
%{_bindir}/list-rpm-versions
%{_bindir}/osg-run-tests
%{_bindir}/vm-test-cleanup

%{_unitdir}/osg-nightly-tests.service
%{_unitdir}/osg-nightly-tests.timer
%{_unitdir}/vm-test-cleanup.service
%{_unitdir}/vm-test-cleanup.timer

%{_localstatedir}/www/html/vmu.css

%changelog
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.1-1.1
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Fri Mar 27 2020 Brian Lin <blin@cs.wisc.edu> 1.1-1
- VM test run service cleanup fixes

* Tue Mar 24 2020 Brian Lin <blin@cs.wisc.edu> 1.0-1
- Package CSS file
- Systemd unit file fixes

* Tue Oct 15 2019 Brian Lin <blin@cs.wisc.edu> 0.1-1
- Initial packaging
