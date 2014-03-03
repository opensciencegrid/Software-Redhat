## Turn off meaningless jar repackaging 
%define __jar_repack 0

Summary: The VOMS Administration service
Name: voms-admin-server
Version: 2.7.0
Release: 1.9%{?dist}
License:    ASL 2.0
Group: System Environment/Libraries
BuildRequires:  maven22
BuildRequires:  jpackage-utils
BuildRequires:  java7-devel
BuildRequires:  emi-trustmanager
BuildRequires:  emi-trustmanager-axis
BuildRequires:  /usr/share/java/jta.jar

Requires: jpackage-utils
Requires: java7-devel
Requires: emi-trustmanager
Requires: emi-trustmanager-tomcat
Requires: bouncycastle >= 1.39
%if 0%{?rhel} <= 5
Requires: tomcat5
Requires: fetch-crl3
%define tomcat tomcat5
%define tomcat_lib /usr/share/tomcat5/common/lib
%define tomcat_endorsed /usr/share/tomcat5/common/endorsed
%define catalina_home /usr/share/tomcat5
%endif
%if 0%{?rhel} == 6
Requires: tomcat6
Requires: fetch-crl
%define tomcat tomcat6
%define tomcat_lib /usr/share/tomcat6/lib
%define tomcat_endorsed /usr/share/tomcat6/endorsed
%define catalina_home /usr/share/tomcat6
%endif
Requires: xml-commons-apis 
Requires(post):/sbin/chkconfig
Requires(preun):/sbin/chkconfig
Requires(preun):/sbin/service
Requires(postun):/sbin/service
# The following requirement makes sure we get the RPM that provides this,
# and not just the JDK which happens to provide it, but not in the right spot. 
Requires: /usr/share/java/xml-commons-apis.jar
Requires: grid-certificates 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
AutoReqProv: yes
Source0:  %{name}-%{version}.tar.gz
Patch1: directory-defaults.patch
Patch2: maven-resources-disable.patch
Patch3: cern-mirror-disable.patch
Patch4: trustmanager-versions.patch
Patch5: fix-suspended-users.patch
Patch6: fix-certificate-issuer-check.patch

Requires: osg-webapp-common
Requires: glite-security-util-java

%description
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

The VOMS Admin service is a web application providing tools for administering
the VOMS VO structure. It provides an intuitive web user interface for daily
administration tasks.

%prep


%setup -q -n voms-admin
%patch1 -p0
%if 0%{?rhel} == 6
# Tried to "BuildRequires: maven-resources-plugin" like in voms-admin-client,
# but it gave me an odd NoClassDefFoundError
# so I'm using a patch to disable using the maven-resources-plugin for el6
# instead. It's just used for copying two spec files that we neither use, nor
# include in the final package. -mat
%patch2 -p0
%endif
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0

%build
# Fix tomcat directory location in init script
# The directory-defaults.patch adds the line we're fixing here
sed -i -e 's/@TOMCAT@/%{tomcat}/' resources/scripts/init-voms-admin.py
 
# Adding system dependencies
mvn22 install:install-file -DgroupId=emi -DartifactId=trustmanager -Dversion=3.0.3 -Dpackaging=jar -Dfile=`build-classpath trustmanager` -Dmaven.repo.local=/tmp/m2-repository
mvn22 install:install-file -DgroupId=emi -DartifactId=trustmanager-axis -Dversion=1.0.1 -Dpackaging=jar -Dfile=`build-classpath trustmanager-axis` -Dmaven.repo.local=/tmp/m2-repository
mvn22 install:install-file -DgroupId=javax.transaction -DartifactId=jta -Dversion=1.0.1B -Dpackaging=jar -Dfile=`build-classpath jta` -Dmaven.repo.local=/tmp/m2-repository

export JAVA_HOME=%{java_home};
mvn22 -B -s src/config/emi-build-settings.xml -e -P EMI -Dmaven.repo.local=/tmp/m2-repository package
  
  

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar xzvf target/%{name}-%{version}.tar.gz -C $RPM_BUILD_ROOT
# Fix some randomly broken permissions
chmod 644 $RPM_BUILD_ROOT/usr/share/webapps/glite-security-voms-siblings.war $RPM_BUILD_ROOT/usr/share/webapps/glite-security-voms-admin.war $RPM_BUILD_ROOT/usr/share/java/glite-security-voms-admin.jar $RPM_BUILD_ROOT/usr/share/voms-admin/tools/classes/logback.xml $RPM_BUILD_ROOT/usr/share/voms-admin/tools/classes/c3p0.properties 
chmod 755 $RPM_BUILD_ROOT/usr/sbin/voms.py $RPM_BUILD_ROOT/usr/sbin/voms-admin-configure $RPM_BUILD_ROOT/etc/rc.d/init.d/voms-admin
# Fix sysconfig file
sed -i -e 's|^CATALINA_HOME=.*|CATALINA_HOME=%{catalina_home}|' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/voms-admin
## Stage oracle jar
#cp `find /usr/lib/oracle/ -name ojdbc14.jar` $RPM_BUILD_ROOT%{_datadir}/voms-admin/tools/lib
find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/voms-admin

