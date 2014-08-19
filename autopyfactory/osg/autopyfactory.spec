%define name autopyfactory
%define version 2.3.9
%define unmangled_version 2.3.9
%define release 1.1

Summary: autopyfactory package
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Jose Caballero <jcaballero@bnl.gov>
Requires: panda-userinterface >= 1.0-4
Requires: python-simplejson
Requires: python-pycurl
Url: https://twiki.cern.ch/twiki/bin/view/Atlas/PanDA

Patch0: build-cleanup.patch

%description
This package contains autopyfactory

%prep
%setup -n %{name}-%{unmangled_version}
%patch0 -p1

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

# add .gz extension to man files
sed -i '/\/man\/man[1-9]\/.*\.[1-9]/s/$/\.gz/' INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if id apf > /dev/null 2>&1; then
    : # do nothing
else
    /usr/sbin/useradd --comment "AutoPyFactory service account" --shell /bin/bash apf
fi 

%post
/sbin/chkconfig --add factory

# By default on install set factory off?
#/sbin/chkconfig factory off


%preun
# Stop factory before uninstalling or upgrading. 
#if [ -x /etc/init.d/factory ] ; then
#  /etc/init.d/factory stop > /dev/null 2>&1
#fi


%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc CHANGELOG INSTALL-ROOT INSTALL-USER NOTES CONFIGURATION LICENSE README
%config(noreplace) %{_sysconfdir}/apf/factory.conf
%config(noreplace) %{_sysconfdir}/apf/logsmonitor.rotate.conf
%config(noreplace) %{_sysconfdir}/apf/monitor.conf
%config(noreplace) %{_sysconfdir}/apf/proxy.conf
%config(noreplace) %{_sysconfdir}/apf/queues.conf
%config(noreplace) %{_sysconfdir}/sysconfig/factory
%config(noreplace) %{_sysconfdir}/sysconfig/proxymanager

