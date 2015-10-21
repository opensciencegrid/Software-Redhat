%global rhel 5

Name: jglobus
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 2.1.0
Release: 6%{?dist}
URL: http://www.globus.org/toolkit/jglobus/
Group: System Environment/Libraries

# If set, the maven build is done in offline mode and a tarball of the maven
# dependencies (basically the local repository tarred up) is used.
%define maven_offline 0

# git clone git://github.com/jglobus/JGlobus.git JGlobus
# cd JGlobus
# git-archive JGlobus-Release-2.1.0 | gzip -9 > JGlobus-Release-2.1.0.tar.gz

Source0: JGlobus-Release-2.1.0.tar.gz

# jglobus-bc146 patch obtained from EPEL version of jglobus 2.1.0
Patch0:  jglobus-bc146.patch

# EL5 has bouncycastle 1.45, not 1.46
Patch1: jglobus-bc146-to-145.patch

# Posted to JGlobus github as a fix for key format issues.
# See SOFTWARE-1607
Patch2: 1607-fix-sl6-certs.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: /usr/share/java-1.7.0

%if %{?rhel} < 7

BuildRequires:  maven22
BuildRequires:  jpackage-utils
BuildRequires:  java7-devel
%define mvn mvn22

%else

BuildRequires:  maven >= 3.0
%define mvn mvn

%endif

%define local_maven /tmp/m2/%{name}/repository
#global mvnopts --batch-mode --fail-fast -Dmaven.repo.local="%{local_maven}"
%global mvnopts --batch-mode -Dmaven.repo.local="%{local_maven}"

%if 0%{?maven_offline}
%global mvnopts %mvnopts --offline
%else
%global mvnopts %mvnopts
%endif

%if 0%{?rhel} >= 7
Requires: java-headless >= 1:1.7.0
%else
Requires: java7
%endif
Requires: jpackage-utils
Requires: log4j
%if 0%{?rhel} <= 5
Requires: tomcat5
%endif
%if 0%{?rhel} == 6
Requires: tomcat6
%endif
%if 0%{?rhel} >= 7
Requires: tomcat
%endif
Conflicts: cog-jglobus-axis < 1.8.0

%if 0%{?maven_offline}

Source5: %{name}-mvn-deps-el5.tar.gz
Source6: %{name}-mvn-deps-el6.tar.gz
Source7: %{name}-mvn-deps-el7.tar.gz

    %if 0%{?el5}
        %define mvn_deps_tarball %{SOURCE5}
    %endif

    %if 0%{?el6}
        %define mvn_deps_tarball %{SOURCE6}
    %endif

    %if 0%{?el7}
        %define mvn_deps_tarball %{SOURCE7}
    %endif

%endif



%description
%{summary}

%prep
%setup -q -c -n JGlobus

%if 0%{?rhel} < 7
%patch0 -p1
%endif
%if 0%{?rhel} <= 5
%patch1 -p1
%endif
%patch2 -p1

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;


%build


# If we're using maven in offline mode, then copy our maven dependencies from
# the tarball(s) we have into the local mvn repo
%if 0%{?maven_offline}

    rm -rf "%{local_maven}"
    tar -xzf "%{mvn_deps_tarball}"

    (
        cd repository
        mkdir -p "%{local_maven}"
        mv -f * "%{local_maven}/"
    )
    rm -rf repository

%endif


%mvn %mvnopts \
    -DskipTests \
    install

%mvn %mvnopts \
    -DskipTests \
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

%if 0%{rhel} >= 6
    %add_maven_depmap  -a "org.jglobus:$module"  "$pomfile"  "$jarfile"
%else
    %add_to_maven_depmap  org.jglobus  jglobus-all  "%{version}"  JPP  "$module-%{version}.jar"
%endif
}

# Inexplicably, the axis sub-module produces a JAR named 'axisg'
# This messes up the installjar macro; seems to be better to rename
# the build directory than to try and rename the actual product.
mv axis axisg

for  module  in  gridftp gss io jsse ssl-proxies axisg
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
* Thu Oct 01 2015 Brian Bockelman <bbockelm@cse.unl.edu> - 2.1.0-5
- Add back patch from SOFTWARE-1607 for OpenSSL 1.0 keys.

* Thu Oct 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 2.1.0-4
- Add patch to EL5 and EL6 builds to fix bouncycastle API compatibility (SOFTWARE-2036)
- Had to disable offline mode for builds to work

* Wed Sep 16 2015 Brian Bockelman <bbockelm@cse.unl.edu> - 2.1.0-3
- Package axisg sub-module (replaces cog-jglobus-axis).

* Tue Sep 15 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 2.1.0-2.osg
- Build on EL7 and EL6; use a bundle of mvn dependencies so we can build in offline mode

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

