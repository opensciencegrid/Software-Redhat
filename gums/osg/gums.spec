%define _noarchlib %{_exec_prefix}/lib
%define dirname gums
%define local_maven /tmp/m2-repository
# Don't want to repack jars
%define __os_install_post %{nil}
%define jglobus_version 2.0.6

%define _alphatag pre3
%define _release 5

Name: gums
Summary: Grid User Management System.  Authz for grid sites
Version: 1.4.0
Release: 0.%{_release}.%{_alphatag}%{?dist}
License: Unknown
Group: System Environment/Daemons
%if 0%{?rhel} < 6
BuildRequires: maven2
%define tomcat tomcat5
%define mvn %{_bindir}/mvn
%define jacc jacc
%endif
%if 0%{?rhel} >= 6
%define tomcat tomcat6
%define mvn %{_bindir}/mvn22
#This is probably not right, but one thing at a time
%define jacc %{nil}
BuildRequires: maven22
## explicitly requiring this because I don't want yum to pick java-1.5.0-gcj-devel
%endif
BuildRequires: java7-devel
BuildRequires: jglobus = %{jglobus_version}
# provides build-classpath
BuildRequires: jpackage-utils 
Requires: java7
Requires: jpackage-utils 
Requires: jglobus = %{jglobus_version}
BuildRequires: voms-api-java
Requires: voms-api-java
BuildRequires: emi-trustmanager
Requires: emi-trustmanager
BuildRequires: emi-trustmanager-axis
Requires: emi-trustmanager-axis
# Standard RPMs from the system
# "Naive" use of slf4j doesn't appear to work
#BuildRequires: slf4j
#Requires: slf4j
BuildRequires: jakarta-commons-beanutils jakarta-commons-cli jakarta-commons-codec jakarta-commons-collections jakarta-commons-digester jakarta-commons-discovery jakarta-commons-httpclient jakarta-commons-lang jakarta-commons-logging
Requires: jakarta-commons-beanutils jakarta-commons-cli jakarta-commons-codec jakarta-commons-collections jakarta-commons-digester jakarta-commons-discovery jakarta-commons-httpclient jakarta-commons-lang jakarta-commons-logging
BuildRequires: jacc jta
Requires: jacc jta
#RHEL5 version of axis is too old
#BuildRequires: axis
#Requires: axis
BuildRequires: ant
Requires: ant
BuildRequires: antlr
Requires: antlr
BuildRequires: joda-time
Requires: joda-time
BuildRequires: mysql-connector-java
Requires: mysql-connector-java
BuildRequires: xerces-j2 xalan-j2 log4j
Requires: xerces-j2 xalan-j2 log4j
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0
BuildRequires: privilege-xacml
Requires: privilege-xacml

# Tarball can be generated by doing the following:
# svn export http://svn.usatlas.bnl.gov/svn/privilege/tags/gums-1.3.18.009 gums
# tar zcf gums-1.3.18.009.tar.gz gums/

# For git-based releases, one can do:
# git archive --format=tar --prefix=gums-1.4.0.pre1/ v1.4.0.pre1 | gzip > gums-1.4.0.pre1.tar.gz
#
Source0: %{name}-%{version}.%{_alphatag}.tar.gz
Source1: gums-host-cron
Source2: gums-client-cron.cron
Source3: gums-client-cron.init
Source4: log4j-client.properties
Source5: log4j-service.properties

# Binary JARs not available from public maven repos.  To be eliminated, one-by-one.
#Source4: glite-security-trustmanager-2.5.5.jar
#Source5: glite-security-util-java-2.8.6.jar
Source6: jta-1.0.1B.jar
Source7: jacc-1.0.jar
Source9: privilege-1.0.1.3.jar
Source10: xmltooling-1.1.1.jar
Source11: xmltooling.pom 
Source12: openws-1.2.2.jar
Source13: jargs-1.0.jar
Source14: velocity-1.5.jar

Patch0: gums-add-mysql-admin.patch

%description
%{summary}

%package client
Requires: osg-vo-map
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(postun): chkconfig
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0
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
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0
Group: System Environment/Daemons
Summary: Tomcat service for GUMS

%description service
%{summary}

%prep

%setup -n %{name}-%{version}.%{_alphatag}
%patch0 -p1

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
%{mvn} install:install-file -B -DgroupId=org.italiangrid -DartifactId=voms-api-java -Dversion=2.0.8 -Dpackaging=jar -Dfile=`build-classpath voms-api-java` -Dmaven.repo.local=%{local_maven}
# gums-client
%{mvn} install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege -Dversion=1.0.1.3 -Dpackaging=jar -Dfile=%{SOURCE9} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.opensaml -DartifactId=xmltooling -Dversion=1.1.1 -Dpackaging=jar -Dfile=%{SOURCE10} -DpomFile=%{SOURCE11} -Dmaven.repo.local=%{local_maven}
# Take SLF4J from the OS.
#%{mvn} install:install-file -B -DgroupId=org.slf4j -DartifactId=slf4j-simple -Dversion=1.5.5 -Dpackaging=jar -Dfile=`build-classpath slf4j/simple` -Dmaven.repo.local=%{local_maven}
#%{mvn} install:install-file -B -DgroupId=org.slf4j -DartifactId=slf4j-simple -Dversion=1.6.1 -Dpackaging=jar -Dfile=`build-classpath slf4j/simple` -Dmaven.repo.local=%{local_maven}

