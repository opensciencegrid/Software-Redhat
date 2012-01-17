
%define _noarchlib %{_exec_prefix}/lib
%define dirname gums
%define local_maven /tmp/m2-repository
%define upstream_version 1.4.0-pre1

Name: gums
Summary: Grid User Management System.  Authz for grid sites
Version: 1.4.0
Release: 0.2.pre1%{?dist}
License: Unknown
Group: System Environment/Daemons
BuildRequires: maven2
BuildRequires: java-devel
Requires: java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

## Tarball can be generated by doing the following:
## svn export https://svn.usatlas.bnl.gov/svn/privilege/tags/gums-1.4.0-pre1
Source0: %{name}-%{upstream_version}.tar.gz

Source1: gums.config.template
Source2: gums.config
Source3: gums-host-cron
Source4: gums-client-cron.cron
Source5: gums-client-cron.init


# Binary JARs not available from public maven repos.  To be eliminated, one-by-one.
Source6:  glite-security-trustmanager-1.8.16.jar
Source7:  glite-security-util-java-1.4.0.jar
Source8:  jta-1.0.1B.jar
Source9:  jacc-1.0.jar
#Source10: xml-apis-2.9.1.jar
#Source11: xercesImpl-2.9.1.jar
Source12: opensaml-2.2.2.jar
Source13: privilege-xacml-2.2.4.jar
Source14: privilege-1.0.1.3.jar
Source15: xmltooling-1.1.1.jar
Source16: xmltooling.pom 

Patch0: gums-build.patch
Patch1: gums-add-mysql-admin.patch
Patch2: gums-setup-mysql-database.patch
Patch3: gums-create-config.patch
#Patch4: gums-use-hostname.patch
Patch5: xml-maven2.patch
Patch6: gums-client-pom.patch

%description
%{summary}

%package client
Requires: %{name} = %{version}
Requires: osg-vo-map
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): chkconfig
Group: System Environment/Daemons
Summary: Clients for GUMS

%description client
%{summary}

%package service
Requires: %{name} = %{version}
Requires: tomcat5
Requires: emi-trustmanager-tomcat
Requires: mysql-server
Group: System Environment/Daemons
Summary: Tomcat5 service for GUMS

%description service
%{summary}

%prep

#setup -c -a 1 -a 2
%setup -n %{name}-%{upstream_version}
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch5 -p0
%patch6 -p0

%build

# Binary JARs not available from public maven repos.
# gums-core
mvn install:install-file -B -DgroupId=org.glite -DartifactId=glite-security-trustmanager -Dversion=1.8.16 -Dpackaging=jar -Dfile=%{SOURCE6} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=org.glite -DartifactId=glite-security-util-java -Dversion=1.4.0 -Dpackaging=jar -Dfile=%{SOURCE7} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=javax.transaction -DartifactId=jta -Dversion=1.0.1B -Dpackaging=jar -Dfile=%{SOURCE8} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=javax.security -DartifactId=jacc -Dversion=1.0 -Dpackaging=jar -Dfile=%{SOURCE9} -Dmaven.repo.local=%{local_maven}
# gums-client
mvn install:install-file -B -DgroupId=org.opensaml -DartifactId=xmltooling -Dversion=1.1.1 -Dpackaging=jar -DpomFile=%{SOURCE16} -Dfile=%{SOURCE15} -Dmaven.repo.local=%{local_maven}
#mvn install:install-file -DgroupId=org.opensaml -DartifactId=opensaml -Dversion=2.2.2 -Dpackaging=jar -Dfile=%{SOURCE12} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege -Dversion=1.0.1.3 -Dpackaging=jar -Dfile=%{SOURCE14} -Dmaven.repo.local=%{local_maven}
mvn install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege-xacml -Dversion=2.2.4 -Dpackaging=jar -Dfile=%{SOURCE13} -Dmaven.repo.local=%{local_maven}
#mvn install:install-file -DgroupId=org.apache.xerces -DartifactId=xercesImpl -Dversion=2.9.1 -Dpackaging=jar -Dfile=%{SOURCE11} -Dmaven.repo.local=%{local_maven}
#mvn install:install-file -DgroupId=org.apache.xerces -DartifactId=xml-apis -Dversion=2.9.1 -Dpackaging=jar -Dfile=%{SOURCE10} -Dmaven.repo.local=%{local_maven}

pushd gums-core
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd
pushd gums-client
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd
pushd gums-service
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd

%install

