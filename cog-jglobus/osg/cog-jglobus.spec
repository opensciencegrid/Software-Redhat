
Name: cog-jglobus
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 1.8.0
Release: 1%{?dist}
URL: http://dev.globus.org/wiki/CoG_JGlobus_1.8.0
Group: System Environment/Libraries
Source0: http://www.globus.org/cog/distribution/1.8.0/cog-jglobus-1.8.0-src.tar.gz
Patch: build.xml-nosasl.patch
BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: ant
BuildRequires: jpackage-utils
BuildRequires: cryptix
BuildRequires: puretls
BuildRequires: bouncycastle13
BuildRequires: jakarta-commons-logging
BuildRequires: log4j
BuildRequires: junit

Requires: java
Requires: jpackage-utils
Requires: puretls
Requires: jakarta-commons-logging
Requires: bouncycastle13
Requires: log4j

%description
%{summary}

%prep
%setup -q

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

build-jar-repository -s -p lib cryptix cryptix-asn1 puretls commons-logging bcprov-1.33 log4j junit

%patch -p0

%build
ant -Dsasl.present=false

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
cp -p build/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-%{version}.jar
cp -p build/cog-jobmanager-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/cog-jobmanager-%{version}.jar
cp -p build/cog-url-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/cog-url-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*

%changelog
* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.8-1
- Initial packaging of JGlobus.


