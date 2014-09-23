
#Redhat auto-repacks jars which messes up build date 
#disable this
%define __jar_repack %{nil}
%if "%{?rhel}" == "5"
%define __os_install_post \
    /usr/lib/rpm/redhat/brp-compress  \
    %{!?__debug_package:/usr/lib/rpm/redhat/brp-strip %{__strip}}  \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip}  \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump}  \
    /usr/lib/rpm/brp-python-bytecompile  \
%{nil}
%endif

Name:           bestman2
Version:        2.3.0
Release:        20%{?dist}
Summary:        SRM server for Grid Storage Elements

Group:          System Environment/Daemons

#Note, licensing is CR-2404 under BSD license with a grant back provision 
#copyright 2010-2011
License:        BSD
URL:            https://sdm.lbl.gov/bestman/

%define install_root /etc/%{name}

# NOTE: CHANGE THESE EACH RELEASE
# To create:
# cd /tmp
# svn export -r 91 https://codeforge.lbl.gov/anonscm/bestman bestman2
# tar czf bestman2.tar.gz bestman2
Source0:        bestman2.tar.gz
#Source1:        bestman2.sh
Source2:        bestman2.init
Source3:        bestman.logrotate
Source4:        dependent.jars.tar.gz
Source5:        bestman2.sysconfig
Source6:        build.xml
Source7:        build.properties
Source8:        configure.in
Source9:        bestman2.rc
Source10:       bestman2lib.sysconfig

Patch0:		upgrade_exception_message.patch
Patch1:		bestman2-2.2.1-2.2.2.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  java7-devel jpackage-utils wget ant axis jakarta-commons-logging jakarta-commons-discovery wsdl4j jakarta-commons-collections jakarta-commons-lang joda-time velocity xalan-j2 xml-security bouncycastle voms-api-java >= 2.0.8 slf4j log4j cog-jglobus-axis autoconf
# v NOTE: Must edit the jglobus-*.path lines in build.properties every time jglobus gets a new version!
BuildRequires: jglobus = 2.0.6
BuildRequires: jetty-client jetty-continuation jetty-deploy jetty-http jetty-io jetty-security jetty-server jetty-servlet jetty-util jetty-webapp jetty-xml
BuildRequires: emi-trustmanager emi-trustmanager-axis
BuildRequires: /usr/lib/gums/opensaml-2.4.1.jar
BuildRequires: /usr/lib/gums/openws-1.4.1.jar
BuildRequires: /usr/lib/gums/privilege-xacml-2.2.4.jar
BuildRequires: /usr/lib/gums/xmltooling-1.3.1.jar

%description
BeStMan 2 - Berkeley Storage Manager

Application server for exporting local file systems securely using the
SRM protocol.  

BeStMan is a full implementation of SRM v2.2, developed by 
Lawrence Berkeley National Laboratory, for disk based storage systems 
and mass storage systems such as HPSS. End users may have their own 
personal BeStMan that manages and provides an SRM interface to their 
local disks or storage systems. It works on top of existing disk-based 
unix file system, and has been reported so far to work on file systems 
such as NFS, PVFS, AFS, GFS, GPFS, PNFS, and Lustre. It also works with 
any existing file transfer service, such as gsiftp, http, https and ftp.

User's guide : http://sdm.lbl.gov/bestman
General support and bug report to <srm@lbl.gov>
Open Science Grid (OSG) support:  osg-storage@opensciencegrid.org
BeStMan Copyright 2010-2011, The Regents of the University of California,
through Lawrence Berkeley National Laboratory.  See LICENSE file for details.

%package common-libs
Summary: Common files BeStMan SRM server client and tester
Group: System Environment/Libraries
Requires:  java7 jpackage-utils axis jakarta-commons-logging jakarta-commons-discovery wsdl4j log4j jglobus cog-jglobus-axis >= 1.8.0-2
# The following are needed for srm client tools and probably tester too
Requires:  joda-time glite-security-trustmanager glite-security-util-java xalan-j2 voms-api-java >= 2.0.8 jakarta-commons-collections
# ensure these are present, from jpackage-utils or missing-java-1.7.0-dirs
Requires: /usr/lib/java-1.7.0
Requires: /usr/share/java-1.7.0
%description common-libs
This package is mostly java libraries (jars) for Bestman.
It contains libraries necessary for Bestman server, client and tester.
It also contains the license, readme, and property files


