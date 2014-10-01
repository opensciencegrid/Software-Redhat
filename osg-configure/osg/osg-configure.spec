Summary: Package for configure-osg and associated scripts
Name: osg-configure
Version: 1.0.60
Release: 2%{?dist}
Source0: %{name}-%{version}.tar.gz
Patch0: ce_collectors.patch
License: Apache 2.0
Group: Grid
Prefix: %{_prefix}
BuildArch: noarch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Vendor: Suchandra Thapa <sthapa@ci.uchicago.edu>
Url: http://www.opensciencegrid.org
Provides: configure-osg

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
Requires: %name = %version-%release
Requires: %name-gateway
%description rsv
This package includes the ini file for configuring rsv using configure-osg

%package gratia
Summary: Configure-osg configuration files for gratia
Group: Grid
Provides: configure-osg-gratia
Requires: %name = %version-%release
%description gratia
This package includes the ini file for configuring gratia using configure-osg

%package gip
Summary: Configure-osg configuration files for gip
Group: Grid
Provides: configure-osg-gip
Requires: %name = %version-%release
%description gip
This package includes the ini file for configuring gip using configure-osg

%package lsf
Summary: Configure-osg configuration files for lsf
Group: Grid
Provides: configure-osg-lsf
Requires: %name = %version-%release
Requires: %name-gateway
%description lsf
This package includes the ini file for configuring lsf using configure-osg

%package pbs
Summary: Configure-osg configuration files for pbs
Group: Grid
Provides: configure-osg-pbs
Requires: %name = %version-%release
Requires: %name-gateway
%description pbs
This package includes the ini file for configuring pbs using configure-osg

%package condor
Summary: Configure-osg configuration files for condor
Group: Grid
Provides: configure-osg-condor
Requires: %name = %version-%release
Requires: %name-gateway
%description condor
This package includes the ini file for configuring condor using configure-osg

%package sge
Summary: Configure-osg configuration files for sge
Group: Grid
Provides: configure-osg-sge
Requires: %name = %version-%release
Requires: %name-gateway
%description sge
This package includes the ini file for configuring sge using configure-osg

%package monalisa
Summary: Configure-osg configuration files for monalisa
Group: Grid
Provides: configure-osg-monalisa
%description monalisa
This is an empty package created as a workaround to upgrade issues.
It may safely be removed.

%package ce
Summary: Configure-osg configuration files for CE
Group: Grid
Provides: configure-osg-ce
Requires: %name = %version-%release
Requires: %name-gateway
%description ce
This package includes the ini files for configuring a basic CE using 
configure-osg.  One of the packages for the job manager configuration also 
needs to be installed for the CE configuration.

%package misc
Summary: Configure-osg configuration files for misc software
Group: Grid
Provides: configure-osg-misc
Requires: %name = %version-%release
%description misc
This package includes the ini files for various osg software including
certificates setup and glexec

%package squid
Summary: Configure-osg configuration files for squid
Group: Grid
Provides: configure-osg-squid
Requires: %name = %version-%release
%description squid
This package includes the ini files for configuring an OSG system to use squid

%package managedfork
Summary: Configure-osg configuration files for managedfork
Group: Grid
Provides: configure-osg-managedfork
Requires: %name = %version-%release
Requires: %name-gateway
%description managedfork
This package includes the ini files for configuring an OSG CE to use
managedfork

%package network
Summary: Configure-osg configuration files for network configuration
Group: Grid
Provides: configure-osg-network
Requires: %name = %version-%release
%description network
This package includes the ini files for configuring network related information
such as firewall ports that globus should use

%package tests
Summary: Configure-osg configuration unit tests and configuration for unit testing
Group: Grid
Provides: configure-osg-tests
Requires: %name = %version-%release
%description tests
This package includes the ini files and files for unit tests that osg-configure
uses to verify functionality

%package slurm
Summary: Configure-osg configuration files for slurm
Group: Grid
Provides: configure-osg-slurm
Requires: %name = %version-%release
Requires: %name-gateway
%description slurm
This package includes the ini file for configuring slurm using configure-osg

%package infoservices
Summary: Configure-osg configuration files for the osg info services
Group: Grid
Provides: configure-osg-infoservices
Requires: %name = %version-%release
%description infoservices
This package includes the ini file for configuring the osg info services using configure-osg

%package gateway
Summary: Configure-osg configuration files for job gateways (globus-gatekeeper / htcondor-ce)
Group: Grid
Provides: configure-osg-gateway
Requires: %name = %version-%release
%description gateway
This package includes the ini file for configuring the job gateways
(globus-gatekeeper or htcondor-ce) using configure-osg

