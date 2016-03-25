Summary: CernVM File System OSG Configuration and Public Keys
Name: cvmfs-config-osg
Version: 1.2
Release: 3%{?dist}
Source0: opensciencegrid.org.pub
Source1: 60-osg.conf
Source2: config-osg.opensciencegrid.org.conf
BuildArch: noarch
Group: Applications/System
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: cvmfs-config = %{version}-%{release}
Obsoletes: cvmfs-keys < 1.6
Provides: cvmfs-keys = 1.7
Obsoletes: cvmfs-init-scripts < 1.0.21
Provides: cvmfs-init-scripts = 1.0.22

Obsoletes: oasis-config < 8
Provides: oasis-config = 9

Conflicts: cvmfs-config-default

Conflicts: cvmfs < 2.2.0
Conflicts: cvmfs-server < 2.2.0

%description
Default configuration parameters and public keys for CernVM-FS, providing access
to repositories under the cern.ch, egi.eu, and opensciencegrid.org domains

%install
rm -rf $RPM_BUILD_ROOT
for cvmfsdir in keys/opensciencegrid.org config.d default.d; do
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/$cvmfsdir
done
for key in %{SOURCE0}; do
    install -D -m 444 "${key}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/keys/opensciencegrid.org
done
for defaultconf in %{SOURCE1}; do
    install -D -m 444 "${defaultconf}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/default.d
done
for conf in %{SOURCE2}; do
    install -D -m 444 "${conf}" $RPM_BUILD_ROOT%{_sysconfdir}/cvmfs/config.d
done

%files
%dir %{_sysconfdir}/cvmfs/keys/opensciencegrid.org
%{_sysconfdir}/cvmfs/keys/opensciencegrid.org/*
%config %{_sysconfdir}/cvmfs/default.d/*
%config %{_sysconfdir}/cvmfs/config.d/*

%changelog
* Fri Mar 25 2016 Dave Dykstra <dwd@fnal.gov> - 1.2-3
- Switch to using config-osg.opensciencegrid.org config repository.

* Mon Feb  1 2016 Dave Dykstra <dwd@fnal.gov> - 1.2-2
- Update to official tagged 2.2.0-1 source.

* Tue Jan 26 2016 Dave Dykstra <dwd@fnal.gov> - 1.2-1
- Update cms.osgstorage.org config to only read cvmfs data with https
  direct from the repository server.

* Fri Jan 22 2016 Dave Dykstra <dwd@fnal.gov> - 1.2-0.2
- Move to osg-upcoming, and adjust configs a little.

* Fri Jan 15 2016 Dave Dykstra <dwd@fnal.gov> - 1.2-0.1
- Testing build for cvmfs-2.2.0, including osgstorage.org configs.

* Fri Oct 16 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-8
- Instead of having egi.eu and opensciencegrid.org domain configurations,
  have a default configuration for any domain besides cern.ch that
  reads from the OSG stratum 1s and accepts any repositorIes that are
  found there and are verified by the opensciencegrid.org.pub key.

* Tue Jul 28 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-7
- Change patch of /etc/cvmfs/domain.d/egi.eu.conf to include the
  OSG public key as legitimate signer of egi.eu repositories, for
  the purpose of emergency blanking.

* Fri May 22 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-6
- Add specific versions on Obsoletes of cvmfs-keys and cvmfs-init-scripts,
  and add a Provides of a version, as was done to cvmfs-config-default
  upstream to follow Fedora packaging guidelines.  Do likewise for
  oasis-config.  Add Conflicts for cvmfs-config-default.

* Fri Mar 27 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-5
- add oasis.opensciencegrid.org.conf to set $OASIS_CERTIFICATES

* Wed Mar 25 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-4
- add patch to set egi and osg repo servers to only OSG stratum 1s

* Wed Mar 25 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-3
- add %{?dist} to release number

* Wed Mar 25 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-2
- bump release only to allow koji to rebuild; the first attempt failed
  because of a mysterious error in koji

* Wed Mar 25 2015 Dave Dykstra <dwd@fnal.gov> - 1.1-1
- initial creation, based on cvmfs-config-default.spec
