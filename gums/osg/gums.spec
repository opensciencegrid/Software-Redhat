%define _noarchlib %{_exec_prefix}/lib
%define gumsdirname gums
%define gumslibdir %{_noarchlib}/%{gumsdirname}
%define webinfdir %{_var}/lib/%{tomcat}/webapps/gums/WEB-INF

%define local_maven /tmp/m2-repository
# Don't want to repack jars
%define __os_install_post %{nil}
%define jglobus_version 2.1.0
%define privilege_xacml_version 2.6.5
%define mvnopts --batch-mode -Dmaven.repo.local="%{local_maven}"

Name: gums
Summary: Grid User Management System.  Authz for grid sites
Version: 1.5.1
Release: 5%{?dist}
License: Unknown
Group: System Environment/Daemons
URL: https://github.com/opensciencegrid/gums


#This is probably not right, but one thing at a time
%define jacc %{nil}

%if 0%{?rhel} <= 5
BuildRequires: maven2
%define tomcat tomcat5
%define mvn %{_bindir}/mvn
%define commons_codec jakarta-commons-codec
%define commons_digester jakarta-commons-digester
%endif

%if 0%{?rhel} == 6
BuildRequires: maven22
%define tomcat tomcat6
%define mvn %{_bindir}/mvn22
%define commons_codec jakarta-commons-codec
%define commons_digester jakarta-commons-digester
%endif

%if 0%{?rhel} >= 7
BuildRequires: maven >= 3.0.0
%define tomcat tomcat
%define mvn %{_bindir}/mvn
%define commons_codec apache-commons-codec
%define commons_digester apache-commons-digester
%define bouncycastle_version 1.50
BuildRequires: bouncycastle = %{bouncycastle_version}
Requires: bouncycastle = %{bouncycastle_version}
BuildRequires: bouncycastle-pkix = %{bouncycastle_version}
Requires: bouncycastle-pkix = %{bouncycastle_version}
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

%if 0%{?rhel} >= 7
BuildRequires: emi-trustmanager >= 3.0.3-9
Requires: emi-trustmanager >= 3.0.3-9
%else
BuildRequires: emi-trustmanager >= 3.0.3-6
Requires: emi-trustmanager >= 3.0.3-6
%endif

BuildRequires: emi-trustmanager-axis
Requires: emi-trustmanager-axis

# Standard RPMs from the system
# "Naive" use of slf4j doesn't appear to work
#BuildRequires: slf4j
#Requires: slf4j
BuildRequires: jakarta-commons-beanutils jakarta-commons-cli %commons_codec jakarta-commons-collections %commons_digester jakarta-commons-discovery jakarta-commons-httpclient jakarta-commons-lang jakarta-commons-logging
Requires:      jakarta-commons-beanutils jakarta-commons-cli %commons_codec jakarta-commons-collections %commons_digester jakarta-commons-discovery jakarta-commons-httpclient jakarta-commons-lang jakarta-commons-logging
#BuildRequires: jacc jta
#Requires: jacc jta
#Requires: /usr/share/java/jacc.jar
#BuildRequires: /usr/share/java/jacc.jar
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
BuildRequires: privilege-xacml >= %privilege_xacml_version
Requires: privilege-xacml >= %privilege_xacml_version

Source0: %{name}-%{version}.tar.gz
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

# Can't get el5 build working with jsp precompile
Patch0: undo-jsp-precompile.patch

Patch1: EL7-Remove-TYPE-InnoDB-from-SQL-templates.patch

Patch2: Use-bouncycastle-1.50.patch
Patch3: Use-jspc-compiler-for-tomcat7.patch

Patch4: gums-client-UsrMove.patch

%description
%{summary}

%package client
Requires: %{name} = %{version}-%{release}
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
%if 0%{rhel} >= 7
Requires: emi-trustmanager-tomcat >= 3.0.0-14
Requires: mariadb-server
%else
Requires: emi-trustmanager-tomcat
Requires: mysql-server
%endif
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

%setup -n %{name}-%{version}

%patch4 -p1
%if 0%{?rhel} < 6
%patch0 -p1
%endif
%if 0%{?rhel} >= 7
%patch1 -p1
%patch2 -p1
%patch3 -p1
%endif

%build

mvn_install_file () {
    groupId=$1
    artifactId=$2
    version=$3
    file=$4
    pomFile=${5-}

    pushd /
    %mvn %mvnopts install:install-file \
        -DgroupId="$groupId" \
        -DartifactId="$artifactId" \
        -Dversion="$version" \
        -Dpackaging=jar \
        -Dfile="$file" \
        ${pomFile:+"-DpomFile=$pomFile"}
    popd
}


