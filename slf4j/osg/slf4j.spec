# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# % define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}
# We don't want to use gcj
%define gcj_support 0

%define section         free

Summary:        Simple Logging Facade for Java
Name:           slf4j
Version:        1.5.2
Release:        5%{dist}
Epoch:          0
Group:          System/Logging
License:        MIT
URL:            http://www.slf4j.org/
Source0:        http://www.slf4j.org/dist/slf4j-1.5.2.tar.gz
Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml
Patch0:         %{name}-pom_xml.patch
BuildRequires:  jpackage-utils
BuildRequires:  java7-devel
BuildRequires:  ant >= 0:1
BuildRequires:  junit >= 0:3.8.2
BuildRequires:  maven22 >= 2.0.7
#BuildRequires:  maven2-plugin-antrun
#BuildRequires:  maven2-plugin-compiler
#BuildRequires:  maven2-plugin-install
#BuildRequires:  maven2-plugin-jar
#BuildRequires:  maven2-plugin-javadoc
#BuildRequires:  maven2-plugin-resources
#BuildRequires:  maven2-plugin-source
#BuildRequires:  maven-surefire-plugin
#BuildRequires:  excalibur-avalon-framework
BuildRequires:  log4j
BuildRequires:  jakarta-commons-logging

Requires(post): jpackage-utils
Requires(postun): jpackage-utils
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Simple Logging Facade for Java or (SLF4J) is intended to serve
as a simple facade for various logging APIs allowing to the end-user
to plug in the desired implementation at deployment time. SLF4J also
allows for a gradual migration path away from
Jakarta Commons Logging (JCL). 
Logging API implementations can either choose to implement the
SLF4J interfaces directly, e.g. NLOG4J or SimpleLogger. Alternatively,
it is possible (and rather easy) to write SLF4J adapters for the given
API implementation, e.g. Log4jLoggerAdapter or JDK14LoggerAdapter.. 

%package javadoc
Group:          Development/Documentation
Summary:        Javadoc for %{name}

%description javadoc
%{summary}.

%package manual
Group:          Development/Documentation
Summary:        Documents for %{name}

%description manual
%{summary}.

%prep
%setup -q
find . -name "*.jar" | xargs rm
cp -p %{SOURCE1} settings.xml
%patch0 -b .sav0

sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL/org.slf4j
ln -sf $(build-classpath maven2/empty-dep) $MAVEN_REPO_LOCAL/org.slf4j/slf4j-api.jar
ln -sf $(build-classpath maven2/empty-dep) $MAVEN_REPO_LOCAL/org.slf4j/slf4j-simple.jar
ln -sf $(build-classpath maven2/empty-dep) $MAVEN_REPO_LOCAL/org.slf4j/slf4j-log4j12.jar

