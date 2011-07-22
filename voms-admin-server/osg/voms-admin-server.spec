Summary: emi.voms.voms-admin-server
Name: voms-admin-server
Version: 2.6.1
Release: 6
License: Apache Software License
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildRequires: maven2
BuildRequires: java-devel-sun
Requires: java-sun
Requires: emi-trustmanager-tomcat
Requires: tomcat5
Requires: fetch-crl
Requires: xml-commons-apis 
BuildRoot: %{_builddir}/%{name}-root
BuildArch: noarch
AutoReqProv: yes
Source: voms-admin-server-2.6.1-1.src.tar.gz
Patch0: maven-deps.patch
Patch1: directory-defaults.patch

%description
emi.voms.voms-admin-server

%prep
 

%setup  
%patch0 -p0
%patch1 -p0

%build
 
 export JAVA_HOME=/usr/java/latest; mvn -P EMI -Dmaven.repo.local=/tmp/m2-repository package
  
  

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
tar xzvf target/glite-security-voms-admin-server.tar.gz -C $RPM_BUILD_ROOT;
# Fix some randomly broken permissions
chmod 644 $RPM_BUILD_ROOT/usr/share/webapps/glite-security-voms-siblings.war $RPM_BUILD_ROOT/usr/share/webapps/glite-security-voms-admin.war $RPM_BUILD_ROOT/usr/share/java/glite-security-voms-admin.jar $RPM_BUILD_ROOT/usr/share/voms-admin/tools/classes/logback.xml $RPM_BUILD_ROOT/usr/share/voms-admin/tools/classes/c3p0.properties 
chmod 755 $RPM_BUILD_ROOT/usr/sbin/voms.py $RPM_BUILD_ROOT/usr/sbin/voms-admin-configure $RPM_BUILD_ROOT/etc/rc.d/init.d/voms-admin
#cp `find /usr -name ojdbc14.jar` $RPM_BUILD_ROOT/usr/share/voms-admin/tools/lib
find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

# Where did this come from?
rm $RPM_BUILD_ROOT/usr/share/voms-admin/tools/lib/voms-admin-server-%{version}.war

mkdir -p $RPM_BUILD_ROOT/etc/voms-admin

