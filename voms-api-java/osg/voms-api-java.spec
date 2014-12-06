# Use maven if it is available - otherwise fall back to ant
%if %{?fedora}%{!?fedora:0} >= 15 || %{?rhel}%{!?rhel:0} >= 7
%global maven 1
%else
%global maven 0
%endif

Name:		voms-api-java
Version:	2.0.8
Release:	1.6%{?dist}
Summary:	Virtual Organization Membership Service Java API

Group:		Development/Libraries
License:	ASL 2.0
URL:		http://glite.web.cern.ch/glite/
#		This source tarball is created from a git checkout:
#		git clone git://github.com/italiangrid/voms-api-java.git
#		cd voms-api-java
#		git archive --format tar --prefix voms-api-java-2.0.8/ 2_0_8 \
#		  | gzip - > ../voms-api-java-2.0.8.tar.gz
Source0:	%{name}-%{version}.tar.gz
#		These are build instructions for ant generated from the maven
#		build instrutions using the maven ant plugin.
#		These are used for building on EPEL since there is no maven
#		available there.
Source1:	build.xml
Source2:	maven-build.xml
Source3:	maven-build.properties
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

# There is no bouncycastle in EPEL 5 ppc and EPEL 6 ppc64
%if %{?rhel}%{!?rhel:0} == 5
ExcludeArch:	ppc
%endif
%if %{?rhel}%{!?rhel:0} == 6
ExcludeArch:	ppc64
%endif

Requires:	java7
Requires:	jpackage-utils
Requires:	bouncycastle >= 1.39
Requires:	jakarta-commons-cli
Requires:	jakarta-commons-lang
Requires:	log4j

Provides:	vomsjapi = %{version}-%{release}
Obsoletes:	vomsjapi < 2.0.7

BuildRequires:	java7-devel
BuildRequires:	jpackage-utils

%if %maven
BuildRequires:	maven-local
BuildRequires:	maven-compiler-plugin
BuildRequires:	maven-install-plugin
BuildRequires:	maven-jar-plugin
BuildRequires:	maven-javadoc-plugin
BuildRequires:	maven-release-plugin
BuildRequires:	maven-resources-plugin
BuildRequires:	maven-surefire-plugin
BuildRequires:	junit4
%else
BuildRequires:	ant
BuildRequires:	ant-junit
%endif

BuildRequires:	bouncycastle >= 1.39
BuildRequires:	jakarta-commons-cli
BuildRequires:	jakarta-commons-lang
BuildRequires:	log4j

%description
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

This package provides a java client API for VOMS.

%package javadoc
Summary:	Virtual Organization Membership Service Java API Documentation
Group:		Documentation
Requires:	jpackage-utils
Requires:	%{name} = %{version}-%{release}
Provides:	vomsjapi-javadoc = %{version}-%{release}
Obsoletes:	vomsjapi-javadoc < 2.0.7

%description javadoc
Virtual Organization Membership Service (VOMS) Java API Documentation.

%prep
%setup -q
install -m 644 %SOURCE1 .
install -m 644 %SOURCE2 .
install -m 644 %SOURCE3 .

sed -e s/bcprov-ext-jdk16/bcprov-jdk16/ -e s/1.45/1.46/ -i pom.xml

%build
%if %{maven}
mvn -B install javadoc:aggregate
%else
export CLASSPATH=$(build-classpath bcprov log4j commons-cli commons-lang)
ant package javadoc
%endif

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -m 644 target/%{name}-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}.jar $RPM_BUILD_ROOT%{_javadir}/vomsjapi.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if %{maven}
cp -pr target/site/javadoc/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%else
cp -pr target/site/apidocs $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%endif

%if %{maven}
mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a org.glite:vomsjapi
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
%{_javadir}/vomsjapi.jar
%if %{maven}
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%endif
%doc AUTHORS LICENSE

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}


%triggerpostun -- vomsjapi < 2.0.8
# vomsjapi also owns %{_javadir}/vomsjapi.jar.
# On some systems, vomsjapi and this package can be installed side-by-side.
# This results in the symlink getting removed if both packages are installed and vomsjapi is erased.
# Recreate the symlink if that is the case.
# Note that we do not want to create the symlink if this package is getting uninstalled too.
if [[ $1 -gt 0 && -e %{_javadir}/%{name}.jar ]]; then
    ln -sf %{name}.jar %{_javadir}/vomsjapi.jar
fi

%changelog
* Fri Dec 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.8-1.6
- Fix build failures on EL7

* Tue Feb 19 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.0.8-1.5
- Rebuilt with OpenJDK7 / changed java dependency to java7

* Tue Nov 20 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.4
- Fixed condition in triggerscript to not create a broken package if both packages are being removed.

* Tue Nov 20 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.3
- Add triggerscript to fix broken symlink issue with older vomsjapi package

* Mon Aug 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.2
- Rebuild for OSG

* Thu May 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.8-1
- Update to version 2.0.8 (EMI 2 version)

* Mon Apr 23 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.7-2
- Fix compatibility maven fragment

* Tue Mar 20 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.7-1
- The Java API is now a separate source tree from the rest of voms