# Adding system dependencies
%{mvn} install:install-file -B -DgroupId=org.apache.xerces -DartifactId=xercesImpl -Dversion=2.10.0 -Dpackaging=jar -Dfile=`build-classpath xerces-j2` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.apache.xalan -DartifactId=xalan -Dversion=2.7.1 -Dpackaging=jar -Dfile=`build-classpath xalan-j2` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=log4j -DartifactId=log4j -Dversion=1.2.12 -Dpackaging=jar -Dfile=`build-classpath log4j` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.opensciencegrid -DartifactId=privilege-xacml -Dversion=2.6.2 -Dpackaging=jar -Dfile=`build-classpath privilege-xacml` -Dmaven.repo.local=%{local_maven}

# Add jglobus system deps
%{mvn} install:install-file -B -DgroupId=jglobus -DartifactId=gridftp -Dversion=%{jglobus_version} -Dpackaging=jar -Dfile=`build-classpath jglobus/gridftp-%{jglobus_version}` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=jglobus -DartifactId=gss -Dversion=%{jglobus_version} -Dpackaging=jar -Dfile=`build-classpath jglobus/gss-%{jglobus_version}` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=jglobus -DartifactId=io -Dversion=%{jglobus_version} -Dpackaging=jar -Dfile=`build-classpath jglobus/io-%{jglobus_version}` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=jglobus -DartifactId=jsse -Dversion=%{jglobus_version} -Dpackaging=jar -Dfile=`build-classpath jglobus/jsse-%{jglobus_version}` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=jglobus -DartifactId=ssl-proxies -Dversion=%{jglobus_version} -Dpackaging=jar -Dfile=`build-classpath jglobus/ssl-proxies-%{jglobus_version}` -Dmaven.repo.local=%{local_maven}


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

