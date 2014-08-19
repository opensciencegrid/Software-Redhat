%define name autopyfactory
%define version 2.3.9
%define unmangled_version 2.3.9
%define release 1

Summary: autopyfactory package
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Jose Caballero <jcaballero@bnl.gov>
Packager: Panda Team <hn-atlas-panda-pathena@cern.ch>
Requires: panda-userinterface >= 1.0-4 python-simplejson python-pycurl
Url: https://twiki.cern.ch/twiki/bin/view/Atlas/PanDA

%description
This package contains autopyfactory

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%pre
#!/bin/bash
#if [ -f /etc/apf/factory.conf ] ; then
#	cp -f /etc/apf/factory.conf /etc/apf/factory.conf.bak
#fi

if id apf > /dev/null 2>&1; then
	: # do nothing
else
    /usr/sbin/useradd --comment "AutoPyFactory service account" --shell /bin/bash apf
fi 

%post
#!/bin/bash
#if [ -f /etc/apf/factory.conf.bak ] ; then
#	cp -f /etc/apf/factory.conf /etc/apf/factory.conf.rpmnew
#	cp -f /etc/apf/factory.conf.bak /etc/apf/factory.conf
#fi
chmod ugo+x /etc/init.d/factory
#chmod ugo+x /usr/libexec/wrapper.sh
/sbin/chkconfig --add factory

# By default on install set factory off?
#/sbin/chkconfig factory off

#  check that factory.sysconfig has been placed in /etc/sysconfig/factory.sysconfig 
SYSCONF=/etc/sysconfig/factory.sysconfig
SYSCONFEXAMPLE=/etc/apf/factory.sysconfig-example
if [ ! -f $SYSCONF ] ; then 
        cp $SYSCONFEXAMPLE $SYSCONF
fi


# --- install the man pages, only if root  ---
gzip /usr/share/doc/apf/autopyfactory.1
mv -f /usr/share/doc/apf/autopyfactory.1.gz /usr/share/man/man1/

gzip /usr/share/doc/apf/autopyfactory-queues.conf.5
mv -f /usr/share/doc/apf/autopyfactory-queues.conf.5.gz /usr/share/man/man5/

gzip /usr/share/doc/apf/autopyfactory-factory.conf.5
mv -f /usr/share/doc/apf/autopyfactory-factory.conf.5.gz /usr/share/man/man5/ 

gzip /usr/share/doc/apf/autopyfactory-proxy.conf.5
mv -f /usr/share/doc/apf/autopyfactory-proxy.conf.5.gz /usr/share/man/man5/ 

gzip /usr/share/doc/apf/autopyfactory-monitor.conf.5
mv -f /usr/share/doc/apf/autopyfactory-monitor.conf.5.gz /usr/share/man/man5/  


%preun
#!/bin/bash
# 
# Stop factory before uninstalling or upgrading. 
#if [ -x /etc/init.d/factory ] ; then
#  /etc/init.d/factory stop > /dev/null 2>&1
#fi


%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc CHANGELOG INSTALL-ROOT INSTALL-USER NOTES CONFIGURATION LICENSE README
