%if ! 0%{?el7}
%{warn:"*** THIS BUILD IS FOR EL7 ONLY ***"}
%endif

Name: jglobus
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 2.1.0
Release: 1%{?dist}
URL: http://www.globus.org/toolkit/jglobus/
Group: System Environment/Libraries

# git clone git://github.com/jglobus/JGlobus.git JGlobus
# cd JGlobus
# git-archive JGlobus-Release-2.1.0 | gzip -9 > JGlobus-Release-2.1.0.tar.gz

Source0: JGlobus-Release-2.1.0.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: maven-local

Requires: java-headless >= 1:1.7.0
Requires: jpackage-utils
#Requires: bouncycastle
#Requires: log4j
#Requires: tomcat
#Conflicts: cog-jglobus-axis < 1.8.0


%description
%{summary}

%prep
%setup -q -c -n JGlobus

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build

#define xmvn_bootstrap 1
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

xmvn \
    -B \
    -DskipTests \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    install

xmvn \
    -B \
    -e \
    -DskipTests \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    install javadoc:javadoc

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

installjar () {
    module=$1
    pomfile=JPP.jglobus-$module.pom
    jarfile=%name/$module.jar

    install  -m 755  "$module/target/$module-%version.jar"  "$RPM_BUILD_ROOT%_javadir/%name/$module-%version.jar"
    install -pm 644  "pom.xml"                              "$RPM_BUILD_ROOT%_mavenpomdir/$pomfile"
    ln -s            "$module-%version.jar"                 "$RPM_BUILD_ROOT%_javadir/$jarfile"

    %add_maven_depmap  -a "org.jglobus:$module"  "$pomfile"  "$jarfile"
}

for  module  in  gridftp gss io jsse ssl-proxies
do
    installjar $module
done




%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP.%{name}-*.pom
%{_mavendepmapfragdir}/%{name}

%changelog
* Fri Nov 07 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.1.0-1
- Update to 2.1.0 for EL7 (SOFTWARE-1541)
- Remove crl-updates.patch (upstream)
- Remove pom.xml.patch (unnecessary)
- Remove 1607-fix-sl6-certs.patch (does not apply)

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

* Wed May  8 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.5-3
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

