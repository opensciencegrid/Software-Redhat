
%define _webapps /var/lib/tomcat5/webapps

Name: gratia-service
Summary: Gratia OSG accounting system
Group: Applications/System
Version: 1.09
Release: 0.1.pre
License: GPL
Group: Applications/System
URL: http://sourceforge.net/projects/gratia/

# Created by:
# svn export http://gratia.svn.sourceforge.net/svnroot/gratia/tags/v1-09-pre4 gratia-1.09
# tar zcf gratia-1.09.tar.gz gratia-1.09
Source0: gratia-%{version}.tar.gz

# Hardcode paths to system values
Patch0: configuration_paths.patch
Patch1: post_install_script.patch
Patch2: makefile_version.patch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: java
Requires: jpackage-utils
Requires: tomcat5
Requires: emi-trustmanager-tomcat
Requires: mysql-server

BuildRequires: java-devel
BuildRequires: jpackage-utils

%description
%{summary}

%prep
%setup -q -n gratia-%{version}

%patch0 -p0
%patch1 -p0
#%patch2 -p0

%build
pushd build-scripts
sed -i 's|@GRATIA_VERSION@|%{version}|' Makefile
make
popd

%install
rm -rf $RPM_BUILD_ROOT

for i in {administration,reporting,services,soap,registration,reports,servlets};
do
mkdir -p $RPM_BUILD_ROOT%{_webapps}/gratia-$i
pushd $RPM_BUILD_ROOT%{_webapps}/gratia-$i
jar xf $OLDPWD/target/gratia-$i.war
popd
done

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/tomcat5/server/lib
install -m 0644 target/gratiaSecurity.jar $RPM_BUILD_ROOT%{_var}/lib/tomcat5/server/lib

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gratia/{sql,hibernate}
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/gratia/data
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gratia/collector
mkdir conf
tar xf target/gratia.tar -C conf
install -m 0644 conf/*.sql $RPM_BUILD_ROOT%{_datadir}/gratia/sql/
install -m 0644 conf/hibernate/* $RPM_BUILD_ROOT%{_datadir}/gratia/hibernate
sed -i 's|@GRATIA_VERSION@|%{version}|' conf/service-configuration.properties
install -m 0600 conf/service-configuration.properties  $RPM_BUILD_ROOT%{_sysconfdir}/gratia/collector/
install -m 0644 conf/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/gratia/collector
install -m 0600 conf/{keystore,truststore} $RPM_BUILD_ROOT%{_var}/lib/gratia/
install -m 0755 conf/post-install.sh $RPM_BUILD_ROOT%{_datadir}/gratia/

# TODO: nightly cron script to update VOMS servers from vo-client

# Logs
mkdir -p $RPM_BUILD_ROOT%{_var}/log/gratia
touch $RPM_BUILD_ROOT%{_var}/log/gratia/gratia{,-rmi-servlet,-security,-administration,-registration,-reporting}.log

%files
%defattr(-,root,root,-)
%{_datadir}/gratia/sql
%{_datadir}/gratia/hibernate
%{_datadir}/gratia/post-install.sh
%dir %{_var}/lib/gratia
%{_var}/lib/tomcat5/server/lib/gratiaSecurity.jar
%attr(-,tomcat,tomcat) %{_var}/lib/gratia/keystore
%attr(-,tomcat,tomcat) %{_var}/lib/gratia/truststore
%attr(-,tomcat,tomcat) %{_var}/lib/gratia/data
%{_webapps}/gratia-*
%dir %{_sysconfdir}/gratia/collector
%attr(0640,root,tomcat) %config(noreplace) %{_sysconfdir}/gratia/collector/service-configuration.properties
%config(noreplace) %{_sysconfdir}/gratia/collector/log4j.properties
%ghost %{_var}/log/gratia/*.log

