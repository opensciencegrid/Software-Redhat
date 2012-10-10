%define _noarchlib %{_exec_prefix}/lib
%define dirname gums
%define local_maven /tmp/m2-repository
# Don't want to repack jars
%define __os_install_post %{nil}

Name: gums
Summary: Grid User Management System.  Authz for grid sites
Version: 1.3.18.009
Release: 7%{?dist}
License: Unknown
Group: System Environment/Daemons
%if 0%{?rhel} < 6
BuildRequires: maven2
%define tomcat tomcat5
%define mvn %{_bindir}/mvn
%endif
%if 0%{?rhel} >= 6
%define tomcat tomcat6
%define mvn %{_bindir}/mvn22
BuildRequires: maven22
BuildRequires: jdk
## explicitly requiring this because I don't want yum to pick java-1.5.0-gcj-devel
BuildRequires: java-1.6.0-sun-compat
%endif
BuildRequires: java-devel
BuildRequires: emi-trustmanager
BuildRequires: voms-api-java
BuildRequires: jglobus
# provides build-classpath
BuildRequires: jpackage-utils 
Requires: java
Requires: jglobus
Requires: voms-api-java
Requires: emi-trustmanager
Requires: emi-trustmanager-axis
# Standard RPMs from the system
# "Naive" use of slf4j doesn't appear to work
#BuildRequires: slf4j
#Requires: slf4j
BuildRequires: jakarta-commons-beanutils jakarta-commons-cli jakarta-commons-codec jakarta-commons-collections jakarta-commons-digester jakarta-commons-discovery jakarta-commons-httpclient jakarta-commons-lang jakarta-commons-logging
Requires: jakarta-commons-beanutils jakarta-commons-cli jakarta-commons-codec jakarta-commons-collections jakarta-commons-digester jakarta-commons-discovery jakarta-commons-httpclient jakarta-commons-lang jakarta-commons-logging
BuildRequires: jacc jta
Requires: jacc jta
BuildRequires: ant
Requires: ant
BuildRequires: antlr
Requires: antlr
BuildRequires: joda-time
Requires: joda-time
BuildRequires: mysql-connector-java
Requires: mysql-connector-java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

# Tarball can be generated by doing the following:
# svn export http://svn.usatlas.bnl.gov/svn/privilege/tags/gums-1.3.18.009 gums
# tar zcf gums-1.3.18.009.tar.gz gums/
Source0: %{name}-%{version}.tar.gz
Source1: gums-host-cron
Source2: gums-client-cron.cron
Source3: gums-client-cron.init

# Binary JARs not available from public maven repos.  To be eliminated, one-by-one.
#Source4: glite-security-trustmanager-2.5.5.jar
#Source5: glite-security-util-java-2.8.6.jar
Source6: jta-1.0.1B.jar
Source7: jacc-1.0.jar
Source8: privilege-xacml-2.2.4.jar
Source9: privilege-1.0.1.3.jar
Source10: xmltooling-1.1.1.jar
Source11: xmltooling.pom 
Source12: openws-1.2.2.jar
Source13: jargs-1.0.jar
Source14: velocity-1.5.jar

Patch0: xml-maven2.patch
Patch1: gums-create-config2.patch
Patch2: get-correct-client-cert.patch
Patch3: emi-trustmanager-pom.patch

%description
%{summary}

%package client
Requires: %{name} = %{version}-%{release}
Requires: osg-vo-map
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): chkconfig
Group: System Environment/Daemons
Summary: Clients for GUMS

%description client
%{summary}

%package service
Requires: %{name} = %{version}-%{release}
Requires: /usr/share/java/xml-commons-apis.jar
Requires: %{tomcat}
Requires: emi-trustmanager-tomcat
Requires: mysql-server
Requires: osg-webapp-common
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Group: System Environment/Daemons
Summary: Tomcat service for GUMS

%description service
%{summary}

%prep

%setup -n %{name}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build

