Name:           bestman2
Version:        2.1.0
Release:        2
Summary:        SRM server for Grid Storage Elements

Group:          System Environment/Daemons
License:        https://sdm.lbl.gov/bestman/
URL:            https://sdm.lbl.gov/bestman/

%define install_root /etc/%{name}

# NOTE: CHANGE THESE EACH RELEASE
%define bestman_url https://codeforge.lbl.gov/frs/download.php/333/bestman2-2.1.0.tar.gz
%define revision 51

Source0:        bestman2.tar.gz
Source1:        bestman2.sh
Source2:        bestman2.init
Source3:        bestman.logrotate

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  jdk wget ant

Obsoletes: bestman

%description
BeStMan 2 - Berkeley Storage Manager

Application server for exporting local file systems securely using the
SRM protocol.  

BeStMan is a full implementation of SRM v2.2, developed by Lawrence Berkeley National Laboratory, for disk based storage systems and mass storage systems such as HPSS. End users may have their own personal BeStMan that manages and provides an SRM interface to their local disks or storage systems. It works on top of existing disk-based unix file system, and has been reported so far to work on file systems such as NFS, PVFS, AFS, GFS, GPFS, PNFS, and Lustre. It also works with any existing file transfer service, such as gsiftp, http, https and ftp.

User's guide : http://sdm.lbl.gov/bestman
General support and bug report to <srm@lbl.gov>
Open Science Grid (OSG) support:  osg-storage@opensciencegrid.org
BeStMan Copyright 2010-2011, The Regents of the University of California,
through Lawrence Berkeley National Laboratory.  See LICENSE file for details.

%package server
Summary: BeStMan SRM server
Group: System Environment/Daemons

Obsoletes: bestman2

Requires: %{name}-libs = %{version}-%{release}
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

%description server
BeStMan SRM server

%package libs
Summary: BeStMan SRM Java libraries
Group: System Environment/Libraries
Requires:  jdk
%description libs
The BeStMan SRM Java libraries

%package client
Summary: SRM clients
Group: System Environment/Applications
Requires: %{name}-libs = %{version}-%{release}
%description client
The srm-* client tools

%prep
%setup -q -n %{name}

%build

# NOTE: Upstream package can be created with the following procedure:
# svn checkout -r 50 https://codeforge.lbl.gov/anonscm/bestman
# pushd bestman
# wget https://codeforge.lbl.gov/frs/download.php/316/bestman2-2.1.0-pre2.tar.gz
# tar xvzf bestman2-2.1.0-pre2.tar.gz
# popd
# mv bestman bestman2
# tar cvzf bestman2.tar.gz bestman2
# NOTE: Revision number (50) and url/tarball name may change per release.

./build.configure --with-bestman-url=%{bestman_url} --with-bestman2-version=%{version} --with-revision=%{revision} --with-java-home=/usr/java/latest --enable-cached-src=yes --enable-cached-pkg=yes

make

pushd bestman2

SRM_HOME=%{install_root}
export SRM_HOME
GLOBUS_LOCATION=/usr
export GLOBUS_LOCATION

pushd setup
./configure --with-srm-home=$SRM_HOME \
    --enable-gateway-mode \
    --enable-gums \
    --enable-sudofsmng \
    --with-java-home=/usr/java/latest \
    --with-eventlog-path=/var/log/%{name} \
    --with-cachelog-path=/var/log/%{name} \
    --with-plugin-path=$SRM_HOME/lib \
    --with-gums-url=https://GUMS_HOST:8443/gums/services/GUMSAuthorizationServicePort \
    --enable-backup=no \
    --with-bestman2-conf-path=../conf/bestman2.rc
popd

#    --with-certfile-path=/etc/grid-security/http/httpcert.pem \
#    --with-keyfile-path=/etc/grid-security/http/httpkey.pem \
#    --with-gums-certfile-path=/etc/grid-security/http/httpcert.pem \
#    --with-gums-keyfile-path=/etc/grid-security/http/httpkey.pem \

