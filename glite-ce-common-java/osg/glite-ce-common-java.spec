Summary: Common libraries for all services running on the CREAM CE
Name: glite-ce-common-java
Version: 1.14.0
%global upstream_release 4
Release: %{upstream_release}.2%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildArch: noarch
BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: xml-commons-apis
BuildRequires: axis2
BuildRequires: bouncycastle
%if %undefined extbuilddir
BuildRequires: argus-pep-common
BuildRequires: argus-pep-api-java >= 2.1.0
BuildRequires: emi-trustmanager
BuildRequires: voms-api-java
%endif
# previously java was implied by subpackages
BuildRequires: java7-devel
BuildRequires: jpackage-utils
Requires: java7-devel
Requires: jpackage-utils


%if 0%{?rhel} > 5
%global _tomcat tomcat6
%global _tomcatclibdir /usr/share/java/tomcat6
BuildRequires: tomcat6-servlet-2.5-api
%else
%global _tomcat tomcat5
%global _tomcatclibdir /var/lib/tomcat5/common/lib
BuildRequires: tomcat5-servlet-2.4-api
%endif

Requires: axis2
Requires: bouncycastle 
Requires: %_tomcat
Requires: argus-pep-common
Requires: argus-pep-api-java >= 2.1.0
Requires: emi-trustmanager
Requires: voms-api-java
Requires: jclassads
Requires: mysql-connector-java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Patch0: build.patch

%description
Common libraries for all services running on the CREAM CE

%prep
%setup -c -q
%patch0 -p1

%build
%if %undefined extbuilddir
  printf "dist.location=%{buildroot}
doc.location=%{buildroot}/%{_javadocdir}/%{name}
stage.location=/
module.version=%{version}">.configuration.properties
  ant
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
%if %undefined extbuilddir
  ant install
%else
  mkdir -p %{buildroot}/usr/share/java
  cp %{extbuilddir}/usr/share/java/*.jar %{buildroot}/usr/share/java
  mkdir -p %{buildroot}/etc/glite-ce-common-java
  cp -R %{extbuilddir}/etc/glite-ce-common-java/* %{buildroot}/etc/glite-ce-common-java
  mkdir -p %{buildroot}/usr/share/doc/glite-ce-common-java-%{version}
  cp %{extbuilddir}/usr/share/doc/glite-ce-common-java-%{version}/LICENSE %{buildroot}/usr/share/doc/glite-ce-common-java-%{version}
  mkdir -p %{buildroot}/%{_javadocdir}/%{name}
  cp -R %{extbuilddir}/usr/share/doc/glite-ce-common-java/html %{buildroot}/%{_javadocdir}/%{name}
%endif
 

%clean
rm -rf %{buildroot} 

%post
if [ $1 -eq 1 ] ; then
  
  touch /etc/grid-security/admin-list
  
  # JDBC driver must be loaded by the same classloader used for dbcp
  ln -s /usr/share/java/mysql-connector-java.jar %{_tomcatclibdir}/mysql-connector-java_forcream.jar


fi

%preun
if [ $1 -eq 0 ] ; then

  rm -f %{_tomcatclibdir}/mysql-connector-java_forcream.jar
 
fi


%files
%defattr(-,root,root)
/usr/share/java/*.jar
%dir /usr/share/doc/glite-ce-common-java-%{version}/
%doc /usr/share/doc/glite-ce-common-java-%{version}/LICENSE
%dir /etc/glite-ce-common-java
%config(noreplace) /etc/glite-ce-common-java/*

%package doc
Summary: Documentation files for the CREAM Common library
Group: Documentation
Requires: %{name}

%description doc
Documentation files for the CREAM Common library

%files doc
%defattr(-,root,root)
%dir %{_javadocdir}/%{name}/html/
%dir %{_javadocdir}/%{name}/html/resources/
%doc %{_javadocdir}/%{name}/html/resources/inherit.gif

%doc %{_javadocdir}/%{name}/html/*.html
%doc %{_javadocdir}/%{name}/html/stylesheet.css
%doc %{_javadocdir}/%{name}/html/package-list
%dir %{_javadocdir}/%{name}/html/org/
%dir %{_javadocdir}/%{name}/html/org/glite/
%dir %{_javadocdir}/%{name}/html/org/glite/ce/
%dir %{_javadocdir}/%{name}/html/org/glite/ce/commonj/
%dir %{_javadocdir}/%{name}/html/org/glite/ce/commonj/configuration/
%dir %{_javadocdir}/%{name}/html/org/glite/ce/commonj/configuration/xppm/
%doc %{_javadocdir}/%{name}/html/org/glite/ce/commonj/configuration/xppm/*.html
%dir %{_javadocdir}/%{name}/html/org/glite/ce/commonj/configuration/xppm/class-use/
%doc %{_javadocdir}/%{name}/html/org/glite/ce/commonj/configuration/xppm/class-use/*.html

%changelog
* Tue Nov 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.2.osg
- Bump to rebuild

* Thu Jun 07 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.1.osg
- Added dist tag
- Tweaked macros
- Added versions to dependencies

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 1.14.0-4.sl5
- Major bugs fixed



