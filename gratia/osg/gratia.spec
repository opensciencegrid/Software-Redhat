Name: gratia
Summary: Gratia OSG accounting system
Group: Applications/System
#Version: 1.13.12
Version: 1.16.3
Release: 2%{?dist}
License: GPL
Group: Applications/System
URL: http://sourceforge.net/projects/gratia/
# Created by:
# svn export https://gratia.svn.sourceforge.net/svnroot/gratia/trunk gratia-1.14.0
# tar zcf gratia-1.14.0.tar.gz gratia-1.14.0
Source0: gratia-%{version}.tar.gz

%description
Gratia OSG accounting system
%package service
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Summary: Gratia OSG accounting system
Group: Applications/System
# this should be by default: Obsoletes: service 
# this should be by default: Obsoletes: service
#Provides: gratia-reporting-web = %{version}-%{release}
Obsoletes: gratia-reporting-web < 1.15.0-2
Requires: java7
Requires: jpackage-utils
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0
#Requires: jsvc 
%if 0%{?rhel} < 6
Requires: fetch-crl3
Requires: tomcat5
%define _tomcat tomcat5
%endif
%if 0%{?rhel} == 6
Requires: fetch-crl
Requires: tomcat6
%define _tomcat tomcat6
%endif

Requires: osg-version 
Requires: emi-trustmanager-tomcat
#Requires: mysql-server
Requires: vo-client-edgmkgridmap
Requires: grid-certificates
# The following requirement makes sure we get the RPM that provides this,
# and not just the JDK which happens to provide it, but not in the right spot. 
Requires: /usr/share/java/xml-commons-apis.jar

BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRequires: ant


%define _webapps /var/lib/%_tomcat/webapps


%description service
%{summary}

%prep
%setup -q -n gratia-%{version}


%build
pushd build-scripts
ant -Dgratia.release='v%{version}-%{release}' -v
popd

%install
rm -rf $RPM_BUILD_ROOT

for i in {administration,services,soap,registration,servlets};
do
echo $RPM_BUILD_ROOT%
pwd
mkdir -p $RPM_BUILD_ROOT%{_webapps}/gratia-$i
pushd $RPM_BUILD_ROOT%{_webapps}/gratia-$i
jar xf $OLDPWD/target/gratia-$i.war
%if 0%{?rhel} == 6
rm -f WEB-INF/lib/slf4j-api-1.5.8.jar WEB-INF/lib/slf4j-log4j12-1.5.8.jar WEB-INF/lib/commons-logging-1.1.1.jar WEB-INF/lib/gratia-util.jar
%endif
popd
done

%if 0%{?rhel} < 6
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%_tomcat/server/lib
install -m 0644 target/gratiaSecurity.jar $RPM_BUILD_ROOT%{_var}/lib/%_tomcat/server/lib
install -m 0644 target/gratiaSecurity.jar $RPM_BUILD_ROOT%{_var}/lib/%_tomcat/server/lib
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%_tomcat/common/classes
pushd $RPM_BUILD_ROOT%{_var}/lib/%_tomcat/common/classes
tar xf $OLDPWD/target/common_classes.tar
popd
%endif
%if 0%{?rhel} == 6
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/%_tomcat/lib
install -m 0644 target/gratiaSecurity.jar $RPM_BUILD_ROOT%{_prefix}/share/%_tomcat/lib
install -m 0644 target/gratia-util.jar $RPM_BUILD_ROOT%{_prefix}/share/%_tomcat/lib
pushd $RPM_BUILD_ROOT%{_prefix}/share/%_tomcat/lib
tar xf $OLDPWD/target/slf4j_lib.tar
popd
%endif

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gratia/{sql,hibernate}
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/gratia-service/data
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gratia/services

