%define local_maven /tmp/m2-repository
%define mvn /usr/share/apache-maven-3.0.4/bin/mvn
%define _noarchlib %{_exec_prefix}/lib

Name:		privilege-xacml
Version:	2.6.1
Release:	1%{?dist}
Summary:	OSG-core java depenency

Group:		OSG/Libraries
License:	Apache 2.0
#URL:		
Source0:	%{name}-%{version}.tar.gz


# Binary JARs not available from public maven repos.  To be eliminated, one-by-one.
# From voms-admin-server
Source4: opensaml-2.4.1.jar 
#From gums 1.3.18
Source7: axis-wsdl4j-1.5.1.jar
# From cog-jglobus 1.8
# From voms-admin-server
#Source9: joda-time-1.6.2.jar
#Source10: xmltooling-1.3.1.jar
# From https://www.racf.bnl.gov/Facility/mvn_old/org/apache/xml/security/xml-security/1.4.1/
Source11: xml-security-1.4.1.jar
# From http://52north.org/maven/repo/releases/com/sun/sunxacml/1.2/
Source12: sunxacml-1.2.jar

# Patch to modify the dependencies on the pom, towards ones which are shipped in mayor repos
Patch0: dep-pom.xml.patch
Patch1: X509java.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot


BuildRequires: jpackage-utils
BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRequires: voms-api-java
BuildRequires: joda-time
Requires: voms-api-java
BuildRequires: emi-trustmanager
Requires: emi-trustmanager
BuildRequires: wsdl4j
#To deal with the xmltooling jar 
BuildRequires: voms-admin-server
Requires: wsdl4j
Requires: axis
Requires: bouncycastle
BuildRequires: bouncycastle
BuildRequires: log4j >= 1.2.14
BuildRequires: axis
#Added this requirement to deal with the axis*.jar of dependencies
BuildRequires: jglobus
Requires: jglobus
#Added this requiremnt to deal with the commons* dep
BuildRequires: jakarta-commons-codec
BuildRequires: jakarta-commons-discovery
BuildRequires: jakarta-commons-lang
BuildRequires: jakarta-commons-logging
BuildRequires: slf4j
BuildRequires: maven3


Requires: joda-time

#Requires:	

%description
%{summary}

%prep
%setup -q
%patch0 -p2
%patch1 -p2

