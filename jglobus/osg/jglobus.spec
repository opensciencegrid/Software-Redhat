Name: jglobus
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 2.0.6
Release: 4%{?dist}
URL: http://www.globus.org/toolkit/jglobus/
Group: System Environment/Libraries

# git clone git://github.com/jglobus/JGlobus.git JGlobus
# cd JGlobus
# git-archive master | gzip -9 > ~/rpmbuild/SOURCES/JGlobus.tar.gz

Source0: JGlobus.tar.gz

Patch0: crl-updates.patch
Patch1: pom.xml.patch
Patch2: 1607-fix-sl6-certs.patch

BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRequires: /usr/share/java-1.7.0
BuildRequires: maven22
BuildRequires: bouncycastle

Requires: java7
Requires: jpackage-utils
Requires: bouncycastle
Requires: log4j
Conflicts: cog-jglobus-axis < 1.8.0

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
%{summary}

%prep
%setup -q -c -n JGlobus
#%patch0 -p1
%patch1 -p0
%patch2 -p1

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
%define mvn %{_bindir}/mvn22

# Force jglobus to build against the local bcprov
%{mvn} install:install-file -B -DgroupId=org.bouncycastle -DartifactId=bcprov-jdk16 -Dversion=1.45 -Dpackaging=jar -Dfile=`build-classpath bcprov` -Dmaven.repo.local=$MAVEN_REPO_LOCAL

%{mvn} \
  -B \
  -e \
  -DskipTests \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -m 755 ssl-proxies/target/ssl-proxies-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/ssl-proxies-%{version}.jar
install -m 755 gridftp/target/gridftp-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/gridftp-%{version}.jar
install -m 755 gss/target/gss-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/gss-%{version}.jar
install -m 755 jsse/target/jsse-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jsse-%{version}.jar
install -m 755 io/target/io-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/io-%{version}.jar

install -d -m 755 $RPM_BUILD_ROOT/usr/share/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/usr/share/maven2/poms/JPP-%{name}.pom

%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP gss-%{version}.jar
%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP jsse-%{version}.jar
%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP gridftp-%{version}.jar
%add_to_maven_depmap org.jglobus jglobus-all %{version} JPP ssl-proxies-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*
/usr/share/maven2/poms/JPP-%{name}.pom
%{_mavendepmapfragdir}/jglobus

%changelog
* Mon Sep 22 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.0.6-4
- Patch to work around SL6-generated certificate issue (SOFTWARE-1607)

* Tue Sep 17 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.6-3
- Add /usr/share/java-1.7.0 to BuildRequires to build on el5
- Require maven22 for el5 as well

* Fri Sep 13 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.6-2
- Update to 2.0.6 release.

* Tue Jul 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.5-4.1
- Add Conflict against cog-jglobus-axis < 1.8.0, since it was built with an older version of JGlobus. (SOFTWARE-1101)

* Tue Jul 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.5-3.1
- Merge changes into JDK 7 rebuild

* Mon May  8 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.5-3
- Update fix for JGlobus #80 to upstream version.

* Mon Apr 22 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.5-2
- Fix CRL refreshing for the trustmanager.
  https://github.com/jglobus/JGlobus/issues/80

* Tue Apr 09 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.5-1
- Update to upstream release.
- Provides fix for CRL updates, https://github.com/jglobus/JGlobus/pull/64

* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.0.4-7
- Rebuild for updated build dependency

* Fri Feb 22 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.0.4-6
- Patch pom.xml to specify encoding instead of patching java source

* Fri Feb 22 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.0.4-5
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

