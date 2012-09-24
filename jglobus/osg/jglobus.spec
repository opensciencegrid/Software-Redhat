
Name: jglobus
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 2.0.4
Release: 3%{?dist}
URL: http://www.globus.org/toolkit/jglobus/
Group: System Environment/Libraries

# git clone git://github.com/jglobus/JGlobus.git JGlobus
# OR
# git clone http://github.com/bbockelm/JGlobus.git
# cd JGlobus
# git-archive master | gzip -9 > ~/rpmbuild/SOURCES/JGlobus.tar.gz
# OR
# git-archive osg_customizations | gzip -9 > ~/rpmbuild/SOURCES/JGlobus.tar.gz

Source0: JGlobus.tar.gz

# Binary dependency whose dep chain is much too large
Source1: spring-core-3.0.1.RELEASE.jar

BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: jpackage-utils
%if "%{?rhel}" == "6"
BuildRequires: maven22
%else
BuildRequires: maven2
%endif
BuildRequires: bouncycastle

Requires: java
Requires: jpackage-utils
Requires: bouncycastle
Requires: log4j

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
%{summary}

%prep
%setup -q -c -n JGlobus

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

cp %{SOURCE1} .

#%patch -p1

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

%if "%{?rhel}" == "6"
mvn22 \
%else
mvn \
%endif
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

install -m 755 spring-core-3.0.1.RELEASE.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/spring-core-3.0.1.RELEASE.jar

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
* Mon Sep 24 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.4-3
- Fix JGlobus client compatibility with older servers.

* Thu Sep 20 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.4-2
- Fix support for older SRM clients.

* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.0-1
- Initial packaging of JGlobus.

