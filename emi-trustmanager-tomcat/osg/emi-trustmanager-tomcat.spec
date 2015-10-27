Summary: Tomcat and axis integration classes
Name: emi-trustmanager-tomcat
Version: 3.0.0
Release: 10%{?dist}
License: Apache Software License
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: bouncycastle
BuildRequires: java7-devel
BuildRequires: jpackage-utils
%if 0%{rhel} <= 5
BuildRequires: tomcat5
%endif
%if 0%{rhel} > 5
BuildRequires: tomcat6
%endif
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0
BuildRequires: emi-trustmanager
BuildRequires: ant
BuildRequires: log4j
Requires: java7-devel
Requires: jpackage-utils
Requires: bouncycastle
Requires: emi-trustmanager
Requires: log4j
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: emi-trustmanager-tomcat-3.0.0-1.src.tar.gz
Source1: config.properties
Patch0: configure.patch
Patch1: build.xml.patch
Patch2: log4j-trustmanager.patch

%description
The classes for integrating the trustmanager with tomcat.

%prep
 

%setup  
%patch0 -p0
%patch1 -p0
%patch2 -p1

%build
 
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT

export JAVA_HOME=/etc/alternatives/java_sdk

 ant dist -Dprefix=$RPM_BUILD_ROOT -Dstage=/ -Dant.build.javac.target=1.7
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
/usr/share/doc/trustmanager-tomcat/html/resources/*.gif
/usr/share/doc/trustmanager-tomcat/html/index-all.html
%dir /var/lib/trustmanager-tomcat/
/var/lib/trustmanager-tomcat/server.xml.template
/var/lib/trustmanager-tomcat/log4j-trustmanager.properties
/var/lib/trustmanager-tomcat/config.properties
/var/lib/trustmanager-tomcat/configure.sh

%changelog
* Fri Apr 24 2015 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-10
- decrease trustmanager log level to WARN (SOFTWARE-1890)

* Tue May 07 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-8
- Require missing java dir names instead of workaround package

* Wed Apr 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-7
- Rebuild for updated build dependency
- Use /etc/alternatives instead of hard coding java-1.7.0 path

* Tue Mar 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-6
- Workaround: Require missing-java-1.7.0-dirs in el5

* Thu Feb 21 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-5
- Updates for JDK 7, require java7-devel + jpackage-utils
- Explicitly point JAVA_HOME to java-1.7.0 to deal with el6 issue
- Various different documentation .gif files are generated in JDK 7
- Patch build.xml to change java target from 1.5->1.7, and fix a warning

* Mon Mar 19 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.0-4
rebuild with tomcat6 on el6

* Fri Jul 22 2011 Tanya Levshina <tlevshin@fnal.gov - 3.0.0-3
added requires (java-sun), buildrequires (java-sun-devel)

* Mon Jul 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-2
Patch trustmanager with OSG defaults and FHS standards.

 
