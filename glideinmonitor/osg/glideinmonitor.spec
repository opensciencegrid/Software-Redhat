# Modified SPEC file starting from the setuptools generated one
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
# Wheels packaging is possible but not recommended
# https://fedoraproject.org/wiki/PythonWheels

# File must be processed to replace 1.1 and 0.2.rc2
# Replace them manually for manual use

# Release Candidates NVR format
#%define release 0.1.rc1
# Official Release NVR format
#%define release 1

%define name glideinmonitor
%define version 1.1
%define unmangled_version %{version}
%define release 0.2.rc2

Summary: GlideinMonitor Web Server and Indexer
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
License: Fermitools Software Legal Information (Modified BSD License)
Group: Development/Libraries
#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix: %{_prefix}
BuildArch: noarch
Vendor: GlideinWMS team <glideinwms-support@fnal.gov>
Url: https://github.com/glideinWMS/glideinmonitor

Source0: %{name}-%{unmangled_version}.tar.gz
Source1: %{name}-pkgrpm-%{unmangled_version}.tar.gz

%global srcname glideinmonitor

%global config_file %{_sysconfdir}/%{srcname}
%global glideinmonitor_dir %{_sharedstatedir}/glideinmonitor
%global archive_dir %{glideinmonitor_dir}/archive
%global upload_dir %{glideinmonitor_dir}/upload
%global processing_dir %{glideinmonitor_dir}/processing
%global db_dir %{glideinmonitor_dir}/db
%global log_dir %{_localstatedir}/log/glideinmonitor
# DB defined in config file (may be local or remote)
# %global db_dir %{_localstatedir}/lib/glideinmonitor/db
# using also:
# /usr/sbin %{_sbindir} , /var/lib %{_sharedstatedir}, /usr/share %{_datadir}, cron dir, ?
%global systemddir %{_prefix}/lib/systemd/system
%global rpm_templates_dir pkg/rpm/templates


Requires: python3
# Should Flask be required or pip-installed?
#Requires: python3-flask
BuildRequires: python3-devel
%description
GlideinMonitor is a package for archiving and serving the log files written by
the Glidein of GlideinWMS (Glidein Workload Management System).

glideinmonitor-webserver
glideinmonitor-indexer


%package common
Summary:        GlideinMonitor common components
Group:          System Environment/Daemons
Requires(pre): /usr/sbin/useradd
%description common
GlideinMonitor is a package for archiving and serving the log files written by
the Glidein of GlideinWMS (Glidein Workload Management System).
This package installs common elements.

%package indexer
Summary:        GlideinMonitor Web Server, Indexer and DB
Group:          System Environment/Daemons
Requires: glideinmonitor-common = %{version}-%{release}
%description indexer
GlideinMonitor is a package for archiving and serving the log files written by
the Glidein of GlideinWMS (Glidein Workload Management System).
This package installs the indexer, that sorts and prepares the archive.

%package webserver
Summary:        GlideinMonitor Web Server, Indexer and DB
Group:          System Environment/Daemons
Requires: glideinmonitor-common = %{version}-%{release}
%description webserver
GlideinMonitor is a package for archiving and serving the log files written by
the Glidein of GlideinWMS (Glidein Workload Management System).
This package installs the webserver, that serves the log archive.

# TODO: is a db package needed?

%package monolith
Summary:        GlideinMonitor Web Server, Indexer and DB
Group:          System Environment/Daemons
#Provides:       glideinmonitor-monolith = %{version}-%{release}
#Obsoletes:      glideinmonitor-monolith < %{version}-%{release}
Requires: glideinmonitor-common = %{version}-%{release}
Requires: glideinmonitor-indexer = %{version}-%{release}
Requires: glideinmonitor-webserver = %{version}-%{release}
# Requires: glideinmonitor-db = %{version}-%{release}
%description monolith
GlideinMonitor is a package for archiving and serving the log files written by
the Glidein of GlideinWMS (Glidein Workload Management System).
This package installs all the components.


%prep

#%autosetup -n %{srcname}-%{version}
%setup -n %{name}-%{unmangled_version}
%setup -T -D -a 1


%build
%{__python3} setup.py build

#install -D bin/stashcp %{buildroot}%{_bindir}/stashcp
#install -D -m 0644 bin/caches.json %{buildroot}%{_datarootdir}/stashcache/caches.json