%build
rm -fr %{local_maven}/*
#log4j                                                                                                                                                                                        
%{mvn} install:install-file -B -DgroupId=log4j.log4j -DartifactId=log4j -Dversion=1.2.14 -Dpackaging=jar -Dfile=`build-classpath log4j` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=emi -DartifactId=emi-security-trustmanager -Dversion=3.0.3 -Dpackaging=jar -Dfile=`build-classpath trustmanager` -Dmaven.repo.local=%{local_maven}
#voms-api-java
%{mvn} install:install-file -B -DgroupId=voms -DartifactId=vomsjapi -Dversion=2.0.0 -Dpackaging=jar -Dfile=`build-classpath voms-api-java` -Dmaven.repo.local=%{local_maven}

#axis
%{mvn} install:install-file -B  -DgroupId=axis -DartifactId=axis -Dversion=1.4 -Dpackaging=jar -Dfile=`build-classpath axis/axis.jar` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.apache.axis  -DartifactId=axis-jaxrpc -Dversion=1.4 -Dpackaging=jar -Dfile=`build-classpath axis/jaxrpc.jar` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=axis -DartifactId=axis-wsdl4j -Dversion=1.5.1 -Dpackaging=jar -Dfile=%{SOURCE7} -Dmaven.repo.local=%{local_maven}

#opensaml
%{mvn} install:install-file -B -DgroupId=opensaml -DartifactId=opensaml -Dversion=2.4.1 -Dpackaging=jar -Dfile=%{SOURCE4} -Dmaven.repo.local=%{local_maven}

#jakarta dependencies commons-codec
%{mvn} install:install-file -B -DgroupId=commons-codec -DartifactId=commons-codec -Dversion=1.3 -Dpackaging=jar -Dfile=`build-classpath jakarta-commons-codec` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=commons-discovery -DartifactId=commons-discovery -Dversion=0.4 -Dpackaging=jar -Dfile=`build-classpath jakarta-commons-discovery` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=commons-lang -DartifactId=commons-lang -Dversion=2.4 -Dpackaging=jar -Dfile=`build-classpath jakarta-commons-lang` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=commons-lang -DartifactId=commons-lang -Dversion=1.0.4 -Dpackaging=jar -Dfile=`build-classpath jakarta-commons-logging-api` -Dmaven.repo.local=%{local_maven}


#Since there is no longer cog-jglobus, I had to add manually all jglobus jars since I am not sure which one in specific it needs from the old cog-jglobus
#%{mvn} install:install-file -B -DgroupId=globus -DartifactId=cog-jglobus -Dversion=1.8 -Dpackaging=jar -Dfile=%{SOURCE8} -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=globus -DartifactId=jglobus-ssl-proxies -Dversion=2.0.6 -Dpackaging=jar -Dfile=`build-classpath jglobus/ssl-proxies-2.0.6.jar` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=globus -DartifactId=jglobus-gss -Dversion=2.0.6 -Dpackaging=jar -Dfile=`build-classpath jglobus/gss-2.0.6.jar` -Dmaven.repo.local=%{local_maven}
#joda-time
%{mvn} install:install-file -B -DgroupId=joda-time -DartifactId=joda-time -Dversion=1.5.2 -Dpackaging=jar -Dfile=`build-classpath joda-time` -Dmaven.repo.local=%{local_maven}

#xmltooloing
%{mvn} install:install-file -B -DgroupId=opensaml -DartifactId=xmltooling -Dversion=1.3.1 -Dpackaging=jar -Dfile=`build-classpath ../voms-admin/tools/lib/xmltooling-1.3.1.jar` -Dmaven.repo.local=%{local_maven}

#slf4j
%{mvn} install:install-file -B -DgroupId=org.slf4j -DartifactId=slf4j-api -Dversion=1.5.8 -Dpackaging=jar -Dfile=`build-classpath slf4j` -Dmaven.repo.local=%{local_maven}
%{mvn} install:install-file -B -DgroupId=org.slf4j -DartifactId=slf4j-simple -Dversion=1.5.8 -Dpackaging=jar -Dfile=`build-classpath slf4j` -Dmaven.repo.local=%{local_maven}

#xml-security
%{mvn} install:install-file -B -DgroupId=xml-security -DartifactId=xml-security -Dversion=1.4.1 -Dpackaging=jar -Dfile=%{SOURCE11} -Dmaven.repo.local=%{local_maven}
#sunxacml
%{mvn} install:install-file -B -DgroupId=sun -DartifactId=sunxacml -Dversion=1.2 -Dpackaging=jar -Dfile=%{SOURCE12} -Dmaven.repo.local=%{local_maven}
#bcprov
%{mvn} install:install-file -B -DgroupId=org.bouncycastle -DartifactId=bcprov-jdk15 -Dversion=1.46 -Dpackaging=jar -Dfile=`build-classpath bcprov` -Dmaven.repo.local=%{local_maven}

#jar tf %{local_maven}/globus/jglobus-ssl-proxies/2.0.6/jglobus-ssl-proxies-2.0.6.jar
%{mvn} generate-sources -Dmaven.repo.local=%{local_maven}
%{mvn} -B -X package -Dmaven.repo.local=%{local_maven}
#source src/test/XACMLClientTest.sh

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_javadir}
install -m 755 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -d -m 755 %{buildroot}/usr/share/maven3/poms
install -pm 644 pom.xml %{buildroot}/usr/share/maven3/poms/%{name}.pom



%clean
rm -rf %{buildroot}


%files
#%defattr(-,root,root,-)
#%doc
%{_javadir}/%{name}.jar
/usr/share/maven3/poms/%{name}.pom


%changelog
* Thu Mar 27 2014 Edgar Fajardo <emfajard@ucsd.edu> 2.6.1-1
- Initial packaging of privilege-xacml
