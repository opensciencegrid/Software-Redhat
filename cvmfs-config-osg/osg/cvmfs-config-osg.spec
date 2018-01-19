Summary: CernVM File System OSG Configuration and Public Keys
Name: cvmfs-config-osg
Version: 2.0
Release: 3%{?dist}
# download with:
# $ curl -L -o cvmfs-config-osg-%{version}.tar.gz \
#   https://github.com/opensciencegrid/cvmfs-config-osg/archive/v%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
Group: Applications/System
License: BSD

Provides: cvmfs-config = %{version}-%{release}
Obsoletes: cvmfs-keys < 1.6
Provides: cvmfs-keys = 1.7
Obsoletes: cvmfs-init-scripts < 1.0.21
Provides: cvmfs-init-scripts = 1.0.22

Obsoletes: oasis-config < 8
Provides: oasis-config = 9

Conflicts: cvmfs-config-default

Conflicts: cvmfs < 2.3.3
Conflicts: cvmfs-server < 2.3.3

%prep
%setup 

%description
Default configuration parameters and public keys for CernVM-FS

%install
make install-redhat DESTDIR=$RPM_BUILD_ROOT

%files
%dir %{_sysconfdir}/cvmfs/keys/opensciencegrid.org
%{_sysconfdir}/cvmfs/keys/opensciencegrid.org/*
%config %{_sysconfdir}/cvmfs/default.d/*
%config %{_sysconfdir}/cvmfs/config.d/*

%changelog
* Tue Feb 28 2017 Dave Dykstra <dwd@fnal.gov> - 2.0-3
- Use common install Makefile between debian and redhat

* Fri Feb 24 2017 Dave Dykstra <dwd@fnal.gov> - 2.0-2
- Convert to store source on github.

* Wed Feb 15 2017 Dave Dykstra <dwd@fnal.gov> - 2.0-1
- Increase the version number further to make sure it is higher than
  cvmfs-config-default.

* Sat Feb 11 2017 Dave Dykstra <dwd@fnal.gov> - 1.3-1
- Add CVMFS_CONFIG_REPO_REQUIRED=yes.  Change Conflicts on cvmfs to be less
  than version 2.3.3 because the option was added then.

* Wed Jun 29 2016 Dave Dykstra <dwd@fnal.gov> - 1.2-5
- Fix copy/paste error

* Wed Jun 29 2016 Dave Dykstra <dwd@fnal.gov> - 1.2-4
- Add CVMFS_FALLBACK_PROXY.

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
