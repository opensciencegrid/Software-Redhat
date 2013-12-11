%global bootstrap 1
%global __jar_repack 0
%global majmin 22

Name:           maven%{majmin}
Epoch:          0
Version:        2.2.1
Release:        23.4.1%{?dist}
Summary:        Java project management and project comprehension tool
Group:          Development/Build Tools
License:        ASL 2.0 and MIT and BSD
URL:            http://maven.apache.org

# export https://svn.apache.org/repos/asf/maven/maven-2/tags/maven-%{version}/ apache-maven-%{version}
# tar czvf maven2-%{version}.tar.gz apache-maven-%{version}
Source0:        maven2-%{version}.tar.gz

# Since we are using the entire dependency set "as is", we need to atleast try
# and make it so that only one version is packaged in the binary blob. This
# server an additional (and more important) purpose ... it ensures that a
# single version of each module is enough; because if not, versioned rpm names
# would be needed for those dependencies. The idea is as follows:

# Required by maven:
#  org/codehaus/plexus/1.0/plexus-1.0.jar
#  org/codehaus/plexus/1.1/plexus-1.1.jar
# What we package in the blob:
#  org/codehaus/plexus/1.1/plexus-1.1.jar
#  org/codehaus/plexus/1.0/plexus-1.0.jar -> ../1.1/plexus-1.1.jar

# Doing this for the hundreds of jars is a huge pain.. so we do the only
# thing sane people can. Crazy scripting magic! To generate the tarball

# rm -rf ~/.m2
# tar xzf SOURCE0
# cd apache-maven-%{version}
# export M2_HOME=`pwd`/installation/apache-maven-%{version}
# ant
# cd ~/.m2
# SOURCE100
# Find maven-%{version}-bootstrapdeps.tar.gz in ./
Source1:        maven2-%{version}-bootstrapdeps.tar.gz

# 1xx for non-upstream/created sources
Source100:      maven2-%{version}-settings.xml
Source101:      maven2-JPackageRepositoryLayout.java
Source102:      maven2-MavenJPackageDepmap.java
Source103:      maven2-%{version}-depmap.xml
Source104:      maven2-empty-dep.pom
Source105:      maven2-empty-dep.jar

# 2xx for created non-buildable sources
Source200:      maven2-script
Source201:      maven2-jpp-script

Patch0:         maven2-antbuild.patch
Patch1:         maven2-%{version}-jpp.patch
Patch2:         maven2-%{version}-update-tests.patch
Patch3:         maven2-%{version}-enable-bootstrap-repo.patch
Patch4:         maven2-%{version}-unshade.patch
Patch5:         maven2-%{version}-default-resolver-pool-size.patch
Patch6:         maven2-RELEASE.patch

%if 0
Provides:       maven2 = %{epoch}:%{version}-%{release}
%endif

BuildRequires:  java7-devel
BuildRequires:  jpackage-utils
BuildRequires:  classworlds
BuildRequires:  jdom

