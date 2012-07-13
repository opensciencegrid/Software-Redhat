Summary: The java classes to integrate the trustmanager with axis2
Name: emi-trustmanager-axis2
Version: 1.0.1
%global upstream_release 1
Release: %{upstream_release}.1%{?dist}
License: Apache Software License
Vendor: ASL 2.0
Group: System Environment/Libraries
BuildArch: noarch
BuildRequires: emi-trustmanager
BuildRequires: bouncycastle
BuildRequires: axis2
%if 0%{?rhel} < 6
BuildRequires: tomcat5
%else
BuildRequires: tomcat6
%endif
BuildRequires: jakarta-commons-logging
BuildRequires: ant
BuildRequires: log4j
BuildRequires: java-devel
Requires: emi-trustmanager
Requires: bouncycastle
Requires: java
Requires: log4j
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
The java classes to integrate the trustmanager with axis2

%prep
 

%setup  

%build
 
 ant compile  -Dprefix=$RPM_BUILD_ROOT -Dstage=/
  
  

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
/usr/share/java/trustmanager-axis2.jar
%dir /usr/share/doc/trustmanager-axis2/
%dir /usr/share/doc/trustmanager-axis2/html/
/usr/share/doc/trustmanager-axis2/html/stylesheet.css
/usr/share/doc/trustmanager-axis2/html/package-list
/usr/share/doc/trustmanager-axis2/html/constant-values.html
%dir /usr/share/doc/trustmanager-axis2/html/resources/
/usr/share/doc/trustmanager-axis2/html/resources/inherit.gif
/usr/share/doc/trustmanager-axis2/html/help-doc.html
/usr/share/doc/trustmanager-axis2/html/allclasses-noframe.html
/usr/share/doc/trustmanager-axis2/html/index-all.html
/usr/share/doc/trustmanager-axis2/html/allclasses-frame.html
%dir /usr/share/doc/trustmanager-axis2/html/org/
%dir /usr/share/doc/trustmanager-axis2/html/org/glite/
%dir /usr/share/doc/trustmanager-axis2/html/org/glite/security/
%dir /usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/
%dir /usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/
/usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/package-summary.html
/usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/AXIS2SocketFactory.html
%dir /usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/class-use/
/usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/class-use/AXIS2SocketFactory.html
/usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/package-frame.html
/usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/package-use.html
/usr/share/doc/trustmanager-axis2/html/org/glite/security/trustmanager/axis2/package-tree.html
/usr/share/doc/trustmanager-axis2/html/index.html
/usr/share/doc/trustmanager-axis2/html/deprecated-list.html
/usr/share/doc/trustmanager-axis2/html/overview-tree.html
/usr/share/doc/trustmanager-axis2/LICENSE

%changelog
 
* Fri Jul 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.1-1.1.osg
- Rebuild for OSG; use tomcat6 on el6