# Binary JARs not available from public maven repos.
# gums-core
# Trustmanager is available from RPMs.
%{mvn} install:install-file -B -DgroupId=emi -DartifactId=emi-trustmanager -Dversion=3.0.3 -Dpackaging=jar -Dfile=`build-classpath trustmanager` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=javax.transaction -DartifactId=jta -Dversion=1.0.1B -Dpackaging=jar -Dfile=%{SOURCE6} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=javax.security -DartifactId=jacc -Dversion=1.0 -Dpackaging=jar -Dfile=%{SOURCE7} -Dmaven.repo.local=%{local_maven}
# These used to be available from the internet2 shibboleth project, but that server is now dead.
%{mvn} install:install-file -B -DgroupId=org.opensaml -DartifactId=openws -Dversion=1.2.2 -Dpackaging=jar -Dfile=%{SOURCE12} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=jargs -DartifactId=jargs -Dversion=1.0 -Dpackaging=jar -Dfile=%{SOURCE13} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=velocity -DartifactId=velocity -Dversion=1.5 -Dpackaging=jar -Dfile=%{SOURCE14} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=emi -DartifactId=voms-api-java -Dversion=2.0.8 -Dpackaging=jar -Dfile=`build-classpath voms-api-java` -Dmaven.repo.local=%{local_maven}
# gums-client
%{mvn} install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege-xacml -Dversion=2.2.4 -Dpackaging=jar -Dfile=%{SOURCE8} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege -Dversion=1.0.1.3 -Dpackaging=jar -Dfile=%{SOURCE9} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.opensaml -DartifactId=xmltooling -Dversion=1.1.1 -Dpackaging=jar -Dfile=%{SOURCE10} -DpomFile=%{SOURCE11} -Dmaven.repo.local=%{local_maven}
# Take SLF4J from the OS.
#%{mvn} install:install-file -B -DgroupId=org.slf4j -DartifactId=slf4j-simple -Dversion=1.5.5 -Dpackaging=jar -Dfile=`build-classpath slf4j/simple` -Dmaven.repo.local=%{local_maven}
#%{mvn} install:install-file -B -DgroupId=org.slf4j -DartifactId=slf4j-simple -Dversion=1.6.1 -Dpackaging=jar -Dfile=`build-classpath slf4j/simple` -Dmaven.repo.local=%{local_maven}

pushd gums-core
%{mvn} -B -e -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd
pushd gums-client
%{mvn} -B -e -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd
pushd gums-service
%{mvn} -B -e -Dmaven.repo.local=/tmp/m2-repository -Dmaven.test.skip=true install
popd

%install