%if %{bootstrap}
BuildRequires:  ant
BuildRequires:  zip
%else
BuildRequires:  %{name} = %{epoch}:%{version}
BuildRequires:  maven2-common-poms
BuildRequires:  apache-resource-bundles
BuildRequires:  objectweb-asm
BuildRequires:  backport-util-concurrent
##BuildRequires:  buildnumber-maven-plugin
BuildRequires:  bsh
BuildRequires:  jsch
BuildRequires:  jakarta-commons-cli
BuildRequires:  jakarta-commons-codec
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jakarta-commons-io
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
BuildRequires:  easymock
BuildRequires:  junit
BuildRequires:  nekohtml
BuildRequires:  ant
BuildRequires:  maven-doxia
BuildRequires:  jetty6
BuildRequires:  maven-archiver
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-shared-doxia-tools
BuildRequires:  maven-enforcer-api
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-enforcer-rules
BuildRequires:  maven-shade-plugin
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-shared-plugin-testing-harness
BuildRequires:  maven-pmd-plugin
BuildRequires:  maven-shared-file-management
BuildRequires:  maven-shared-common-artifact-filters
BuildRequires:  maven-shared-dependency-tree
BuildRequires:  maven-shared-repository-builder
BuildRequires:  maven-shared-io
BuildRequires:  maven-shared-downloader
BuildRequires:  maven-shared-filtering
BuildRequires:  maven-reporting-api
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-scm
BuildRequires:  maven-wagon
BuildRequires:  modello
BuildRequires:  multithreadedtc
BuildRequires:  oro
BuildRequires:  plexus-active-collections 
BuildRequires:  plexus-ant-factory 
BuildRequires:  plexus-archiver
#BuildRequires:  plexus-cipher
BuildRequires:  plexus-bsh-factory
BuildRequires:  plexus-build-api
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-compiler
BuildRequires:  plexus-component-api
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-container-default
BuildRequires:  plexus-i18n
BuildRequires:  plexus-interactivity
BuildRequires:  plexus-interpolation
BuildRequires:  plexus-io
BuildRequires:  plexus-resources
##BuildRequires:  plexus-sec-dispatcher
BuildRequires:  plexus-utils
BuildRequires:  plexus-velocity
BuildRequires:  regexp
BuildRequires:  forge-parent
##BuildRequires:  spice-parent
BuildRequires:  jakarta-oro
BuildRequires:  regexp
BuildRequires:  slf4j
BuildRequires:  velocity
%endif

Requires:       classworlds
Requires:       jdom

%if !%{bootstrap}
Requires:       apache-resource-bundles
Requires:       objectweb-asm
Requires:       backport-util-concurrent
Requires:       bsh
Requires:       jsch
Requires:       jakarta-commons-cli
Requires:       jakarta-commons-codec
Requires:       jakarta-commons-collections
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-io
Requires:       jakarta-commons-lang
Requires:       jakarta-commons-logging
#Requires:      apache-commons-parent
Requires:       easymock
Requires:       junit
Requires:       nekohtml
Requires:       ant
Requires:       maven-doxia
Requires:       jetty6
Requires:       maven-archiver
Requires:       maven-shared-doxia-tools
Requires:       maven-enforcer-api
Requires:       maven-enforcer-plugin
Requires:       maven-plugin-testing-harness
Requires:       maven-shared-file-management
Requires:       maven-shared-common-artifact-filters
Requires:       maven-shared-dependency-tree
Requires:       maven-shared-repository-builder
Requires:       maven-shared-io
Requires:       maven-shared-downloader
Requires:       maven-shared-filtering
Requires:       maven-shared-reporting-api
Requires:       maven-surefire-provider-junit
Requires:       maven-scm
Requires:       maven-wagon
Requires:       maven2-common-poms
Requires:       modello
Requires:       multithreadedtc
Requires:       jakarta-oro
Requires:       plexus-active-collections
Requires:       plexus-ant-factory
Requires:       plexus-archiver
##Requires:       plexus-cipher
Requires:       plexus-bsh-factory
Requires:       plexus-build-api
Requires:       plexus-classworlds
Requires:       plexus-compiler
Requires:       plexus-component-api
Requires:       plexus-containers-container-default
Requires:       plexus-container-default
Requires:       plexus-i18n
Requires:       plexus-interactivity
Requires:       plexus-interpolation
Requires:       plexus-io
Requires:       plexus-resources
##Requires:       plexus-sec-dispatcher
Requires:       plexus-utils
Requires:       plexus-velocity
Requires:       regexp
Requires:       forge-parent
##Requires:       spice-parent
Requires:       jakarta-oro
Requires:       regexp
Requires:       slf4j
Requires:       velocity
%endif

Requires(post): jpackage-utils
Requires(postun): jpackage-utils
Requires:       jpackage-utils