%install
%{__python3} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
# Glidein logs directories
install -d $RPM_BUILD_ROOT%{archive_dir}
install -d $RPM_BUILD_ROOT%{upload_dir}
install -d $RPM_BUILD_ROOT%{processing_dir}
install -d $RPM_BUILD_ROOT%{db_dir}
# Log, system startup, cron and config files
install -d $RPM_BUILD_ROOT%{glideinmonitor_dir}
install -d $RPM_BUILD_ROOT%{log_dir}
install -d $RPM_BUILD_ROOT%{systemddir}
install -m 0644 %{rpm_templates_dir}/glideinmonitor-indexer.service $RPM_BUILD_ROOT%{systemddir}/
install -m 0644 %{rpm_templates_dir}/glideinmonitor-webserver.service $RPM_BUILD_ROOT%{systemddir}/
install -m 0644 pkg/rpm/templates/glideinmonitor-indexer.timer $RPM_BUILD_ROOT%{systemddir}/
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m 0644 %{rpm_templates_dir}/initscript_functions $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 %{rpm_templates_dir}/glideinmonitor-indexer $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 %{rpm_templates_dir}/glideinmonitor-webserver $RPM_BUILD_ROOT%{_sbindir}/
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/glideinmonitor-indexer
install -d $RPM_BUILD_ROOT%{_sysconfdir}/glideinmonitor-indexer/filter.d
install -m 0644 %{rpm_templates_dir}/glideinmonitor.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 0644 %{rpm_templates_dir}/glideinmonitor-indexer.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 0644 %{rpm_templates_dir}/glideinmonitor-webserver.conf $RPM_BUILD_ROOT%{_sysconfdir}/

%pre common
# Add the "gmonitor" user and group if they do not exist
getent group gmonitor >/dev/null || groupadd -r gmonitor
getent passwd gmonitor >/dev/null || \
       useradd -r -g gmonitor -d /var/lib/glideinmonitor -c "GlideinMonitor user" -s /sbin/nologin gmonitor
# If the gmonitor user already exists make sure it is part of gmonitor group
usermod --append --groups gmonitor gmonitor >/dev/null


%post common
# this is optional, needed only if MySQL is used
pip3 install mysql-connector-python

%post indexer
# $1 = 1 - Installation
# $1 = 2 - Upgrade
# Source: http://www.ibm.com/developerworks/library/l-rpm2/
systemctl daemon-reload

%post webserver
pip3 install flask
pip3 install flask_httpauth
systemctl daemon-reload
# Protecting from failure in case it is not running/installed
#/sbin/service httpd reload > /dev/null 2>&1 || true


%preun indexer
# $1 = 0 - Action is uninstall
# $1 = 1 - Action is upgrade
if [ "$1" = "0" ] ; then
    systemctl daemon-reload
fi
#if [ "$1" = "0" ]; then
#    # Remove the symlinks if added
#    # A lot of files are generated, but rpm won't delete those
#
##    rm -rf %{glideinmonitor_dir}/*
##    rm -rf %{_localstatedir}/log/glideinmonitor/*
#fi

%preun webserver
if [ "$1" = "0" ] ; then
    systemctl daemon-reload
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files common -f INSTALLED_FILES
%defattr(-,root,root)
%attr(-, gmonitor, gmonitor) %dir %{archive_dir}
%attr(-, gmonitor, gmonitor) %dir %{upload_dir}
%attr(-, gmonitor, gmonitor) %dir %{processing_dir}
%attr(-, gmonitor, gmonitor) %dir %{db_dir}
%attr(-, gmonitor, gmonitor) %dir %{glideinmonitor_dir}
%attr(-, gmonitor, gmonitor) %dir %{log_dir}
%attr(0644, root, root) %{_sbindir}/initscript_functions
%attr(-, gmonitor, gmonitor) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/glideinmonitor.conf

%files indexer
%attr(0755, root, root) %{_sbindir}/glideinmonitor-indexer
%attr(0644, root, root) %{systemddir}/glideinmonitor-indexer.service
%attr(0644, root, root) %{systemddir}/glideinmonitor-indexer.timer
%attr(-, gmonitor, gmonitor) %dir %{_sysconfdir}/glideinmonitor-indexer
%attr(-, gmonitor, gmonitor) %dir %{_sysconfdir}/glideinmonitor-indexer/filter.d
%attr(-, gmonitor, gmonitor) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/glideinmonitor-indexer.conf

%files webserver
%attr(0755, root, root) %{_sbindir}/glideinmonitor-webserver
%attr(0644, root, root) %{systemddir}/glideinmonitor-webserver.service
%attr(-, gmonitor, gmonitor) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/glideinmonitor-webserver.conf

%files monolith
# empty, but needed to have the RPM


%changelog

