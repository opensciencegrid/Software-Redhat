
%define _webapps /var/lib/tomcat5/webapps

Name: gratia-service
Summary: Gratia OSG accounting system
Group: Applications/System
Version: 1.11
Release: 04.pre%{?dist}
License: GPL
Group: Applications/System
URL: http://sourceforge.net/projects/gratia/

# Created by:
# svn export https://gratia.svn.sourceforge.net/svnroot/gratia/branches/dev/v1_10_rpm gratia-1.11
# tar zcf gratia-1.11.tar.gz gratia-1.11
Source0: gratia-%{version}.tar.gz


BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: java
Requires: jpackage-utils
Requires: tomcat5
Requires: emi-trustmanager-tomcat
Requires: mysql-server
Requires: vo-client-edgmkgridmap
Requires: grid-certificates
# The following requirement makes sure we get the RPM that provides this,
# and not just the JDK which happens to provide it, but not in the right spot. 
Requires: /usr/share/java/xml-commons-apis.jar

BuildRequires: java-devel
BuildRequires: jpackage-utils

%description
%{summary}

%prep
%setup -q -n gratia-%{version}


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
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/gratia-service/data
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gratia/collector
mkdir conf
tar xf target/gratia.tar -C conf
install -m 0644 conf/*.sql $RPM_BUILD_ROOT%{_datadir}/gratia/sql/
install -m 0644 conf/hibernate/* $RPM_BUILD_ROOT%{_datadir}/gratia/hibernate
install -m 0644 conf/server.xml.template $RPM_BUILD_ROOT%{_datadir}/gratia/server.xml.template
sed -i 's|@GRATIA_VERSION@|%{version}|' conf/service-configuration.properties
install -m 0600 conf/service-configuration.properties  $RPM_BUILD_ROOT%{_sysconfdir}/gratia/collector/
install -m 0644 conf/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/gratia/collector
install -m 0600 conf/{keystore,truststore} $RPM_BUILD_ROOT%{_var}/lib/gratia-service/
install -m 0755 conf/post-install.sh $RPM_BUILD_ROOT%{_datadir}/gratia/
install -m 0755 conf/install_database.sh $RPM_BUILD_ROOT%{_datadir}/gratia/
install -m 0755 conf/configure_tomcat $RPM_BUILD_ROOT%{_datadir}/gratia/
install -m 0755 conf/voms-server.sh $RPM_BUILD_ROOT%{_datadir}/gratia/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
install -m 0644 conf/voms-server.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/


# TODO: nightly cron script to update VOMS servers from vo-client

# Logs
mkdir -p $RPM_BUILD_ROOT%{_var}/log/gratia-service
touch $RPM_BUILD_ROOT%{_var}/log/gratia-service/gratia{,-rmi-servlet,-security,-administration,-registration,-reporting}.log

%files
%defattr(-,root,root,-)
%{_datadir}/gratia/sql
%{_datadir}/gratia/hibernate
%{_datadir}/gratia/post-install.sh
%{_datadir}/gratia/install_database.sh
%{_datadir}/gratia/configure_tomcat
%{_datadir}/gratia/server.xml.template
%{_datadir}/gratia/voms-server.sh
%{_sysconfdir}/cron.d/voms-server.cron
%dir %{_var}/lib/gratia-service
%{_var}/lib/tomcat5/server/lib/gratiaSecurity.jar
%attr(-,tomcat,tomcat) %{_var}/lib/gratia-service/keystore
%attr(-,tomcat,tomcat) %{_var}/lib/gratia-service/truststore
%attr(-,tomcat,tomcat) %{_var}/lib/gratia-service/data
%{_webapps}/gratia-*
%dir %{_sysconfdir}/gratia/collector
%attr(0640,root,tomcat) %config(noreplace) %{_sysconfdir}/gratia/collector/service-configuration.properties
%config(noreplace) %{_sysconfdir}/gratia/collector/log4j.properties
%attr(0750,tomcat,tomcat) %dir %{_var}/lib/tomcat5/webapps/gratia-reporting/logs
%attr(0750,tomcat,tomcat) %dir %{_var}/lib/tomcat5/webapps/gratia-reporting/WEB-INF/platform/configuration
%attr(0750,tomcat,tomcat) %dir %{_var}/log/gratia-service
%ghost %{_var}/log/gratia-service/*.log

%changelog
* Wed Mar 07 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.11.04pre 
Changed name of the directory (gratia-service) under /var/lib and /var/log
Used server.xml.template provided by Brian Bockelman
log4j is linked to gratia-*/WEB-INF/lib