BuildArch:      noarch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Apache Maven is a software project management and comprehension tool. Based on
the concept of a project object model (POM), Maven can manage a project's
build, reporting and documentation from a central piece of information.

%prep
%setup -q -n apache-maven-%{version}

%patch0 -p0 -b .antbuild
%patch1 -p0 -b .jpp
%patch2 -p0 -b .update-tests
%patch6 -p0 -b .release

%if ! %{bootstrap}
%patch4 -p0 -b .unshade
%endif

%if %{bootstrap}
%patch3 -p0 -b .enable-bootstrap-repo
%endif

# set cache location
export M2_REPO=`pwd`/.m2
mkdir $M2_REPO

# if bootstrapping, extract the dependencies
%if %{bootstrap}
(cd $M2_REPO

  tar xzf %{SOURCE1}

  # maven-remote-resources-plugin (m-r-r-p) is used side-by-side with
  # plexus-velocity (p-v) 1.1.3 upstream.. we collapse to a single p-v version
  # of 1.1.7. 1.1.7 however has a component descriptor that conflicts
  # with the one in m-r-r-p. We therefore need to remove the descriptor
  # from m-r-r-p first
  zip -d repository/org/apache/maven/plugins/maven-remote-resources-plugin/1.0-beta-2/maven-remote-resources-plugin-1.0-beta-2.jar \
         META-INF/plexus/components.xml

  # resource bundle 1.3 is needed during build, but not when done via
  # upstream, for some reason
  mkdir -p repository/org/apache/apache-jar-resource-bundle/1.3
  ln -s ../1.4/apache-jar-resource-bundle-1.4.jar \
        repository/org/apache/apache-jar-resource-bundle/1.3/apache-jar-resource-bundle-1.3.jar
  ln -s ../1.4/apache-jar-resource-bundle-1.4.jar.sha1 \
        repository/org/apache/apache-jar-resource-bundle/1.3/apache-jar-resource-bundle-1.3.jar.sha1
)
%else
# FIXME: These tests fail when building with maven for an unknown reason
rm maven-core/src/test/java/org/apache/maven/WagonSelectorTest.java
rm maven-artifact-manager/src/test/java/org/apache/maven/artifact/manager/DefaultWagonManagerTest.java
%endif

cp %{SOURCE101} maven-artifact/src/main/java/org/apache/maven/artifact/repository/layout/JPackageRepositoryLayout.java
cp %{SOURCE102} maven-artifact/src/main/java/org/apache/maven/artifact/repository/layout/MavenJPackageDepmap.java

# disable parallel artifact resolution
%patch5 -p1 -b .parallel-artifacts-resolution

# test case is incorrectly assuming that target executed by antcall
# can propagate references to its parent (stopped working with ant 1.8)
rm maven-script/maven-script-ant/src/test/java/org/apache/maven/script/ant/AntMojoWrapperTest.java

# FIXIT: look why these tests are failing with maven-surefire 2.6
rm maven-artifact/src/test/java/org/apache/maven/artifact/resolver/DefaultArtifactCollectorTest.java
rm maven-project/src/test/java/org/apache/maven/project/validation/DefaultModelValidatorTest.java

%build
export M2_REPO=`pwd`/.m2
export M2_HOME=`pwd`/installation/apache-maven-%{version}

# copy settings to where ant reads from
mkdir -p $M2_HOME/conf
cp %{SOURCE100} $M2_HOME/conf/settings.xml

# replace locations in the copied settings file
sed -i -e s:__M2_LOCALREPO_PLACEHOLDER__:"file\://$M2_REPO/cache":g $M2_HOME/conf/settings.xml
sed -i -e s:__M2_REMOTEREPO_PLACEHOLDER__:"file\://$M2_REPO/repository":g $M2_HOME/conf/settings.xml

# replace settings file location before patching
sed -i -s s:__M2_SETTINGS_FILE__:$M2_HOME/conf/settings.xml:g build.xml