%package server
Summary: BeStMan SRM server
Group: System Environment/Daemons
Obsoletes: bestman2
Requires: java7-devel
Requires: jpackage-utils
Requires: %{name}-common-libs = %{version}-%{release}
Requires: %{name}-server-libs = %{version}-%{release}
Requires: %{name}-server-dep-libs = %{version}-%{release}
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service
%description server
BeStMan SRM server

%package server-libs
Summary: BeStMan Server SRM Java libraries
Group: System Environment/Libraries
Requires: java7-devel
Requires: jpackage-utils
%description server-libs
The BeStMan Server SRM Java libraries

%package server-dep-libs
Summary: BeStMan Server SRM Java libraries
Group: System Environment/Libraries
Requires: java7-devel jpackage-utils jakarta-commons-lang joda-time emi-trustmanager emi-trustmanager-axis xalan-j2 voms-api-java >= 2.0.8 jakarta-commons-collections
Requires: jetty-client jetty-continuation jetty-deploy jetty-http jetty-io jetty-security jetty-server jetty-servlet jetty-util jetty-webapp jetty-xml
Requires: /usr/lib/gums/opensaml-2.4.1.jar
Requires: /usr/lib/gums/openws-1.4.1.jar
Requires: /usr/lib/gums/privilege-xacml-2.2.4.jar
Requires: /usr/lib/gums/velocity-1.5.jar
Requires: /usr/lib/gums/xmlsec-1.4.2.jar
Requires: /usr/lib/gums/xmltooling-1.3.1.jar

%description server-dep-libs
The BeStMan Server SRM Java libraries
This includes all the dependencies and should be 
eventually deprecated once we eventually link
correctly to all the dependencies.

%package client
Summary: Bestman LBNL SRM client
Group: Applications/Internet
Requires: %{name}-client-libs = %{version}-%{release}
Requires: %{name}-common-libs = %{version}-%{release}
%description client
The srm-* client tools

%package client-libs
Summary: Libraries needed for Bestman LBNL SRM client
Group: System Environment/Libraries
Requires:  java7-devel
Requires:  jpackage-utils
%description client-libs
These are the libraries needed solely for the client 

%package tester
Summary: srmtester application for verifying a SRM endpoint
Group: Applications/Internet
Requires:  java7-devel
Requires:  jpackage-utils
Requires: %{name}-tester-libs = %{version}-%{release}
Requires: %{name}-common-libs = %{version}-%{release}
Requires: %{name}-client-libs = %{version}-%{release}
%description tester
srmtester application for verifying a SRM endpoint
This application can run through various funcionality of
the SRM v2.2 specification to make sure that all aspects
of the SRM protocol are functioning on an SRM endpoint.

%package tester-libs
Summary: Libraries needed for Bestman LBNL SRM client
Group: System Environment/Libraries
Requires:  java7-devel
Requires:  jpackage-utils
%description tester-libs
These are the libraries needed solely for the srmtester application 



%prep
BUILDROOT=$PWD

%setup -T -b 4 -q -n lib
cd ..
%setup -T -b 0 -q -n %{name}

%patch0 -p1
%patch1 -p0

pushd bestman2/setup-osg/bestman.in
sed -i "s/@SRM_HOME@/\/etc\/bestman2/" *
popd

pushd bestman2/setup-osg/
mkdir -p dist/conf
cp %{SOURCE9} dist/conf
popd

cp %{SOURCE7} bestman2/branches/osg-dev/
cp %{SOURCE7} bestman2/setup-osg/
sed -i "s/install.root=.*/install.root=dist/" bestman2/setup-osg/build.properties
sed -i "s|@BUILDROOT@|$BUILDROOT|"  bestman2/setup-osg/build.properties bestman2/branches/osg-dev/build.properties

cp %{SOURCE8} bestman2/setup-osg/