mkdir -p $RPM_BUILD_ROOT%{tomcat_lib}
ln -s /usr/share/java/eclipse-ecj.jar $RPM_BUILD_ROOT%{tomcat_lib}/voms-admin-eclipse-ecj.jar

mkdir -p $RPM_BUILD_ROOT%{tomcat_endorsed}/
ln -s /usr/share/java/xalan-j2.jar $RPM_BUILD_ROOT%{tomcat_endorsed}/
ln -s /usr/share/java/xalan-j2-serializer.jar $RPM_BUILD_ROOT%{tomcat_endorsed}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add voms-admin

%preun
if [ $1 = 0 ]; then
    /sbin/service voms-admin stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del voms-admin
fi



%files
%defattr(-,root,root)
%attr(-,tomcat,tomcat) %dir %{_sysconfdir}/voms-admin
%{_initrddir}/voms-admin
%dir %{_datadir}/webapps/
%{_datadir}/webapps/glite-security-voms-siblings.war
%{_datadir}/webapps/glite-security-voms-admin.war
%{_javadir}/glite-security-voms-admin.jar
%config(noreplace) %{_sysconfdir}/sysconfig/voms-admin
%docdir %{_datadir}/doc/%{name}-%{version}
%{_datadir}/doc/%{name}-%{version}/AUTHORS
%{_datadir}/doc/%{name}-%{version}/README
%{_datadir}/doc/%{name}-%{version}/license.txt
%{_datadir}/doc/%{name}-%{version}/NEWS

%{_sbindir}/*
%{_datadir}/voms-admin/*
%{tomcat_lib}/voms-admin-eclipse-ecj.jar
%{tomcat_endorsed}/xalan-j2.jar
%{tomcat_endorsed}/xalan-j2-serializer.jar

%changelog
* Mon Mar 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.7.0-1.9
- bump to rebuild against xml-commons from jpackage repo (SOFTWARE-1279)

* Thu Feb 27 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.7.0-1.8
- Require glite-security-util-java (SOFTWARE-1408)

* Thu Feb 27 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.7.0-1.7
- apply patch to fix check for adding new certificates (SOFTWARE-1408)

* Tue Feb 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.7.0-1.6
- fix build for voms-admin-server (SOFTWARE-1299)
  - disable cern mirror, fix trustmanager versions, explicitly build require
    /usr/share/java/jta.jar, and add maven dependencies to local maven repo
- apply patch to fix suspended/expired users (SOFTWARE-1349)

* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.7.0-1.5
- Rebuild for updated build dependency

* Tue Feb 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.7.0-1.4
- Updates to build with OpenJDK 7; require java7-devel + jpackage-utils

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 2.7.0-1.3
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Tue Aug 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.7.0-1.2
Add symlinks for xalan-j2 to tomcat endorsed dir
Fix CATALINA_HOME in sysconfig file

* Tue Aug 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.7.0-1.1
Version update; added changes from upstream spec file; its changelog:
  * Fri Dec 16 2011 Andrea Ceccanti <andrea.ceccanti at cnaf.infn.it> - 2.7.0-1
  - Self-managed packaging
Removed fix for maven-surefire-plugin on el6--no longer needed
Removed maven-deps patch

* Fri May 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.6.1-12
Add dependency on osg-webapp-common

* Wed Mar 21 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.6.1-11
Make directory-defaults.patch work for tomcat6 as well

* Mon Mar 19 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.6.1-10
Fix maven-surefire-plugin on el6
Disable maven-resources-plugin on el6
Fix JAVA_HOME on el6
Use tomcat6 on el6

* Wed Sep 21 2011 Alain Roy <roy@cs.wisc.edu> - 2.6.1-9
Tweaked xml-commons-apis dependency to work
Added chkconfig

* Mon Jul 25 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-8
changed patch1 - patches voms.py and not voms-admin-configure.py

* Fri Jul 22 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-7
added requires grid-certificates

* Fri Jul 22 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-6
added requires xmi-commons-api

* Thu Jul 21 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-5
added requires (java-sun,fetch-crl), buildrequires (java-sun-devel)

* Thu Jul 21 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-4
mock creates *.pyc, *.pyo files, so they should be in file

* Thu Jul 21 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-3
Modified patch, get rid of *.pyc, *.pyo files

 