%if %{bootstrap}
%{ant} -Dmaven.repo.local=$M2_REPO/cache
%else
%{_bindir}/mvn%{majmin}-jpp -e -P all-models -Dmaven.repo.local=$M2_REPO/cache -Dmaven2.jpp.depmap.file=%{SOURCE103} install
%endif

%install
rm -rf $RPM_BUILD_ROOT

export M2_HOME=$(pwd)/installation/apache-maven-%{version}

rm -rf $M2_HOME

mkdir -p $(pwd)/installation/
(cd $(pwd)/installation/
tar jxf ../apache-maven/target/*bz2
)

# maven2 directory in /usr/share/java
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

###########
# M2_HOME #
###########
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}

###############
# M2_HOME/bin #
###############
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/bin
cp -a $M2_HOME/bin/* $RPM_BUILD_ROOT%{_datadir}/%{name}/bin

# Remove unnecessary batch scripts
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/*.bat

# Update conf file for unversioned jar names
sed -i -e s:'-classpath "${M2_HOME}"/boot/classworlds-\*.jar':'-classpath "${M2_HOME}"/boot/classworlds.jar':g \
        $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/mvn $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/mvnDebug

################
# M2_HOME/boot #
################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/boot
%if %{bootstrap}
cp -a $M2_HOME/boot/* $RPM_BUILD_ROOT%{_datadir}/%{name}/boot/
%endif

################
# M2_HOME/conf #
################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/conf
cp -a $M2_HOME/conf/* $RPM_BUILD_ROOT%{_datadir}/%{name}/conf/

###############
# M2_HOME/lib #
###############
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/lib

install -p -m 644 $M2_HOME/lib/maven-%{version}-uber.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/uber-%{version}.jar
ln -s uber-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/uber.jar
ln -s %{_javadir}/%{name}/uber.jar $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/maven-%{version}-uber.jar

################
# M2_HOME/poms #
#*##############
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/poms

########################
# /etc/maven/fragments #
########################
install -dm 755 $RPM_BUILD_ROOT/%{_sysconfdir}/maven/fragments

##############################
# /usr/share/java repository #
##############################
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/repository
ln -s %{_javadir} $RPM_BUILD_ROOT%{_datadir}/%{name}/repository/JPP
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/repository-signed
ln -s %{_javadir}-signed $RPM_BUILD_ROOT%{_datadir}/%{name}/repository-signed/JPP

##################
# javadir/%%{name} #
#*################
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

#######################
# javadir/%%{name}/poms #
#*#####################
ln -s %{_datadir}/%{name}/poms $RPM_BUILD_ROOT%{_javadir}/%{name}/poms

############
# /usr/bin #
############
install -dm 755 $RPM_BUILD_ROOT%{_bindir}

# Install files
install -m 644 %{SOURCE104} $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.maven2-empty-dep.pom
install -m 644 %{SOURCE105} $RPM_BUILD_ROOT%{_javadir}/%{name}/empty-dep.jar

# Wrappers
/bin/cp -af %{SOURCE200} $RPM_BUILD_ROOT%{_bindir}/mvn%{majmin}
/bin/cp -af %{SOURCE201} $RPM_BUILD_ROOT%{_bindir}/mvn%{majmin}-jpp

%if %{bootstrap}
    cp -af `pwd`/.m2/repository $RPM_BUILD_ROOT%{_datadir}/%{name}/bootstrap_repo
%endif

###################
# Individual jars #
###################

for file in \
    maven-script/maven-script-ant/target/maven-script-ant-%{version}.jar \
    maven-script/maven-script-beanshell/target/maven-script-beanshell-%{version}.jar \
    apache-maven/target/apache-maven-%{version}.jar \
    maven-profile/target/maven-profile-%{version}.jar \
    maven-artifact-manager/target/maven-artifact-manager-%{version}.jar \
    maven-artifact-test/target/maven-artifact-test-%{version}.jar \
    maven-monitor/target/maven-monitor-%{version}.jar \
    maven-toolchain/target/maven-toolchain-%{version}.jar \
    maven-toolchain/target/original-maven-toolchain-%{version}.jar \
    maven-project/target/maven-project-%{version}.jar \
    maven-settings/target/maven-settings-%{version}.jar \
    maven-plugin-parameter-documenter/target/maven-plugin-parameter-documenter-%{version}.jar \
    maven-model/target/maven-model-%{version}.jar \
    maven-artifact/target/maven-artifact-%{version}.jar \
    maven-repository-metadata/target/maven-repository-metadata-%{version}.jar \
    maven-plugin-api/target/maven-plugin-api-%{version}.jar \
    maven-error-diagnostics/target/maven-error-diagnostics-%{version}.jar \
    maven-compat/target/maven-compat-%{version}.jar \
    maven-core/target/maven-core-%{version}.jar \
    maven-plugin-registry/target/maven-plugin-registry-%{version}.jar \
    maven-plugin-descriptor/target/maven-plugin-descriptor-%{version}.jar; do \

        FNAME=`basename $file`
        FNAME_NO_EXT=`basename $file .jar`
        DIR=`dirname $file`
        UNVER_NAME=`basename $file | sed -e s:-%{version}::g`
        UNVER_NAME_WITH_NO_EXT=`echo $FNAME_NO_EXT | sed -e s:-%{version}::g`
        ARTIFACT=`basename \`dirname $DIR\``


        pushd $DIR
          install -m 644 $FNAME $RPM_BUILD_ROOT%{_javadir}/%{name}/
          ln -s $FNAME $RPM_BUILD_ROOT%{_javadir}/%{name}/$UNVER_NAME
          install -m 644 ../pom.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.%{name}-$UNVER_NAME_WITH_NO_EXT.pom
          %add_to_maven_depmap org.apache.maven $ARTIFACT %{version} JPP/%{name} $UNVER_NAME_WITH_NO_EXT
        popd
done

# maven-reporting-api
install -m 644  maven-reporting/maven-reporting-api/target/maven-reporting-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/
ln -s maven-reporting-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/maven-reporting-api.jar
install -m 644 maven-reporting/maven-reporting-api/pom.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.%{name}-maven-reporting-api.pom
%add_to_maven_depmap org.apache.maven.reporting maven-reporting-api %{version} JPP/%{name} maven-reporting-api

# maven-reporting pom
install -m 644 maven-reporting/pom.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.%{name}-maven-reporting.pom
%add_to_maven_depmap org.apache.maven.reporting maven-reporting %{version} JPP/%{name} maven-reporting

# maven pom
install -m 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/poms/JPP.%{name}-maven.pom
%add_to_maven_depmap org.apache.maven maven %{version} JPP/%{name} maven

(cd %{buildroot}%{_datadir}/%{name}/lib
  %{__ln_s} `build-classpath jdom` jdom.jar
)

(cd %{buildroot}%{_datadir}/%{name}/boot
%if %{bootstrap}
  # FIXME: how does this get here?
  %{__rm} classworlds-1.1.jar
%endif
  %{__ln_s} `build-classpath classworlds` classworlds.jar
)

%if ! %{bootstrap}
(cd %{buildroot}%{_datadir}/%{name}/lib
  # FIXME: add back maven-doxia/logging-api which is in 1.1+
  for i in backport-util-concurrent jsch commons-cli commons-httpclient commons-codec nekohtml maven-reporting-api maven-doxia/sink-api \
maven-wagon/wagon-file maven-wagon/wagon-http maven-wagon/wagon-http-lightweight maven-wagon/wagon-http-shared maven-wagon/wagon-provider-api maven-wagon/wagon-ssh maven-wagon/wagon-ssh-common maven-wagon/wagon-ssh-external plexus/container-default \
plexus/interactivity-api plexus-interpolation plexus/utils slf4j/slf4j-api slf4j/slf4j-nop plexus/plexus-cipher plexus/plexus-sec-dispatcher xerces-j2; do
    file=`build-classpath ${i} 2>/dev/null`
    if test -f ${file}; then
        %{__ln_s} ${file}
    fi
done
)
%endif

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/mvn%{majmin}
%attr(0755,root,root) %{_bindir}/mvn%{majmin}-jpp
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/bin
%config(noreplace) %{_datadir}/%{name}/bin/*.conf
%attr(0755,root,root) %{_datadir}/%{name}/bin/mvn
%attr(0755,root,root) %{_datadir}/%{name}/bin/mvnDebug
%dir %{_datadir}/%{name}/boot
%{_datadir}/%{name}/boot/classworlds.jar
%dir %{_datadir}/%{name}/conf
# XXX: should this be in %%{_sysconfdir} and marked as %%config
%{_datadir}/%{name}/conf/settings.xml
%{_javadir}/%{name}/apache-maven-%{version}.jar
%{_javadir}/%{name}/apache-maven.jar
%{_javadir}/%{name}/empty-dep.jar
%{_javadir}/%{name}/maven-artifact-%{version}.jar
%{_javadir}/%{name}/maven-artifact-manager-%{version}.jar
%{_javadir}/%{name}/maven-artifact-manager.jar
%{_javadir}/%{name}/maven-artifact-test-%{version}.jar
%{_javadir}/%{name}/maven-artifact-test.jar
%{_javadir}/%{name}/maven-artifact.jar
%{_javadir}/%{name}/maven-compat-%{version}.jar
%{_javadir}/%{name}/maven-compat.jar
%{_javadir}/%{name}/maven-core-%{version}.jar
%{_javadir}/%{name}/maven-core.jar
%{_javadir}/%{name}/maven-error-diagnostics-%{version}.jar
%{_javadir}/%{name}/maven-error-diagnostics.jar
%{_javadir}/%{name}/maven-model-%{version}.jar
%{_javadir}/%{name}/maven-model.jar
%{_javadir}/%{name}/maven-monitor-%{version}.jar
%{_javadir}/%{name}/maven-monitor.jar
%{_javadir}/%{name}/maven-plugin-api-%{version}.jar
%{_javadir}/%{name}/maven-plugin-api.jar
%{_javadir}/%{name}/maven-plugin-descriptor-%{version}.jar
%{_javadir}/%{name}/maven-plugin-descriptor.jar
%{_javadir}/%{name}/maven-plugin-parameter-documenter-%{version}.jar
%{_javadir}/%{name}/maven-plugin-parameter-documenter.jar
%{_javadir}/%{name}/maven-plugin-registry-%{version}.jar
%{_javadir}/%{name}/maven-plugin-registry.jar
%{_javadir}/%{name}/maven-profile-%{version}.jar
%{_javadir}/%{name}/maven-profile.jar
%{_javadir}/%{name}/maven-project-%{version}.jar
%{_javadir}/%{name}/maven-project.jar
%{_javadir}/%{name}/maven-reporting-api-%{version}.jar
%{_javadir}/%{name}/maven-reporting-api.jar
%{_javadir}/%{name}/maven-repository-metadata-%{version}.jar
%{_javadir}/%{name}/maven-repository-metadata.jar
%{_javadir}/%{name}/maven-script-ant-%{version}.jar
%{_javadir}/%{name}/maven-script-ant.jar
%{_javadir}/%{name}/maven-script-beanshell-%{version}.jar
%{_javadir}/%{name}/maven-script-beanshell.jar
%{_javadir}/%{name}/maven-settings-%{version}.jar
%{_javadir}/%{name}/maven-settings.jar
%{_javadir}/%{name}/maven-toolchain-%{version}.jar
%{_javadir}/%{name}/maven-toolchain.jar
%{_javadir}/%{name}/original-maven-toolchain-%{version}.jar
%{_javadir}/%{name}/original-maven-toolchain.jar
%dir %{_javadir}/%{name}/poms
%{_javadir}/%{name}/uber-%{version}.jar
%{_javadir}/%{name}/uber.jar
%dir %{_datadir}/%{name}/lib
%{_datadir}/%{name}/lib/jdom.jar
%if !%{bootstrap}
%{_datadir}/%{name}/lib/backport-util-concurrent.jar
%{_datadir}/%{name}/lib/commons-cli.jar
%{_datadir}/%{name}/lib/commons-codec.jar
%{_datadir}/%{name}/lib/commons-httpclient.jar
%{_datadir}/%{name}/lib/jsch.jar
# FIXME: only in 1.1+
%if 0
%{_datadir}/%{name}/lib/maven-doxia-logging-api.jar
%endif
%{_datadir}/%{name}/lib/sink-api.jar
%{_datadir}/%{name}/lib/maven-reporting-api.jar
%{_datadir}/%{name}/lib/wagon-file.jar
%{_datadir}/%{name}/lib/wagon-http-lightweight.jar
%{_datadir}/%{name}/lib/wagon-http-shared.jar
%{_datadir}/%{name}/lib/wagon-http.jar
%{_datadir}/%{name}/lib/wagon-provider-api.jar
%{_datadir}/%{name}/lib/wagon-ssh-common.jar
%{_datadir}/%{name}/lib/wagon-ssh-external.jar
%{_datadir}/%{name}/lib/wagon-ssh.jar
%{_datadir}/%{name}/lib/nekohtml.jar
%{_datadir}/%{name}/lib/container-default.jar
%{_datadir}/%{name}/lib/interactivity-api.jar
%{_datadir}/%{name}/lib/plexus-interpolation.jar
##%{_datadir}/%{name}/lib/plexus-cipher.jar
##%{_datadir}/%{name}/lib/plexus-sec-dispatcher.jar
%{_datadir}/%{name}/lib/utils.jar
%{_datadir}/%{name}/lib/slf4j-api.jar
%{_datadir}/%{name}/lib/slf4j-nop.jar
%{_datadir}/%{name}/lib/xerces-j2.jar
%endif
%{_datadir}/%{name}/lib/maven-%{version}-uber.jar
%{_datadir}/%{name}/poms
%{_datadir}/%{name}/repository
%{_datadir}/%{name}/repository-signed
%{_mavendepmapfragdir}/%{name}
%dir %{_javadir}/%{name}
%if %{bootstrap}
%{_datadir}/%{name}/bootstrap_repo
%endif
%doc

%changelog
* Wed Apr 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.2.1-23.4.1.osg
- Build with OpenJDK7

* Tue Jun 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> 2.2.1-23.4.0.osg
- Rebuild for osg on el5 and el6; build as bootstrap

* Sat Oct 15 2011 David Walluck <dwalluck@redhat.com> 2.2.1-23.4
- build as non-bootstrap

* Sat Oct 15 2011 David Walluck <dwalluck@redhat.com> 2.2.1-23.3
- fix M2_HOME in scripts

* Tue Oct 11 2011 David Walluck <dwalluck@redhat.com> 2.2.1-23.2
- fix some issues found with bootstap

* Mon Oct 10 2011 David Walluck <dwalluck@redhat.com> 2.2.1-23.1
- enable bootstrap
- BuildRequires: zip in bootstrap mode
- fix patch macros (for mdv)
- switch some build-jar-repository calls to build-classpath calls
- fix file list in bootstrap mode
- remove versioned classworlds-1.1.jar

* Mon Jul 18 2011 David Walluck <dwalluck@redhat.com> 2.2.1-23
- add missing org.apache.maven:maven-artifact-test

* Wed Feb 09 2011 David Walluck <dwalluck@redhat.com> 2.2.1-22
- own symlinks
- don't create symlinks outside of %%install
- use %%{_bindir} macro
- only use slf4j api and nop (drop jcl-over-slf4j and jdk14)

* Wed Dec 15 2010 David Walluck <dwalluck@redhat.com> 2.2.1-21
- add back Requires: maven2-common-poms

* Tue Dec 14 2010 David Walluck <dwalluck@redhat.com> 2.2.1-20
- partially merge with 2.2.1-16
- add Requires on jpackage-utils
- FIXME: unowned files due to post and preun build-jar-repository

* Thu Oct 28 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-19
- Create repository-signed

* Wed Oct 27 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-18
- Add __jpps_repo__ repository for signed JARs, located in
  /usr/share/maven2/repository-signed

* Fri Oct 22 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-17
- Use full path to build-jar-repository in post (mock problem?)

* Fri Oct 22 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-16
- Requires jpp-utils on post as we use build-jar-repository

* Fri Oct 22 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-15
- Adds (post) to jdom and classworlds (missing from last release fix)
- Backport fix from Deepak Bhole created for our 2.0.8 version:
  Handle RELEASE version strings properly

* Fri Oct 22 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-14
- Re-add backport-util-concurrent

* Fri Oct 22 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-13
- Remove backport-util-concurrent not necesary with JDK 1.5 onwards
- Make sure all packages used in post are Required(post)

* Wed Oct 20 2010 Hui Wang <huwang@redhat.com> - 2.2.1-12
- Add Requires: maven2-common-poms
- Add jpp depmap entry of plexus-container-default

* Tue Oct 19 2010 Fernando Nasser <fnasser@redhat.com> - 2.2.1-11
- Backport fixes from Deepak Bhole created for our 2.0.8 version:
  Honour the classifier field in the pom
  Handle artifacts other than just poms and jars

* Sun Sep 19 2010 Hui Wang <huwang@redhat.com> - 2.2.1-10
- Change BR maven-enforcer-rule-api to maven-enforcer-rules
- Add BR maven2-common-poms
- Add -P all-models to generate maven model v3

* Mon Aug 30 2010 Hui Wang <huwang@redhat.com> - 2.2.1-9
- Change jetty requires to jetty6

* Mon Aug 30 2010 Hui Wang <huwang@redhat.com> - 2.2.1-8
- Comment jna and svnkit requirements out
- Change BR maven-plugin-shade to maven-shade-plugin
- Change BR buildnumber-plugin-maven to mojo-maven2-plugin-buildnumber
- Add jdom jpp depmap

* Tue Jun 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-7
- Updated previous patch to only modify behaviour in JPP mode

* Mon Jun 28 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.1-6
- Disable parallel artifact resolution

* Wed Jun 23 2010 Yong Yang <yyang@redhat.com> 2.2.1-5
- Add Requires: maven-enforcer-plugin

* Fri Jun 18 2010 Deepak Bhole <dbhole@redhat.com> 2.2.1-4
- Final non-bootstrap build against non-bootstrap maven

* Fri Jun 18 2010 Deepak Bhole <dbhole@redhat.com> 2.2.1-3
- Added buildnumber plugin requirements
- Rebuild in non-bootstrap

* Thu Jun 17 2010 Deepak Bhole <dbhole@redhat.com> - 0:2.2.1-2
- Added support for dumping mapping info (in debug mode)
- Add a custom depmap
- Added empty-dep
- Added proper requirements
- Fixed classworlds jar name used at runtime
- Install individual components
- Install poms and mappings
- Remove non maven items from shaded uber jar
- Create dependency links in $M2_HOME/lib at install time

* Thu Nov 26 2009 Deepak Bhole <dbhole@redhat.com> - 0:2.2.1-1
- Initial bootstrap build
