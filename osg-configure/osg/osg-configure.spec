Summary: Configuration tool for the OSG Software Stack
Name: osg-configure
Version: 4.2.0
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: Apache 2.0
BuildArch: noarch
Url: https://github.com/opensciencegrid/osg-configure
BuildRequires: python3-devel
BuildRequires: python3-condor >= 9.0.9
Requires: python3
%global __python /usr/bin/python3
Requires: %{name}-libs = %{version}-%{release}


Obsoletes: %{name}-managedfork < 2.2.2-2
Obsoletes: %{name}-network < 2.2.2-2


%description
%{summary}

%package -n osg-ce-attributes-generator
Summary: Generates CE attributes that will be uploaded to the central collector
Requires: python3-condor
Requires: %name-libs = %version-%release
Requires: %name-siteinfo
Requires: %name-cluster
%description -n osg-ce-attributes-generator
Generates CE attributes that will be uploaded to the central collector

%package libs
Summary: OSG Configure libraries
Requires: python3
%description libs
This package containers the Python libraries used by osg-configure

%package siteinfo
Summary: OSG configuration file for site information
%description siteinfo
This package includes the ini file for configuring site information using osg-configure
and resource/resource_group information with osg-ce-attributes-generator.

%package rsv
Summary: Transitional package
%description rsv
This is an empty package to make upgrades easier. It may be removed.

%package gratia
Summary: OSG configuration file for gratia
Requires: %name = %version-%release
Requires: %name-siteinfo
%description gratia
This package includes the ini file for configuring gratia using osg-configure

%package gip
Summary: Transitional package for osg-configure 4
Requires: %name-cluster
%description gip
This is an empty package to make upgrades to osg-configure 4 easier.
It may be removed.

%package cluster
Summary: OSG configuration files for describing cluster
%description cluster
This package contains 31-cluster.ini for Subcluster and Resource Entry sections,
and 35-pilots.ini for Pilot sections, for use with osg-configure and
osg-ce-attributes-generator.

%package lsf
Summary: OSG configuration file for lsf
Requires: %name = %version-%release
Requires: %name-gateway
%description lsf
This package includes the ini file for configuring lsf using osg-configure

%package pbs
Summary: OSG configuration file for pbs
Requires: %name = %version-%release
Requires: %name-gateway
%description pbs
This package includes the ini file for configuring pbs using osg-configure

%package condor
Summary: OSG configuration file for condor
Requires: %name = %version-%release
Requires: %name-gateway
%description condor
This package includes the ini file for configuring condor using osg-configure

%package sge
Summary: OSG configuration file for sge
Requires: %name = %version-%release
Requires: %name-gateway
%description sge
This package includes the ini file for configuring sge using osg-configure

%package ce
Summary: OSG configuration file for CE
Requires: %name = %version-%release
Requires: %name-gateway
Requires: %name-siteinfo
%description ce
This package includes the ini files for configuring a basic CE using
osg-configure.  One of the packages for the job manager configuration also
needs to be installed for the CE configuration.

%package misc
Summary: OSG configuration file for misc software
%description misc
This is a dummy package to help upgrades

%package squid
Summary: OSG configuration file for squid
Requires: %name = %version-%release
%description squid
This package includes the ini files for configuring an OSG system to use squid

%package tests
Summary: OSG-Configure unit tests and configuration for unit testing
Requires: %name = %version-%release
%description tests
This package includes the ini files and files for unit tests that osg-configure
uses to verify functionality

%package slurm
Summary: OSG configuration file for slurm
Requires: %name = %version-%release
Requires: %name-gateway
%description slurm
This package includes the ini file for configuring slurm using osg-configure

%package bosco
Summary: OSG configuration file for bosco
Requires: %name = %version-%release
Requires: %name-gateway
Requires: /usr/bin/condor_remote_cluster
%description bosco
This package includes the ini file for configuring bosco using osg-configure

%package infoservices
Summary: OSG configuration file for the osg info services
Requires: %name = %version-%release
Requires: %name-cluster
Requires: osg-ce-attributes-generator
%description infoservices
This package includes the ini file for configuring the osg info services using osg-configure

%package gateway
Summary: OSG configuration file for job gateway (htcondor-ce)
Requires: %name = %version-%release
%description gateway
This package includes the ini file for configuring the job gateway
(htcondor-ce) using osg-configure


%prep
%setup -q

%build
%{__python} setup.py build

%install
find . -type f -exec sed -ri '1s,^#!\s*(/usr)?/bin/(env *)?python.*,#!%{__python},' '{}' +
make install DESTDIR=$RPM_BUILD_ROOT PYTHON=%{__python}

