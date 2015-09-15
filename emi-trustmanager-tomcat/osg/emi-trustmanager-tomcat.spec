Summary: Tomcat and axis integration classes
Name: emi-trustmanager-tomcat
Version: 3.0.0
Release: 13%{?dist}
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
%if 0%{rhel} == 6
BuildRequires: tomcat6
%endif
%if 0%{rhel} == 7
BuildRequires: tomcat
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
Source2: server7.xml.template
Patch0: configure.patch
Patch1: build.xml.patch
Patch2: log4j-trustmanager.patch
Patch10: 0010-Tomcat-7-ServerSocketFactory-changed-from-abstract-c.patch
Patch11: 0011-Tomcat-7-Implement-getSSLUtil-in-TMSSLImplementation.patch
Patch12: 0012-Tomcat-7-getServerSocketFactory-that-takes-an-Abstra.patch
Patch13: 0013-Tomcat-7-Don-t-catch-ClassNotFoundException.patch
Patch14: 0014-Tomcat-7-Use-AbstractEndpoint.patch
Patch15: initproxy.patch
Patch16: configure_tomcat7.patch

%description
The classes for integrating the trustmanager with tomcat.

%prep
 

%setup  
%patch1 -p0
%patch2 -p1

%if 0%{?rhel} == 7
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p0
%patch16 -p0
%else
%patch0 -p0
%endif

%build
 
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT

export JAVA_HOME=/etc/alternatives/java_sdk

 ant dist -Dprefix=$RPM_BUILD_ROOT -Dstage=/ -Dant.build.javac.target=1.7
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

cp %SOURCE1 $RPM_BUILD_ROOT/var/lib/trustmanager-tomcat/config.properties
%if 0%{?rhel} == 7
cp %SOURCE2 $RPM_BUILD_ROOT/var/lib/trustmanager-tomcat/server7.xml.template
%endif

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
/var/lib/trustmanager-tomcat/server7.xml.template
/var/lib/trustmanager-tomcat/log4j-trustmanager.properties
/var/lib/trustmanager-tomcat/config.properties
/var/lib/trustmanager-tomcat/configure.sh

%changelog
* Tue Sep 15 2015 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-13
- Avoid NPE when initializing security settings.

* Wed Aug 12 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-12
- Patch to build on el7 (SOFTWARE-1604)

* Fri Aug 07 2015 Mátyás Selmeci (matyas@cs.wisc.edu) - 3.0.0-11
- Merge el7 changes into 3.3 branch

* Fri Apr 24 2015 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-10
- decrease trustmanager log level to WARN (SOFTWARE-1890)

* Tue Dec 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.0.0-9
- Build with 'tomcat' on el7

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

 
