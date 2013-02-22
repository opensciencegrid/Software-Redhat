Summary: Computing Resource Execution And Management service
Name: glite-ce-cream
Version: 1.14.0
%global upstream_release 4
Release: %{upstream_release}.6%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: Applications/Internet
BuildArch: noarch
BuildRequires: %{!?extbuilddir: glite-ce-cream-api-java, emi-trustmanager-axis2, } ant
BuildRequires: classpathx-jaf, jakarta-commons-codec, jakarta-commons-httpclient, jakarta-commons-logging
Requires: glite-ce-cream-utils, glite-ce-cream-core, blahp, mysql-connector-java
Requires: xml-commons-apis
Requires: emi-trustmanager
Requires: globus-gass-copy-progs
Requires: mysql
Requires: grid-certificates
Requires: glexec
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
Requires(post): openssl
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Patch0: build.patch

%if 0%{?el6}
%global _tomcat tomcat6
%else
%global _tomcat tomcat5
%endif

%description
The Computing Resource Execution And Management service is a web application
taking care of the any job related operation

%prep
 

%setup -c -q
%patch0 -p1

%build
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  printf "dist.location=%{buildroot}
stage.location=
module.version=%{version}">.configuration.properties
  ant
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  ant install
else
  mkdir -p %{buildroot}/usr/share/java
  cp %{extbuilddir}/usr/share/java/*.jar %{buildroot}/usr/share/java
  mkdir -p %{buildroot}/usr/share/glite-ce-cream/modules
  cp %{extbuilddir}/usr/share/glite-ce-cream/modules/*.mar %{buildroot}/usr/share/glite-ce-cream/modules 
  mkdir -p %{buildroot}/usr/share/glite-ce-cream/services
  cp %{extbuilddir}/usr/share/glite-ce-cream/services/*.aar %{buildroot}/usr/share/glite-ce-cream/services
  mkdir -p %{buildroot}/etc/glite-ce-cream
  cp %{extbuilddir}/etc/glite-ce-cream/* %{buildroot}/etc/glite-ce-cream
  mkdir -p %{buildroot}/etc/glite-ce-cream-es
  cp -R %{extbuilddir}/etc/glite-ce-cream-es/* %{buildroot}/etc/glite-ce-cream-es
  mkdir -p %{buildroot}/usr/share/doc/glite-ce-cream-%{version}
  cp %{extbuilddir}/usr/share/doc/glite-ce-cream-%{version}/LICENSE %{buildroot}/usr/share/doc/glite-ce-cream-%{version}
fi

mkdir -p %{buildroot}/usr/share/doc/glite-ce-cream-core-%{version}
cp %{buildroot}/usr/share/doc/glite-ce-cream-%{version}/LICENSE %{buildroot}/usr/share/doc/glite-ce-cream-core-%{version}

mkdir -p %{buildroot}/usr/share/doc/glite-ce-cream-es-%{version}
cp %{buildroot}/usr/share/doc/glite-ce-cream-%{version}/LICENSE %{buildroot}/usr/share/doc/glite-ce-cream-es-%{version}

%clean
rm -rf %{buildroot}

%pre
for((idx=0; idx<5; idx++)) ; do
  /sbin/service %{_tomcat} stop
  if [ $? == 0 ] ; then idx=5; else sleep 5; fi
done

%if 0%{?el5}
# Remove the axis1-based installation 
if [ -f /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/server-config.wsdd ] ; then
  rm -rf /var/lib/%{_tomcat}/webapps/ce-cream
  rm -f /etc/%{_tomcat}/Catalina/localhost/ce-cream.xml
  rm -rf /var/cache/%{_tomcat}/work/Catalina/localhost/ce-cream
fi
%endif

%post
# Do not overwrite axis2-based installation
if [ ! -L /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/services/glite-ce-cream.aar ] ; then

  cp -R /usr/share/axis2/webapp /var/lib/%{_tomcat}/webapps/ce-cream || exit 1
  
  ln -s /usr/share/java/jclassads/cedar.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/jclassads/classad.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/argus-pep-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/argus-pep-common.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/trustmanager.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/bcprov.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/delegation-java.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-common-java.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-blahExecutor.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-core.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-delegationExecutor.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-skeleton.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-delegation-skeleton.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/glite-jdl-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib
  ln -s /usr/share/java/voms-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/lib

%if 0%{?el6}
  # set allowLinking option for tomcat6
  mkdir /var/lib/%{_tomcat}/webapps/ce-cream/META-INF
  echo '<Context override="true" allowLinking="true"></Context>' > /var/lib/%{_tomcat}/webapps/ce-cream/META-INF/context.xml
%endif

  # customization of axis2.conf
  REPLACE1='s|__CHANGE_SERVICE__|/etc/glite-ce-cream/cream-config.xml|g'
  REPLACE2='s|__CHANGE_LOG4J__|/etc/glite-ce-cream/log4j.properties|g'
  TMPPWD=`openssl rand -base64 15`
  REPLACE3='s|__CHANGE_PWD__|'$TMPPWD'|g'
  
  sed "$REPLACE1 ; $REPLACE2 ; $REPLACE3" /etc/glite-ce-common-java/axis2.xml > /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/conf/axis2.xml
  
  # cannot use symlinks for the following files:
  cp -f /etc/glite-ce-common-java/web.xml /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/

  ln -s /usr/share/glite-ce-cream/modules/glite-ce-cream-authorization.mar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/modules
  rm /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/modules/modules.list
  for item in `ls /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/modules/*.mar`; do 
    echo `basename $item` >> /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/modules/modules.list ; 
  done
  
  ln -s /usr/share/glite-ce-cream/services/glite-ce-cream.aar /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/services
  rm /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/services/services.list
  for item in `ls /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/services/*.aar`; do 
    echo `basename $item` >> /var/lib/%{_tomcat}/webapps/ce-cream/WEB-INF/services/services.list ; 
  done

  cp /etc/glite-ce-dbtool/creamdb_min_access.conf.template /etc/glite-ce-cream/creamdb_min_access.conf
  
fi

if [ $1 -eq 1 ] ; then
# Creation of the back-end and log dir
  if [ ! "x`grep tomcat /etc/passwd`" == "x" ] ; then
    mkdir -p /var/cream
    chown tomcat:tomcat /var/cream
    chmod 700 /var/cream

    mkdir -p /var/cream_sandbox
    chown tomcat:tomcat /var/cream_sandbox
    chmod 700 /var/cream_sandbox

    mkdir -p /var/log/cream
    chown tomcat:tomcat /var/log/cream
    chmod 755 /var/log/cream

  fi
    
  /sbin/service %{_tomcat} start
  
fi

%preun
if [ $1 -eq 0 ] ; then

  for((idx=0; idx<5; idx++)) ; do
    /sbin/service %{_tomcat} stop
    if [ $? == 0 ] ; then idx=5; else sleep 5; fi
  done

  if [ -d /var/lib/%{_tomcat}/webapps/ce-cream ] ; then 
    rm -rf /var/lib/%{_tomcat}/webapps/ce-cream
  fi
    
  rm -f /etc/glite-ce-cream/creamdb_min_access.conf

fi

%postun
/sbin/service %{_tomcat} start


%files
%defattr(-,root,root)
%dir /etc/glite-ce-cream/
%config(noreplace) /etc/glite-ce-cream/*.sql
%config(noreplace) /etc/glite-ce-cream/*.template
%config(noreplace) /etc/glite-ce-cream/*.tpl
%config(noreplace) /etc/glite-ce-cream/*.properties
%dir /usr/share/doc/glite-ce-cream-%{version}/
%doc /usr/share/doc/glite-ce-cream-%{version}/LICENSE
/usr/share/glite-ce-cream/services/glite-ce-cream.aar







%package core
Summary: Common classes for CREAM services
Group: Applications/Internet
Requires: glite-ce-cream-api-java

%description core
This package contains the core libraries used by CREAM services

%files core
%defattr(-,root,root)
/usr/share/java/glite-ce-cream*.jar
%dir /usr/share/doc/glite-ce-cream-core-%{version}/
%doc /usr/share/doc/glite-ce-cream-core-%{version}/LICENSE
%dir /usr/share/glite-ce-cream/modules
/usr/share/glite-ce-cream/modules/*.mar
%dir /usr/share/glite-ce-cream/services








%package es
Summary: The gLite implementation of EMI Execution Service
Group: Applications/Internet
Requires: glite-ce-cream-utils, glite-ce-cream-core, blahp, mysql-connector-java

%description es
This package provides the gLite implementation of Execution Service interface.
The interface is built on top of the core of the Computing Resource Execution 
And Management service.

%files es
%defattr(-,root,root)
%dir /usr/share/doc/glite-ce-cream-es-%{version}/
%doc /usr/share/doc/glite-ce-cream-es-%{version}/LICENSE
%dir /etc/glite-ce-cream-es/
%config(noreplace) /etc/glite-ce-cream-es/*.sql
%config(noreplace) /etc/glite-ce-cream-es/*.template
%config(noreplace) /etc/glite-ce-cream-es/*.tpl
%config(noreplace) /etc/glite-ce-cream-es/*.properties
%config(noreplace) /etc/glite-ce-cream-es/storedprocedures/*.sql
/usr/share/glite-ce-cream/services/glite-ce-cream-es.aar

%pre es
for((idx=0; idx<5; idx++)) ; do
  /sbin/service %{_tomcat} stop
  if [ $? == 0 ] ; then idx=5; else sleep 5; fi
done

%post es
# Do not overwrite axis2-based installation
if [ ! -L /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/services/glite-ce-cream-es.aar ] ; then

  cp -R /usr/share/axis2/webapp /var/lib/%{_tomcat}/webapps/ce-cream-es || exit 1
  
  ln -s /usr/share/java/jclassads/cedar.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/jclassads/classad.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/argus-pep-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/argus-pep-common.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/trustmanager.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/bcprov.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/delegation-java.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-common-java.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-blahExecutor.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-core.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-delegationExecutor.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-cream-es-skeleton.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-ce-delegation-skeleton.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/glite-jdl-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib
  ln -s /usr/share/java/voms-api-java.jar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/lib

%if 0%{?el6}
  # set allowLinking option for tomcat6
  mkdir /var/lib/%{_tomcat}/webapps/ce-cream-es/META-INF
  echo '<Context override="true" allowLinking="true"></Context>' > /var/lib/%{_tomcat}/webapps/ce-cream-es/META-INF/context.xml
%endif

  # customization of axis2.conf
  REPLACE1='s|__CHANGE_SERVICE__|/etc/glite-ce-cream-es/cream-config.xml|g'
  REPLACE2='s|__CHANGE_LOG4J__|/etc/glite-ce-cream-es/log4j.properties|g'
  TMPPWD=`openssl rand -base64 15`
  REPLACE3='s|__CHANGE_PWD__|'$TMPPWD'|g'
  
  sed "$REPLACE1 ; $REPLACE2 ; $REPLACE3" /etc/glite-ce-common-java/axis2.xml > /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/conf/axis2.xml
  
  # cannot use symlinks for the following files:
  cp -f /etc/glite-ce-common-java/web.xml /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/

  ln -s /usr/share/glite-ce-cream/modules/glite-ce-cream-authorization.mar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/modules
  rm /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/modules/modules.list
  for item in `ls /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/modules/*.mar`; do 
    echo `basename $item` >> /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/modules/modules.list ; 
  done
  
  ln -s /usr/share/glite-ce-cream/services/glite-ce-cream-es.aar /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/services
  rm /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/services/services.list
  for item in `ls /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/services/*.aar`; do 
    echo `basename $item` >> /var/lib/%{_tomcat}/webapps/ce-cream-es/WEB-INF/services/services.list ; 
  done

  cp /etc/glite-ce-dbtool/creamdb_min_access.conf.template /etc/glite-ce-cream-es/creamdb_min_access.conf
  
fi

if [ $1 -eq 1 ] ; then
# Creation of the back-end and log dir
  if [ ! "x`grep tomcat /etc/passwd`" == "x" ] ; then
    mkdir -p /var/cream-es
    chown tomcat:tomcat /var/cream-es
    chmod 700 /var/cream-es

    mkdir -p /var/cream_es_sandbox 
    chown tomcat:tomcat /var/cream_es_sandbox 
    chmod 700 /var/cream_es_sandbox 
    
    mkdir -p /var/log/cream-es
    chown tomcat:tomcat /var/log/cream-es
    chmod 755 /var/log/cream-es

  fi
    
  /sbin/service %{_tomcat} start
  
fi

%preun es
if [ $1 -eq 0 ] ; then

  for((idx=0; idx<5; idx++)) ; do
    /sbin/service %{_tomcat} stop
    if [ $? == 0 ] ; then idx=5; else sleep 5; fi
  done

  if [ -d /var/lib/%{_tomcat}/webapps/ce-cream-es ] ; then 
    rm -rf /var/lib/%{_tomcat}/webapps/ce-cream-es
  fi
    
  rm -f /etc/glite-ce-cream-es/creamdb_min_access.conf
  
fi

%postun es
/sbin/service %{_tomcat} start


%changelog
* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.14.0-4.6
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Fri Aug 10 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.5
- Added as requirements: mysql, grid-certificates, glexec, fetch-crl

* Fri Aug 10 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.4
- Added as requirements: xml-commons-apis, emi-trustmanager, globus-gass-copy-progs

* Wed Aug 08 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.3
- "glite-ce-blahp" requirement changed to "blahp" for es subpackage as well

* Fri Jul 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.2
- "glite-ce-blahp" requirement changed to "blahp"

* Fri Jun 01 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.1
- Add dist tag
- Fix conditional expressions to work in osg build environment

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 1.14.0-4.sl5
- Major bugs fixed