%build
alias mvn="/usr/bin/mvn22"
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -m 644 jcl104-over-slf4j/target/jcl104-over-slf4j-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl104-over-slf4j-%{version}.jar
install -m 644 jcl-over-slf4j/target/jcl-over-slf4j-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl-over-slf4j-%{version}.jar
install -m 644 jul-to-slf4j/target/jul-to-slf4j-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jul-to-slf4j-%{version}.jar
install -m 644 log4j-over-slf4j/target/log4j-over-slf4j-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j-over-slf4j-%{version}.jar
install -m 644 slf4j-api/target/%{name}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/api-%{version}.jar
install -m 644 slf4j-api/target/%{name}-api-%{version}-tests.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/api-tests-%{version}.jar
#install -m 644 slf4j-archetype/target/%{name}-archetype-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/archetype-%{version}.jar
install -m 644 slf4j-jcl/target/%{name}-jcl-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl-%{version}.jar
install -m 644 slf4j-jdk14/target/%{name}-jdk14-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jdk14-%{version}.jar
install -m 644 slf4j-log4j12/target/%{name}-log4j12-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j12-%{version}.jar
install -m 644 slf4j-migrator/target/%{name}-migrator-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/migrator-%{version}.jar
install -m 644 slf4j-nop/target/%{name}-nop-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/nop-%{version}.jar
install -m 644 slf4j-simple/target/%{name}-simple-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/simple-%{version}.jar
#install -m 644 slf4j-site/target/%{name}-site-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/site-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.slf4j jcl104-over-slf4j %{version} JPP/slf4j jcl104-over-slf4j
%add_to_maven_depmap org.slf4j jcl-over-slf4j %{version} JPP/slf4j jcl-over-slf4j
%add_to_maven_depmap org.slf4j jul-to-slf4j %{version} JPP/slf4j jul-to-slf4j
%add_to_maven_depmap org.slf4j log4j-over-slf4j %{version} JPP/slf4j log4j-over-slf4j
%add_to_maven_depmap org.slf4j %{name}-parent %{version} JPP/slf4j parent
%add_to_maven_depmap org.slf4j %{name}-api %{version} JPP/slf4j api
%add_to_maven_depmap org.slf4j %{name}-archetype %{version} JPP/slf4j archetype
%add_to_maven_depmap org.slf4j %{name}-jcl %{version} JPP/slf4j jcl
%add_to_maven_depmap org.slf4j %{name}-jdk14 %{version} JPP/slf4j jdk14
%add_to_maven_depmap org.slf4j %{name}-log4j12 %{version} JPP/slf4j log4j12
%add_to_maven_depmap org.slf4j %{name}-migrator %{version} JPP/slf4j migrator
%add_to_maven_depmap org.slf4j %{name}-nop %{version} JPP/slf4j nop
%add_to_maven_depmap org.slf4j %{name}-simple %{version} JPP/slf4j simple

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-parent.pom
install -pm 644 jcl104-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jcl104-over-slf4j.pom
install -pm 644 jcl-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jcl-over-slf4j.pom
install -pm 644 jul-to-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jul-to-slf4j.pom
install -pm 644 log4j-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-log4j-over-slf4j.pom
install -pm 644 slf4j-api/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-api.pom
#install -pm 644 slf4j-archetype/pom.xml \
#    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-archetype.pom
install -pm 644 slf4j-jcl/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jcl.pom
install -pm 644 slf4j-jdk14/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-jdk14.pom
install -pm 644 slf4j-log4j12/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-log4j12.pom
install -pm 644 slf4j-migrator/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-migrator.pom
install -pm 644 slf4j-nop/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-nop.pom
install -pm 644 slf4j-simple/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-simple.pom

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf target/site/api*

# manual
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr target/site $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
install -m 644 LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/%{name}
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*-%{version}.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}/site

%changelog
* Wed Apr 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 0:1.5.2-5
- Build with OpenJDK7

* Wed Nov 14 2012 Doug Strain <dstrain@fnal.gov> - 0:1.5.2-4
- Rebuild for OSG. 
- Note: a newer version is available for el6 in os repos
-   so this release is targeted only for el5 distributions
-   (clean builds are only guaranteed on el5-based systems)
- Also, changed to use OSG maven22 to get rid of maven issues

* Tue Oct 16 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0:1.5.2-3
- Relax the jpackage-utils dependency.

* Fri Jul 18 2008 David Walluck <dwalluck@redhat.com> 0:1.5.2-2
- use excalibur for avalon
- remove javadoc scriptlets
- GCJ fixes
- fix maven directory ownership
- fix -bc --short-circuit by moving some of %%build to %%prep

* Sun Jul 06 2008 Ralph Apel <r.apel at r-apel.de> 0:1.5.2-1.jpp5
- 1.5.2

* Mon Feb 04 2008 Ralph Apel <r.apel at r-apel.de> 0:1.4.2-2jpp
- Fix macro misprint
- Add maven2-plugin BRs

* Wed Jul 18 2007 Ralph Apel <r.apel at r-apel.de> 0:1.4.2-1jpp
- Upgrade to 1.4.2
- Build with maven2
- Add poms and depmap frags
- Add gcj_support option

* Mon Jan 30 2006 Ralph Apel <r.apel at r-apel.de> 0:1.0-0.rc5.1jpp
- First JPackage release.
