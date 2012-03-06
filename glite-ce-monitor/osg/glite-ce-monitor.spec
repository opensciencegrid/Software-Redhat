Summary: The CE monitor service is a web application that publishes information about the Computing Element
Name: glite-ce-monitor
Version: 1.13.1
Release: 17%{?dist}
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
Requires: xml-commons-apis
# The following line added as a workaround for the JDK 'providing'
# xml-commons-apis, whereas we want the actual package of the same name.
Requires: /usr/share/java/xml-commons-apis.jar
Requires: glite-ce-osg-ce-plugin
Requires: vo-client

#Requires: httpd
#Requires: mod_ssl
Source0: glite-ce-monitor-1.13.1-3.src.tar.gz
Source1: build.xml
Source2: web.xml
Source3: glite-ce-monitor.logrotate
Source4: glite-ce-info
Patch0: osg-config.patch

%description
The CE monitor service is a web application that publishes information about the Computing Element

%prep
%setup  
%patch0 -p1

%build
# Increase heap size to avoid OutOfMemoryError
export ANT_OPTS="-Xmx2048m -Xms2048m -XX:-UseGCOverheadLimit"
cp %{SOURCE1} .
cp %{SOURCE2} $RPM_BUILD_ROOT
TEMP_BUILD_LOCATION=`pwd`
printf "stage.location=$RPM_BUILD_ROOT/usr
sysconfig.location=$RPM_BUILD_ROOT/etc
dist.location=$RPM_BUILD_ROOT/usr
var.location=$RPM_BUILD_ROOT/var/lib/glite-ce-monitor
tomcat.location=/usr/share/tomcat5
axis.location=$RPM_BUILD_ROOT/usr/local/axis1.4
axislib.location=/usr/share/java/axis
log4j.location=/usr/share/java
src.location=$TEMP_BUILD_LOCATION/src
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
org.glite.authz.pep-common.location=/usr/share/java
org.glite.authz.pep-java.location=/usr/share/java
org.glite.security.trustmanager.location=/usr
module.version=1.13.1">.configuration.properties;
 ant
  
  

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/tomcat5/Catalina/localhost
cp %{SOURCE2} $RPM_BUILD_ROOT
ant install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;
rm $RPM_BUILD_ROOT/web.xml 
mkdir -p $RPM_BUILD_ROOT/var/lib/glite-ce-monitor
mkdir -p $RPM_BUILD_ROOT/var/log/glite-ce-monitor
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/var/lib/glite-ce-monitor
cp $RPM_BUILD_ROOT/etc/glite-ce-monitor/ce-monitor.xml $RPM_BUILD_ROOT/etc/tomcat5/Catalina/localhost

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre



%post
certdir=/etc/grid-security/http
if [[ -e $certdir/hostcert.pem && ! -e $certdir/httpcert.pem ]]; then
    ln -s $certdir/hostcert.pem $certdir/httpcert.pem
fi
if [[ -e $certdir/hostkey.pem && ! -e $certdir/httpkey.pem ]]; then
    ln -s $certdir/hostkey.pem $certdir/httpkey.pem
fi



%preun



%files
%defattr(-,root,root)
%dir /etc/glite-ce-monitor/
%config(noreplace) /etc/glite-ce-monitor/log4j.properties
/etc/glite-ce-monitor/cemonitor-config.xml.template
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) /etc/glite-ce-monitor/cemonitor-config.xml
%config(noreplace) /etc/glite-ce-monitor/cemonitor-argus-config.xml
%config(noreplace) /etc/glite-ce-monitor/cemonitor-authz-config.xml
%config(noreplace) /etc/glite-ce-monitor/ce-monitor.xml
/usr/share/java/glite-ce-monitor/glite-ce-monitor-RegExProcessor.jar
/usr/share/java/glite-ce-monitor/glite-ce-monitor.jar
/usr/share/java/glite-ce-monitor/glite-ce-monitor-ClassAdProcessor.jar
/usr/share/java/glite-ce-monitor/glite-ce-monitor-DoNotSendNotificationAction.jar
/usr/share/java/glite-ce-monitor/glite-ce-monitor-SendNotificationAction.jar
/usr/share/java/glite-ce-monitor/glite-ce-monitor-SendExpiredNotificationAction.jar
%dir /usr/share/doc/glite-ce-monitor-1.13.1/
/usr/share/doc/glite-ce-monitor-1.13.1/LICENSE
%defattr(-,tomcat,tomcat)
/var/lib/glite-ce-monitor
%dir /var/log/glite-ce-monitor
%config(noreplace) /etc/tomcat5/Catalina/localhost/ce-monitor.xml

%changelog
* Tue Feb 17 2012 Doug Strain <dstrain@fnal.gov> - 1.13.1-17
- Set purge=true to prevent long reporting delays on startup
- Redirect stderr to a file in glite-ce-info
- Added logrotate

* Mon Nov 21 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.1-16
- Modified hostkey/hostcert default location in cemonitor-config.xml again.
- Added symlinks in post-install script to make upgrading easier.

* Fri Nov 18 2011 Burt Holzman <burt@fnal.gov> - 1.13.1-15
- Change OSG-CE sensor execution delay from 60000s to 600s

* Fri Oct 14 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.1-14
- Modified hostkey/hostcert default location in cemonitor-config.xml to match
  other software.

* Wed Oct 05 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.1-13
- Modified hostkey/hostcert default location in cemonitor-config.xml to match
  our documentation.
- Removed OSG subscription from cemonitor-config.xml since osg-configure will
  add it now.

* Tue Oct 04 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.1-12
- Removed httpd-related stuff, we're using tomcat without it

* Mon Oct 03 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.1-11
- Added mod_ssl as a dependency (since the configuration we provide depends on it.
- Marked config files as such

* Fri Sep 30 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.1-10
- Added workaround for xml-commons-apis not being brought in

* Thu Sep 22 2011 Doug Strain <dstrain@fnal.gov> 1.13.1-5
- Changing locations of some things so that CEMon works correctly
-- with tomcat5 from RHEL rpm

* Tue Sep 20 2011 Doug Strain <dstrain@fnal.gov> 1.13.1-4
- Created new osg rpm
- Added tomcat / apache requirements, apache conf file
- Added log and backend directories
