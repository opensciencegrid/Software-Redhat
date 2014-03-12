%define _noarchlib %{_exec_prefix}/lib
%define dirname saz
# Don't want to repack jars
%define __jar_repack %{nil}
%define __os_install_post %{nil}
%define jglobus_version 2.0.6

Name:    saz
Version: 4.0.0
Release: 2%{?dist}
Summary: Site AuthoriZation Service.  Banning tool for grid sites

License: Fermilab
Group:   System Environment/Daemons
URL:     http://www.saz.fnal.gov

Source0: %{name}-%{version}-2.tar.gz
Source1: %{name}-dependencies.tar.gz
Source2: build.properties
Source3: build.xml


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

%if 0%{?rhel} < 6
%define tomcat tomcat5
%endif

%if 0%{?rhel} >= 6
%define tomcat tomcat6
#This is probably not right, but one thing at a time
## explicitly requiring this because I don't want yum to pick java-1.5.0-gcj-devel
#Neha commenting for now since probably not needed
#BuildRequires: java-1.6.0-sun-compat
%endif

BuildRequires: ant
BuildRequires: antlr
BuildRequires: axis

BuildRequires: emi-trustmanager
BuildRequires: emi-trustmanager-axis

BuildRequires: java7-devel
#BuildRequires: java-1.6.0-sun-compat
BuildRequires: jaxrpc
BuildRequires: jta
BuildRequires: joda-time
BuildRequires: jglobus = %{jglobus_version}
BuildRequires: jpackage-utils
BuildRequires: jakarta-commons-codec
BuildRequires: jakarta-commons-collections
BuildRequires: jakarta-commons-discovery
BuildRequires: jakarta-commons-lang
BuildRequires: jakarta-commons-logging

BuildRequires: log4j

BuildRequires: voms-api-java >= 2.0.8

BuildRequires: wsdl4j

BuildRequires: xerces-j2
BuildRequires: xalan-j2

#  Commenting since package name contains number 5/6 and not sure how
# to specify that in build.properties file. instead packaging in dependant tarball instead
#BuildRequires: %{tomcat}-servlet-2.5-api
#  Commenting since this is much older version that what is available. packaging instead.
#BuildRequires: mysql-connector-java


Requires: java7
Requires: jglobus = %{jglobus_version}
Requires: emi-trustmanager
Requires: emi-trustmanager-axis
Requires: jakarta-commons-codec jakarta-commons-collections jakarta-commons-discovery jakarta-commons-lang jakarta-commons-logging
Requires: jacc jta
Requires: ant
Requires: antlr
Requires: axis
Requires: joda-time
Requires: xerces-j2 xalan-j2 log4j
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0

%description
%{summary}

%package service
Summary: Tomcat service for SAZ
Group: System Environment/Daemons

Requires: %{name} = %{version}-%{release}
Requires: %{tomcat}
Requires: emi-trustmanager-tomcat
Requires: mysql-server
Requires: osg-webapp-common
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%description service
%{summary}

%prep
BUILDROOT=$PWD
%setup -T -b 1 -q -n lib
cd ..
%setup -T -b 0 -q -n %{name}

pwd
ls
cp %{SOURCE2} $PWD/
cp %{SOURCE3} $PWD/
sed -i "s|@BUILDROOT@|$BUILDROOT|"  build.properties

%build
ant build

%install

function replace_jar {
 if [[ -e $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/lib/$1 ]]; then
  rm -f $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/lib/$1
  ln -s %{_noarchlib}/%{dirname}/$1 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/lib/$1
 fi
}

function replace_conf {
  rm -f $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/classes/$1
  ln -s %{_sysconfdir}/%{dirname}/$1 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/classes/$1
}

function replace_server_conf {
  rm -f $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/classes/$1
  ln -s %{_sysconfdir}/%{dirname}/$1 $RPM_BUILD_ROOT%{_usr}/share/java/$1
}
#Making sure the build root is empty
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}
pwd
ls