mkdir -p $RPM_BUILD_ROOT/usr/share/tomcat5/common/lib
ln -s /usr/share/java/eclipse-ecj.jar $RPM_BUILD_ROOT/usr/share/tomcat5/common/lib/voms-admin-eclipse-ecj.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(-,tomcat,tomcat) /etc/voms-admin
%dir /etc/rc.d/init.d/
/etc/rc.d/init.d/voms-admin
%dir /usr/share/webapps/
/usr/share/webapps/glite-security-voms-siblings.war
/usr/share/webapps/glite-security-voms-admin.war
/usr/share/java/glite-security-voms-admin.jar
%dir /usr/share/doc/voms-admin-server/
/usr/share/doc/voms-admin-server/AUTHORS
/usr/share/doc/voms-admin-server/README
/usr/share/doc/voms-admin-server/license.txt
/usr/share/doc/voms-admin-server/NEWS
%dir /usr/share/voms-admin/
%dir /usr/share/voms-admin/endorsed/
/usr/share/voms-admin/endorsed/xml-apis-2.9.1.jar
/usr/share/voms-admin/endorsed/serializer-2.9.1.jar
/usr/share/voms-admin/endorsed/resolver-2.9.1.jar
/usr/share/voms-admin/endorsed/xercesImpl-2.9.1.jar
%dir /usr/share/voms-admin/wsdls/
/usr/share/voms-admin/wsdls/glite-security-voms-acl-2.0.2.wsdl
/usr/share/voms-admin/wsdls/glite-security-voms-registration-2.0.2.wsdl
/usr/share/voms-admin/wsdls/glite-security-voms-admin-2.0.2.wsdl
/usr/share/voms-admin/wsdls/glite-security-voms-compatibility-2.0.2.wsdl
/usr/share/voms-admin/wsdls/glite-security-voms-attributes-2.0.2.wsdl
/usr/share/voms-admin/wsdls/glite-security-voms-certificates-2.0.2.wsdl
%dir /usr/share/voms-admin/tools/
%dir /usr/share/voms-admin/tools/lib/
/usr/share/voms-admin/tools/lib/commons-digester-1.8.jar
/usr/share/voms-admin/tools/lib/tiles-core-2.0.6.jar
/usr/share/voms-admin/tools/lib/commons-logging-api-1.1.jar
/usr/share/voms-admin/tools/lib/struts2-core-2.2.1.jar
/usr/share/voms-admin/tools/lib/joda-time-1.6.jar
/usr/share/voms-admin/tools/lib/tiles-jsp-2.0.6.jar
/usr/share/voms-admin/tools/lib/commons-email-1.1.jar
/usr/share/voms-admin/tools/lib/wsdl4j-1.5.1.jar
/usr/share/voms-admin/tools/lib/xml-apis-2.9.1.jar
#/usr/share/voms-admin/tools/lib/ojdbc14.jar
/usr/share/voms-admin/tools/lib/axis-saaj-1.2.1.jar
/usr/share/voms-admin/tools/lib/hibernate-annotations-3.3.1.GA.jar
/usr/share/voms-admin/tools/lib/commons-logging-1.0.4.jar
/usr/share/voms-admin/tools/lib/logback-core-0.9.18.jar
/usr/share/voms-admin/tools/lib/xmlsec-1.4.3.jar
/usr/share/voms-admin/tools/lib/openws-1.3.0.jar
/usr/share/voms-admin/tools/lib/commons-collections-3.2.1.jar
/usr/share/voms-admin/tools/lib/ejb3-persistence-1.0.1.GA.jar
/usr/share/voms-admin/tools/lib/ehcache-1.2.3.jar
/usr/share/voms-admin/tools/lib/commons-beanutils-1.7.0.jar
/usr/share/voms-admin/tools/lib/commons-beanutils-core-1.7.0.jar
/usr/share/voms-admin/tools/lib/commons-configuration-1.5.jar
/usr/share/voms-admin/tools/lib/struts2-convention-plugin-2.2.1.jar
/usr/share/voms-admin/tools/lib/not-yet-commons-ssl-0.3.9.jar
/usr/share/voms-admin/tools/lib/asm-1.5.3.jar
/usr/share/voms-admin/tools/lib/axis-1.2.1.jar
/usr/share/voms-admin/tools/lib/bcprov-ext-jdk15-1.44.jar
/usr/share/voms-admin/tools/lib/hibernate-3.2.6.ga.jar
/usr/share/voms-admin/tools/lib/jcip-annotations-1.0.jar
/usr/share/voms-admin/tools/lib/ognl-3.0.jar
/usr/share/voms-admin/tools/lib/xalan-2.7.1.jar
/usr/share/voms-admin/tools/lib/serializer-2.7.1.jar
/usr/share/voms-admin/tools/lib/antlr-2.7.6.jar
/usr/share/voms-admin/tools/lib/freemarker-2.3.16.jar
/usr/share/voms-admin/tools/lib/commons-lang-2.3.jar
/usr/share/voms-admin/tools/lib/serializer-2.9.1.jar
/usr/share/voms-admin/tools/lib/struts2-tiles-plugin-2.2.1.jar
/usr/share/voms-admin/tools/lib/javassist-3.8.0.GA.jar
/usr/share/voms-admin/tools/lib/commons-fileupload-1.2.1.jar
/usr/share/voms-admin/tools/lib/standard-1.1.2.jar
/usr/share/voms-admin/tools/lib/commons-codec-1.3.jar
/usr/share/voms-admin/tools/lib/cglib-2.1_3.jar
/usr/share/voms-admin/tools/lib/c3p0-0.9.1.jar
/usr/share/voms-admin/tools/lib/log4j-over-slf4j-1.5.10.jar
/usr/share/voms-admin/tools/lib/tiles-api-2.0.6.jar
/usr/share/voms-admin/tools/lib/util-java-2.8.6.jar
/usr/share/voms-admin/tools/lib/logback-classic-0.9.18.jar
/usr/share/voms-admin/tools/lib/jta-1.0.1B.jar
/usr/share/voms-admin/tools/lib/oro-2.0.8.jar
/usr/share/voms-admin/tools/lib/commons-cli-1.1.jar
/usr/share/voms-admin/tools/lib/xmltooling-1.2.1.jar
/usr/share/voms-admin/tools/lib/velocity-1.5.jar
/usr/share/voms-admin/tools/lib/commons-io-1.3.2.jar
/usr/share/voms-admin/tools/lib/asm-attrs-1.5.3.jar
/usr/share/voms-admin/tools/lib/slf4j-api-1.5.10.jar
/usr/share/voms-admin/tools/lib/xwork-core-2.2.1.jar
/usr/share/voms-admin/tools/lib/activation-1.1.jar
/usr/share/voms-admin/tools/lib/jstl-1.1.2.jar
/usr/share/voms-admin/tools/lib/resolver-2.9.1.jar
/usr/share/voms-admin/tools/lib/commons-discovery-0.2.jar
/usr/share/voms-admin/tools/lib/struts2-json-plugin-2.2.1.jar
/usr/share/voms-admin/tools/lib/axis-jaxrpc-1.2.1.jar
/usr/share/voms-admin/tools/lib/xercesImpl-2.9.1.jar
/usr/share/voms-admin/tools/lib/opensaml-2.3.0.jar
/usr/share/voms-admin/tools/lib/dom4j-1.6.1.jar
/usr/share/voms-admin/tools/lib/commons-httpclient-3.1.jar
/usr/share/voms-admin/tools/lib/mysql-connector-java-5.0.7.jar
/usr/share/voms-admin/tools/lib/hibernate-commons-annotations-3.0.0.ga.jar
%dir /usr/share/voms-admin/tools/classes/
/usr/share/voms-admin/tools/classes/logback.xml
/usr/share/voms-admin/tools/classes/c3p0.properties
%dir /usr/share/voms-admin/templates/
/usr/share/voms-admin/templates/siblings-context.xml.template
/usr/share/voms-admin/templates/voms.conf.template
%dir /usr/share/voms-admin/templates/aup/
/usr/share/voms-admin/templates/aup/vo-aup.txt
/usr/share/voms-admin/templates/logback.runtime.xml
/usr/share/voms-admin/templates/context.xml.template
/usr/share/voms-admin/templates/voms.database.properties.template
/usr/share/voms-admin/templates/voms.service.properties.template
/usr/sbin/voms-db-deploy.py
/usr/sbin/voms-admin-configure.py
/usr/sbin/voms.py
/usr/sbin/init-voms-admin.py
/usr/sbin/init-voms-admin.pyc
/usr/sbin/init-voms-admin.pyo
/usr/sbin/voms-admin-configure.pyc
/usr/sbin/voms-admin-configure.pyo
/usr/sbin/voms-db-deploy.pyc
/usr/sbin/voms-db-deploy.pyo
/usr/sbin/voms.pyc
/usr/sbin/voms.pyo
/usr/sbin/voms-admin-ping
/usr/sbin/voms-admin-configure
/usr/share/tomcat5/common/lib/voms-admin-eclipse-ecj.jar

%changelog
* Fri Jul 22 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-6
added requires xmi-commons-api

* Thu Jul 21 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-5
added requires (java-sun,fetch-crl), buildrequires (java-sun-devel)

* Thu Jul 21 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-4
mock creates *.pyc, *.pyo files, so they should be in file

* Thu Jul 21 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.6.1-3
Modified patch, get rid of *.pyc, *.pyo files

 
