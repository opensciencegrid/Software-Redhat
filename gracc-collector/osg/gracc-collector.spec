Name:           gracc-collector
Version:        1.1.7
Release:        1%{?dist}
Summary:        Gratia-compatible collector for grid accounting records
License:        MIT

URL:            https://gracc.opensciencegrid.org
Source:         %{name}.tar.gz

BuildRequires:  systemd-units
Requires(pre): shadow-utils

%description
The gracc-collector is a "Gratia-Compatible Collector" that acts as a transitional
interface between the obsolete Gratia accounting collector and probes and the new
GRÅCC accounting system.

It listens for bundles of records (as would be sent via replication from a Gratia
collector or from a Gratia probe) on HTTP, processes the bundle into individual
usage records, and sends those to RabbitMQ or another AMQP 0.9.1 broker.

%define debug_packages ${nil}
%define debug_package ${nil}

%prep
%autosetup -n %{name}

%build
# setup local GOPATH vith source and vendored dependencies
mkdir src
ln -rs vendor/* src/
mkdir -p src/github.com/opensciencegrid
ln -rs ./ src/github.com/opensciencegrid/gracc-collector
export GOPATH=$(pwd)
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}/
cp -p gracc-collector %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_unitdir}/
cp -p etc/gracc-collector.service %{buildroot}%{_unitdir}/
cp -p etc/gracc-collector@.service %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_sysconfdir}/gracc
cp -p etc/gracc-collector.cfg %{buildroot}%{_sysconfdir}/gracc/gracc-collector.cfg
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -p etc/gracc-collector.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/gracc-collector
mkdir -p %{buildroot}%{_var}/log/gracc


%files
%doc README.md
%{_bindir}/gracc-collector
%{_unitdir}/gracc-collector.service
%{_unitdir}/gracc-collector@.service
%config(noreplace) %{_sysconfdir}/gracc/gracc-collector.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/gracc-collector
%attr(755, gracc, gracc) %{_var}/log/gracc/


%pre
getent group gracc >/dev/null || groupadd -r gracc
getent passwd gracc >/dev/null || \
    useradd -r -g gracc -d /etc/gracc -s /sbin/nologin \
    -c "Account used to run the GRACC collector" gracc
exit 0

%changelog
* Thu Nov 02 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 1.1.7-1
- Add persistence to the gracc-collector

* Wed May 17 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 1.1.6-1
- Add support for running behind nginx.

* Wed Apr 05 2017 Kevin Retzke <kretzke@fnal.gov> - 1.1.5-1
- Package v1.1.5. Reset blocked flag if RabbitMQ connection is closed.

* Thu Mar 30 2017 Kevin Retzke <kretzke@fnal.gov> - 1.1.4-1
- Package v1.1.4. Fix catching AMQP unblock signal.

* Sat Feb 25 2017 Kevin Retzke <kretzke@fnal.gov> - 1.1.3-1
- Package v1.1.3. Better handle AMQP blocked connections.

* Wed Feb 22 2017 Kevin Retzke <kretzke@fnal.gov> - 1.1.2-1
- Package v1.1.2. Fix resource leak.

* Mon Jan 30 2017 Kevin Retzke <kretzke@fnal.gov> - 1.1.1-1
- Package v1.1.1. Support AMQP+TLS.

* Thu Jan 12 2017 Kevin Retzke <kretzke@fnal.gov> - 1.1.0-1
- Package v1.1.0. Accept UsageRecord.

* Wed Jan 11 2017 Kevin Retzke <kretzke@fnal.gov> - 1.0.1-1
- Package v1.0.1. Ignore bundlesize from probe.

* Thu Jan 05 2017 Kevin Retzke <kretzke@fnal.gov> - 1.0.0-1
- Package v1.0.0. Feature-complete for GRACC production deployment.

* Mon Oct 17 2016 Kevin Retzke <kretzke@fnal.gov> - 0.04.01-1
- Package v0.4.1

* Mon Aug 15 2016 Kevin Retzke <kretzke@fnal.gov> - 0.04.00-1
- Package v0.4.0

* Mon Jun 06 2016 Kevin Retzke <kretzke@fnal.gov> - 0.03.01-1
- Package v0.03.01: fully flattened JSON records

* Fri Jun 03 2016 Kevin Retzke <kretzke@fnal.gov> - 0.03.00-1
- Initial rpm release.
