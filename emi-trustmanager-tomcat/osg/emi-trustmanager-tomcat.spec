Summary: Tomcat and axis integration classes
Name: emi-trustmanager-tomcat
Version: 3.0.0
Release: 2
License: Apache Software License
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: bouncycastle
BuildRequires: java-devel
BuildRequires: tomcat5
BuildRequires: emi-trustmanager
BuildRequires: ant
BuildRequires: log4j
Requires: bouncycastle
Requires: emi-trustmanager
Requires: log4j
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: emi-trustmanager-tomcat-3.0.0-1.src.tar.gz
Source1: config.properties
Patch0: configure.patch

%description
The classes for integrating the trustmanager with tomcat.

%prep
 

%setup  
%patch0 -p0

%build
 
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 ant dist -Dprefix=$RPM_BUILD_ROOT -Dstage=/ -Dant.build.javac.target=1.5
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

cp %SOURCE1 $RPM_BUILD_ROOT/var/lib/trustmanager-tomcat/config.properties

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/trustmanager-tomcat.jar
%dir /usr/share/doc/trustmanager-tomcat/
/usr/share/doc/trustmanager-tomcat/USAGE
/usr/share/doc/trustmanager-tomcat/INSTALL
%dir /usr/share/doc/trustmanager-tomcat/html/
/usr/share/doc/trustmanager-tomcat/html/index.html
/usr/share/doc/trustmanager-tomcat/html/overview-tree.html
/usr/share/doc/trustmanager-tomcat/html/allclasses-frame.html
/usr/share/doc/trustmanager-tomcat/html/constant-values.html
/usr/share/doc/trustmanager-tomcat/html/package-list
/usr/share/doc/trustmanager-tomcat/html/stylesheet.css
/usr/share/doc/trustmanager-tomcat/html/allclasses-noframe.html
%dir /usr/share/doc/trustmanager-tomcat/html/org/
%dir /usr/share/doc/trustmanager-tomcat/html/org/glite/
%dir /usr/share/doc/trustmanager-tomcat/html/org/glite/security/
%dir /usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/
%dir /usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/package-frame.html
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/TMSSLServerSocketFactory.html
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/package-tree.html
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/package-summary.html
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/package-use.html
%dir /usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/class-use/
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/class-use/TMSSLServerSocketFactory.html
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/class-use/TMSSLImplementation.html
/usr/share/doc/trustmanager-tomcat/html/org/glite/security/trustmanager/tomcat/TMSSLImplementation.html
/usr/share/doc/trustmanager-tomcat/html/deprecated-list.html
/usr/share/doc/trustmanager-tomcat/html/help-doc.html
%dir /usr/share/doc/trustmanager-tomcat/html/resources/
/usr/share/doc/trustmanager-tomcat/html/resources/inherit.gif
/usr/share/doc/trustmanager-tomcat/html/index-all.html
%dir /var/lib/trustmanager-tomcat/
/var/lib/trustmanager-tomcat/server.xml.template
/var/lib/trustmanager-tomcat/log4j-trustmanager.properties
/var/lib/trustmanager-tomcat/config.properties
/var/lib/trustmanager-tomcat/configure.sh

%changelog
* Mon Jul 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-2
Patch trustmanager with OSG defaults and FHS standards.

 
