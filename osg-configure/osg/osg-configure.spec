%global name osg-configure
%global version 0.7.3
%global release 1%{?dist}

Summary: Package for configure-osg and associated scripts
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: Apache 2.0
Group: Grid
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Suchandra Thapa <sthapa@ci.uchicago.edu>
Url: http://www.opensciencegrid.org
Requires: python 
Requires: yum
Provides: osg-configure

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}

%package rsv
Summary: Configure-osg configuration files for rsv
Group: Grid
Provides: configure-osg-rsv
%description rsv
This package includes the ini file for configuring rsv using configure-osg
%package cemon
Summary: Configure-osg configuration files for cemon
Group: Grid
Provides: configure-osg-cemon
%description cemon
This package includes the ini file for configuring cemon using configure-osg
%package gratia
Summary: Configure-osg configuration files for gratia
Group: Grid
Provides: configure-osg-gratia
%description gratia
This package includes the ini file for configuring gratia using configure-osg
%package gip
Summary: Configure-osg configuration files for gip
Group: Grid
Provides: configure-osg-gip
%description gip
This package includes the ini file for configuring gip using configure-osg
%package lsf
Summary: Configure-osg configuration files for lsf
Group: Grid
Provides: configure-osg-lsf
%description lsf
This package includes the ini file for configuring lsf using configure-osg
%package pbs
Summary: Configure-osg configuration files for pbs
Group: Grid
Provides: configure-osg-pbs
%description pbs
This package includes the ini file for configuring pbs using configure-osg
%package condor
Summary: Configure-osg configuration files for condor
Group: Grid
Provides: configure-osg-condor
%description condor
This package includes the ini file for configuring condor using configure-osg
%package sge
Summary: Configure-osg configuration files for sge
Group: Grid
Provides: configure-osg-sge
%description sge
This package includes the ini file for configuring sge using configure-osg
%package monalisa
Summary: Configure-osg configuration files for monalisa
Group: Grid
Provides: configure-osg-monalisa
%description monalisa
This package includes the ini files for configuring monalisa
%package ce
Summary: Configure-osg configuration files for CE
Group: Grid
Provides: configure-osg-ce
%description ce
This package includes the ini files for configuring a basic CE using 
configure-osg.  One of the packages for the job manager configuration also 
needs to be installed for the CE configuration.
%package misc
Summary: Configure-osg configuration files for misc software
Group: Grid
Provides: configure-osg-misc
%description misc
This package includes the ini files for various osg software including
certificates setup and glexec
%package squid
Summary: Configure-osg configuration files for squid
Group: Grid
Provides: configure-osg-squid
%description squid
This package includes the ini files for configuring an OSG system to use squid
%package managedfork
Summary: Configure-osg configuration files for managedfork
Group: Grid
Provides: configure-osg-managedfork
%description managedfork
This package includes the ini files for configuring an OSG CE to use
managedfork 

