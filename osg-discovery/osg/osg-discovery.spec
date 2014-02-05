Name:           osg-discovery
Version:        1.0.7
Release:        6%{?dist}
Summary:        OSG Discovery Tools
Group:          System Environment
License:        Stanford (modified BSD with advert clause)
URL:            http://code.google.com/p/osg-discovery/

Source0:        osg-discovery.tar.gz
Source1:        maven.patch
Patch0:        avoid_npe.patch
Patch1:        system.pom.patch
Patch2:        nogrizzly.patch

BuildRoot:      %{_tmppath}/%{name}-root
BuildArch:      noarch
BuildRequires:  maven22 subversion dos2unix java7-devel jpackage-utils
Requires:  java

%description
The OSG Discovery Tool allows users to discover the BDII information 
they need in order to use grid resources. 
Commands print out storage and computing resources for a given
virtual organization (VO)

%prep
%setup -q -n %{name}
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
# To download source
# svn checkout https://osg-discovery.googlecode.com/svn/osg/xpathsearch/trunk/  osg-discovery --username doug.strain

rm osg/discovery/xpathsearch/src/main/java/gov/fnal/xpathsearch/rest/RunXPathSearchResource.java
pushd osg
pushd discovery
sed -i "s/<scope>compile<\/scope>//" pom.xml
sed -i "s/<doUpdate>true<\/doUpdate>/<doUpdate>false<\/doUpdate>/" pom.xml
mvn22 install:install-file -npu -npr -c -Dfile=./external/el4j/lib/module-xml_merge-console-1.0.jar -DgroupId=ch.elca.el4j.modules -DartifactId=module-xml_merge-console -Dversion=1.0 -Dpackaging=jar
mvn22 install:install-file -npu -npr -c -Dfile=./external/el4j/lib/module-xml_merge-common-1.0.jar -DgroupId=ch.elca.el4j.modules -DartifactId=module-xml_merge-common -Dversion=1.0 -Dpackaging=jar
mvn22 install:install-file -npu -npr -c -Dfile=./external/xquery2007/lib/xqueryx-2007.jar -DgroupId=xquery -DartifactId=xqueryx -Dversion=2007 -Dpackaging=jar
mvn22 install:install-file -npu -npr -c -Dfile=./external/saxon/lib/saxon-9.1.0.7.jar -DgroupId=saxon -DartifactId=saxon -Dversion=9.1.0.7 -Dpackaging=jar
mvn22 install:install-file -npu -npr -c -Dfile=./external/dbxml/lib/dbxml-2.4.jar -DgroupId=oracle -DartifactId=dbxml -Dversion=2.4 -Dpackaging=jar
mvn22 install:install-file -npu -npr -c -Dfile=./external/dbxml/lib/db-2.4.jar -DgroupId=oracle -DartifactId=db -Dversion=2.4 -Dpackaging=jar

#sha1sum /usr/share/maven2/bootstrap_repo/JPP/maven2/poms/JPP.maven-surefire-surefire.pom > /usr/share/maven2/bootstrap_repo/JPP/maven2/poms/JPP.maven-surefire-surefire.pom.sha1


mvn22 -e -npu -npr -c -X -Pdev package assembly:attached || true
ls -R ~/.m2
pushd ~/.m2/repository/org/apache/maven/plugins/maven-surefire-plugin/2.4.3
dos2unix *.pom
patch -p0 < %SOURCE1
popd
mvn22 -e -npu -npr -c -X -Pdev package


popd
popd

