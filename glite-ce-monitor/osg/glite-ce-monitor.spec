Summary: The CE monitor service is a web application that publishes information about the Computing Element
Name: glite-ce-monitor
Version: 1.13.1
Release: 3.sl5
License: Apache License 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: OSG
BuildArch: noarch
BuildRequires: ant
BuildRequires: axis
BuildRequires: log4j
BuildRequires: jclassads
BuildRequires: jakarta-commons-codec
BuildRequires: bouncycastle
BuildRequires: tomcat5
BuildRequires: jakarta-commons-httpclient
BuildRequires: emi-trustmanager-tomcat
BuildRequires: emi-trustmanager-axis
BuildRequires: argus-pep-common
BuildRequires: jakarta-commons-logging
BuildRequires: jakarta-commons-discovery
BuildRequires: classpathx-jaf
BuildRequires: glite-ce-monitor-api-java
BuildRequires: glite-ce-common-java
BuildRequires: vomsjapi
BuildRequires: argus-pep-api-java
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source0: glite-ce-monitor-1.13.1-3.src.tar.gz
Source1: build.xml
Source2: web.xml

%description
The CE monitor service is a web application that publishes information about the Computing Element

%prep
%setup  

%build
cp %{SOURCE1} .
cp %{SOURCE2} $RPM_BUILD_ROOT

printf "stage.location=/usr
sysconfig.location=$RPM_BUILD_ROOT/etc
dist.location=$RPM_BUILD_ROOT/usr
tomcat.location=/usr/share/tomcat5
axis.location=$RPM_BUILD_ROOT/usr/local/axis1.4
axislib.location=/usr/share/java/axis
log4j.location=/usr/share/java
web_xml.location=$RPM_BUILD_ROOT
jclassads.location=/usr/share/java/jclassads
jaf.location=/usr/share/java
bcprov.location=/usr/share/java
hessian-java.location=/usr/share/java
jakarta-commons-codec.location=/usr/share/java
jakarta-commons-httpclient.location=/usr/share/java
jakarta-commons-logging.location=/usr/share/java
org.glite.ce.commonj.location=/usr
org.glite.ce.monitorapij.location=/usr
org.glite.security.utilj.location=/usr
org.glite.security.vomsapij.location=/usr
org.glite.authz.pep-common.location=/usr
org.glite.authz.pep-java.location=/usr
org.glite.security.trustmanager.location=/usr
module.version=1.13.1">.configuration.properties;
 ant
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 cp %{SOURCE2} $RPM_BUILD_ROOT
 ant install
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;
 rm $RPM_BUILD_ROOT/web.xml 

%clean
rm -rf $RPM_BUILD_ROOT

%pre



%post



%preun



%files
%defattr(-,root,root)
%dir /etc/glite-ce-monitor/
/etc/glite-ce-monitor/log4j.properties
/etc/glite-ce-monitor/cemonitor-config.xml.template
/etc/glite-ce-monitor/cemonitor-argus-config.xml
/etc/glite-ce-monitor/cemonitor-authz-config.xml
/etc/glite-ce-monitor/ce-monitor.xml
%dir /usr/share/webapps/
/usr/share/webapps/ce-monitor.war
/usr/share/java/glite-ce-monitor-RegExProcessor.jar
/usr/share/java/glite-ce-monitor.jar
/usr/share/java/glite-ce-monitor-ClassAdProcessor.jar
/usr/share/java/glite-ce-monitor-DoNotSendNotificationAction.jar
/usr/share/java/glite-ce-monitor-SendNotificationAction.jar
/usr/share/java/glite-ce-monitor-SendExpiredNotificationAction.jar
%dir /usr/share/doc/glite-ce-monitor-1.13.1/
/usr/share/doc/glite-ce-monitor-1.13.1/LICENSE

%changelog
 
