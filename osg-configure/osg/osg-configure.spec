%global name osg-configure
%global version 0.5.3
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

%prep
%setup

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
# delete config files for subpackges from file list
/bin/sed "/[23]0-*/d" INSTALLED_FILES > tmp_file
mv tmp_file INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/var/log/osg/
touch $RPM_BUILD_ROOT/var/log/osg/configure-osg.log
mkdir -p $RPM_BUILD_ROOT/var/lib/osg
touch $RPM_BUILD_ROOT/var/lib/osg/osg-attributes.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-local-job-environment.conf
touch $RPM_BUILD_ROOT/var/lib/osg/osg-job-environment.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
# Need the following for builds on batlab
%{python_sitelib}/configure_osg/modules/*.pyo
%{python_sitelib}/configure_osg/configure_modules/*.pyo
%ghost /var/log/osg/configure-osg.log
%ghost /var/lib/osg/osg-attributes.conf
%ghost /var/lib/osg/osg-local-job-environment.conf
%ghost /var/lib/osg/osg-job-environment.conf
# Need the following for builds on batlab
%{python_sitelib}/configure_osg/*.pyo
%{python_sitelib}/configure_osg/modules/*.pyo
%{python_sitelib}/configure_osg/configure_modules/*.pyo
%config(noreplace) %{_sysconfdir}/osg/config.d/0*.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/1*.ini
%config(noreplace) %{_sysconfdir}/osg/config.d/4*.ini

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

%changelog
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