mkdir -p $RPM_BUILD_ROOT/etc/condor-ce/config.d
echo 'OSG_CONFIGURE_PRESENT=true' > $RPM_BUILD_ROOT/etc/condor-ce/config.d/50-osg-configure-present.conf  # SOFTWARE-2805
touch $RPM_BUILD_ROOT/etc/condor-ce/config.d/50-osg-configure.conf
mkdir -p $RPM_BUILD_ROOT/var/log/osg/
touch $RPM_BUILD_ROOT/var/log/osg/osg-configure.log
mkdir -p $RPM_BUILD_ROOT/var/lib/osg
touch $RPM_BUILD_ROOT/var/lib/osg/osg-attributes.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-local-job-environment.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-job-environment.conf

%check
for module in $RPM_BUILD_ROOT/%{python_sitelib}/osg_configure/configure_modules/[a-z]*.py; do
    %{__python} -c "import osg_configure.configure_modules.$(basename "$module" .py)"
done
for module in $RPM_BUILD_ROOT/%{python_sitelib}/osg_configure/modules/[a-z]*.py; do
    %{__python} -c "import osg_configure.modules.$(basename "$module" .py)"
done
PYTHONPATH=$RPM_BUILD_ROOT/%{python_sitelib}:$PYTHONPATH %{__python} $RPM_BUILD_ROOT/usr/sbin/osg-configure --version
PYTHONPATH=$RPM_BUILD_ROOT/%{python_sitelib}:$PYTHONPATH %{__python} $RPM_BUILD_ROOT/usr/bin/osg-ce-attributes-generator --version

%files
%{python_sitelib}/osg_configure/configure_modules/__init__.py*
%{python_sitelib}/osg_configure/configure_modules/bosco.py*
%{python_sitelib}/osg_configure/configure_modules/condor.py*
%{python_sitelib}/osg_configure/configure_modules/gateway.py*
%{python_sitelib}/osg_configure/configure_modules/gratia.py*
%{python_sitelib}/osg_configure/configure_modules/localsettings.py*
%{python_sitelib}/osg_configure/configure_modules/lsf.py*
%{python_sitelib}/osg_configure/configure_modules/pbs.py*
%{python_sitelib}/osg_configure/configure_modules/sge.py*
%{python_sitelib}/osg_configure/configure_modules/siteinformation.py*
%{python_sitelib}/osg_configure/configure_modules/slurm.py*
%{python_sitelib}/osg_configure/configure_modules/squid.py*
%{python_sitelib}/osg_configure/configure_modules/storage.py*

%{python_sitelib}/osg_configure/configure_modules/__pycache__/__init__*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/bosco*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/condor*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/gateway*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/gratia*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/localsettings*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/lsf*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/pbs*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/sge*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/siteinformation*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/slurm*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/squid*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/storage*

/usr/sbin/osg-configure
%dir %attr(-,root,root) /var/log/osg
%dir %attr(-,root,root) /var/lib/osg
%ghost /var/log/osg/osg-configure.log
%ghost /var/lib/osg/osg-attributes.conf
%ghost /var/lib/osg/osg-local-job-environment.conf
%ghost /var/lib/osg/osg-job-environment.conf
%ghost /etc/condor-ce/config.d/50-osg-configure.conf

%files libs
%{python_sitelib}/osg_configure-%{version}-*.egg-info
%{python_sitelib}/osg_configure/__init__.py*
%{python_sitelib}/osg_configure/modules/__init__.py*
%{python_sitelib}/osg_configure/modules/baseconfiguration.py*
%{python_sitelib}/osg_configure/modules/configfile.py*
%{python_sitelib}/osg_configure/modules/exceptions.py*
%{python_sitelib}/osg_configure/modules/jobmanagerconfiguration.py*
%{python_sitelib}/osg_configure/modules/utilities.py*
%{python_sitelib}/osg_configure/modules/validation.py*
%{python_sitelib}/osg_configure/version.py*

%{python_sitelib}/osg_configure/__pycache__/__init__*
%{python_sitelib}/osg_configure/modules/__pycache__/__init__*
%{python_sitelib}/osg_configure/modules/__pycache__/baseconfiguration*
%{python_sitelib}/osg_configure/modules/__pycache__/configfile*
%{python_sitelib}/osg_configure/modules/__pycache__/exceptions*
%{python_sitelib}/osg_configure/modules/__pycache__/jobmanagerconfiguration*
%{python_sitelib}/osg_configure/modules/__pycache__/utilities*
%{python_sitelib}/osg_configure/modules/__pycache__/validation*
%{python_sitelib}/osg_configure/__pycache__/version*

%files rsv

%files gratia
%config(noreplace) %{_sysconfdir}/osg/config.d/30-gratia.ini

%files gip