# --- create temporary dir for gratia.tar modules ---
#pushd %{_topdir}
rm -rf conf
mkdir conf
#tar xf %{_builddir}/target/gratia.tar -C conf
tar xf target/gratia.tar -C conf
install -m 0644 conf/*.sql $RPM_BUILD_ROOT%{_datadir}/gratia/sql/
install -m 0644 conf/hibernate/* $RPM_BUILD_ROOT%{_datadir}/gratia/hibernate
install -m 0644 conf/my-cnf-large-site.template $RPM_BUILD_ROOT%{_datadir}/gratia/my-cnf-large-site.template
install -m 0644 conf/my-cnf.template $RPM_BUILD_ROOT%{_datadir}/gratia/my-cnf.template
install -m 0644 conf/server.xml.template $RPM_BUILD_ROOT%{_datadir}/gratia/server.xml.template
install -m 0755 conf/tomcat5.jsvc.initd.template $RPM_BUILD_ROOT%{_datadir}/gratia/tomcat5.jsvc.initd.template
install -m 0755 conf/tomcat6.jsvc.initd.template $RPM_BUILD_ROOT%{_datadir}/gratia/tomcat6.jsvc.initd.template
# not needed (only reports were unauthenticated):  install -m 0644 conf/server.xml.noauth.template $RPM_BUILD_ROOT%{_datadir}/gratia/server.xml.noauth.template
install -m 0444 conf/gratia-release      $RPM_BUILD_ROOT%{_datadir}/gratia/gratia-release
# Setting NULL instead of a release because reporting has been removed
#sed -i 's|^gratia.reporting.version.*=*|gratia.reporting.version = v%{version}-%{release}|' conf/service-configuration.properties
#sed -i 's|^gratia.reporting.version.*=*|gratia.reporting.version = v%{version}-%{release}|' conf/service-authorization.properties
sed -i 's|^gratia.reporting.version.*=*|gratia.reporting.version = NULL|' conf/service-configuration.properties
sed -i 's|^gratia.reporting.version.*=*|gratia.reporting.version = NULL|' conf/service-authorization.properties
sed -i 's|^gratia.services.version.*=*|gratia.services.version = v%{version}-%{release}|'   conf/service-configuration.properties
sed -i 's|^gratia.services.version.*=*|gratia.services.version = v%{version}-%{release}|'   conf/service-authorization.properties
install -m 0600 conf/service-configuration.properties  $RPM_BUILD_ROOT%{_sysconfdir}/gratia/services/
install -m 0600 conf/service-authorization.properties  $RPM_BUILD_ROOT%{_sysconfdir}/gratia/services/
install -m 0644 conf/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/gratia/services
install -m 0600 conf/{keystore,truststore} $RPM_BUILD_ROOT%{_var}/lib/gratia-service/
install -m 0755 conf/post-install $RPM_BUILD_ROOT%{_datadir}/gratia/
install -m 0755 conf/install-database $RPM_BUILD_ROOT%{_datadir}/gratia/
install -m 0755 conf/configure_tomcat $RPM_BUILD_ROOT%{_datadir}/gratia/
install -m 0755 conf/voms-server.sh $RPM_BUILD_ROOT%{_datadir}/gratia/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
install -m 0644 conf/voms-server.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
rm -rf conf
#popd


# Logs
mkdir -p $RPM_BUILD_ROOT%{_var}/log/gratia-service
#touch $RPM_BUILD_ROOT%{_var}/log/gratia-service/gratia{,-rmi-servlet,-security,-administration,-registration,-reporting}.log
touch $RPM_BUILD_ROOT%{_var}/log/gratia-service/gratia{,-rmi-servlet,-security,-administration,-registration}.log

# We need to get rid of log4j.jar files we have done in previous version
%pre service
if [ $1 = 2 ]; then
  for d in `ls -1d %{_prefix}/share/%_tomcat/webapps/*/WEB-INF/lib`; do
        if [ -f $d/log4j.jar ]; then
                rm -f  $d/log4j.jar
        fi
  done
  %if 0%{?rhel} < 6
        if [ ! -f %{_prefix}/share/%_tomcat/common/lib/log4j.jar ]; then
                ln -s %{_prefix}/share/java/log4j.jar %{_prefix}/share/%_tomcat/common/lib/log4j.jar
        fi
  %endif

fi



%files service
%defattr(-,root,root,-)
%{_datadir}/gratia/sql
%{_datadir}/gratia/hibernate
%{_datadir}/gratia/post-install
%{_datadir}/gratia/install-database
%{_datadir}/gratia/configure_tomcat
%{_datadir}/gratia/server.xml.template
#%{_datadir}/gratia/server.xml.noauth.template
%{_datadir}/gratia/tomcat5.jsvc.initd.template
%{_datadir}/gratia/tomcat6.jsvc.initd.template
%{_datadir}/gratia/my-cnf-large-site.template
%{_datadir}/gratia/my-cnf.template
%{_datadir}/gratia/voms-server.sh
%{_datadir}/gratia/gratia-release
%{_sysconfdir}/cron.d/voms-server.cron
%dir %{_var}/lib/gratia-service
%attr(-,tomcat,tomcat) %{_var}/lib/gratia-service/keystore
%attr(-,tomcat,tomcat) %{_var}/lib/gratia-service/truststore
%attr(-,tomcat,tomcat) %{_var}/lib/gratia-service/data
%{_webapps}/gratia-*
%dir %{_sysconfdir}/gratia/services
%attr(0640,root,tomcat) %config(noreplace) %{_sysconfdir}/gratia/services/service-configuration.properties
%attr(0640,root,tomcat) %config(noreplace) %{_sysconfdir}/gratia/services/service-authorization.properties
%config(noreplace) %{_sysconfdir}/gratia/services/log4j.properties
%verify(not md5 size mtime user) %{_sysconfdir}/gratia/services/service-configuration.properties
%verify(not md5 size mtime user) %{_sysconfdir}/gratia/services/service-authorization.properties
%verify(not md5 size mtime user) %{_sysconfdir}/gratia/services/log4j.properties
%attr(0750,tomcat,tomcat) %dir %{_var}/log/gratia-service
%ghost %{_var}/log/gratia-service/*.log
%if 0%{?rhel} < 6
%{_var}/lib/%_tomcat/server/lib/gratiaSecurity.jar
%dir %{_var}/lib/%_tomcat/common/classes/net/sf/gratia/util/TidiedDailyRollingFileAppender$DatedFileFilter.class
%dir %{_var}/lib/%_tomcat/common/classes/net/sf/gratia/util/TidiedDailyRollingFileAppender.class
%endif
%if 0%{?rhel} == 6
%{_prefix}/share/%_tomcat/lib/gratiaSecurity.jar
%{_prefix}/share/%_tomcat/lib/gratia-util.jar
%{_prefix}/share/%_tomcat/lib/slf4j-api-1.5.8.jar
%{_prefix}/share/%_tomcat/lib/slf4j-log4j12-1.5.8.jar
%endif



%post service
#sed -i 's|^gratia.reporting.version.*=|gratia.reporting.version = v%{version}-%{release}\n#gratia.reporting.version=|' %{_sysconfdir}/gratia/services/service-configuration.properties
sed -i 's|^gratia.reporting.version.*=|gratia.reporting.version = NULL\n#gratia.reporting.version=|' %{_sysconfdir}/gratia/services/service-configuration.properties
sed -i 's|^gratia.services.version.*=|gratia.services.version = v%{version}-%{release}\n#gratia.services.version=|'    %{_sysconfdir}/gratia/services/service-configuration.properties
#sed -i 's|^gratia.reporting.version.*=|gratia.reporting.version = v%{version}-%{release}\n#gratia.reporting.version=|' %{_sysconfdir}/gratia/services/service-authorization.properties
sed -i 's|^gratia.reporting.version.*=|gratia.reporting.version = NULL\n#gratia.reporting.version=|' %{_sysconfdir}/gratia/services/service-authorization.properties
sed -i 's|^gratia.services.version.*=|gratia.services.version = v%{version}-%{release}\n#gratia.services.version=|'    %{_sysconfdir}/gratia/services/service-authorization.properties

if [ -d %{_sysconfdir}/gratia/collector ]
then
mv %{_sysconfdir}/gratia/services/service-authorization.properties  %{_sysconfdir}/gratia/services/service-authorization.properties.rpmnew
mv %{_sysconfdir}/gratia/collector/service-authorization.properties %{_sysconfdir}/gratia/services/service-authorization.properties
mv %{_sysconfdir}/gratia/services/service-configuration.properties  %{_sysconfdir}/gratia/services/service-configuration.properties.rpmnew
mv %{_sysconfdir}/gratia/collector/service-configuration.properties %{_sysconfdir}/gratia/services/service-configuration.properties
mv %{_sysconfdir}/gratia/services/log4j.properties  %{_sysconfdir}/gratia/services/log4j.properties.rpmnew
mv %{_sysconfdir}/gratia/collector/log4j.properties %{_sysconfdir}/gratia/services/log4j.properties
rmdir %{_sysconfdir}/gratia/collector/
# not needed echo "service.reporting.urlrewrite = false"    >> %{_sysconfdir}/gratia/services/service-configuration.properties
# not needed echo "service.reporting.permanent-redirect = " >> %{_sysconfdir}/gratia/services/service-configuration.properties
fi






%changelog
* Fri Sep 18 2015 Kevin Retzke - 1.16.3-2
- Changed primary key id generator to hilo for compatability with MySQL cluster.

* Thu Sep 17 2015 Kevin Retzke - 1.16.3
- Added primary keys to JobUsageRecord auxiliary tables (e.g. Disk, Network) and
   DatabaseMaintenance routine to migrate schema.

* Thu May 28 2015 Kevin Retzke - 1.16.2
- Patched potential vulnerabilities in Gratia service administration interface
- Fixed tomcat6.jsvc init script status, increased timeout
- Improved post-install and install-database scripts, fixed issues with remote and/or
  unprivileged database access

* Fri Oct 29 2014 Hyunwoo Kim - 1.16.1
- install-database is debugged. now letting local mysql rootuser have different name other than root

* Fri Oct 10 2014 Hyunwoo Kim - 1.16.0
- Basically equivalent to 1.15.2 which was a test version and was improved from 1.15.1. Also Marco modified DataScrubber.java

* Tue Oct 09 2014 Hyunwoo Kim - 1.15.2
- Modified install-database and post-install to handle MySQL root user, removed mysql-server dependency from gratia.spec

* Thu Sep 04 2014 Hyunwoo Kim - 1.15.1
- better install-database,post-install,service-authorization.properties,hibernate.cfg.xml to handle MySQL 5 6

* Thu Jun 12 2014 Marco Mambelli - 1.15.0-2
- added Obsoletes reporting-web to avoid upgrade conflicts

* Thu Jun 12 2014 Hyunwoo Kim - 1.15.0
- hibernate4 branch meged with trunk, hibernate4, mysql51, new install-database

* Thu Mar 06 2014 Tanya Levshina - 1.14.0
- merge with trunk Marco's branch

* Thu Feb 06 2014 Marco Mambelli <marcom@fnal.gov> - 1.14.rc0
- remove reporting

* Wed Dec 11 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.12-1.1
- revert back hibernate4 modifications because of the problem with handling duplicate records

* Wed Nov 13 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.11-1
- pre-production release:
- ant build
- fixes for Logging and Admin Interface (GRATIA-512)
- Hibernate4 upgrade

* Fri Aug 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.10-1.1
- rebuild with Java 7

* Tue May 14 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.10-1
pre-proudction release, add verify not for configuration files.
Hyunwoo fixes for SiteMgmt.java

* Tue May 07 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.13.9-7
- Require missing java dir names instead of workaround package

* Wed Mar 27 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.13.9-6
- Merge fetch-crl changes into upcoming

* Tue Mar 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.13.9-5
- Workaround: Require missing-java-1.7.0-dirs in el5

* Tue Mar 05 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.9-4
fetch-crl3 is required for sl5

* Mon Mar 04 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.9-3
added fetch-crl, fetch-crl3 dependencies 

* Tue Feb 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.13.9-2
- Updates to build with OpenJDK 7; require java7-devel + jpackage-utils

* Mon Feb 11 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.9-1
Merged fermi branch and trunk; Changed version to 1.13.9 and rpm package to 1, according to OSG ST reqs

* Mon Feb 11 2013 Hyunwoo Kim <hyunwoo@fnal.gov> - 1.13.9
a bug fix in this spec file, new lines in post section to deal with /etc/gratia/collector in old version

* Mon Jan 14 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.8
minor fixes, replace staticReports.py with staticReports

* Fri Jan 11 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.7
added StaticReports and cronjob templated, modified jsvc startup script for sl5

* Fri Jan 04 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.6
added jsvc startup scripts, modified configure_tomcat

* Tue Dec 04 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.13.6pre
Added url redirection filter 

* Wed Nov 14 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.13.5
Added osg-version to spec requirements 

* Mon Nov 12 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.13.4
Fix post-install script for the case when root password is not set for mysql database 

* Thu Aug 09 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.13.3
Added check for ProjectName not being null in NewProjectNameUpdate.java

* Wed Aug 01 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.13.2
Modification in that allow to retreat ProjectName without adding Project Description in NewProjectNameUpdate.java
This prevented correct summarization of records with ProjectNameDescriptions

* Thu Jul 12 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.13.1pre
ProjectName implementation , see https://jira.opensciencegrid.org/browse/GRATIA-59

* Thu Jul 05 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.11
production release, second attempt - fixed tomcat_configure again

* Mon Jul 03 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.10
production release

* Mon Jul 02 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.10pre
fixes for configure-tomcat, voms-server.cron and gratia-service.spec

* Thu Jun 28 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.9pre
modification in configure_tomact, install_database, fixed data directory location

e Mon Jun 25 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.8
* Mon Jun 25 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.8
ready for osg-test repo

* Mon Jun 25 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.8pre
modified configure_tomcat for tomcat6 (created link to gratia-util)

* Wed Jun 20 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.7pre
fixed core calculation  https://jira.opensciencegrid.org/browse/GRATIA-65

* Fri May 04 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.4
fixed   database-install for omitted mysql port

* Wed Apr 25 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.4pre
fixed gratia.spec - get rid of tomcat5

* Wed Apr 25 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.3pre
changes in tomcat-configure for tomcat6

* Tue Apr 24 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.2
Fixed online documentation and voms-server.sh

* Fri Apr 23 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.1
Production release

* Fri Apr 20 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.0pre 
Added mysql templates, improvments for database-install

* Mon Apr 15 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.11.06pre 
Modified spec file to be able to build on sl6

* Wed Apr 04 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.11.05pre 
Separated service-configuration.properties from service-authorization.properties
Changed names and improved post-install and database-install scripts

* Wed Mar 07 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.11.04pre 
Changed name of the directory (gratia-service) under /var/lib and /var/log
Used server.xml.template provided by Brian Bockelman
log4j is linked to gratia-*/WEB-INF/lib


