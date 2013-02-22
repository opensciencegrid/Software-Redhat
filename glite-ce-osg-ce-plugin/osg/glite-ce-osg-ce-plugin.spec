Summary: The plugin is a sensor for the CE monitor service that accesses the Open Science Grid information system
Name: glite-ce-osg-ce-plugin
Version: 1.13.1
Release: 5%{?dist}
License: Apache License 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: ant
BuildRequires: glite-ce-monitor-api-java
BuildRequires: glite-ce-common-java
BuildRequires: java7-devel
BuildRequires: jpackage-utils
Requires: java7-devel
Requires: jpackage-utils
Requires: glite-ce-monitor
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: glite-ce-osg-ce-plugin-1.13.1-3.src.tar.gz
Patch0: build.xml.patch

%description
The plugin is a sensor for the CE monitor service that accesses the Open Science Grid information system

%prep
 

%setup  
%patch0 -p0

%build
# should be %{java_home}, but that points to 1.6.0 in el6
export JAVA_HOME=/usr/lib/jvm/java-1.7.0
printf "stage.location=/usr
dist.location=$RPM_BUILD_ROOT/usr
org.glite.ce.commonj.location=/usr
org.glite.ce.monitorapij.location=/usr
module.version=1.13.1">.configuration.properties;
 ant
  
  

%install
export JAVA_HOME=/usr/lib/jvm/java-1.7.0
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
* Fri Feb 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.13.1-5
- Updates to build with JDK 7; require java7-devel + jpackage-utils
- Explicitly set JAVA_HOME since it points to 1.6.0 in el6
- Patch build.xml to fix warning

* Mon Mar 12 2012 Doug Strain <dstrain@fnal.gov> 
- SOFTWARE-570: CEMon OSG plugin tomcat user should be in gip group
- Fixes writing problems to /var/log/gip and /var/cache/gip
 