%prep
%setup

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
# delete config files for subpackges from file list
/bin/sed "/[01234][0125]-*/d" INSTALLED_FILES > tmp_file
mv tmp_file INSTALLED_FILES
/bin/sed "s_/usr/bin/osg-configure_/usr/sbin/osg-configure_" INSTALLED_FILES > tmp_file
mv tmp_file INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/var/log/osg/
touch $RPM_BUILD_ROOT/var/log/osg/osg-configure.log
mkdir -p $RPM_BUILD_ROOT/var/lib/osg
touch $RPM_BUILD_ROOT/var/lib/osg/osg-attributes.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-local-job-environment.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-job-environment.conf
# following is needed to move script to sbin directory
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mv $RPM_BUILD_ROOT/usr/bin/osg-configure $RPM_BUILD_ROOT/usr/sbin/osg-configure
ln -s /usr/sbin/osg-configure $RPM_BUILD_ROOT/usr/sbin/configure-osg 
rmdir $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
# Need the following for builds on batlab
%{python_sitelib}/osg_configure/*.pyo
%{python_sitelib}/osg_configure/modules/*.pyo
%{python_sitelib}/osg_configure/configure_modules/*.pyo
/usr/sbin/configure-osg
%ghost /var/log/osg/osg-configure.log
%ghost /var/lib/osg/osg-attributes.conf
%ghost /var/lib/osg/osg-local-job-environment.conf
%ghost /var/lib/osg/osg-job-environment.conf

%files rsv
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-rsv.ini
%files cemon
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-cemon.ini
%files gratia
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-gratia.ini
%files gip
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-gip.ini
%files lsf
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-lsf.ini
%files pbs
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-pbs.ini
%files condor
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-condor.ini
%files sge
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-sge.ini
%files ce
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/40-*.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/10-storage.ini
%files misc
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/10-misc.ini
%files squid
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/01-squid.ini
%files monalisa
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/02-monalisa.ini
%files managedfork
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/15-managedfork.ini

%changelog
* Thu Jan 05 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.7.3-1
- Added support for globus job manager config
- Added support for updating lcmaps.db and gums-client.properties files
- Added support for configuring SEG for job managers that support it
- Improved error reporting
- Internal refactoring done to improve maintainability

* Fri Dec 30 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.7.2-1
- Improved RSV configuration

* Wed Dec 7 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.7.1-1
- Fix the default location of the condor_config file
- Update ini comments to point to correct documentation

* Mon Dec 1 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.7.0-1
- Fix fetching VO names from user-vo-map file

* Mon Nov 21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.9-1
- Update defaults for rsv certs

* Thu Nov 17 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.8-1
- Fix bugs in configuring gratia probes

* Mon Nov 8 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.7-1
- Update to 0.6.7 to incorporate a variety of bug fixes
- Add support for configuring authentication methods

* Mon Oct 31 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.6-1
- Update to 0.6.6 to fix setting default job manager
- Update config files to use DEFAULT instead of UNAVAILABLE where appropriate

* Wed Oct 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.6.5-1
- Fixed a few RSV configuration issues.

* Tue Oct 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.4-1
- Writing to osg attributes file and update to 0.6.4

* Fri Oct 21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.3-1
- Fix a few bugs and update to 0.6.3

* Fri Oct 21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.2-1
- Added support for accept_limited in all job managers

* Thu Oct 20 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.1-1
- Added bugfixes dealing with managed fork configuration

* Thu Oct 20 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.6.0-1
- Added configuration of globus job manager for managed fork 
- Fixed unit tests for RSV

* Mon Oct 10 2011 Matyas Selmeci <matyas@cs.wisc.edu> 0.5.10-1
- Added configuration of glite-ce-monitor

* Mon Sep 26 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.5.8-1
- Fixed a bug in RSV configuration of gridftp hosts

* Tue Sep 13 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.5.7-1
- Fixed a bug in RSV configuration of Gratia Metric ProbeConfig

* Fri Sep 09 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.5.5-1
- Fixed a bug in rsv configuration when meta directory is not present

* Thu Sep 8 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.4-1
- Update to 0.5.4
- Add more subpackages for config files

* Mon Aug 26 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.2-1
- Update to 0.5.2
- Let config files reside in /etc/osg/config.d
- Make output files in /var/lib/osg ghost files

* Mon Aug 1 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.1-1
- Update to 0.5.1
- Add symlink for config.ini
- Make output files in /var/lib/osg ghost files

* Mon Jul 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.5.0-1
- Update to 0.5.0

* Mon Jul 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.0.4-1
- Update to 0.0.4

* Mon Jul 25 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> - 0.0.3-1
- Update to 0.0.3
- Fix python_sitelab declaration
- Use %{__python} instead of python

* Fri Jul  22 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.2-2
- Include .pyo files in files

* Fri Jul  22 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.2-1
- Created initial configure-osg rpm using real source 

* Thu Jul  21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.1-1
- Created an initial osg-configure RPM 