# Binary JARs not available from public maven repos.
# gums-core
# Trustmanager is available from RPMs.
mvn_install_file  emi               emi-trustmanager 3.0.3  `build-classpath trustmanager`
mvn_install_file  javax.transaction jta              1.0.1B %{SOURCE6}
mvn_install_file  javax.security    jacc             1.0    %{SOURCE7}

# These used to be available from the internet2 shibboleth project, but that server is now dead.
mvn_install_file  org.opensaml    openws        1.2.2 %{SOURCE12}
mvn_install_file  jargs           jargs         1.0   %{SOURCE13}
mvn_install_file  velocity        velocity      1.5   %{SOURCE14}

# gums-client
mvn_install_file  org.opensciencegrid privilege  1.0.1.3 %{SOURCE9}
mvn_install_file  org.opensaml        xmltooling 1.1.1   %{SOURCE10} %{SOURCE11}
# Take SLF4J from the OS.
#mvn_install_file  org.slf4j slf4j-simple 1.5.5 `build-classpath slf4j/simple`
#mvn_install_file  org.slf4j slf4j-simple 1.6.1 `build-classpath slf4j/simple`

mvn_install_file  org.italiangrid voms-api-java 2.0.8 `build-classpath voms-api-java`
# Adding system dependencies
mvn_install_file  org.apache.xerces   xercesImpl          2.10.0                   `build-classpath xerces-j2`
mvn_install_file  org.apache.xalan    xalan               2.7.1                    `build-classpath xalan-j2`
mvn_install_file  log4j               log4j               1.2.12                   `build-classpath log4j`
mvn_install_file  org.opensciencegrid privilege-xacml     %privilege_xacml_version `build-classpath privilege-xacml`
%if 0%{?rhel} >= 7
mvn_install_file  org.bouncycastle bcprov-jdk15on %{bouncycastle_version} `build-classpath bcprov`
%endif

# Add jglobus system deps
mvn_install_file  jglobus gridftp     %{jglobus_version} `build-classpath jglobus/gridftp-%{jglobus_version}`
mvn_install_file  jglobus gss         %{jglobus_version} `build-classpath jglobus/gss-%{jglobus_version}`
mvn_install_file  jglobus io          %{jglobus_version} `build-classpath jglobus/io-%{jglobus_version}`
mvn_install_file  jglobus jsse        %{jglobus_version} `build-classpath jglobus/jsse-%{jglobus_version}`
mvn_install_file  jglobus ssl-proxies %{jglobus_version} `build-classpath jglobus/ssl-proxies-%{jglobus_version}`


pushd gums-core
%{mvn} %{mvnopts} -e -Dmaven.test.skip=true install
popd
pushd gums-client
%{mvn} %{mvnopts} -e -Dmaven.test.skip=true install
popd
pushd gums-service
%{mvn} %{mvnopts} -e -Dmaven.test.skip=true install
popd

%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