#Fix paths in bestman2.rc
JAVADIR=`echo %{_javadir} |  sed 's/\//\\\\\//g'`
sed -i "s/SRM_HOME=.*/SRM_HOME=\/etc\/bestman2/" conf/bestman2.rc
sed -i "s/SRM_OWNER=.*/SRM_OWNER=daemon/" conf/bestman2.rc
sed -i "s/GridMapFileName=.*/GridMapFileName=\/etc\/bestman2\/conf\/grid-mapfile.empty/" conf/bestman2.rc
sed -i "s/BESTMAN_SYSCONF=.*/BESTMAN_SYSCONF=\/etc\/bestman2\/conf\/bestman2.rc/" conf/bestman2.rc
sed -i "s/BESTMAN_LOG=.*/BESTMAN_LOG=\/var\/log\/bestman2\/bestman2.log/" conf/bestman2.rc
sed -i "s/BESTMAN_LIB=.*/BESTMAN_LIB=$JAVADIR\/bestman2/" conf/bestman2.rc
sed -i "s/EventLogLocation=.*/EventLogLocation=\/var\/log\/bestman2/" conf/bestman2.rc
sed -i "s/X509_CERT_DIR=.*/X509_CERT_DIR=\/etc\/grid-security\/certificates/" conf/bestman2.rc
sed -i "s/BESTMAN_GUMSCERTPATH=.*/BESTMAN_GUMSCERTPATH=\/etc\/grid-security\/http\/httpcert.pem/" conf/bestman2.rc
sed -i "s/BESTMAN_GUMSKEYPATH=.*/BESTMAN_GUMSKEYPATH=\/etc\/grid-security\/http\/httpkey.pem/" conf/bestman2.rc
sed -i "s/CertFileName=.*/CertFileName=\/etc\/grid-security\/http\/httpcert.pem/" conf/bestman2.rc
sed -i "s/KeyFileName=.*/KeyFileName=\/etc\/grid-security\/http\/httpkey.pem/" conf/bestman2.rc

#Fix paths in binaries.  Wish I could do this in configure...
sed -i "s/SRM_HOME=\/.*/SRM_HOME=\/etc\/bestman2/" bin/*

popd

%install
rm -rf $RPM_BUILD_ROOT

pushd bestman2



mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{install_root}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp -arp conf $RPM_BUILD_ROOT%{install_root}
cp -arp lib $RPM_BUILD_ROOT%{_javadir}/%{name}
cp -arp properties $RPM_BUILD_ROOT%{install_root}


install -m 0755 version $RPM_BUILD_ROOT%{install_root}/
install -m 0755 sbin/bestman.server $RPM_BUILD_ROOT%{_sbindir}/bestman.server


mkdir -p $RPM_BUILD_ROOT%{_bindir}
for i in `ls bin`; do
  install -m 0755 bin/$i $RPM_BUILD_ROOT%{_bindir}/
done

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir
touch $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem

mkdir -p $RPM_BUILD_ROOT%{_var}/log/%{name}

popd

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
getent group daemon >/dev/null || groupadd -r daemon
getent passwd daemon >/dev/null || \
       useradd -r -g daemon -d %{install_root} -c "General daemon user" \
       -s /bin/bash daemon

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

%files libs
%defattr(-,root,root,-)
%dir %{install_root}
%{_javadir}/bestman2/axis
%{_javadir}/bestman2/jglobus
%{_javadir}/bestman2/bestman2.jar
%{_javadir}/bestman2/bestman2-stub.jar
%{_javadir}/bestman2/bestman2-printintf.jar
%{_javadir}/bestman2/bestman2-transfer.jar
%{install_root}/version
%{install_root}/properties

%files client
%defattr(-,root,root,-)
%{_javadir}/bestman2/bestman2-aux.jar
%{_javadir}/bestman2/bestman2-client.jar
%{_javadir}/bestman2/bestman2-tester-driver.jar
%{_javadir}/bestman2/bestman2-tester-main.jar
%config(noreplace) %{install_root}/conf/srmclient.conf
%{install_root}/conf/srmclient.conf.sample
%config(noreplace) %{install_root}/conf/srmtester.conf
%config(noreplace) %{install_root}/conf/bestman2.rc
%{install_root}/conf/srmtester.conf.sample
%{_bindir}/*

%files server
%defattr(-,root,root,-)
%{_javadir}/bestman2/others
%{_javadir}/bestman2/voms
%{_javadir}/bestman2/gums
%{_javadir}/bestman2/gums2
%{_javadir}/bestman2/jetty
%{_javadir}/bestman2/plugin
%{_sbindir}/bestman.server
%{install_root}/conf/WEB-INF
%{install_root}/conf/bestman2.gateway.sample.rc
%{install_root}/conf/grid-mapfile.empty
%{install_root}/conf/bestman-diag-msg.conf
%{install_root}/conf/bestman-diag.conf.sample
%config(noreplace) %{install_root}/conf/bestman2.rc
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644,root,root) %{_sysconfdir}/grid-security/vomsdir/vdt-empty.pem
%attr(-,daemon,daemon) %dir %{_var}/log/%{name}

%changelog
* Sun Jul 10 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre4-3
- Changed RPM to not require certs

* Mon Jul 07 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre4
Updated to bestman2.1.0pre4
Changed the locations to be FHS compliant:
- Moved java jar files to javadir/bestman2
- Moved bestman.server to sbindir
- Moved base location (now only configuration) to /etc/bestman2
- Moved bestman2.rc to /etc/bestman2/conf and added to client package
- Deleted setup directory in favor of combined bestman2.rc/sysconfig

* Mon Jul 01 2011 Doug Strain <dstrain@fnal.gov> 2.1.0.pre2
Creating Bestman2 spec file based on Hadoop repository

* Mon Jun 13 2011 Doug Strain <dstrain@fnal.gov> 2.0.13.t5-43
Creating Bestman2 spec file based on Hadoop repository

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