# Remove system JARs to whatever extent possible.  We will later link these directly.
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/ant-1.6.3.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/antlr-2.7.5H3.jar
#rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/axis-{1.4,ant-1.4,jaxrpc-1.4,saaj-1.4}.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/bcprov-jdk15-*.jar
rm -f {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/commons-{beanutils-1.7.0,cli-1.2,codec-1.3,collections-3.2,digester-1.8,discovery-0.2,httpclient-3.0,lang-2.1,logging-1.1}.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/emi-trustmanager-3.0.3.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/joda-time-1.6.2.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/{jacc-1.0,jta-1.0.1B}.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/mysql-connector-java-5.1.6.jar
#rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/*slf4j*.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/xercesImpl*.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/xalan*.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/log4j*.jar
rm {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/privilege-xacml*.jar


## Link the exploded WAR to gums-core JARs, instead of including a copy
# this works because we explicitly configure tomcat6 with allowLinking="true"
for x in $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/*.jar; do
    replace_jar $(basename $x)
done


# Delete broken RPMs from the Shibboleth repository
#  (we need to fix the build so that they are not even pulled in)
rm -f {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/resolver-2.9.1.jar
rm -f {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/serializer-2.9.1.jar
rm -f {$RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib,$RPM_BUILD_ROOT%{_noarchlib}/%{dirname}}/xml-apis-2.9.1.jar
rm -f $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/endorsed/xercesImpl-2.9.1.jar
rm -f $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/endorsed/xml-apis-2.9.1.jar

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

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,cron.d}
mv %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/gums-client-cron
mv %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/gums-client-cron
chmod +x $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/gums-client-cron

mkdir -p $RPM_BUILD_ROOT%{_javadir}
touch $RPM_BUILD_ROOT%{_javadir}/javamail.jar

# jglobus is required by XACML callouts in gums-client, but not gums-core.
build-jar-repository $RPM_BUILD_ROOT%{_noarchlib}/%{dirname} jglobus trustmanager trustmanager-axis ant antlr bcprov commons-cli commons-codec commons-collections commons-digester commons-discovery commons-httpclient commons-lang commons-logging %{jacc} jta joda-time mysql-connector-java xerces-j2 xalan-j2 log4j privilege-xacml

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib
build-jar-repository $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/lib jglobus trustmanager trustmanager-axis ant antlr bcprov commons-beanutils commons-cli commons-codec commons-collections commons-digester commons-discovery commons-httpclient commons-lang commons-logging %{jacc} jta joda-time mysql-connector-java xalan-j2 xerces-j2 log4j privilege-xacml


#Fix log4j mess and replace with standard ones
rm $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/log4j.properties
rm $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/log4j.properties
rm $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/classes/log4j.properties
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/log4j.properties
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/log4j-service.properties
ln -s %{_sysconfdir}/%{dirname}/log4j-service.properties $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/classes/log4j.properties

# Add context to allow sym linking
cat > $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/META-INF/context.xml << EOL
<?xml version="1.0" encoding="UTF-8"?>
<Context path="/gums" allowLinking="true">
</Context>
EOL

%files
%defattr(-,root,root,-)
%dir %{_noarchlib}/%{dirname}
%{_noarchlib}/%{dirname}/endorsed
%{_noarchlib}/%{dirname}/*.jar

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
%{_sysconfdir}/rc.d/init.d/gums-client-cron
%{_noarchlib}/%{dirname}/gums-client-1.4.0.pre3.jar
%{_noarchlib}/%{dirname}/gums-core-1.4.0.pre3.jar
%{_noarchlib}/%{dirname}/log4j-1.2.12.jar
%{_noarchlib}/%{dirname}/log4j-over-slf4j-1.6.1.jar

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
%config(noreplace) %{_sysconfdir}/%{dirname}/log4j-service.properties
%attr(0600,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{dirname}/gums.config
%attr(0750,tomcat,tomcat) %dir %{_var}/lib/%{tomcat}/webapps/gums/WEB-INF/config
%dir %{_var}/lib/%{tomcat}/webapps/gums
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
* Tue Aug 19 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-0.5.pre3
- Symlink WEB-INF jars in gums-service to core gums jars (SOFTWARE-173)

* Tue Aug 19 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-0.4.pre3
- Remove gums-client dependency on core gums jars (SOFTWARE-173)
- Use /etc/rc.d/init.d instead of /etc/init.d

* Mon Aug 11 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-0.3.pre3
- Make gums-add-mysql-admin suitable for automated use (SOFTWARE-1577)

* Thu Jun 05 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-0.1.pre3
- NVR-sortable pre-release package versioning (SOFTWARE-1498)

* Tue Jun 03 2014 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.0.pre3-1
- Third pre-release of 1.4.0.  Adds support for simplified user banning.

* Thu May 29 2014 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.0.pre2-1
- Test second pre-release of GUMS 1.4.

* Wed May 28 2014 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.0.pre1-1
- Test pre-release of GUMS 1.4.

* Mon Mar 17 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.3.18.009-21
- Do not create duplicate admins in gums-add-mysql-admin (SOFTWARE-1425)

* Mon Sep 23 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.18.009-20
- Include missing voms-api-java symlink in EL5

* Sun Sep 22 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.18.009-19
- Extract VOMS FQAN from the client SSL connection, if present.

* Thu Sep 19 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.3.18.009-18
- Rebuild against jGlobus 2.0.6 and add versioned jGlobus dependencies

* Wed Sep 04 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.18.009-17
- Revert changes made in 1.3.18.009-15.3

* Tue Aug 27 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.18.009-16.1
- Merge changes from trunk

* Fri Aug 02 2013 Brian Lin <blin@cs.wisc.edu> - 1.3.18.009-16
- Use system dependency for jglobus

* Tue May 07 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.18.009-15.9
- Require missing java dir names instead of workaround package

* Mon Apr 08 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.18.009-15.8
- Rebuild for updated build dependency

* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.18.009-15.7
- Rebuild for updated build dependency

* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.18.009-15.6
- Rebuild for updated build dependencies

* Tue Mar 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.18.009-15.5
- Workaround: Require missing-java-1.7.0-dirs in el5

* Tue Feb 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.18.009-15.4
- Updates to build with OpenJDK 7; require java7-devel and jpackage-utils

* Tue Jan 29 2013 Doug Strain <dstrain@fnal.gov> - 1.3.18.009-15.3
- Fix for directory location of gums client log files

* Fri Jan 18 2013 Doug Strain <dstrain@fnal.gov> - 1.3.18.009-15.2
- Moved deletion of Shibboleth outside of if statement

* Thu Jan 17 2013 Doug Strain <dstrain@fnal.gov> - 1.3.18.009-15.1
- Added OSG release number
- Delete broken shibboleth RPMs (repository moved and broken)

* Wed Dec 5 2012 Doug Strain <dstrain@fnal.gov> - 1.3.18.009-15
- Eliminated the voms-api-java dependency 

* Mon Dec 3 2012 Doug Strain <dstrain@fnal.gov> - 1.3.18.009-14
- Use system dependency for log4j

* Thu Nov 29 2012 Doug Strain <dstrain@fnal.gov> - 1.3.18.009-13
- Use system dependencies for xalan and xerces jars
- Change gums to use log4j.properties in /etc/gums and fix log properties
- Allow symlinking in gums webapp

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