%build
pushd bestman2/branches/osg-dev

#sed -i "s/Generating stubs from/Gen stubs \${axis.path}/" wsdl/build.xml

ant build # <- XXX dies here
ant install
popd

pushd bestman2/setup-osg
cp bestman.in/aclocal.m4 .
autoconf configure.in > configure
chmod +x configure
./configure --with-srm-owner=bestman --with-sysconf-path=./dist/bestman.sysconfig
ant deploy

pushd dist
#Fix paths in bestman2.rc
JAVADIR=`echo %{_javadir} |  sed 's/\//\\\\\//g'`

#Fix paths in binaries.  Wish I could do this in configure...
sed -i "s/BESTMAN_SYSCONF=.*/BESTMAN_SYSCONF=\/etc\/sysconfig\/bestman2/" bin/*
sed -i "s/BESTMAN_SYSCONF=.*/BESTMAN_SYSCONF=\/etc\/sysconfig\/bestman2/" sbin/*
sed -i "s/BESTMAN_SYSCONF_LIB=.*/BESTMAN_SYSCONF_LIB=\/etc\/sysconfig\/bestman2lib/" bin/*
sed -i "s/BESTMAN_SYSCONF_LIB=.*/BESTMAN_SYSCONF_LIB=\/etc\/sysconfig\/bestman2lib/" sbin/*
sed -i "s/\${BESTMAN_SYSCONF}/\/etc\/bestman2\/conf\/bestman2.rc/" sbin/bestman.server


BUILDHOSTNAME=`hostname -f`
# Fix version
#sed -i "s/Built on .* at/Built on $BUILDHOSTNAME at/" version
popd
popd


%install
rm -rf $RPM_BUILD_ROOT

