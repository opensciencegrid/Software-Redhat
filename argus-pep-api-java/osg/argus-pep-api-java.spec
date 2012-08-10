Summary: Argus PEP client Java API
Name: argus-pep-api-java
Version: 2.1.0
%global upstream_release 1
Release: %{upstream_release}.1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
BuildArch: noarch
BuildRequires: maven2
BuildRequires: jpackage-utils
BuildRequires: argus-pep-common
BuildRequires: argus-parent
BuildRequires: java-devel
Requires: voms-api-java
Requires: argus-pep-common
Requires: java
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz
Source1: maven-surefire-plugin-2.4.3.jar
Source2: maven-surefire-plugin-2.4.3-fixed.pom

%description
Argus PEP client Java API (EMI)

%prep
 

%setup  

%build
mkdir -p /tmp/m2-repository && cp -rvf m2-repository/* /tmp/m2-repository
export JAVA_HOME=%{java_home}
%if 0%{?rhel} == 6
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dfile=%{SOURCE1} -DpomFile=%{SOURCE2} install:install-file
%endif
mvn -DskipTests -B -Dmaven.repo.local=/tmp/m2-repository -PEMI install
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT/usr/share/java $RPM_BUILD_ROOT/usr/share/doc/argus-pep-api-java-2.1.0 && test -f target/pep-java.jar && cp -v target/pep-java.jar $RPM_BUILD_ROOT/usr/share/java/argus-pep-api-java-2.1.0.jar && cp doc/* $RPM_BUILD_ROOT/usr/share/doc/argus-pep-api-java-2.1.0 && cd $RPM_BUILD_ROOT/usr/share/java && ln -s argus-pep-api-java-2.1.0.jar argus-pep-api-java.jar
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/argus-pep-api-java-2.1.0.jar
/usr/share/java/argus-pep-api-java.jar
%dir /usr/share/doc/argus-pep-api-java-2.1.0/
/usr/share/doc/argus-pep-api-java-2.1.0/RELEASE-NOTES
/usr/share/doc/argus-pep-api-java-2.1.0/COPYRIGHT
/usr/share/doc/argus-pep-api-java-2.1.0/AUTHORS
/usr/share/doc/argus-pep-api-java-2.1.0/LICENSE
/usr/share/doc/argus-pep-api-java-2.1.0/README

%changelog
* Fri Jun 08 2012 Matyas Selmeci <matyas@cs.wisc.edu> 2.1.0-1.1
- Add osg changes
- Use a maven-surefire-plugin-2.4.3 with a patched .pom for the build.

* Tue Apr 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 2.1.0-1

- Initial PEP client Java API for EMI 2.



