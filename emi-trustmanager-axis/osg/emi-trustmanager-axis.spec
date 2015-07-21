Summary: The java classes to integrate trustmanager with axis.
Name: emi-trustmanager-axis
Version: 1.0.1
Release: 1.4%{?dist}
License: Apache Software License
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: bouncycastle
%if 0%{rhel} <= 5
BuildRequires: tomcat5
%endif
%if 0%{rhel} == 6
BuildRequires: tomcat6
%endif
%if 0%{rhel} == 7
BuildRequires: tomcat
%endif
BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRequires: emi-trustmanager
BuildRequires: ant
BuildRequires: log4j
BuildRequires: axis
Requires: emi-trustmanager
Requires: axis
Requires: java7
Requires: jpackage-utils
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: emi-trustmanager-axis-1.0.1-1.src.tar.gz
Patch0: build.xml.patch


%description
The java classes to integrate trustmanager with axis.

%prep
 

%setup  

%patch0 -p0

%build
 
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 ant dist -Dprefix=$RPM_BUILD_ROOT -Dstage=/
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/trustmanager-axis.jar
%dir /usr/share/doc/trustmanager-axis/
/usr/share/doc/trustmanager-axis/USAGE
/usr/share/doc/trustmanager-axis/README
/usr/share/doc/trustmanager-axis/LICENSE
%dir /usr/share/doc/trustmanager-axis/html/
/usr/share/doc/trustmanager-axis/html/index.html
/usr/share/doc/trustmanager-axis/html/overview-frame.html
/usr/share/doc/trustmanager-axis/html/overview-tree.html
/usr/share/doc/trustmanager-axis/html/allclasses-frame.html
/usr/share/doc/trustmanager-axis/html/constant-values.html
/usr/share/doc/trustmanager-axis/html/overview-summary.html
/usr/share/doc/trustmanager-axis/html/package-list
/usr/share/doc/trustmanager-axis/html/stylesheet.css
/usr/share/doc/trustmanager-axis/html/serialized-form.html
/usr/share/doc/trustmanager-axis/html/allclasses-noframe.html
%dir /usr/share/doc/trustmanager-axis/html/org/
%dir /usr/share/doc/trustmanager-axis/html/org/glite/
%dir /usr/share/doc/trustmanager-axis/html/org/glite/security/
%dir /usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/
%dir /usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/SSLConfigSender.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/package-frame.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/AXISSocketFactory.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/package-tree.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/package-summary.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/package-use.html
%dir /usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/class-use/
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/class-use/SSLConfigSender.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/trustmanager/axis/class-use/AXISSocketFactory.html
%dir /usr/share/doc/trustmanager-axis/html/org/glite/security/util/
%dir /usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/
/usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/package-frame.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/package-tree.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/package-summary.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/package-use.html
%dir /usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/class-use/
/usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/class-use/InitSecurityContext.html
/usr/share/doc/trustmanager-axis/html/org/glite/security/util/axis/InitSecurityContext.html
/usr/share/doc/trustmanager-axis/html/deprecated-list.html
/usr/share/doc/trustmanager-axis/html/help-doc.html
%dir /usr/share/doc/trustmanager-axis/html/resources/
/usr/share/doc/trustmanager-axis/html/resources/*.gif
/usr/share/doc/trustmanager-axis/html/index-all.html

%changelog
* Tue Dec 02 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.1-1.4
- Build with tomcat on el7

* Tue Feb 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.1-1.3
- build with tomcat6 on el6 (SOFTWARE-1279)

* Mon Apr 01 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0.1-1.2
- Build for OpenJDK7

