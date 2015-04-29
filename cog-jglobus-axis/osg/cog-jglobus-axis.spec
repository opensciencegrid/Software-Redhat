
Name: cog-jglobus-axis
Summary: An implementation of Globus for Java
License: Apache 2.0
Version: 1.8.0
Release: 7%{?dist}
URL: http://dev.globus.org/wiki/CoG_JGlobus_1.8.0
Group: System Environment/Libraries
Source0: http://www.globus.org/cog/distribution/1.8.0/cog-jglobus-fx-1.8.0-src.tar.gz
Source1: build.properties
BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java7-devel
BuildRequires: ant
BuildRequires: jpackage-utils
BuildRequires: jglobus
BuildRequires: axis
BuildRequires: jakarta-commons-httpclient
BuildRequires: jakarta-commons-logging
BuildRequires: junit
BuildRequires: /usr/share/java-1.7.0

Requires: java7
Requires: jpackage-utils
Requires: jglobus >= 2.0.0
Requires: jakarta-commons-httpclient
Requires: jakarta-commons-logging

%description
%{summary}

%prep
%setup -q -n jglobus-fx

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

pushd gsi

mkdir -p jwscore/lib
build-jar-repository -s -p jwscore/lib axis jglobus commons-httpclient junit jakarta-commons-logging

cp %{SOURCE1} .

popd

%build

pushd gsi
ant axisJar
popd

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}/
cp -p gsi/build/lib/cog-axis-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{_javadir}/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/cog-axis-%{version}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*

%changelog
* Fri Oct 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.8.0-7
- Bump to rebuild with latest jglobus2

* Thu Sep 05 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.8.0-6
- Bump to rebuild without Oracle JDK

* Thu Sep 05 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.8.0-5
- Bump to rebuild with latest jglobus2
- Add /usr/share/java-1.7.0 dependency to fix el5 build failure

* Tue Jul 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.8.0-4.1
- Make jglobus2 requirement explicit (SOFTWARE-1101)

* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.8.0-3
- Build with OpenJDK7

* Thu Sep 20 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.8.0-2
- Switch build to use jglobus2 instead of jglobus 1.8.

* Fri Mar 02 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.8.0-1
- Updated from cog-1.2 to jglobus-fx to get this JAR.

* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.2-1
- Initial packaging of COG-JGlobus 1.2.0, axis JAR only.


