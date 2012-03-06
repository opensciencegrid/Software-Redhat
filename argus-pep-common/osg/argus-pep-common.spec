Summary: Argus PEP client and server common library (with hessian)
Name: argus-pep-common
Version: 2.1.0
Release: 2%{?dist}
License: ASL 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: java-devel
BuildRequires: maven2
Requires: java
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: argus-pep-common-2.1.0-2.src.tar.gz

%description
Argus PEP client and server Java common library (EMI)

%prep
 

%setup  

%build
mkdir -p /tmp/m2-repository; cp -rvf m2-repository/* /tmp/m2-repository
 export JAVA_HOME=/usr/java/latest; mvn -Dmaven.repo.local=/tmp/m2-repository -Petics install
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT/usr/share/java $RPM_BUILD_ROOT/usr/share/doc/argus-pep-common-2.1.0; test -f target/pep-common.jar && cp target/pep-common.jar $RPM_BUILD_ROOT/usr/share/java/argus-pep-common.jar && cp doc/* $RPM_BUILD_ROOT/usr/share/doc/argus-pep-common-2.1.0
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/argus-pep-common.jar
%dir /usr/share/doc/argus-pep-common-2.1.0/
/usr/share/doc/argus-pep-common-2.1.0/RELEASE-NOTES
/usr/share/doc/argus-pep-common-2.1.0/Hessian.LICENSE
/usr/share/doc/argus-pep-common-2.1.0/COPYRIGHT
/usr/share/doc/argus-pep-common-2.1.0/LICENSE

%changelog
 
