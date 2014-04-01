%define local_maven /tmp/m2-repository
%define _noarchlib %{_exec_prefix}/lib

Name:		privilege-xacml
Version:	2.6.1
Release:	1%{?dist}
Summary:	OSG-core java depenency

Group:		OSG/Libraries
License:	Apache 2.0
#URL:		
Source0:	%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot


BuildRequires: jpackage-utils
BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRequires: voms-api-java
Requires: voms-api-java
BuildRequires: emi-trustmanager
Requires: emi-trustmanager
BuildRequires: log4j
BuildRequires: emi-trustmanager-axis
#Added this requirement to deal with the axis*.jar of dependencies
BuildRequires: jglobus
#Added to deal with axis* req
# Added to deal with build requirement xmltooling 
#BuildRequires: /usr/share/java/bestman2/gums2/xmltooling-1.3.3.jar


%if 0%{?rhel} < 6
BuildRequires: maven2
%define mvn %{_bindir}/mvn
%endif
%if 0%{?rhel} >= 6
%define mvn %{_bindir}/mvn22
#This is probably not right, but one thing at a time                                                                                                                                           
BuildRequires: maven22
%endif


#Requires:	

%description
%{summary}

%prep
%setup -q


%build

#log4j                                                                                                                                                                                         
%{mvn} install:install-file -B -DgroupId=log4j.log4j -DartifactId=log4j -Dversion=1.2.16 -Dpackaging=jar -Dfile=`build-classpath log4j` -Dmaven.repo.local=%{local_maven}

# Trustmanager is available from RPMs. I am just changing the name here from the OSG repo emi-trustmanager to the pom original one emi-security-trustmanager   
%{mvn} install:install-file -B -DgroupId=emi -DartifactId=emi-security-trustmanager -Dversion=3.0.3 -Dpackaging=jar -Dfile=`build-classpath trustmanager` -Dmaven.repo.local=%{local_maven}


#voms-api-java
%{mvn} install:install-file -B -DgroupId=voms -DartifactId=vomsjapi -Dversion=2.0.0 -Dpackaging=jar -Dfile=`build-classpath voms-api-java` -Dmaven.repo.local=%{local_maven}

#axis
#%{mvn} install:install-file -B -DgroupId=axis -DartifactId=axis -Dversion=1.4 -Dpackaging=jar -Dfile=`/usr/share/srm/lib/axis-1.4.jar` -Dmaven.repo.local=%{local_maven}
#%{mvn} install:install-file -B -DgroupId=org.apache.axis  -DartifactId=axis-jaxrpc -Dversion=1.4 -Dpackaging=jar -Dfile=`/usr/share/srm/lib/axis-jaxrpc-1.4.jar` -Dmaven.repo.local=%{local_maven}
#%{mvn} install:install-file -B -DgroupId=axis.axis-wsdl4j -DartifactId=axis-wdl4j -Dversion=1.5.1 -Dpackaging=jar -Dfile=`/usr/share/srm/lib/axis-wsdl4j-1.5.1.jar` -Dmaven.repo.local=%{local_maven}


#cog-jglobus
#%{mvn} install:install-file -B -DgroupId=globus.cog-jglobus -DartifactId=cog-jglobus -Dversion=1.8 -Dpackaging=jar -Dfile=`build-classpath jglobus` -Dmaven.repo.local=%{local_maven}

#joda-time
#%{mvn} install:install-file -B -DgroupId=joda-time.joda-time -DartifactId=joda-time -Dversion=1.6 -Dpackaging=jar -Dfile=`/usr/lib/gums/joda-time-1.6.2.jar` -Dmaven.repo.local=%{local_maven}

#xmltooloing
#%{mvn} install:install-file -B -DgroupId=opensaml.xmltooling -DartifactId=xmltooling -Dversion=1.3.1 -Dpackaging=jar -Dfile=`/usr/share/java/bestman2/gums2/xmltooling-1.3.3.jar` -Dmaven.repo.local=%{local_maven}
%{mvn} package

%install
rm -rf $RPM_BUILD_ROOT



%clean
rm -rf $RPM_BUILD_ROOT


%files
#%defattr(-,root,root,-)
#%doc



%changelog
* Thu Mar 27 2014 Edgar Fajardo <emfajard@ucsd.edu> 2.6.1-1
- Initial packaging of privilege-xacml