%package cemon
Summary: Transitional dummy package for OSG 3.2
Group: Grid
Provides: configure-osg-cemon
Requires: %name
%description cemon
This is an empty package created as a workaround to OSG 3.1->3.2 upgrade issues.
It may safely be removed once the upgrade is finished.


%prep
%setup
%patch0 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/condor-ce/config.d
touch $RPM_BUILD_ROOT/etc/condor-ce/config.d/50-osg-configure.conf
mkdir -p $RPM_BUILD_ROOT/var/log/osg/
touch $RPM_BUILD_ROOT/var/log/osg/osg-configure.log
mkdir -p $RPM_BUILD_ROOT/var/lib/osg
touch $RPM_BUILD_ROOT/var/lib/osg/osg-attributes.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-local-job-environment.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-job-environment.conf
touch $RPM_BUILD_ROOT/var/lib/osg/globus-firewall
mkdir -p $RPM_BUILD_ROOT/etc/profile.d/
touch $RPM_BUILD_ROOT/etc/profile.d/osg.sh
touch $RPM_BUILD_ROOT/etc/profile.d/osg.csh
# following is needed to move script to sbin directory
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mv $RPM_BUILD_ROOT/usr/bin/osg-configure $RPM_BUILD_ROOT/usr/sbin/osg-configure
ln -s /usr/sbin/osg-configure $RPM_BUILD_ROOT/usr/sbin/configure-osg
rmdir $RPM_BUILD_ROOT/usr/bin
# Remove cemon files, don't need this on OSG 3.2+
rm -f $RPM_BUILD_ROOT/%{python_sitelib}/osg_configure/configure_modules/cemon.py*
rm -fr $RPM_BUILD_ROOT/usr/share/osg-configure/tests/configs/cemon
rm -fr $RPM_BUILD_ROOT/usr/share/osg-configure/tests/test_cemon.*
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/osg/config.d/30-cemon.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%{python_sitelib}/*
/usr/sbin/*
%ghost /var/log/osg/osg-configure.log
%ghost /var/lib/osg/osg-attributes.conf
%ghost /var/lib/osg/osg-local-job-environment.conf
%ghost /var/lib/osg/osg-job-environment.conf
%ghost /etc/condor-ce/config.d/50-osg-configure.conf

%files rsv
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-rsv.ini

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
%config(noreplace) %{_sysconfdir}/osg/config.d/40-localsettings.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/40-siteinfo.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/10-storage.ini
%config(noreplace) %{_sysconfdir}/osg/grid3-locations.txt

%files misc
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/10-misc.ini

%files squid
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/01-squid.ini

%files monalisa
# This section intentionally left blank

%files managedfork
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/15-managedfork.ini

%files network
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/40-network.ini
%ghost /var/lib/osg/globus-firewall
%ghost %{_sysconfdir}/profile.d/osg.sh
%ghost %{_sysconfdir}/profile.d/osg.csh

%files infoservices
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/30-infoservices.ini

%files tests
%defattr(-,root,root)
/usr/share/osg-configure/*

%files slurm
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/20-slurm.ini

%files gateway
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/osg/config.d/10-gateway.ini

%files cemon
# This section intentionally left blank


%changelog
* Wed Oct 1 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.60-2
- Add patch to fix ce_collectors special values

* Tue Sep 30 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.60-1
- Remove SOFTWARE-1567 patch (in upstream)
- Work for Phase 1 of the HTCondor-CE Info-Services project:
    - Advertise some OSG-CE attributes in HTCondor-CE (SOFTWARE-1592)
    - Set CONDOR_VIEW_HOST in HTCondor-CE configs (SOFTWARE-1615)
- Increase core count limit in Gip configuration module (SOFTWARE-1605)
- Skip CEMon configuration of CEMon is missing

* Tue Sep 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.59-2
- Add patch to not try to mess with grid3-locations.txt if OSG_APP is UNSET (SOFTWARE-1567)

* Fri Aug 22 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.59-1
- Remove SOFTWARE-771 patch (in upstream)
- Allow unsetting OSG_APP by setting app_dir to a special 'UNSET' value (SOFTWARE-1567)

* Tue Aug 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.58-3
- Improve phrasing of warning message when OSG_JOB_CONTACT cannot be set because no batch system modules exist/are enabled (SOFTWARE-771)
- Mark the config file that gets created in /etc/condor-ce/config.d as a ghost file so it gets properly removed (SOFTWARE-1551)

* Wed Jul 30 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.58-1
- Since job environment attributes may be mapped to more than one section/option, display a list on error (SOFTWARE-1537)
- Don't require OSG_JOB_CONTACT if (a) there's no place to specify it (i.e. no jobmanager module is enabled) or (b) gram is disabled (SOFTWARE-771)
- Only set PATH if using htcondor-ce with condor (SOFTWARE-1554)

* Tue Jul 29 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.57-1
- Change error when no batch system is set to be configured into a warning (SOFTWARE-771)
- Improve error messages for missing job environment attributes (SOFTWARE-1537)
- Improve HTCondor-CE configuration for the Condor batch system (SOFTWARE-1551)
- Set PATH in osg-job-environment.conf (SOFTWARE-1554)

* Fri Jun 20 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.56-1
- Create service keys from host keys if desired (SOFTWARE-422)
- Fix bug in detection of installed Gratia probes (SOFTWARE-1518)

* Fri May 30 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.55-2
- Fix typo in 20-config.ini (SOFTWARE-1475)

* Thu May 22 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.55-1
- New version 1.0.55 (SOFTWARE-1482) with these changes:
-   Fix warnings when adding wlcg_* attributes to the [Site Information] section (SOFTWARE-1486)
-   Add setting for SGE configuration location (SOFTWARE-1481)
-   Fix path for SGE Gratia ProbeConfig file (SOFTWARE-1479)
-   Improve error message when condor_location is set wrong (SOFTWARE-1475)
-   Support one site with multiple CE types on different hosts (SOFTWARE-1471)
-   Remove monalisa module (SOFTWARE-1465)

* Mon May 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.54-3
- Create dummy osg-configure-cemon subpackage on el6 too (SOFTWARE-1468)
- Remove the obsoletes line for osg-configure-cemon.

* Mon May 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.54-2
- Added an obsoletes for osg-configure-cemon (SOFTWARE-1468)
- Also added a dummy osg-configure-cemon subpackage because the obsoletes doesn't work properly on el5

* Fri May 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.54-1
- Rename 'htcondor_ce_gateway_enabled' to 'htcondor_gateway_enabled' (SOFTWARE-1446)

* Thu May 01 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.53-1
- Rename 10-ce.ini to 10-gateway.ini and place it in a separate subpackage
- Fix semantics of listing enabled gateway services

* Wed Apr 23 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.52-1
- Ignore some fetch-crl errors the user has no control over (SOFTWARE-1428)
- Add run-osg-configure-tests script to run all the unit tests (SOFTWARE-710)
- Improve support for configuring RSV to use HTCondor-CE; add 10-ce.ini to
  choose between GRAM and HTCondor-CE (SOFTWARE-1446)

* Mon Feb 24 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.0.51-1
- Info-services fixes, unit tests and new config file 30-infoservices.ini (SOFTWARE-1276)

* Mon Feb 03 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.50-1
- Error in listing enabled services 

* Mon Jan 28 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.49-1
- Fix unit test reliance on cemon config test files

* Mon Jan 28 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.48-1
- Add support for osg infoservice
- Better checks in  gratia condor probe

* Thu Oct 24 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.47-1
- Fix for hostname identification on CentOS 6
- Fixes for bugs in condor-cron id fixes

* Thu Oct 17 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.46-1
- Allow sge binary location to be specified
- Give better error messages when options are missing
- Add requires in sub-rpms for osg-configure main rpm
- Check and fix condor-cron ids for RSV

* Wed Sep 16 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.45-1
- Update unit tests for http proxy validation

* Wed Sep 16 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.44-1
- Change http proxy validation per dicussions with Brian and Tim

* Wed Sep 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.43-1
- Fix gratia configuration errors for slurm configuration
- Update squid location checks 

* Wed Sep 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.42-1
- Fix gratia configuration errors for slurm/sge

* Wed Sep 4 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.41-1
- Added missing config files for unit tests
- Temporarily disable unit test for unused functionality

* Tue Sep 3 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.40-1
- Fix gratia condor probe configuration
- Fix breakage when variable substitution across files or bad variable
  substitution is present
- Add unit tests for above issue

* Thu Aug 29 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.39-1
- Fix squid unit test

* Thu Aug 29 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.38-1
- Add unit tests for squid location check
- Fixes for squid location check

* Fri Aug 23 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.37-1
- Unit test fixes
- Test squid location

* Mon Aug 19 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.36-1
- Multiple bug fixes
- Add Slurm gratia support

* Mon Aug 5 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.35-1
- Fix error message when ram_mb is too high

* Fri Aug 2 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.34-1
- Add unit tests for spaces in ini files

* Thu Aug 1 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.33-1
- Fixes for lines with spaces at beginning of sections in ini files
- Increase the allowed memory to 512GB per node in GIP sanity checks

* Thu Apr 25 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.30-1
- Remove duplicate and broken check for SGE log files

* Tue Apr 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.29-1
- Fix SGE unit test errors

* Tue Apr 9 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.28-1
- Fix SGE verification issue 
- Removed stray character in 20-lsf.ini file

* Fri Apr 5 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.27-1
- More fixes for LSF gratia probe configuration

* Fri Mar 29 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.26-1
- Fixes for LSF gratia probe configuration

* Thu Mar 28 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.25-1
- Use log_directory for LSF instead of accounting_log_directory

* Wed Mar 27 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.24-1
- Added support for configuring gratia LSF module

* Wed Mar 19 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.23-1
- Added multiple fixes for LSF

* Wed Feb 20 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.22-1
- Added support for fetch-crl3 if present

* Mon Feb 04 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.21-1
- Added support for SLURM and unit tests for SLURM

* Thu Jan 10 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.20-1
- Multiple clean ups in unit tests
- Add --enabled-services argument to retun a list of services configured

* Tue Dec 04 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.19-1
- Fix localsettings configuration (add getAttributes back)
- Fix gratia unit tests due to change in test configs
- Clean up unit test code based on pylint output

* Tue Dec 04 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.18-1
- Don't configure metric probe in gratia test configs

* Tue Dec 04 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.17-1
- Fix for SOFTWARE-859 / GOC-12974 
- Multiple cleanups and fixes based on pylint analysis

* Thu Nov 15 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.16-1
- Fixes for software-811, software-834 
- Code cleanups based on pylint

* Thu Aug 08 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.15-1
- Update tests for storage
- Incorporate SGE fixes
- Add support for sites without OSG_DATA or which dynamically set OSG_WN_TMP
- Fix various bugs reported by Patrick @ UTA

* Thu Jun 14 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.14-1
- Update tests and fix some minor bugs

* Thu Jun 14 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.13-1
- Fix network state file checking
- Update logging in unit tests

* Fri Jun 8 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.12-1
- Include a few test related changes that were accidentally left out of the
  previous release

* Fri Jun 8 2012 Suchandra Thapa <sthapa@ci.uchicago.edu>  1.0.11-1
- Allow WN_TMP to be left blank
- Don't require globus port state files to be present
- Updates to test packaging and cleanups

* Mon Jun 4 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.10-1
- Don't try to get rsv user uid, gid in __init__

* Fri Jun 1 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.8-1
- Multiple fixes

* Wed May 2 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.8-1
- Fix for SOFTWARE-597
- Fix for SOFTWARE-599 
- Added tests subpackage to distribute tests
- Added fixes for gip configuration issue Alain ran into

* Mon Apr 23 2012 Alain Roy <roy@cs.wisc.edu> 1.0.7-2
- Patched to fix SOFTWARE-637 (incorrectly setting accounting dir for PBS)
- Added proper setup for Gratia Metric probe -SWK
- Added new RSV option - legacy_proxy -SWK

* Wed Mar 14 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.7-1
- Fix for Software-552
- Implemented Software-568
- Fixes and changes suggested by Alain
- Unit test updates

* Wed Feb 29 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.6-1
- Add support for configuring gratia condor and pbs probes
- Fix missing newline in message when -d is used

* Thu Feb 23 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.5-1
- Cleaned up pbs and lsf config scripts to remove unused home settings
- Removed itb entries from cemon ini file
- Fixed gip errors when on a standalone RSV install

* Tue Feb 21 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.4-1
- Fixed a bug in RSV configuration that prevented the use of user proxies.

* Fri Jan 27 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.3-1
- Minor tweak to let configuration continue if grid3-locations isn't present
- Remove seg_enabled option from condor jobmanager section, it's not used or
  supported by globus condor lrm

* Fri Jan 20 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.2-1
- Minor bug fix for condor_location knob in 30-rsv.ini

* Fri Jan 20 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.1-1
- Added condor_location knob for RSV to specify non-standard installs.

* Tue Jan 17 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.0.0-1
- Added support for network/firewall configuration
- Improved error reporting 
- Bug fixes for error reporting

* Wed Jan 11 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.7.4-1
- Added configuration for osg-cleanup scripts

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