function replace_jar {
  rm -f $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/$1
  ln -s %{_noarchlib}/%{dirname}/$1 $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/$1
}

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

# JARs
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/endorsed
install -m 0644 gums-client/target/lib/*.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/
install -m 0644 gums-core/target/*.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/
install -m 0644 gums-client/target/lib/endorsed/*.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/endorsed/

# Service
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/
pushd $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/
jar xf $OLDPWD/gums-service/target/gums.war 
popd
rm -f $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/config/gums.config
ln -s %{_sysconfdir}/%{dirname}/gums.config $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/config

# Link the exploded WAR to gums-core JARs, instead of including a copy
replace_jar ant-1.6.3.jar
replace_jar antlr-2.7.5H3.jar
replace_jar asm-1.4.3.jar
replace_jar avalon-framework-4.1.3.jar
replace_jar axis-1.4.jar
replace_jar axis-ant-1.4.jar
replace_jar axis-jaxrpc-1.4.jar
replace_jar axis-saaj-1.4.jar
replace_jar axis-wsdl4j-1.5.1.jar
#replace_jar bcprov-ext-jdk15-1.40.jar
#replace_jar bcprov-jdk15-140.jar
replace_jar bcprov-jdk15-1.45.jar
replace_jar c3p0-0.9.1.2.jar
replace_jar cglib-2.0.2.jar
replace_jar cglib-full-2.0.2.jar
replace_jar commons-beanutils-1.7.0.jar
replace_jar commons-cli-1.2.jar
replace_jar commons-codec-1.3.jar
replace_jar commons-collections-3.2.jar
replace_jar commons-digester-1.8.jar
replace_jar commons-discovery-0.2.jar
# BNL's version of openws depends on commons-httpclient.  maven.org's doesn't.
replace_jar commons-httpclient-3.0.jar
replace_jar commons-lang-2.1.jar
replace_jar commons-logging-1.1.jar
replace_jar concurrent-1.3.4.jar
replace_jar dom4j-1.4.jar
replace_jar ehcache-1.1.jar
replace_jar glite-security-trustmanager-1.8.16.jar
replace_jar glite-security-util-java-1.4.0.jar
replace_jar gums-core-1.3.18.002.jar
replace_jar hibernate-3.0.3.jar
replace_jar jacc-1.0.jar
replace_jar jargs-1.0.jar
replace_jar jboss-cache-1.2.2.jar
replace_jar jboss-common-4.0.2.jar
replace_jar jboss-j2se-200504122039.jar
replace_jar jboss-minimal-4.0.2.jar
replace_jar jboss-system-4.0.2.jar
replace_jar jcl-over-slf4j-1.6.1.jar
replace_jar jcip-annotations-1.0.jar
replace_jar jgroups-all-2.2.8.jar
replace_jar joda-time-1.6.2.jar
replace_jar jta-1.0.1B.jar
replace_jar log4j-1.2.12.jar
#replace_jar log4j-over-slf4j-1.5.5.jar
replace_jar logkit-1.0.1.jar
replace_jar mysql-connector-java-5.1.6.jar
replace_jar not-yet-commons-ssl-0.3.9.jar
replace_jar odmg-3.0.jar
replace_jar opensaml-2.2.3.jar
replace_jar openws-1.2.2.jar
replace_jar oscache-2.1.jar
replace_jar privilege-1.0.1.3.jar
replace_jar privilege-xacml-2.2.4.jar
replace_jar proxool-0.8.3.jar
replace_jar resolver-2.9.1.jar
replace_jar serializer-2.9.1.jar
replace_jar servlet-api-2.3.jar
# gums-core and gums-service use different versions here...
#replace_jar slf4j-api-1.6.1.jar
#replace_jar slf4j-simple-1.6.1.jar
rm -f $RPM_BUILD_ROOT%{_var}/lib/tomcat5/webapps/gums/WEB-INF/lib/slf4j-jdk14-1.5.2.jar
replace_jar swarmcache-1.0RC2.jar
replace_jar velocity-1.5.jar
replace_jar webdavlib-2.0.jar
replace_jar xalan-xalan-2.7.1.jar
# No longer necessary
#replace_jar xercesImpl-2.8.0.jar
replace_jar xercesImpl-2.9.1.jar
replace_jar xml-apis-2.9.1.jar
replace_jar xmlParserAPIs-2.6.2.jar
#replace_jar xmlsec-1.4.2.jar
#replace_jar xmltooling-1.1.1.jar
replace_jar xmltooling-1.3.2-1.jar


# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 gums-client/src/main/scripts/* $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/gums-host-cron
install -m 0755 gums-service/src/main/resources/scripts/gums-setup-mysql-database $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-add-mysql-admin $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-create-config $RPM_BUILD_ROOT%{_bindir}/

# Configuration files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}
install -m 0644 gums-client/src/main/config/*  $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/
install -m 0600 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}
#install -m 0600 gums-service/src/main/config/gums.config $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}

# Templates
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/config
install -m 0644 gums-service/src/main/resources/sql/{addAdmin,setupDatabase}.mysql $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/config/
#install -m 0644 gums-service/src/main/resources/gums.config.template $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/config/

# Log directory
mkdir -p $RPM_BUILD_ROOT/var/log/%{dirname}

mkdir -p $RPM_BUILD_ROOT/var/lib/osg
cat > $RPM_BUILD_ROOT/var/lib/osg/user-vo-map << EOF
# This is an empty user-vo-map.
# Run gums-host-cron to generate a real one.
EOF

cat > $RPM_BUILD_ROOT/var/lib/osg/supported-vo-list << EOF
# This is an empty supported-vo-list.
# Run gums-host-cron to generate a real one.
EOF

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{init.d,cron.d}
mv -f %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/gums-client-cron
mv -f %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/gums-client-cron
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/init.d/gums-client-cron

%files
%defattr(-,root,root,-)
%dir %{_noarchlib}/%{dirname}
%dir %{_noarchlib}/%{dirname}/endorsed
%{_noarchlib}/%{dirname}/*.jar
%{_noarchlib}/%{dirname}/endorsed/*.jar

%files client
%defattr(-,root,root,-)
%{_bindir}/gums
%{_bindir}/gums-gridmapfile
%{_bindir}/gums-host
%{_bindir}/gums-host-cron
%{_bindir}/gums-nagios
%{_bindir}/gums-service
%{_bindir}/gums-vogridmapfile
%dir %{_sysconfdir}/%{dirname}
%config(noreplace) %{_sysconfdir}/%{dirname}/gums-client.properties
%config(noreplace) %{_sysconfdir}/%{dirname}/gums-nagios.conf
%config(noreplace) %{_sysconfdir}/%{dirname}/log4j.properties
%config(noreplace) /var/lib/osg/user-vo-map
%config(noreplace) /var/lib/osg/supported-vo-list
%dir /var/log/%{dirname}
%config(noreplace) %{_sysconfdir}/cron.d/gums-client-cron
%{_sysconfdir}/init.d/gums-client-cron

%post client
/sbin/chkconfig --add gums-client-cron

%preun client
if [ $1 -eq 0 ] ; then
    /sbin/service gums-client-cron stop >/dev/null 2>&1
    /sbin/chkconfig --del gums-client-cron
fi

%postun client
if [ "$1" -ge "1" ] ; then
    /sbin/service gums-client-cron condrestart >/dev/null 2>&1 || :
fi

%files service
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{dirname}
%attr(0600,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{dirname}/gums.config
%attr(0750,tomcat,tomcat) %dir %{_var}/lib/tomcat5/webapps/gums/WEB-INF/config
%{_var}/lib/tomcat5/webapps/gums
%{_noarchlib}/%{dirname}/sql
%{_noarchlib}/%{dirname}/config
%{_bindir}/gums-add-mysql-admin
%{_bindir}/gums-create-config
%{_bindir}/gums-setup-mysql-database

%changelog
* Tue Jan 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-0.2.pre1
- Added gums.config and gums.config.template, copied from gums 1.3.18.002

* Tue Jan 10 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-0.1.pre1
- Version bump to upstream 1.4.0-pre1; updated patches; added gums-client-pom.patch
- gums.config and gums.config.template removed until we have replacements using the new config format.

* Wed Nov 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.002-6
- Remove old copy of GUMS jar.  Remove ability to contact Archiva at BNL.

* Wed Nov 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.002-5
- Allow service to use the DNS hostname instead of DN for host mappings.  Allows glexec callouts without a hostcert for privileged user groups.
- Clean up some of the maven deps so this package can be built solely from the public maven repos; no BNL-private ones necessary.

* Sat Oct 08 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.002-4
- Add a minimal packaging of the service itself.

* Mon Aug 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.3.18.002-3
- Added init script for enabling/disabling gums-host-cron.

* Fri Jul 29 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.3.18.002-2
- Rewrite gums-host-cron to work with the RPM layout.

* Thu Jun 2 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.3.17-2
- Initial source RPM from GUMS website's binary tarball.

