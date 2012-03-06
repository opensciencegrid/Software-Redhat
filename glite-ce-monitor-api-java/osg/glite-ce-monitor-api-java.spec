Summary: Java libraries for the CEMonitor service
Name: glite-ce-monitor-api-java
Version: 1.13.1
Release: 3%{?dist}
License: Apache License 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: ant
BuildRequires: axis
BuildRequires: glite-ce-common-java
BuildRequires: glite-ce-wsdl
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source0: glite-ce-monitor-api-java-1.13.1-3.src.tar.gz
Source1: build.xml

%description
Java libraries for the CEMonitor service

%prep
 

%setup  

%build
cp %{SOURCE1} .
printf "stage.location=/usr
org.glite.ce.wsdl.location=/usr
org.glite.ce.commonj.location=/usr
axis.location=/usr/local/axis1.4
axislib.location=/usr/share/java/axis
javashare.location=/usr/share/java
module.version=1.13.1
dist.location=$RPM_BUILD_ROOT/usr" >.configuration.properties;
 ant; mkdir -p wsdlfiles; cp -pfr $RPM_BUILD_ROOT/usr/share/glite-ce-monitor-api-java wsdlfiles
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
cp %{SOURCE1} .
 ant install; mkdir -p $RPM_BUILD_ROOT/usr/share; cp -pfr wsdlfiles/glite-ce-monitor-api-java $RPM_BUILD_ROOT/usr/share
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%pre



%post



%preun



%files
%defattr(-,root,root)
/usr/share/java/glite-ce-monitor-api-java.jar
%dir /usr/share/glite-ce-monitor-api-java/
/usr/share/glite-ce-monitor-api-java/ce-monitor-service-undeploy.wsdd
/usr/share/glite-ce-monitor-api-java/ce-monitor-consumer-undeploy.wsdd
/usr/share/glite-ce-monitor-api-java/ce-monitor-service-deploy.wsdd
/usr/share/glite-ce-monitor-api-java/ce-monitor-consumer-deploy.wsdd
%dir /usr/share/doc/glite-ce-monitor-api-java-1.13.1/
/usr/share/doc/glite-ce-monitor-api-java-1.13.1/LICENSE

%changelog
 