# JARs
mkdir -p $RPM_BUILD_ROOT%{gumslibdir}
mkdir -p $RPM_BUILD_ROOT%{gumslibdir}/endorsed
install -m 0644 gums-client/target/lib/*.jar $RPM_BUILD_ROOT%{gumslibdir}/
install -m 0644 gums-core/target/*.jar $RPM_BUILD_ROOT%{gumslibdir}/
install -m 0644 gums-client/target/lib/endorsed/*.jar $RPM_BUILD_ROOT%{gumslibdir}/endorsed/

# Service
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/
pushd $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/
jar xf $OLDPWD/gums-service/target/gums.war 
popd
rm $RPM_BUILD_ROOT%{webinfdir}/config/gums.config
ln -s %{_sysconfdir}/%{gumsdirname}/gums.config $RPM_BUILD_ROOT%{webinfdir}/config

# Hack: we want slf4j-api-1.5.5 in core, but that's not what comes with
# it. Get it from the exploded WAR instead.
install -m 0644 $RPM_BUILD_ROOT%{webinfdir}/lib/slf4j-api-1.5.5.jar $RPM_BUILD_ROOT%{gumslibdir}/

%define remove_system_jars 1

%if %remove_system_jars

# Remove system JARs to whatever extent possible.  We will later link these directly.

systemjars=()
#systemjars+=(ant-1.6.3.jar)
systemjars+=(antlr-2.7.\*.jar)
#systemjars+=(axis-{1.4,ant-1.4,jaxrpc-1.4,saaj-1.4}.jar)
systemjars+=(bcprov-jdk15\*.jar)
systemjars+=(commons-{beanutils-1.7.0,cli-1.2,codec-1.3,collections-3.2,digester-1.8,discovery-0.2,httpclient-3.0,lang-2.1,logging-1.1}.jar)
systemjars+=(emi-trustmanager-3.0.3.jar)
systemjars+=(jacc-1.0.jar)
systemjars+=(joda-time-1.6.2.jar)
systemjars+=(jta-1.0.1B.jar)
systemjars+=(log4j\*.jar)
systemjars+=(mysql-connector-java-5.1.6.jar)
systemjars+=(privilege-xacml\*.jar)
#systemjars+=(\*slf4j\*.jar)
systemjars+=(xalan\*.jar)
systemjars+=(xercesImpl\*.jar)

for libdir in  %{webinfdir}/lib  %{gumslibdir}; do
    for systemjar in "${systemjars[@]}"; do
        eval rm -f "$RPM_BUILD_ROOT$libdir/$systemjar"
    done
done



## Link the exploded WAR to gums-core JARs, instead of including a copy
for jarpath in $RPM_BUILD_ROOT%{gumslibdir}/*.jar; do
    jarfile=$(basename $jarpath)
    if [[ -e $RPM_BUILD_ROOT%{webinfdir}/lib/$jarfile ]]; then
        rm -f $RPM_BUILD_ROOT%{webinfdir}/lib/$jarfile
        ln -s %{gumslibdir}/$jarfile $RPM_BUILD_ROOT%{webinfdir}/lib/$jarfile
    fi
done

%endif

# Delete broken RPMs from the Shibboleth repository
#  (we need to fix the build so that they are not even pulled in)
rm -f {$RPM_BUILD_ROOT%{webinfdir}/lib,$RPM_BUILD_ROOT%{gumslibdir}}/resolver-2.9.1.jar
rm -f {$RPM_BUILD_ROOT%{webinfdir}/lib,$RPM_BUILD_ROOT%{gumslibdir}}/serializer-2.9.1.jar
rm -f {$RPM_BUILD_ROOT%{webinfdir}/lib,$RPM_BUILD_ROOT%{gumslibdir}}/xml-apis-2.9.1.jar
rm -f $RPM_BUILD_ROOT%{gumslibdir}/endorsed/xercesImpl-2.9.1.jar
rm -f $RPM_BUILD_ROOT%{gumslibdir}/endorsed/xml-apis-2.9.1.jar

## gums-core and gums-service use different versions here...
rm -f $RPM_BUILD_ROOT%{webinfdir}/lib/slf4j-jdk14-1.5.2.jar


# Scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 gums-client/src/main/scripts/* $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/gums-host-cron
install -m 0755 gums-service/src/main/resources/scripts/gums-setup-mysql-database $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-add-mysql-admin $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 gums-service/src/main/resources/scripts/gums-create-config $RPM_BUILD_ROOT%{_bindir}/

# Configuration files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{gumsdirname}
install -m 0644 gums-client/src/main/config/*  $RPM_BUILD_ROOT%{_sysconfdir}/%{gumsdirname}/
install -m 0600 gums-service/src/main/config/gums.config $RPM_BUILD_ROOT%{_sysconfdir}/%{gumsdirname}

# Templates
mkdir -p $RPM_BUILD_ROOT%{gumslibdir}/sql
mkdir -p $RPM_BUILD_ROOT%{gumslibdir}/config
install -m 0644 gums-service/src/main/resources/sql/{addAdmin,setupDatabase}.mysql $RPM_BUILD_ROOT%{gumslibdir}/sql/
install -m 0644 gums-service/src/main/resources/gums.config.template $RPM_BUILD_ROOT%{gumslibdir}/config/

# Log directory
mkdir -p $RPM_BUILD_ROOT/var/log/%{gumsdirname}

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
packages=()
packages+=(ant)
packages+=(antlr)
packages+=(bcprov)
%if 0%{?rhel} >= 7
packages+=(bcpkix)
%endif
packages+=(commons-{beanutils,cli,codec,collections,digester,discovery,httpclient,lang,logging})
packages+=(%{jacc})
packages+=(jglobus)
packages+=(jta)
packages+=(joda-time)
packages+=(log4j)
packages+=(mysql-connector-java)
packages+=(privilege-xacml)
packages+=(trustmanager)
packages+=(trustmanager-axis)
packages+=(xalan-j2)
packages+=(xerces-j2)
%if 0%{?rhel} >= 7
packages+=(xml-commons-apis)
%endif
for jardir in %{gumslibdir} %{webinfdir}/lib; do
    mkdir -p "$RPM_BUILD_ROOT$jardir"
    build-jar-repository "$RPM_BUILD_ROOT$jardir" "${packages[@]}"
done
%if 0%{?rhel} >= 7
mkdir -p "$RPM_BUILD_ROOT%{gumslibdir}/endorsed"
build-jar-repository "$RPM_BUILD_ROOT%{gumslibdir}/endorsed" xml-commons-apis
%endif

#Fix log4j mess and replace with standard ones
rm $RPM_BUILD_ROOT%{webinfdir}/log4j.properties
rm $RPM_BUILD_ROOT%{_sysconfdir}/%{gumsdirname}/log4j.properties
rm $RPM_BUILD_ROOT%{webinfdir}/classes/log4j.properties
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/%{gumsdirname}/log4j.properties
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/%{gumsdirname}/log4j-service.properties
ln -s %{_sysconfdir}/%{gumsdirname}/log4j-service.properties $RPM_BUILD_ROOT%{webinfdir}/classes/log4j.properties

# Add context to allow sym linking
cat > $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/gums/META-INF/context.xml << EOL
<?xml version="1.0" encoding="UTF-8"?>
<Context path="/gums" allowLinking="true">
</Context>
EOL

%files
%defattr(-,root,root,-)
%dir %{gumslibdir}
%{gumslibdir}/endorsed
%{gumslibdir}/*.jar

%files client
%defattr(-,root,root,-)
%{_bindir}/gums
%{_bindir}/gums-gridmapfile
%{_bindir}/gums-host
%{_bindir}/gums-host-cron
%{_bindir}/gums-nagios
%{_bindir}/gums-service
%{_bindir}/gums-vogridmapfile
%dir %{_sysconfdir}/%{gumsdirname}
%config(noreplace) %{_sysconfdir}/%{gumsdirname}/gums-client.properties
%config(noreplace) %{_sysconfdir}/%{gumsdirname}/gums-nagios.conf
%config(noreplace) %{_sysconfdir}/%{gumsdirname}/log4j.properties
%config(noreplace) /var/lib/osg/user-vo-map
%config(noreplace) /var/lib/osg/supported-vo-list
%dir /var/log/%{gumsdirname}
%config(noreplace) %{_sysconfdir}/cron.d/gums-client-cron
%{_sysconfdir}/rc.d/init.d/gums-client-cron

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
%dir %{_sysconfdir}/%{gumsdirname}
%config(noreplace) %{_sysconfdir}/%{gumsdirname}/log4j-service.properties
%attr(0600,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{gumsdirname}/gums.config
%attr(0750,tomcat,tomcat) %dir %{webinfdir}/config
%dir %{_var}/lib/%{tomcat}/webapps/gums
%{_var}/lib/%{tomcat}/webapps/gums
%{gumslibdir}/sql
%{gumslibdir}/config
%{_bindir}/gums-add-mysql-admin
%{_bindir}/gums-create-config
%{_bindir}/gums-setup-mysql-database
%ghost %{_javadir}/javamail.jar

%post service
%{_sbindir}/update-alternatives --install %{_javadir}/javamail.jar javamail %{gumslibdir}/mail-1.4.1.jar 5000

# clear out cached jsp pages on install/update
rm -f %{_usr}/share/%{tomcat}/work/Catalina/localhost/gums/org/apache/jsp/*

%postun service
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove javamail %{gumslibdir}/mail-1.4.1.jar
fi

%changelog
* Thu Oct 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.1-5.osg
- Fix path issue in client tools on EL7 (SOFTWARE-2040)

* Mon Oct 26 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.1-4.osg
- Use bouncycastle 1.50 from the OS on EL7 (SOFTWARE-2040)
- Use jspc-compiler for tomcat7 on EL7 (SOFTWARE-2040)

* Thu Oct 08 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.1-2.osg
- Fix gums db creation template to avoid syntax error with mariadb (SOFTWARE-2040)

* Wed Sep 30 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.1-1
- Update to GUMS 1.5.1 (SOFTWARE-2055)
  - Fix functionality of mapAccount (SOFTWARE-2028)
  - Handle null FQANs in vomsUserGroup (SOFTWARE-2035)
  - Update to jglobus 2.1.0 (SOFTWARE-2036)
  - Update to privilege-xacml 2.6.5 (SOFTWARE-2037)
  - Support groupName in pool account mappers (SOFTWARE-2047)

* Wed Sep 30 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.0-12
- Minor fix for pool account mapper groupName support (SOFTWARE-2047)

* Tue Sep 29 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.0-11
- Drop patch from -3 build, shown to be broken in nightlies (SOFTWARE-1981)
- Code cleanup for pool account mapper groupName support (SOFTWARE-2047)

* Fri Sep 25 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.0-10
- Support groupName in pool account mappers (SOFTWARE-2047)

* Fri Sep 25 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.0-9
- Handle null FQANs in vomsUserGroup (SOFTWARE-2035)

* Tue Sep 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-8
- Fix commons dependencies on el6

* Fri Sep 18 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-7
- Build on el5 again

* Thu Sep 17 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-6
- Apply changes to build on el6 again

* Thu Sep 17 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-5
- Apply Brian Bockelman's patch from SOFTWARE-2040 to build against el7

* Wed Sep 16 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.0-4
- Rebuild against jGlobus 2.1.0 (SOFTWARE-2036)

* Tue Sep 15 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.0-3
- Use maven profile to disable jsp precompilation for el5 (SOFTWARE-1981)

* Thu Sep 10 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.0-2
- Fix functionality of mapAccount (SOFTWARE-2028)

* Mon Aug 31 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.5.0-1
- Update to GUMS 1.5.0 (SOFTWARE-2007)
  - Add support for CSRF and XSS prevention

* Mon Aug 03 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.4-3
- Bugfix; handle null objects correctly if using an older lcmaps client or
  gums-host (SOFTWARE-1989)

* Thu Jul 23 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.4-1
- Update to GUMS 1.4.4 (SOFTWARE-1726)
  - Add support for recycling accounts
  - Use client verification information to validate VOMS attributes
  - Travis CI integration

* Mon Apr 27 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.3-2
- Don't save 'gums-test' entries when writing gums.config

* Mon Apr 27 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.3-1
- Update to GUMS 1.4.3 (SOFTWARE-1891)

* Tue Jan 27 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.2-1
- Update to GUMS 1.4.2 (SOFTWARE-1770)

* Mon Jan 26 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-5
- configuration update for simple host matching (SOFTWARE-1714)

* Mon Jan 12 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-4
- bugfix related to new scas client (SOFTWARE-1749)

* Wed Dec 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-3
- remove the GUMS SAML service definition (SOFTWARE-992)

* Fri Nov 21 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-2
- Update to GUMS 1.4.1 (SOFTWARE-1654)
- Add versioned dependency on emi-trustmanager >= 3.0.3-6

* Mon Nov 17 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-0.6.pre4
- Buildfix: don't pre-compile jsp pages for el5 (SOFTWARE-1654)
- Remove cached jsp pages on install/upgrade

* Fri Nov 14 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-0.5.pre4
- Patch to use correct version of jspc-compiler-tomcat artifact (SOFTWARE-1654)

* Wed Nov 12 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-0.4.pre4
- Update to GUMS 1.4.1.pre4 (SOFTWARE-1654)
  - Updated Ban Users UI (SOFTWARE-1655)
  - Pre-compile JSP pages
  - Logging improvements

* Fri Oct 31 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-0.1.pre3
- Update to GUMS 1.4.1.pre3 (SOFTWARE-1654)

* Thu Oct 30 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-0.1.pre2
- Update to GUMS 1.4.1.pre2 (SOFTWARE-1654)

* Wed Oct 29 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.1-0.1.pre1
- Update to GUMS 1.4.1.pre1 (SOFTWARE-1654)
  - Support is added for new "account" obligation extension to XACML profile
  - Almost all mysql queries are cached in memory by Hibernate
  - Hibernate is updated from 3.0.3 to 3.6.10

* Wed Sep 24 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-5
- Modify gums-host-cron to support local-user-vo-map (SOFTWARE-1606)

* Thu Sep 18 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-4
- Enable service jar symlinking and system jar removal (SOFTWARE-1498)

* Thu Sep 18 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-3
- Include commons-beanutils system jar in /usr/lib/gums (SOFTWARE-1498)
- Have xmltooling version match between gums/gums-service (SOFTWARE-1498)

* Wed Sep 17 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-2
- Do not remove system jars for EL5 (SOFTWARE-1498)

* Tue Sep 16 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-1
- Update to GUMS 1.4.0 (SOFTWARE-1498)

* Tue Aug 19 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-0.4.pre3
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

