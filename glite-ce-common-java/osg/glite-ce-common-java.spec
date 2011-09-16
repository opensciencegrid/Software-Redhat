Summary: Common libraries for all services running on the CREAM CE
Name: glite-ce-common-java
Version: 1.13.1
Release: 3.sl5
License: Apache License 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: OSG
BuildArch: noarch
BuildRequires: ant
BuildRequires: bouncycastle
BuildRequires: glite-ce-wsdl
BuildRequires: tomcat5
BuildRequires: emi-trustmanager-axis
BuildRequires: argus-pep-common
BuildRequires: emi-trustmanager
BuildRequires: axis
BuildRequires: vomsjapi
BuildRequires: argus-pep-api-java
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source0: glite-ce-common-java-1.13.1-3.src.tar.gz
Source1: build.xml

%description
Common libraries for all services running on the CREAM CE

%prep
 

%setup  

%build
printf "stage.location=/usr
tomcat.location=/usr/share/tomcat5
axis.location=/usr/local/axis1.4
javashare.location=/usr/share/java
axislib.location=/usr/share/java/axis
bcprov.location=/usr/share/java
org.glite.ce.wsdl.location=/usr
org.glite.security.utilj.location=/usr
org.glite.security.vomsapij.location=/usr
org.glite.authz.pep-common.location=/usr
org.glite.authz.pep-java.location=/usr
module.version=1.13.1
dist.location=$RPM_BUILD_ROOT/usr" >.configuration.properties
cp %{SOURCE1} .
 ant
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 cp %{SOURCE1} .
 ant install
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/glite-ce-common-java.jar
%dir /usr/share/doc/glite-ce-common-java-1.13.1/
/usr/share/doc/glite-ce-common-java-1.13.1/LICENSE

%changelog
 
