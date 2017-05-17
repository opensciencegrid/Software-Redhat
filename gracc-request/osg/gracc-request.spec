Name:           gracc-request
Version:        3.6.0
Release:        1%{?dist}
Summary:        GRACC Listener for Raw and Summary Records

License:        ASL 2.0
URL:            https://opensciencegrid.github.io/gracc/
Source0:        gracc-request-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  systemd
BuildRequires:  python-srpm-macros 
BuildRequires:  python-rpm-macros 
BuildRequires:  python2-rpm-macros 
BuildRequires:  epel-rpm-macros
BuildRequires:  systemd
Requires:       python2-pika
Requires:       python-elasticsearch-dsl
Requires:       python-dateutil
Requires:       python-toml
Requires:       python2-filelock
Requires(pre):  shadow-utils

%description
GRACC Listener for Raw and Summary Records

%package -n %{name}-client
Summary:        GRACC Listener Client
Requires:       python2-pika
Requires:       python-dateutil
%description -n %{name}-client
GRACC Listener for Raw and Summary Records


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


install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/graccreq/config.d/
install -m 0744 config/gracc-request.toml $RPM_BUILD_ROOT/%{_sysconfdir}/graccreq/config.d/gracc-request.toml
install -d -m 0755 $RPM_BUILD_ROOT/%{_unitdir}
install -m 0744 config/graccreq.service $RPM_BUILD_ROOT/%{_unitdir}/



%files
%defattr(-, gracc, gracc)
%{python2_sitelib}/graccreq
%{python2_sitelib}/graccreq-%{version}-py2.?.egg-info
%attr(755, root, root) %{_bindir}/*
%{_unitdir}/graccreq.service
%config %{_sysconfdir}/graccreq/config.d/gracc-request.toml

%doc



%changelog
* Tue May 16 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.6.0-1
- Fix bug in Field of Science calculation

* Mon May 08 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.5.0-1
- Add Field of Science to VO records
- Add timeout to service file for rabbitmq failures

* Wed Mar 30 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.4.0-1
- Remove Resource_Source and Resource_Destination from transfer summaries

* Wed Feb 15 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.3.0-1
- Use URLs to specify AMQP host

* Wed Feb 15 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.2.0-1
- Add support for non-standard ports

* Wed Feb 15 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.1.0-1
- Add Njobs aggregation

* Tue Feb 14 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.0.1-1
- Remove some logging lines

* Mon Feb 13 2017 Derek Weitzel <dweitzel@cse.unl.edu> 3.0-1
- Add Transfer Summaries

* Wed Dec 21 2016 Derek Weitzel <dweitzel@cse.unl.edu> 2.7-1
- Optimize OIMTopology with caching
- Increase profiler coverage.

* Mon Dec 19 2016 Derek Weitzel <dweitzel@cse.unl.edu> 2.6-1
- Fix size bug with new ES5.  Set it to max signed int

* Wed Dec 14 2016 Derek Weitzel <dweitzel@cse.unl.edu> 2.5-1
- Changing OIM naming
- Fix bug in profiler

* Tue Dec 13 2016 Derek Weitzel <dweitzel@cse.unl.edu> 2.4-1
- Add profiling to summarizer
- Fix bug with Processors = 0

* Fri Oct 7 2016 Kevin Retzke <kretzke@fnal.gov> 2.3-1
- Add name corrections

* Fri Sep 23 2016 Derek Weitzel <dweitzel@cse.unl.edu> 2.2-1
- Dramatically improve OIM Topology performance

* Fri Sep 23 2016 Derek Weitzel <dweitzel@cse.unl.edu> 2.1-1
- Add OIM Topology information from OIM to summary records

* Wed Sep 08 2016 Derek Weitzel <dweitzel@cse.unl.edu> 2.0-1
- Add Project information from OIM to summary records

* Mon Aug 29 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.7-1
- Round up the day for summary records, so it can retrieve all of the last day requested.
- Use configuartion options rather than hard code exchanges and queues

* Fri Aug 26 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.6-1
- Add ProbeName and SiteName to summaries

* Fri Aug 19 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.5-1
- Add ProjectName, DN, and ReportableVOName terms to summary

* Tue Aug 02 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.4-1
- Fix Summary metrics accounting

* Tue Aug 02 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.3-1
- Fix summary records for new indexes

* Fri Jul 29 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.2-1
- Use EndTime for summarized range

* Wed Jul 20 2016 Derek Weitzel <dweitzel@cse.unl.edu> 1.1-1
- Updating the client with new arguments for summarizer

