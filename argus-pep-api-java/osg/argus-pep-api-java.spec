Summary: Argus PEP client Java API
Name: argus-pep-api-java
Version: 2.0.1
Release: 3%{?dist}
License: ASL 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: argus-pep-common
BuildRequires: java-devel
BuildRequires: maven2
BuildRequires: jpackage-utils
Requires: java
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: argus-pep-api-java-2.0.1-2.src.tar.gz
Source1: maven-surefire-plugin-2.4.3.jar
Source2: maven-surefire-plugin-2.4.3-fixed.pom

%description
Argus PEP client Java API (EMI)

%prep
 

%setup  

%build
mkdir -p /tmp/m2-repository; cp -rvf m2-repository/* /tmp/m2-repository
export JAVA_HOME=%{java_home}
%if 0%{?rhel} == 6
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dfile=%{SOURCE1} -DpomFile=%{SOURCE2} install:install-file
%endif
mvn -B -DskipTests -Dmaven.repo.local=/tmp/m2-repository -Petics install
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT/usr/share/java $RPM_BUILD_ROOT/usr/share/doc/argus-pep-api-java-2.0.1; test -f target/pep-java.jar && cp -v target/pep-java.jar $RPM_BUILD_ROOT/usr/share/java/argus-pep-api-java.jar && cp doc/* $RPM_BUILD_ROOT/usr/share/doc/argus-pep-api-java-2.0.1
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/argus-pep-api-java.jar
%dir /usr/share/doc/argus-pep-api-java-2.0.1/
/usr/share/doc/argus-pep-api-java-2.0.1/RELEASE-NOTES
/usr/share/doc/argus-pep-api-java-2.0.1/AUTHORS
/usr/share/doc/argus-pep-api-java-2.0.1/README
/usr/share/doc/argus-pep-api-java-2.0.1/COPYRIGHT
/usr/share/doc/argus-pep-api-java-2.0.1/LICENSE

%changelog
 
* Thu Mar 15 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.1-3.osg
- Use a maven-surefire-plugin-2.4.3 with a patched .pom for the build.

