Name:           gracc-summary
Version:        4.2.0
Release:        1%{?dist}
Summary:        GRACC Summary Agents

License:        ASL 2.0
URL:            https://opensciencegrid.github.io/gracc/
Source0:        gracc-summary-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  systemd
BuildRequires:  python-srpm-macros 
BuildRequires:  python-rpm-macros 
BuildRequires:  python2-rpm-macros 
BuildRequires:  epel-rpm-macros
BuildRequires:  systemd
Requires:       python2-pika
Requires:       python-toml
Requires(pre):  shadow-utils

%description
GRACC Summary Agents


%pre
getent group gracc >/dev/null || groupadd -r gracc
getent passwd gracc >/dev/null || \
    useradd -r -g gracc -d /tmp -s /sbin/nologin \
    -c "GRACC Services Account" gracc
exit 0

%prep
%setup -q


%build
%{py2_build}


%install
%{py2_install}


install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/graccsum/config.d/
install -m 0744 config/gracc-summary.toml $RPM_BUILD_ROOT/%{_sysconfdir}/graccsum/config.d/gracc-summary.toml
install -d -m 0755 $RPM_BUILD_ROOT/%{_unitdir}
install -m 0744 config/graccsumperiodic.service $RPM_BUILD_ROOT/%{_unitdir}/
install -m 0744 config/graccsumperiodic.timer $RPM_BUILD_ROOT/%{_unitdir}/
install -m 0744 config/graccsumperiodicyearly.service $RPM_BUILD_ROOT/%{_unitdir}/
install -m 0744 config/graccsumperiodicyearly.timer $RPM_BUILD_ROOT/%{_unitdir}/



%files
%defattr(-, gracc, gracc)
%{python2_sitelib}/graccsum
%{python2_sitelib}/graccsum-%{version}-py2.?.egg-info
%attr(755, root, root) %{_bindir}/*
%{_unitdir}/graccsumperiodic.service
%{_unitdir}/graccsumperiodic.timer
%{_unitdir}/graccsumperiodicyearly.service
%{_unitdir}/graccsumperiodicyearly.timer
%config %{_sysconfdir}/graccsum/config.d/gracc-summary.toml

%doc



%changelog
* Tue May 16 2017 Derek Weitzel <dweitzel@cse.unl.edu> 4.2.0
- Fix bug in summarizer that leads to infinite loop, again

* Tue May 16 2017 Derek Weitzel <dweitzel@cse.unl.edu> 4.1.0
- Fix bug in summarizer that leads to infinite loop 

* Mon May 08 2017 Derek Weitzel <dweitzel@cse.unl.edu> 4.0.0
- Add configuration for yearly re-summarize every night

* Thu Feb 16 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.0.0
- Configuration now requires a URL setting

* Mon Feb 13 2017 Derek Weitzel <dweitzel@cse.unl.edu> 2.0-1
- Adding helpful text to command line options

* Mon Feb 13 2017 Derek Weitzel <dweitzel@cse.unl.edu> 2.0-1
- Adding transfer summaries
- Breaks configuration from earlier versions

* Tue Dec 13 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.3-1
- Change summarizer to systemd service
- Update tests for ES5

* Tue Aug 23 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.2-1
- Add vhost argument to summarizer

* Tue Aug 23 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.1-1
- Adding the summarizer command line

* Wed Jul 20 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.0-1
- Initial build