cp -R bestman2/sources/dist/* bestman2/setup-osg/dist/
pushd bestman2
pushd setup-osg
pushd dist
ls -R
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{install_root}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}

#bestmanclient.conf should be srmclient.conf
mv conf/bestmanclient.conf conf/srmclient.conf

cp -arp conf $RPM_BUILD_ROOT%{install_root}
cp -arp lib/* $RPM_BUILD_ROOT%{_javadir}/%{name}/
cp -arp properties $RPM_BUILD_ROOT%{install_root}

#Install dependent jars (prune this list)
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/others
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}/axis
cp -arp ../../../../lib/plugin $RPM_BUILD_ROOT%{_javadir}/%{name}

#Install the non-system jars
libdir=../../../../lib
jardir=$RPM_BUILD_ROOT%{_javadir}/%{name}

for jar in "slf4j-api-1.6.2.jar" "slf4j-log4j12-1.6.2.jar" "slf4j-simple-1.6.2.jar" "jcl-over-slf4j-1.6.0.jar" "je-4.1.10.jar" "servlet-api-3.0.jar" "which4j.jar"
do
	install -m 0644 $libdir/others/$jar $jardir/others/
done

for jar in "xercesImpl-2.11.0.jar" "xml-apis-2.11.0.jar"
do
        install -m 0644 $libdir/axis/$jar $jardir/axis/
done


rm -rf $RPM_BUILD_ROOT%{install_root}/properties/.svn

install -m 0644 version $RPM_BUILD_ROOT%{install_root}/version
install -m 0755 sbin/bestman.server $RPM_BUILD_ROOT%{_sbindir}/bestman.server

mkdir -p $RPM_BUILD_ROOT%{_bindir}
for i in `ls bin`; do
  install -m 0755 bin/$i $RPM_BUILD_ROOT%{_bindir}/
done

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/bestman
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
install -m 0644 conf/bestman2.rc $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf/bestman2.rc
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}lib

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir
touch $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem

mkdir -p $RPM_BUILD_ROOT%{_var}/log/%{name}

popd
popd

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
getent group bestman >/dev/null || groupadd -r bestman
getent passwd bestman >/dev/null || \
       useradd -r -g bestman -d %{install_root} -c "BeStMan 2 Server user" \
       -s /bin/bash bestman

%post server
/sbin/chkconfig --add %{name}

%preun server
if [ "$1" = "0" ]; then
    /sbin/chkconfig --del %{name}
fi

%postun server
if [ "$1" -ge "1" ] ; then
    /sbin/service bestman2 condrestart >/dev/null 2>&1 || :
fi

%files common-libs
%defattr(-,root,root,-)
%dir %{install_root}
%{_javadir}/bestman2/axis/xercesImpl-2.11.0.jar
%{_javadir}/bestman2/axis/xml-apis-2.11.0.jar
%{_javadir}/bestman2/bestman2-stub.jar
%config(noreplace) %{install_root}/properties/authmod-unix.properties
%config(noreplace) %{install_root}/properties/authmod-win.properties
%config(noreplace) %{install_root}/properties/log4j.properties
%{install_root}/version
%doc LICENSE
%doc COPYRIGHT
%doc bestman2/sources/README


%files client
%defattr(-,root,root,-)
%config(noreplace) %{install_root}/conf/srmclient.conf
%config(noreplace) %{install_root}/conf/bestman2.rc
%config(noreplace) %{_sysconfdir}/sysconfig/bestman2
%config(noreplace) %{_sysconfdir}/sysconfig/bestman2lib
%{_bindir}/srm-common.sh
%{_bindir}/srm-copy
%{_bindir}/srm-copy-status
%{_bindir}/srm-extendfilelifetime
%{_bindir}/srm-ls
%{_bindir}/srm-ls-status
%{_bindir}/srm-mkdir
%{_bindir}/srm-mv
%{_bindir}/srm-permission-check
%{_bindir}/srm-permission-get
%{_bindir}/srm-permission-set
%{_bindir}/srm-ping
%{_bindir}/srm-putdone
%{_bindir}/srm-release
%{_bindir}/srm-req-abort
%{_bindir}/srm-req-abortfiles
%{_bindir}/srm-req-resume
%{_bindir}/srm-req-summary
%{_bindir}/srm-req-suspend
%{_bindir}/srm-req-tokens
%{_bindir}/srm-rm
%{_bindir}/srm-rmdir
%{_bindir}/srm-sp-change
%{_bindir}/srm-sp-change-status
%{_bindir}/srm-sp-info
%{_bindir}/srm-sp-purge
%{_bindir}/srm-sp-release
%{_bindir}/srm-sp-reserve
%{_bindir}/srm-sp-reserve-status
%{_bindir}/srm-sp-tokens
%{_bindir}/srm-sp-update
%{_bindir}/srm-sp-update-status
%{_bindir}/srm-transferprotocols
%{install_root}/version
%doc LICENSE
%doc COPYRIGHT
%doc bestman2/sources/CHANGES.SOURCES
%doc bestman2/setup-osg/CHANGES.SETUP
%doc bestman2/sources/README

%files server
%defattr(-,root,root,-)
%{_sbindir}/bestman.server
%{_bindir}/bestman-diag
%config(noreplace) %{install_root}/conf/WEB-INF
%config(noreplace) %{install_root}/conf/grid-mapfile.empty
%config(noreplace) %{install_root}/conf/bestman-diag-msg.conf
%config(noreplace) %{install_root}/conf/bestman-diag.conf.sample
%config(noreplace) %{install_root}/conf/bestman2.rc
%config(noreplace) %{_sysconfdir}/sysconfig/bestman2
%config(noreplace) %{_sysconfdir}/sysconfig/bestman2lib
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem
%attr(-,bestman,bestman) %dir %{_var}/log/%{name}
%attr(-,bestman,bestman) %dir %{_sysconfdir}/grid-security/bestman

%files client-libs
%{_javadir}/bestman2/bestman2-client.jar

%files server-libs
%doc LICENSE
%doc COPYRIGHT
%doc bestman2/sources/CHANGES.SOURCES
%doc bestman2/setup-osg/CHANGES.SETUP
%doc bestman2/sources/README
%{_javadir}/bestman2/bestman2.jar
%{_javadir}/bestman2/bestman2-aux.jar


%files server-dep-libs
%{_javadir}/bestman2/others/jcl-over-slf4j-1.6.0.jar
%{_javadir}/bestman2/others/je-4.1.10.jar
%{_javadir}/bestman2/others/servlet-api-3.0.jar
%{_javadir}/bestman2/others/slf4j-api-1.6.2.jar
%{_javadir}/bestman2/others/slf4j-log4j12-1.6.2.jar
%{_javadir}/bestman2/others/slf4j-simple-1.6.2.jar
%{_javadir}/bestman2/others/which4j.jar
%{_javadir}/bestman2/plugin/LBNL.RFF.README.txt
%{_javadir}/bestman2/plugin/LBNL.RFF.jar
%{_javadir}/bestman2/plugin/LBNL.SSFP.jar
%{_javadir}/bestman2/plugin/LBNL.SSFP.README.txt

%files tester
%{_bindir}/srm-tester
%{_bindir}/srm-common.sh
%config(noreplace) %{install_root}/conf/srmtester.conf
%config(noreplace) %{install_root}/conf/bestman2.rc
%config(noreplace) %{_sysconfdir}/sysconfig/bestman2
%config(noreplace) %{_sysconfdir}/sysconfig/bestman2lib

%files tester-libs
%{_javadir}/bestman2/bestman2-tester-driver.jar
%{_javadir}/bestman2/bestman2-tester-main.jar


%changelog
* Tue Sep 23 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-20
- fix xmltooling version to match latest GUMS (SOFTWARE-1610)

* Fri Sep 19 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-19
- update GUMS dependencies to require specific jars (SOFTWARE-1610)

* Wed Jun 04 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-18
- handle empty pidfile in init script (SOFTWARE-1504)

* Mon Feb 10 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-17
- Patch to include "root" SRM transfer protocol from 2.2.2 (SOFTWARE-1379)

* Tue Sep 17 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.3.0-16
- Fixed build to work with jglobus 2.0.6

* Wed Sep 04 2013 Neha Sharma <neha@fnal.gov> - 2.3.0-15
- As per GOC ticket 14020, adding the copy-truncate logrotate option and 
  modify logrotate to only handle bestman2.log, not event.srm.log 

* Tue May 07 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-14
- Require missing java dir names instead of workaround package

 Mon Apr 29 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-13
- Require missing-java-1.7.0-dirs for el5

* Thu Apr 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-12
- Rebuild for updated build dependencies

* Tue Mar 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-11
- Change JAVA_HOME in bestman2.sysconfig from /usr/java/latest to
  /etc/alternatives/java_sdk

* Tue Feb 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-10
- Updates to build with OpenJDK 7; require java7-devel + jpackage-utils

* Thu Jan 10 2013 Neha Sharma <neha@fnal.gov> - 2.3.0-9
- modify the init script to cd in to /tmp to void build-classpath issue on SL5

* Wed Jan 09 2013 Neha Sharma <neha@fnal.gov> - 2.3.0-8
- tester also requires client libraries

* Fri Jan 04 2013 Neha Sharma <neha@fnal.gov> - 2.3.0-7
- Added bestman2lib to separate out the server/client lib settings
- Added version requirement for cog-jglobus-axis and gums

* Mon Nov 19 2012 Neha Sharma <neha@fnal.gov> - 2.3.0-6
- Adding emi-trustmanager-axis to server-dep-libs

* Mon Nov 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.3.0-5
- Require voms-api-java instead of vomsjapi

* Wed Nov 08 2012 Neha Sharma <neha@fnal.gov> - 2.3.0-4
- Updated file 'version' to include latest version and removed the build host line from build.xml

* Tue Nov 06 2012 Neha Sharma <neha@fnal.gov> - 2.3.0-3
- Adding cog-jglobus-axis to common-libs

* Fri Nov 02 2012 Neha Sharma <neha@fnal.gov> - 2.3.0-2
- Removing the patch since changes have been incorporated in to code itself

* Thu Sep 20 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.3-1
- Switch to jglobus2.

* Thu Sep 20 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.2.1-5
- Cleanup spec file in preparation of jglobus transition.

* Tue Jul 25 2012 Doug Strain <dstrain@fnal.gov> - 2.2.1-4
- Changes to client lib requirement to fix SOFTWARE-716

* Mon Jun 25 2012 Neha Sharma <neha@fnal.gov> - 2.2.1a
- Upgrade of Jetty Jars to 8.1.4.v20120524

* Tue Jun 12 2012 Doug Strain <dstrain@fnal.gov> - 2.2.1-3
- Changes to fix pid permission problems

* Thu May 17 2012 Doug Strain <dstrain@fnal.gov> - 2.2.1-2
- Added Neha's change to timeout (now 30 seconds)

* Thu May 17 2012 Doug Strain <dstrain@fnal.gov> - 2.2.1-1
- Fixed pid file in init script
- Added comments in srmclient.conf

* Tue May 01 2012 Doug Strain <dstrain@fnal.gov> - 2.2.1-0.rc3
- Modified build spec file to incorporate new build procedure
- Separated setup and sources directory with separate ant tasks.
- Changed binaries to use srm-common.sh
- Got rid of bestman2.sh
- Added delay and checking of pid process.

* Tue May 01 2012 Neha Sharma <neha@fnal.gov> - 2.2.0a-9
- modified bestman2.sh to give 10 sec to bestman server to
- startup and then get the correct exit code
- also, added proper check of startup process

* Tue May 01 2012 Neha Sharma <neha@fnal.gov> - 2.2.0a-8
- modified init script stop function to really check whether or not
- bestman server process is running and not give a 'fake OK'

* Thu Apr 26 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0a-7
- Fixed SOFTWARE-636: Reports java version error even if 
-   java is missing or heap size is broke

* Thu Apr 26 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0a-6
- Fixed a bouncycastle conflict in SL6

* Wed Apr 25 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0a-5
- Updated BeStMan client lib to include system dependencies
- Updated BeStMan client tools to use multi-line CLIENT_LIBs

* Fri Mar 02 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0a-2
- Changed build procedure to use dependent_jar.tar.gz
-- Separates all the dependencies into external
-- We will gradually prune these out into other rpms
- Changed all the libs to install only non-system jars
- Now classpaths grab from system jars when possible:
-- commons-discovery commons-logging wsdl4j 
-- xerces-j2 commons-collections joda-time 
-- glite-security-trustmanager glite-security-util-java
-- xalan-j2 log4j vomsjapi


* Tue Jan 31 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0-14
- Added a patch to fix Invalid Blocked Path issue

* Wed Jan 18 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0-13
- Added a default value for clients for ServiceHandle

* Wed Jan 18 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0-12
- Changed accessFileSysViaSudo=true and made sudoonLs explictly true

* Wed Jan 18 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 2.2.0-11
- Rebased bestman.server.patch for sl6 fuzz=0

* Wed Jan 18 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0-10
- This rpm spec was not grabbing the newly compiled lib jars
- Changed it so it would grab the jars from dist/ directory from ant

* Tue Jan 17 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0-9
- Added a patch to fix srmrm issues (SOFTWARE-482)

* Tue Jan 10 2012 Doug Strain <dstrain@fnal.gov> - 2.2.0-8
- Changed bestmanclient.conf to srmclient.conf
- Added default 8443 port
- Fixed build date / host

* Wed Dec 28 2011 Doug Strain <dstrain@fnal.gov> - 2.2.0-6
- Fixing various sysconfig for Bestman2 2.2.0
- Fixing classpath paths for sysconfig
- Changed GUMS default to XACML
- Changed cert default to /etc/grid-security/bestman/bestmancert.pem

* Fri Dec 16 2011 Doug Strain <dstrain@fnal.gov> - 2.2.0-1
- Updating for Bestman2 2.2.0
- Also done with Neha Sharma (neha@fnal.gov)

* Mon Nov 28 2011 Doug Strain <dstrain@fnal.gov> - 2.1.3-9
- Fixing chkconfig to be off by default

* Tue Nov 22 2011 Doug Strain <dstrain@fnal.gov> - 2.1.3-8
- Splitting sysconfig and configuration of bestman2.rc

* Tue Nov 22 2011 Doug Strain <dstrain@fnal.gov> - 2.1.3-6
- Added changes to fix SOFTWARE-384
- Changed SRM_OWNER to SRMOWNER
- Fixed version string in version file
- Disabled default start up

* Tue Nov 15 2011 Doug Strain <dstrain@fnal.gov> - 2.1.3-5
- Added post os install expression to disable redhat jar repacking
- This fixes the build date issue.

* Tue Nov 15 2011 Doug Strain <dstrain@fnal.gov> - 2.1.3-3
- Added bestman2.rc for srm-tester to function correctly.

* Fri Oct 28 2011 Doug Strain <dstrain@fnal.gov> - 2.1.3-2
- Updated for Bestman 2.1.3
- Fixed requires to java sun compat to pull sun jdk not openjdk

* Fri Aug 26 2011 Doug Strain <dstrain@fnal.gov> - 2.1.2-1
- Updated for Bestman 2.1.2

* Mon Aug 08 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.1.1-5
New bestman server patch

* Fri Aug 05 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.1.1-4
get rid of bestman2 dependency of client and server

* Wed Aug 3 2011 Doug Strain <dstrain@fnal.gov> 2.1.1-3
- Changing to use bestman user instead of daemon user.

* Mon Aug 1 2011 Doug Strain <dstrain@fnal.gov> 2.1.1-2
- Fixing dependencies

* Thu Jul 28 2011 Doug Strain <dstrain@fnal.gov> 2.1.1-1
- Updating bestman to 2.1.1.
- Splitting RPMs into multiple RPMS
-  common-libs,tester-libs,server-libs,client-libs,server-dep-libs

* Fri Jul 15 2011 Doug Strain <dstrain@fnal.gov> 2.1.0-3
- Fixing some rpmlint warnings and errors

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.1.0-3
- Fixed java deps to reflect new java strategy.

* Sun Jul 10 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre4-3
- Changed RPM to not require certs

* Mon Jul 07 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre4
- Updated to bestman2.1.0pre4
- Changed the locations to be FHS compliant:
- Moved java jar files to javadir/bestman2
- Moved bestman.server to sbindir
- Moved base location (now only configuration) to /etc/bestman2
- Moved bestman2.rc to /etc/bestman2/conf and added to client package
- Deleted setup directory in favor of combined bestman2.rc/sysconfig

* Mon Jul 01 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre2
- Creating Bestman2 spec file based on Hadoop repository

* Mon Jun 13 2011 Doug Strain <dstrain@fnal.gov> 2.0.13.t5-43
- Creating Bestman2 spec file based on Hadoop repository

* Wed May 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.12-3
- Add log4j.properties to Jetty, allowing the logging of GSI issues
- Fix deps for bestman2-server and -libs

* Tue May 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.12-2
- Split packages into server, libs, and client
- Move everything into FHS locations.

* Tue May 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.12-1
- Update to 2.0.12
- Change bestman2 to a source build
- Fix bestman.server.in so folks don't nuke their install if they run configure again.

* Mon Apr 25 2011 Jeff Dost <jdost@ucsd.edu> 2.0.10-1
- Update to 2.0.10

* Mon Apr 25 2011 Jeff Dost <jdost@ucsd.edu> 2.0.5-2
- Fix bestman.logrotate to point to /var/log/bestman2/*.log

* Wed Jan 26 2011 Jeff Dost <jdost@ucsd.edu> 2.0.5-1
- Update to 2.0.5

* Thu Dec 23 2010 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.4-2
- Patch the configuration file to use the correct port and some initial
  suggestions.

* Tue Dec 21 2010 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.4-1
- Bump to latest upstream version.
- Added "Obsoletes" for original bestman package since we have run
  bestman2 stably for awhile.

* Tue Oct 12 2010 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.2-4
- Fixed the init scripts to behave more like a RHEL init script.
- Added condrestart upon upgrade.

* Wed Sep 22 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.2-1
- Update to 2.0.2

* Thu Jul 1 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.0-3
- Update log file locations so that they don't conflict with earlier bestman

* Thu Jul 1 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.0-2
- Fix path problems in init script

* Tue Jun 8 2010 Michael Thomas <thomas@hep.caltech.edu> 2.0.0-1
- Initial package of bestman2, based on original bestman spec file

