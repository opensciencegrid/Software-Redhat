
Name: jglobus
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 2.0.4
Release: 5%{?dist}
URL: http://www.globus.org/toolkit/jglobus/
Group: System Environment/Libraries

# git clone git://github.com/jglobus/JGlobus.git JGlobus
# cd JGlobus
# git-archive master | gzip -9 > ~/rpmbuild/SOURCES/JGlobus.tar.gz

Source0: JGlobus.tar.gz

# Skip tomcat integration until we get relevant code patches from EPEL.
Patch0: no-ssl-proxies-tomcat.patch
Patch1: FTPClient.java.patch

BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java7-devel
BuildRequires: jpackage-utils
%if "%{?rhel}" == "6"
BuildRequires: maven22
%else
BuildRequires: maven2
%endif
BuildRequires: bouncycastle

Requires: java7
Requires: jpackage-utils
Requires: bouncycastle
Requires: log4j

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
%{summary}

%prep
%setup -q -c -n JGlobus
%patch0 -p1
%patch1 -p0

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
%define mvn %{_bindir}/mvn
%if 0%{?rhel} >= 6
%define mvn %{_bindir}/mvn22
%endif

# Force jglobus to build against the local bcprov
%{mvn} install:install-file -B -DgroupId=org.bouncycastle -DartifactId=bcprov-jdk16 -Dversion=1.45 -Dpackaging=jar -Dfile=`build-classpath bcprov` -Dmaven.repo.local=$MAVEN_REPO_LOCAL

%{mvn} \
  -e \
  -DskipTests \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -m 755 ssl-proxies/target/ssl-proxies-2.0-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/ssl-proxies-%{version}.jar
install -m 755 gridftp/target/gridftp-2.0-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/gridftp-%{version}.jar
install -m 755 gss/target/gss-2.0-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/gss-%{version}.jar
install -m 755 jsse/target/jsse-2.0-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jsse-%{version}.jar
install -m 755 io/target/io-2.0-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/io-%{version}.jar

install -d -m 755 $RPM_BUILD_ROOT/usr/share/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/usr/share/maven2/poms/JPP-%{name}.pom

%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP gss-2.0-SNAPSHOT.jar
%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP jsse-2.0-SNAPSHOT.jar
%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP gridftp-2.0-SNAPSHOT.jar
%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP ssl-proxies-2.0-SNAPSHOT.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*
/usr/share/maven2/poms/JPP-%{name}.pom
%{_mavendepmapfragdir}/jglobus

%changelog
* Fri Feb 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.0.4-5
- Update to build with JDK 7, require java7-devel + jpackage-utils
- Patch java source file with non-ascii chars that breaks the build in 1.7

* Wed Oct 10 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.4-4
- Update to latest master.
- Remove spring embedded JAR.
- On RHEL6, build against the installed bcprov instead of the maven one.

* Mon Sep 24 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.4-3
- Fix JGlobus client compatibility with older servers.

* Thu Sep 20 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.4-2
- Fix support for older SRM clients.

* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.0-1
- Initial packaging of JGlobus.

