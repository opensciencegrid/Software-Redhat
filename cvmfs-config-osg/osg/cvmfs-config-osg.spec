Summary: CernVM File System OSG Configuration and Public Keys
Name: cvmfs-config-osg
Version: 2.5
Release: 1%{?dist}
# download with:
# $ curl -L -o cvmfs-config-osg-%{version}.tar.gz \
#   https://github.com/opensciencegrid/cvmfs-config-osg/archive/v%{version}.tar.gz
Source: %{name}-%{version}.tar.gz
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

Obsoletes: cvmfs-config-default
Conflicts: cvmfs-config-egi

%prep
%setup

%description
Default configuration parameters and public keys for CernVM-FS

%install
rm -rf $RPM_BUILD_ROOT
make install-redhat DESTDIR=$RPM_BUILD_ROOT

%files
%dir %{_sysconfdir}/cvmfs/keys/opensciencegrid.org
%{_sysconfdir}/cvmfs/keys/opensciencegrid.org/*
%config %{_sysconfdir}/cvmfs/default.d/*
%config %{_sysconfdir}/cvmfs/config.d/*

%changelog
* Mon Oct 12 2020 Dave Dykstra <dwd@fnal.gov> - 2.5-1
- Update the configuration for the config repo to apply all the logic
  from the config repo's default.conf and common.conf.  That is, support
  USE_CVMFS_CDN and CVMFS_CLIENT_PROFILE and set default CVMFS_PAC_URLS
  covering the WLCG Web Proxy Auto Discovery.
- Reverse the order of the fallback proxies because of the bug in 
  https://sft.its.cern.ch/jira/browse/CVM-1920

* Fri Mar 27 2020 Dave Dykstra <dwd@fnal.gov> - 2.4-4
- Skipped release 2.4-2 and 2.4-3 to make consistent with cvmfs-config-egi.
- Change Conflicts: cvmfs-config-default to Obsoletes: to make it
  easier to replace. Add Conflicts: cvmfs-config-egi because it
  is mutually exclusive.

* Tue Jul 23 2019 Dave Dykstra <dwd@fnal.gov> - 2.4-1
- Change the server urls for the config-osg repository to use openhtc.io
  aliases when the proxy url can use DIRECT.

* Fri Feb 23 2018 Dave Dykstra <dwd@fnal.gov> - 2.3-1
- Change the changelog date on version 2.0.3 from Feb 28 2017 to
  May 28 2017 because osg-build complained about non-descending order
  of the dates.
- Change the rpm/rpmbuild-cvmfs-config-osg development test script 
  to read from rpm instead of packaging/redhat.

* Thu Feb 22 2018 Dave Dykstra <dwd@fnal.gov> - 2.2-1
- Just change the version number because the OSG github-source for
  reading spec files doesn't work with dash release tags.

* Wed Dec 20 2017 Dave Dykstra <dwd@fnal.gov> - 2.1-2
- Restore the changes from 2.0-2 that were accidentally wiped out in
  the conversion to github.

* Fri Nov 17 2017 Dave Dykstra <dwd@fnal.gov> - 2.1-1
- Merge LIGO changes to debian packaging
- Move packaging/debian to debian and packaging/redhat to rpm, to work
  better with OBS and new OSG github packaging standard

* Tue May 28 2017 Dave Dykstra <dwd@fnal.gov> - 2.0-3
- Use common install Makefile between debian and redhat

* Fri May 19 2017 Brian Lin <blin@cs.wisc.edu> - 2.0-2
- Drop conflicts (SOFTWARE-2678)

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
