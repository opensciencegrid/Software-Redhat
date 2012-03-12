Summary: The plugin is a sensor for the CE monitor service that accesses the Open Science Grid information system
Name: glite-ce-osg-ce-plugin
Version: 1.13.1
Release: 4%{?dist}
License: Apache License 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: ant
BuildRequires: glite-ce-monitor-api-java
BuildRequires: glite-ce-common-java
Requires: glite-ce-monitor
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: glite-ce-osg-ce-plugin-1.13.1-3.src.tar.gz

%description
The plugin is a sensor for the CE monitor service that accesses the Open Science Grid information system

%prep
 

%setup  

%build
printf "stage.location=/usr
dist.location=$RPM_BUILD_ROOT/usr
org.glite.ce.commonj.location=/usr
org.glite.ce.monitorapij.location=/usr
module.version=1.13.1">.configuration.properties;
 ant
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 ant install
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add tomcat user to gip group
getent group gip >/dev/null || groupadd -r gip
getent group tomcat >/dev/null || groupadd -r tomcat
getent passwd tomcat >/dev/null || \
       useradd -r -g tomcat -d %{install_root} -c "Apache Tomcat user" \
       -s /bin/bash tomcat
usermod -a -G gip tomcat

%files
%defattr(-,root,root)
/usr/share/java/glite-ce-osg-ce-plugin.jar
%dir /usr/share/doc/glite-ce-osg-ce-plugin-1.13.1/
/usr/share/doc/glite-ce-osg-ce-plugin-1.13.1/LICENSE

%changelog
* Mon Mar 12 2012 Doug Strain <dstrain@fnal.gov> 
- SOFTWARE-570: CEMon OSG plugin tomcat user should be in gip group
- Fixes writing problems to /var/log/gip and /var/cache/gip
 
