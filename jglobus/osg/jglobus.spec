
Name: jglobus
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 2.0.0
Release: 1%{?dist}
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
#Patch: rhel5-maven-fixes.patch
BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: maven2
BuildRequires: bcprov

Requires: java
Requires: jpackage-utils
Requires: bcprov
Requires: log4j

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
%{summary}

%prep
%setup -q -c -n JGlobus

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

#%patch -p1

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn -e \
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
* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.0-1
- Initial packaging of JGlobus.