%files cluster
%config(noreplace) %{_sysconfdir}/osg/config.d/31-cluster.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/35-pilot.ini

%files lsf
%config(noreplace) %{_sysconfdir}/osg/config.d/20-lsf.ini

%files pbs
%config(noreplace) %{_sysconfdir}/osg/config.d/20-pbs.ini

%files condor
%config(noreplace) %{_sysconfdir}/osg/config.d/20-condor.ini

%files sge
%config(noreplace) %{_sysconfdir}/osg/config.d/20-sge.ini

%files bosco
%config(noreplace) %{_sysconfdir}/osg/config.d/20-bosco.ini

%files siteinfo
%config(noreplace) %{_sysconfdir}/osg/config.d/40-siteinfo.ini

%files ce
%config(noreplace) %{_sysconfdir}/osg/config.d/40-localsettings.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/10-storage.ini
%config(noreplace) %{_sysconfdir}/osg/grid3-locations.txt

%files misc

%files squid
%config(noreplace) %{_sysconfdir}/osg/config.d/01-squid.ini

%files infoservices
%config(noreplace) %{_sysconfdir}/osg/config.d/30-infoservices.ini
%{python_sitelib}/osg_configure/configure_modules/infoservices.py*
%{python_sitelib}/osg_configure/configure_modules/__pycache__/infoservices*

%files -n osg-ce-attributes-generator
/usr/bin/osg-ce-attributes-generator
%{python_sitelib}/osg_configure/modules/ce_attributes.py*
%{python_sitelib}/osg_configure/modules/resourcecatalog.py*
%{python_sitelib}/osg_configure/modules/reversevomap.py*
%{python_sitelib}/osg_configure/modules/subcluster.py*
%{python_sitelib}/osg_configure/modules/__pycache__/ce_attributes*
%{python_sitelib}/osg_configure/modules/__pycache__/resourcecatalog*
%{python_sitelib}/osg_configure/modules/__pycache__/reversevomap*
%{python_sitelib}/osg_configure/modules/__pycache__/subcluster*

