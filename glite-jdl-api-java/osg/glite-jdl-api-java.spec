Summary: Java libraries handling Job Description Language
Name: glite-jdl-api-java
Version: 3.2.0
%global upstream_release 3
Release: %{upstream_release}.2%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildArch: noarch
Requires: jclassads
Requires: java7-devel
Requires: jpackage-utils
BuildRequires: ant, jclassads
BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Patch0: build.xml.patch
Patch1: ExtractFiles.java.patch

%description
Java libraries and utilities for dealing with Job Description Language

%prep
 
%setup -c -q
%patch0 -p0
%patch1 -p0

%build
# should be ${java_home} but that points to 1.6.0 for el6
export JAVA_HOME=/usr/lib/jvm/java-1.7.0
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  printf "dist.location=%{buildroot}
stage.location=
doc.location=%{buildroot}/%{_javadocdir}/%{name}
module.version=%{version}">.configuration.properties
  ant
fi


%install
export JAVA_HOME=/usr/lib/jvm/java-1.7.0
rm -rf %{buildroot}
mkdir -p %{buildroot}
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  ant install
else
  mkdir -p %{buildroot}/usr/share/java
  cp %{extbuilddir}/usr/share/java/glite-jdl-api-java.jar %{buildroot}/usr/share/java
  mkdir -p %{buildroot}/usr/share/doc/glite-jdl-api-java-%{version}
  cp %{extbuilddir}/usr/share/doc/glite-jdl-api-java-%{version}/LICENSE %{buildroot}/usr/share/doc/glite-jdl-api-java-%{version}
  mkdir -p %{buildroot}/%{_javadocdir}/%{name}
  cp -R %{extbuilddir}/usr/share/doc/glite-jdl-api-java/html %{buildroot}/%{_javadocdir}/%{name}
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/share/java/glite-jdl-api-java.jar
%dir /usr/share/doc/glite-jdl-api-java-%{version}/
%doc /usr/share/doc/glite-jdl-api-java-%{version}/LICENSE


%package doc
Summary: Documentation files for Job Description Language library
Group: Documentation
Requires: %{name}

%description doc
Documentation files for dealing with Job Description Language

%files doc
%defattr(-,root,root)
%dir %{_javadocdir}/%{name}/html/
%dir %{_javadocdir}/%{name}/html/resources/
%doc %{_javadocdir}/%{name}/html/resources/*.gif

%doc %{_javadocdir}/%{name}/html/*.html
%doc %{_javadocdir}/%{name}/html/stylesheet.css
%doc %{_javadocdir}/%{name}/html/package-list
%dir %{_javadocdir}/%{name}/html/org/
%dir %{_javadocdir}/%{name}/html/org/glite/
%dir %{_javadocdir}/%{name}/html/org/glite/jdl/
%doc %{_javadocdir}/%{name}/html/org/glite/jdl/*.html
%dir %{_javadocdir}/%{name}/html/org/glite/jdl/class-use/
%doc %{_javadocdir}/%{name}/html/org/glite/jdl/class-use/*.html


%changelog
* Thu Feb 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2.0-3.2
- Updates to build with JDK 7
- Require java7-devel, jpackage-utils explicitly
- Set JAVA_HOME explicity or else el6 finds 1.6.0
- Various different documentation .gif files are generated in JDK 7
- Patch source version and includeantruntime in build.xml to fix warnings
- Patch one java source file with non-ascii chars which breaks the build in 1.7

* Fri Jun 01 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.2.0-3.1
- Added dist tag

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 3.2.0-3.sl5
- Major bugs fixed

