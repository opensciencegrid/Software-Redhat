Name:           gracc-archive
Version:        1.6.0
Release:        2%{?dist}
Summary:        GRACC Archive

License:        ASL 2.0
URL:            https://opensciencegrid.github.io/gracc/
Source0:        gracc-archive-%{version}.tar.gz
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
Requires:       python-setuptools
Requires:       python-urllib3
Requires(pre):  shadow-utils

%description
GRACC Archive Agent


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


install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/graccarchive/config/
install -m 0744 config/gracc-archive-raw.toml $RPM_BUILD_ROOT/%{_sysconfdir}/graccarchive/config/gracc-archive-raw.toml
install -d -m 0755 $RPM_BUILD_ROOT/%{_unitdir}
install -m 0744 config/graccarchive@.service $RPM_BUILD_ROOT/%{_unitdir}/

# For the archiver output directories
install -d -m 0755 $RPM_BUILD_ROOT/%{_sharedstatedir}/graccarchive/sandbox
install -d -m 0755 $RPM_BUILD_ROOT/%{_sharedstatedir}/graccarchive/output


%files
%defattr(-, gracc, gracc)
%{python2_sitelib}/graccarchive
%{python2_sitelib}/graccarchive-%{version}-py2.?.egg-info
%attr(755, root, root) %{_bindir}/*
%{_unitdir}/graccarchive@.service
%config %{_sysconfdir}/graccarchive/config/gracc-archive-raw.toml
%{_sharedstatedir}/graccarchive


%doc



%changelog
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.6.0-2
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Tue Jan 30 2018 Derek Weitzel <dweitzel@cse.unl.edu> - 1.6.0-1
- Place hostname in archive file name

* Tue Dec 19 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.5.0-1
- Use select connection for better performance

* Wed May 31 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.4.1-1
- Fix bug in timer causing it to be destroyed

* Tue May 23 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.4.0-1
- Run daemon in single thread
- Properly flush gzfile every 10 seconds
- ACK rabbitmq messages

* Tue May 23 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.3.1-1
- Capture disconnections on initial connection creations

* Mon May 22 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.3.0-1
- Fix memory leak caused by python tarfile implementation
- Implement proper flushes of the gzip stream

* Wed May 17 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.2.2-1
- Capture and retry when a connection fails

* Mon Apr 03 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.2-1
- Adding service instances

* Mon Apr 03 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.1-1
- Adding service instances

* Tue Mar 21 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-2
- Add state directories

* Tue Dec 13 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.0-1
- Initial build