%files tests
/usr/share/osg-configure/*

%files slurm
%config(noreplace) %{_sysconfdir}/osg/config.d/20-slurm.ini

%files gateway
%config(noreplace) %{_sysconfdir}/osg/config.d/10-gateway.ini
%config(noreplace) %{_sysconfdir}/condor-ce/config.d/50-osg-configure-present.conf



%changelog
* Tue Jun 18 2024 Mátyás Selmeci <matyas@cs.wisc.edu> 4.2.0-1
- Turn osg-configure-rsv into a dummy package (SOFTWARE-4511)
- Add "queue" to OSG_ResourceCatalog for Pilot sections (SOFTWARE-5881)

* Fri Feb 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> 4.1.1-3
- Declare ownership of /var/lib/osg and /var/log/osg (SOFTWARE-5808)

* Sat Apr 09 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 4.1.1-1
- Version 4.1.1 (SOFTWARE-5122)

* Thu Mar 03 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 4.1.0-1
- Version 4.1.0 (SOFTWARE-4972)

* Sun Jan 30 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 4.1.0-0.15
- Depend on /usr/bin/condor_remote_cluster instead of condor-bosco (SOFTWARE-4973)
- Split libs into separate RPM
- Add osg-ce-attributes-generator (SOFTWARE-4895)
- Don't require base osg-configure package in osg-configure-siteinfo and osg-configure-cluster
  because they can also be used by osg-ce-attributes-generator
- Advertise batch system used by bosco (SOFTWARE-3720)

* Thu Feb 25 2021 Mátyás Selmeci <matyas@cs.wisc.edu> 4.0.0-1
- Drop lcmaps-db-templates dependency (SOFTWARE-4503)
- Turn osg-configure-misc into a dummy package (SOFTWARE-4507)
- Rename 30-gip.ini to 31-cluster.ini and osg-configure-gip to osg-configure-cluster (SOFTWARE-4485)
- Deprecate RSV  (SOFTWARE-4511)

* Thu Jan 07 2021 Mátyás Selmeci <matyas@cs.wisc.edu> 3.11.0-1
- Add Pilot entries (SOFTWARE-4177)
- Don't try to resolve Squid on the CE (SOFTWARE-4362)
- Ignore all fetch-crl errors, but warn if no CRLs exist (SOFTWARE-4364)

* Mon Sep 14 2020 Mátyás Selmeci <matyas@cs.wisc.edu> 3.10.0-1
- Convert entirely to Python 3 and drop Python 2 support  (SOFTWARE-4191)

* Thu Sep 03 2020 Mátyás Selmeci <matyas@cs.wisc.edu> 3.1.2.1-1
- Python 3 / RHEL 8 support (SOFTWARE-4191)

* Wed Jan 29 2020 Mátyás Selmeci <matyas@cs.wisc.edu> 3.1.1-1
- Relax hostname validation in 40-siteinfo.ini (failing to resolve is now a warning) (SOFTWARE-3953)
- No longer make resource_group mandatory for CEs in 40-siteinfo.ini (SOFTWARE-3949)

* Fri Sep 13 2019 Brian Lin <blin@cs.wisc.edu> 3.1.0-1
- Add support for bosco_cluster overrides (SOFTWARE-3818)

* Wed Aug 28 2019 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-1
- New version 3.0.0 (SOFTWARE-3789)

* Wed Aug 21 2019 Mátyás Selmeci <matyas@cs.wisc.edu> 2.99.0-0.4
- Prerelease for 3.0.0 (SOFTWARE-3789)

* Wed Jul 10 2019 Mátyás Selmeci <matyas@cs.wisc.edu> 2.4.0-1
- Stop checking sponsor field in site information (SOFTWARE-3722)
- Don't change batch system from slurm to pbs (SOFTWARE-3717)
- Add option to configure blahp for PBS Pro (SOFTWARE-3674)
- Stop osg-configure when a bad attribute is found (SOFTWARE-3581)
- Own a section of the SSH config for bosco (SOFTWARE-3630)

* Mon Jun 25 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 2.3.1-1
- Replace info about GOC/OIM in 40-siteinfo.ini comments (SOFTWARE-3297)
- More thoroughly disable WN proxy renewal in BLAHP config (SOFTWARE-3161)

* Thu Apr 26 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 2.3.0-1
- Drop configuration for RSV gratia-consumer (SOFTWARE-3218)

* Fri Apr 06 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 2.2.4-1
- Improve comment for app_dir in 10-storage.ini (SOFTWARE-3150)
- Handle exception caused by parse error (SOFTWARE-2310)
- Don't require CE site information for non-CEs (SOFTWARE-3094)
- Warn on long-deprecated "site information/site_name" attribute (SOFTWARE-3093)
- Remove functions used for condor-python < 8.4 (SOFTWARE-3126)
- Don't make /etc/condor-ce/config.d/50-osg-configure.conf without condor-ce (SOFTWARE-3160)
- Validate environment variables in 40-localsettings.ini (SOFTWARE-3131)
- Rename siteattributes.py to siteinformation.py

* Tue Dec 12 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.2.3-1
- Replace dummy packages with obsoletes (SOFTWARE-3020)
- Drop el5-isms (SOFTWARE-3050)
- Put site info config into a separate module so osg-configure-gratia can require it (SOFTWARE-3018)
- Remove remaining TWiki references (SOFTWARE-3036)

* Tue Oct 17 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.2.2-1
- Add option to evaluate all FQANs with vomsmap auth (SOFTWARE-2932)
- Tweak comments in 10-misc.ini (SOFTWARE-2941)

* Fri Sep 22 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.2.1-1
- Don't use condor_config_val -expand (SOFTWARE-2902)
- Handle missing fetch_crl (SOFTWARE-2891)

* Wed Aug 16 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.2.0-1
- Improve logging code (SOFTWARE-2744)
- Remove GRAM code (SOFTWARE-2822)

* Wed Jul 19 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.1.1-1
- Fix logging in ensure_valid_user_vo_file (SOFTWARE-2819)
- Configure GUMS before running gums-host-cron (SOFTWARE-2792)
- Fix missing warnings in -v (SOFTWARE-2772)
- Remove unused test configs (SOFTWARE-2701)
- Make exception usage consistent (SOFTWARE-2700)

* Tue Jul 11 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.1.0-3
- Add OSG_CONFIGURE_PRESENT sentinel (SOFTWARE-2805)

* Tue Jun 27 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.1.0-2
- Use GUMS JSON interface (SOFTWARE-2482)
- Drop fix-host-port-test.patch (upstream)

* Thu Jun 22 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.0-4
- Only bring in condor-python with osg-configure-infoservices (SOFTWARE-2757)

* Fri Jun 02 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.0-3
- Add fix-host-port-test.patch

* Tue May 30 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.0-2
- bump to rebuild

* Tue May 30 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.0-1
- Drop osg-cleanup support (SOFTWARE-2695)
- Drop glexec support (SOFTWARE-2697)
- Drop warning if RSV is not installed (SOFTWARE-2748)
- Drop managedfork and network config and add transitional dummy packages (SOFTWARE-2705)
- Deprecate GUMS support (SOFTWARE-2737)
- Drop GRAM support (SOFTWARE-2726)
- Drop 'configure-osg' aliases and transitional dummy packages for monalisa and cemon (SOFTWARE-2699)