# tar xzvf osg/discovery/target/discovery-*.tar.gz
# mv discovery-1.0-r* discovery-built
mkdir discovery-built
mkdir discovery-built/bin
mkdir discovery-built/lib
cp osg/discovery/xpathsearch/target/filtered/src/main/bin/* discovery-built/bin
cp osg/discovery/xpathsearch/src/main/bin/*.xq discovery-built/bin
cp osg/discovery/xpathsearch/src/main/resources/xquery/* discovery-built/bin
cp -arp osg/discovery/xpathsearch/src/main/conf discovery-built
cp osg/discovery/xpathsearch/target/filtered/src/main/doc/* discovery-built

#libs
cp ~/.m2/repository/javax/activation/activation/1.1/activation-1.1.jar discovery-built/lib
#cp ~/.m2/repository/asm/asm/3.1/asm-3.1.jar discovery-built/lib
cp ~/.m2/repository/commons-cli/commons-cli/1.2/commons-cli-1.2.jar discovery-built/lib
cp ~/.m2/repository/commons-codec/commons-codec/1.2/commons-codec-1.2.jar discovery-built/lib
cp ~/.m2/repository/commons-logging/commons-logging/1.0.4/commons-logging-1.0.4.jar discovery-built/lib
cp ~/.m2/repository/javax/xml/bind/jaxb-api/2.1/jaxb-api-2.1.jar discovery-built/lib
cp ~/.m2/repository/jdom/jdom/1.0/jdom-1.0.jar discovery-built/lib
cp ~/.m2/repository/javax/ws/rs/jsr311-api/1.1/jsr311-api-1.1.jar discovery-built/lib
cp ~/.m2/repository/log4j/log4j/1.2.14/log4j-1.2.14.jar discovery-built/lib
cp ~/.m2/repository/saxon/saxon/9.1.0.7/saxon-9.1.0.7.jar discovery-built/lib
cp ~/.m2/repository/xalan/serializer/2.7.1/serializer-2.7.1.jar discovery-built/lib
cp ~/.m2/repository/javax/servlet/servlet-api/2.5/servlet-api-2.5.jar discovery-built/lib
cp ~/.m2/repository/javax/xml/stream/stax-api/1.0-2/stax-api-1.0-2.jar discovery-built/lib
cp ~/.m2/repository/stax/stax-api/1.0.1/stax-api-1.0.1.jar discovery-built/lib
cp ~/.m2/repository/stax/stax/1.2.0/stax-1.2.0.jar discovery-built/lib
cp ~/.m2/repository/xalan/xalan/2.7.1/xalan-2.7.1.jar discovery-built/lib
cp ~/.m2/repository/xerces/xercesImpl/2.9.0/xercesImpl-2.9.0.jar discovery-built/lib
cp ~/.m2/repository/xml-apis/xml-apis/1.3.04/xml-apis-1.3.04.jar discovery-built/lib

cp osg/discovery/openldap-jldap/target/*.jar discovery-built/lib
cp osg/discovery/xpathsearch/target/*.jar discovery-built/lib

sed -i "s/XPATHCACHE_DIR=.*/XPATHCACHE_DIR=~\/.osg-discovery/" discovery-built/conf/xpathsearch.rc

#Patch java detection in order to remove locate dependency
sed -i "s/\${JAVA_HOME}/\/usr/" discovery-built/bin/*
sed -i "s/EOF)/EOF\n)/" discovery-built/bin/*
sed -i "s/\. \$XPATHSEARCH_HOME\/bin\/detect-java.sh//" discovery-built/bin/*

#add back external libraries
cp osg/discovery/external/dbxml/lib/*.jar discovery-built/lib
cp osg/discovery/external/el4j/lib/*.jar discovery-built/lib
cp osg/discovery/external/saxon/lib/*.jar discovery-built/lib
cp osg/discovery/external/xquery2007/lib/*.jar discovery-built/lib

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}

pushd discovery-built
rm bin/detect-java.sh
for i in `ls bin`; do
	install -m 0755 bin/$i $RPM_BUILD_ROOT%{_bindir}
done
for i in `ls lib`; do
	install -m 0644 lib/$i $RPM_BUILD_ROOT%{_javadir}/%{name}
done
install -m 0644 conf/xpathsearch.properties $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -m 0644 conf/xpathsearch.rc $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
popd

mkdir -p $RPM_BUILD_ROOT/var/run/%{name}
mkdir -p $RPM_BUILD_ROOT/var/log/%{name}

%files
%{_bindir}/*
%{_javadir}/%{name}/*
%{_sysconfdir}/%{name}/xpathsearch.rc
%{_sysconfdir}/%{name}/xpathsearch.properties
/var/run/%{name}
/var/log/%{name}


%changelog
* Tue Feb 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.7-6
- Updating to build with maven22

* Tue Apr 03 2012 Doug Strain <dstrain@fnal.gov> 1.0.7-5
- Updating to get rid of grizzly web server and build on SL6
- Also fixing EOF bash here-documents to not give warnings

* Mon Jul 12 2011 Doug Strain <dstrain@fnal.gov> 1.0.6
Initial creation of spec file
