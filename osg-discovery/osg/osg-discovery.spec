Name:           osg-discovery
Version:        1.0.7
Release:        3
Summary:        OSG Discovery Tools
Group:          System Environment
License:        Stanford (modified BSD with advert clause)
URL:            http://code.google.com/p/osg-discovery/

Source:        osg-discovery.tar.gz
Patch0:        avoid_npe.patch
Patch1:        system.pom.patch

BuildRoot:      %{_tmppath}/%{name}-root
BuildArch:      noarch
BuildRequires:  maven2 subversion
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

%build
# To download source
# svn checkout https://osg-discovery.googlecode.com/svn/osg/xpathsearch/trunk/  osg-discovery --username doug.strain
pushd osg
pushd discovery
sed -i "s/<scope>compile<\/scope>//" pom.xml
mvn install:install-file -Dfile=./external/el4j/lib/module-xml_merge-console-1.0.jar -DgroupId=ch.elca.el4j.modules -DartifactId=module-xml_merge-console -Dversion=1.0 -Dpackaging=jar
mvn install:install-file -Dfile=./external/el4j/lib/module-xml_merge-common-1.0.jar -DgroupId=ch.elca.el4j.modules -DartifactId=module-xml_merge-common -Dversion=1.0 -Dpackaging=jar
mvn install:install-file -Dfile=./external/xquery2007/lib/xqueryx-2007.jar -DgroupId=xquery -DartifactId=xqueryx -Dversion=2007 -Dpackaging=jar
mvn install:install-file -Dfile=./external/saxon/lib/saxon-9.1.0.7.jar -DgroupId=saxon -DartifactId=saxon -Dversion=9.1.0.7 -Dpackaging=jar
mvn install:install-file -Dfile=./external/dbxml/lib/dbxml-2.4.jar -DgroupId=oracle -DartifactId=dbxml -Dversion=2.4 -Dpackaging=jar
mvn install:install-file -Dfile=./external/dbxml/lib/db-2.4.jar -DgroupId=oracle -DartifactId=db -Dversion=2.4 -Dpackaging=jar


mvn -Pdev package assembly:attached
popd
popd
tar xzvf osg/discovery/target/discovery-*.tar.gz
mv discovery-1.0-r* discovery-built
sed -i "s/XPATHCACHE_DIR=.*/XPATHCACHE_DIR=~\/.osg-discovery/" discovery-built/conf/xpathsearch.rc

#Patch java detection in order to remove locate dependency
sed -i "s/\${JAVA_HOME}/\/usr/" discovery-built/bin/*
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
* Mon Jul 12 2011 Doug Strain <dstrain@fnal.gov> 1.0.6
Initial creation of spec file
