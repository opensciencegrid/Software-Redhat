Summary: Argus PEP client Java API
Name: argus-pep-api-java
Version: 2.0.1
Release: 2%{?dist}
License: ASL 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: argus-pep-common
BuildRequires: java-devel
BuildRequires: maven2
Requires: java
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: argus-pep-api-java-2.0.1-2.src.tar.gz

%description
Argus PEP client Java API (EMI)

%prep
 

%setup  

%build
mkdir -p /tmp/m2-repository; cp -rvf m2-repository/* /tmp/m2-repository
 export JAVA_HOME=/usr/java/latest; mvn -DskipTests -Dmaven.repo.local=/tmp/m2-repository -Petics install
  
  

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
 
