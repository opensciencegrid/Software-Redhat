
Name: cog-jglobus-axis
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 1.2
Release: 1%{?dist}
URL: http://dev.globus.org/wiki/CoG_JGlobus_1.2
Group: System Environment/Libraries
Source0: http://www-unix.globus.org/cog/distribution/1.2/cog-1.2-src.tar.gz
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
BuildRequires: axis
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
%setup -q -n cog-%{version}

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

build-jar-repository -s -p lib cryptix cryptix-asn1 puretls commons-logging bcprov-1.33 log4j junit
mkdir -p axis/lib
build-jar-repository -s -p axis/lib axis

%patch -p0

%build
ant -Dsasl.present=false -Daxis.dir=axis jar

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
cp -p build/cog-axis.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/cog-axis-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*

%changelog
* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.2-1
- Initial packaging of COG-JGlobus 1.2.0, axis JAR only.


