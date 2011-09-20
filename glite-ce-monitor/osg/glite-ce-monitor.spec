Summary: The CE monitor service is a web application that publishes information about the Computing Element
Name: glite-ce-monitor
Version: 1.13.1
Release: 4%{?dist}
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

# Gonna have to change this for sl6 to tomcat6 -dds
Requires: tomcat5

Requires: httpd
Source0: glite-ce-monitor-1.13.1-3.src.tar.gz
Source1: build.xml
Source2: web.xml
Source3: osg-cemon.conf
Patch0: osg-config.patch

%description
The CE monitor service is a web application that publishes information about the Computing Element

%prep
%setup  
%patch0 -p1

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
 mkdir -p $RPM_BUILD_ROOT/var/lib/glite-ce-monitor
 mkdir -p $RPM_BUILD_ROOT/var/log/glite-ce-monitor
 mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
 install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/httpd/conf.d

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
%defattr(-,tomcat,tomcat)
%dir /var/lib/glite-ce-monitor
%dir /var/log/glite-ce-monitor
/etc/httpd/conf.d/osg-cemon.conf

%changelog
* Tue Sep 20 2011 Doug Strain <dstrain@fnal.gov> 1.13.1-4
- Created new osg rpm
- Added tomcat / apache requirements, apache conf file
- Added log and backend directories