#copy all the jars needed by saz (which as packaged with saz) into /var/tmp/saz-4.0.0-1.osg.el5-buildroot/usr/lib/saz/
install -m 0644 ../lib/*.jar $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/

# Service
# setting up /var/lib/tomcat5/webapps/saz area
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/
pushd $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/
jar xf $OLDPWD/saz.war 
popd

# Create the WEB-INF/lib directory
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/WEB-INF/lib

install -m 0644 ../lib/*.jar $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/WEB-INF/lib/

## Link the exploded WAR to JARs, instead of including a copy
# tomcat6 doesn't seem to like this.
for x in $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/*.jar; do
    replace_jar $(basename $x)
done

# Move various SAZ configuration files under /etc/saz so they are all in one place
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/Admin.hbm.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/Admin.hbm.xml
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/CA.hbm.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/CA.hbm.xml
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/User.hbm.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/User.hbm.xml
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/VO.hbm.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/VO.hbm.xml
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/Role.hbm.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/Role.hbm.xml
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/log4j.properties
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/ehcache.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/ehcache.xml
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/template/hibernate.cfg.xml.template $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/hibernate.cfg.xml.template
install -m 0600 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config/template/sazserver.conf.template $RPM_BUILD_ROOT%{_sysconfdir}/%{dirname}/sazserver.conf.template


# Move various SAZ setup/wrapper scripts under /usr/bin/saz
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/setup/saz-create-config $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/setup/saz-db-conf-setup $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/setup/saz-add-mysql-admin $RPM_BUILD_ROOT%{_bindir}/

# Move various SAZ DB scripts under /usr/lib/saz/sql
mkdir -p $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql
install -m 0644 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/sql/createSAZDB.mysql $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql/
install -m 0644 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/sql/addAdmin.mysql $RPM_BUILD_ROOT%{_noarchlib}/%{dirname}/sql/

# Create the Log directory
mkdir -p $RPM_BUILD_ROOT/var/log/%{dirname}

# Create the ehcache directory
mkdir -p $RPM_BUILD_ROOT/var/log/ehcache

# Create symlinks for various config files
for x in "Admin.hbm.xml" "User.hbm.xml" "CA.hbm.xml" "VO.hbm.xml" "Role.hbm.xml" "ehcache.xml" "log4j.properties" "sazserver.conf.template" "hibernate.cfg.xml.template"; do
    replace_conf $x
done

# Create symlink
#ln -s %{_sysconfdir}/%{dirname}/$1 $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/classes/$1
# Neha - 03/11/2014 commenting since build vbreaks 
#ln -s %{_sysconfdir}/%{dirname}/$1 /usr/share/java/$1

# Create symlinks in a given directory
#build-jar-repository $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/lib ant antlr commons-codec commons-collections commons-discovery commons-httpclient commons-lang commons-logging jta joda-time jglobus log4j trustmanager trustmanager-axis wsdl4j xalan-j2-serializer xalan-j2 xerces-j2

#commenting axis since several broken links get created
#[axis]axis-1.4.jar -> /usr/share/java/axis/axis-1.4.jar
#[axis]axis-ant-1.4.jar -> /usr/share/java/axis/axis-ant-1.4.jar
#[axis]axis-schema-1.4.jar -> /usr/share/java/axis/axis-schema-1.4.jar
#etc
#build-jar-repository $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/lib axis antlr jglobus trustmanager trustmanager-axis commons-codec commons-collections commons-discovery commons-lang commons-logging jta joda-time xalan-j2 xerces-j2 log4j

build-jar-repository $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/WEB-INF/lib antlr jglobus trustmanager trustmanager-axis commons-codec commons-collections commons-discovery commons-lang commons-logging jta joda-time xalan-j2 xerces-j2 log4j

# Add context to allow sym linking
cat > $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/saz/META-INF/context.xml << EOL
<?xml version="1.0" encoding="UTF-8"?>
<Context path="/saz" allowLinking="true">
</Context>
EOL

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir
touch $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem

# Cleanup the resulting rpm
rm -rf $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/config
rm -rf $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/sql
rm -rf $RPM_BUILD_ROOT%{_var}/lib/%{tomcat}/webapps/%{dirname}/setup


%files
%defattr(-,root,root,-)
%dir %{_noarchlib}/%{dirname}
%{_noarchlib}/%{dirname}/*.jar

%files service
%defattr(-,root,root,-)
%{_sysconfdir}/%{dirname}
%attr(0600,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{dirname}/sazserver.conf.template
%attr(0600,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{dirname}/hibernate.cfg.xml.template
%attr(0644,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{dirname}/*.xml
%attr(0644,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{dirname}/log4j.properties
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem
%attr(-,tomcat,tomcat) %dir %{_var}/log/%{dirname}
%attr(-,tomcat,tomcat) %dir %{_var}/log/ehcache

%{_var}/lib/%{tomcat}/webapps/saz
%{_noarchlib}/%{dirname}/sql
%{_bindir}/saz-create-config
%{_bindir}/saz-db-conf-setup
%{_bindir}/saz-add-mysql-admin

%changelog
* Tue Mar 12 2014 Neha Sharma <neha@fnal.gov> 4.0.0-2
- Build using OpenJDK7, jglobus 2.0.6
- Added SHA2 support
- Removed support for SAZ legacy protocol
- Newer hibernate (4.2.0), privilege-xacml (2.6.1)
* Tue Apr 30 2013 Neha Sharma <neha@fnal.gov> 4.0.0-1
- First attempt at creating rpm for SAZ service