function replace_jar {
    if [[ -e $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib/$1 ]]; then
        rm -f $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib/$1
        ln -s %{_noarchlib}/%{dirname}/$1 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib/$1
    fi
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
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/
pushd $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/
jar xf $OLDPWD/gums-service/target/gums.war 
popd
rm $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/config/gums.config
ln -s %{_sysconfdir}/%{dirname}/gums.config $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/config

# Hack: we want slf4j-api-1.5.5 in core, but that's not what comes with
# it. Get it from the exploded WAR instead.
install -m 0644 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib/slf4j-api-1.5.5.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/

%if 0%{?rhel} < 6
# Remove system JARs to whatever extent possible.  We will later link these directly.
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/ant-1.6.3.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/antlr-2.7.5H3.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/axis-{1.4,ant-1.4,jaxrpc-1.4,saaj-1.4}.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/bcprov-jdk15-*.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/commons-{beanutils-1.7.0,cli-1.2,codec-1.3,collections-3.2,digester-1.8,discovery-0.2,httpclient-3.0,lang-2.1,logging-1.1}.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/emi-trustmanager-3.0.3.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/joda-time-1.6.2.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/{jacc-1.0,jta-1.0.1B}.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/mysql-connector-java-5.1.6.jar
#rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/*slf4j*.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/voms-api-java-2.0.8.jar

## Link the exploded WAR to gums-core JARs, instead of including a copy
# tomcat6 doesn't seem to like this.
for x in $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/*.jar; do
    replace_jar $(basename $x)
done

%endif

## gums-core and gums-service use different versions here...
rm -f $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib/slf4j-jdk14-1.5.2.jar


# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 gums-client/src/main/scripts/* $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/gums-host-cron
install -m 0755 gums-service/src/main/resources/scripts/gums-setup-mysql-database $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-add-mysql-admin $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-create-config $RPM_BUILD_ROOT%{_bindir}/

# Configuration files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}
install -m 0644 gums-client/src/main/config/*  $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/
install -m 0600 gums-service/src/main/config/gums.config $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}

# Templates
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/config
install -m 0644 gums-service/src/main/resources/sql/{addAdmin,setupDatabase}.mysql $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql/
install -m 0644 gums-service/src/main/resources/gums.config.template $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/config/

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
mv %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/gums-client-cron
mv %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/gums-client-cron
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/init.d/gums-client-cron

mkdir -p $RPM_BUILD_ROOT%{_javadir}
touch $RPM_BUILD_ROOT%{_javadir}/javamail.jar

# jglobus is required by XACML callouts in gums-client, but not gums-core.
build-jar-repository $RPM_BUILD_ROOT%{_noarchlib}/%{dirname} jglobus trustmanager trustmanager-axis ant antlr axis bcprov commons-cli commons-codec commons-collections commons-digester commons-discovery commons-httpclient commons-lang commons-logging jacc jta voms-api-java joda-time mysql-connector-java

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib
build-jar-repository $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib trustmanager trustmanager-axis ant antlr axis bcprov commons-beanutils commons-cli commons-codec commons-collections commons-digester commons-discovery commons-httpclient commons-lang commons-logging jacc jta voms-api-java joda-time mysql-connector-java

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
%attr(0750,tomcat,tomcat) %dir %{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/config
%{_var}/lib/%{tomcat}/webapps/gums
%{_noarchlib}/%{dirname}/sql
%{_noarchlib}/%{dirname}/config
%{_bindir}/gums-add-mysql-admin
%{_bindir}/gums-create-config
%{_bindir}/gums-setup-mysql-database
%ghost %{_javadir}/javamail.jar

%post service
%{_sbindir}/update-alternatives --install %{_javadir}/javamail.jar javamail %{_noarchlib}/%{dirname}/mail-1.4.1.jar 5000

%postun service
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove javamail %{_noarchlib}/%{dirname}/mail-1.4.1.jar
fi

%changelog
* Tue Oct 09 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.009-7
- Improve usage of system RPMs.
- Add emi-trustmanager-axis (SOFTWARE-808) into the GUMS webapp JARs.

* Thu Oct 04 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.009-6
- Switch to EMI trustmanager from glite trustmanager.
- Fix DN parsing for proxies delegated multiple times.
- Switch to jglobus2 from jglobus.
- Manually cache binary JARs which are no longer publicly available.

* Wed Jun 06 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.009-5
- Move osg-webapp-common dependency to gums-service

* Fri May 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.009-4
- Add dependency on osg-webapp-common

* Thu Apr 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.009-3
- Add cog-jglobus dependency and symlinks

* Mon Apr 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.009-2
- Add gums-create-config2.patch to fix default template path in gums-create-config

* Mon Apr 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.009-1
- Version bump
- gums-build.patch, gums-add-mysql-admin.patch,
  gums-setup-mysql-database.patch, gums-create-config.patch,
  gums-4-drs-logging.patch incorporated upstream

* Thu Apr 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.008-6
- Use jpackage maven22

* Wed Apr 11 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.008-5
- Build with the apache binary maven for EL 6 since the jpackage rpm didn't work
- Use tomcat6 for EL 6
- Disabled replace_jar in EL 6 -- tomcat6 doesn't seem to like the symlinks

* Tue Apr 10 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.008-4
- Remove some debugging messages (GUMS-4)

* Thu Mar 15 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.008-3
- bump for rebuild

* Thu Mar 08 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.008-2
- Added alternatives entry for using /usr/lib/gums/mail-1.4.1.jar as 'javamail'. This gets around "No such provider" errors in the log files.

* Wed Feb 29 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.008-1
- New version. Updated trustmanager.

* Mon Feb 20 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.006-2
- Fix for wrong version of slf4j-api in client

* Fri Feb 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.006-1
- New version.
- Build is now a multi-project

* Thu Feb 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.002-7
- Disabled jar repacking.
- Added /usr/share/java/xml-commons-apis.jar as a dependency to get around sun jdk falsely providing xml-commons-apis
- Cleaned up the way duplicate jar files are replaced with symlinks (replace_jar)

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

