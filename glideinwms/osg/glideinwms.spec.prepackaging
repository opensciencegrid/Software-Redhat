# The following should be either "v2_plus" or "v3_plus"
%define v2_plus 1
%define v3_plus 0

Name:           glideinwms

%if %{v2_plus}
%define version 2.6.3
%define release 0.rc2.6
%define frontend_xml frontend.xml
%define factory_xml glideinWMS.xml
%endif

%if %{v3_plus}
%define version 3.0.0 
%define release 5
%define frontend_xml frontend.master.xml
%define factory_xml glideinWMS.master.xml
%endif

Version:        %{version}
Release:        %{release}%{?dist}

Summary:        The VOFrontend for glideinWMS submission host

Group:          System Environment/Daemons
License:        Fermitools Software Legal Information (Modified BSD License)
URL:            http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v2/manual/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%define web_dir %{_localstatedir}/lib/gwms-frontend/web-area
%define web_base %{_localstatedir}/lib/gwms-frontend/web-base
%define frontend_dir %{_localstatedir}/lib/gwms-frontend/vofrontend
%define factory_web_dir %{_localstatedir}/lib/gwms-factory/web-area
%define factory_web_base %{_localstatedir}/lib/gwms-factory/web-base
%define factory_dir %{_localstatedir}/lib/gwms-factory/work-dir
%define condor_dir %{_localstatedir}/lib/gwms-factory/condor


#Source0:        http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/glideinWMS_v2_5_1_frontend.tgz
Source:	glideinwms.tar.gz

# How to build tar file
# git clone http://cdcvs.fnal.gov/projects/glideinwms
# cd glideinwms
# git archive v3_0_rc3 --prefix='glideinwms/' | gzip > ../glideinwms.tar.gz
# change v3_0_rc3 to the proper tag in the above line

Source1:        frontend_startup
Source2:        %{frontend_xml}
Source3:        gwms-frontend.conf.httpd
Source4:	%{factory_xml}
Source5:       gwms-factory.conf.httpd
Source6:       factory_startup
Source7:	chksum.sh

%description
This is a package for the glidein workload management system.
GlideinWMS provides a simple way to access the Grid resources
through a dynamic condor pool of grid-submitted resources.
Two packages exist (factory and vofrontend) plus 
dependent condor packages for additional condor customizability.

%package vofrontend
Summary:        The VOFrontend for glideinWMS submission host
Group:          System Environment/Daemons
Provides:	GlideinWMSFrontend = %{version}-%{release}
Obsoletes:	GlideinWMSFrontend < 2.5.1-11
Requires: glideinwms-vofrontend-standalone
Requires: glideinwms-userschedd
Requires: glideinwms-usercollector
Obsoletes: glideinwms-vofrontend-condor < 2.6.2-2

%description vofrontend
The purpose of the glideinWMS is to provide a simple way 
to access the Grid resources. GlideinWMS is a Glidein 
Based WMS (Workload Management System) that works on top of 
Condor. For those familiar with the Condor system, it is used 
for scheduling and job control. 
This package is for a one-node vofrontend install
(userschedd,submit,vofrontend).


%package vofrontend-standalone
Summary:        The VOFrontend for glideinWMS submission host
Group:          System Environment/Daemons
Requires: httpd
# We require Condor 7.6.0 (and newer) to support
# condor_advertise -multiple -tcp which is enabled by default
Requires: condor >= 7.6.0
Requires: python-rrdtool
Requires: m2crypto
Requires: javascriptrrd
Requires: osg-client
Requires: glideinwms-minimal-condor
Requires: condor >= 7.6.0
#To be added in 2.6.3+ once probe is finished.
#Requires: gratia-probe-gwms
#Requires: vdt-vofrontend-essentials
Requires(post): /sbin/service
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig

%description vofrontend-standalone
The purpose of the glideinWMS is to provide a simple way
to access the Grid resources. GlideinWMS is a Glidein
Based WMS (Workload Management System) that works on top of
Condor. For those familiar with the Condor system, it is used
for scheduling and job control.
This package is for a standalone vofrontend install

%package usercollector
Summary:        The VOFrontend glideinWMS collector host
Group:          System Environment/Daemons
Requires: condor >= 7.6.0
%description usercollector
The user collector matches user jobs to glideins in the user pool.
It can be split off into its own node.

%package userschedd
Summary:        The VOFrontend glideinWMS submission host
Group:          System Environment/Daemons
Requires: condor >= 7.6.0
%description userschedd
This is a package for a glideinwms submit host.


%package minimal-condor
Summary:        The VOFrontend minimal condor config
Group:          System Environment/Daemons
Provides: gwms-condor-config

%description minimal-condor
This is an alternate condor config for just the minimal amount
needed for vofrontend.


%package factory
Summary:        The Factory for glideinWMS
Group:          System Environment/Daemons
Provides:       GlideinWMSFactory = %{version}-%{release}
Requires: httpd
# We require Condor 7.6.0 (and newer) to support
# condor_advertise -multiple -tcp which is enabled by default
Requires: condor >= 7.6.0
Requires: python-rrdtool
Requires: m2crypto
Requires: javascriptrrd
Requires: gwms-factory-config
Requires(post): /sbin/service
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig

%description factory
The purpose of the glideinWMS is to provide a simple way
to access the Grid resources. GlideinWMS is a Glidein
Based WMS (Workload Management System) that works on top of
Condor. For those familiar with the Condor system, it is used
for scheduling and job control.



%package factory-condor
Summary:        The VOFrontend condor config
Group:          System Environment/Daemons
Provides: gwms-factory-config

%description factory-condor
This is a package including condor_config for a full one-node
install of wmscollector + wms factory




%prep
%setup -q -n glideinwms
# Apply the patches
#%patch -P 0 -p1
#%patch -P 1 -p1
#%patch -P 2 -p1
#%patch -P 3 -p1

%build
cp %{SOURCE7} .
chmod 700 chksum.sh
./chksum.sh v%{version}-%{release}.osg etc/checksum.frontend "CVS config_examples doc .git .gitattributes poolwatcher factory/check* factory/glideFactory* factory/test* factory/manage* factory/stop* factory/tools creation/create_glidein creation/reconfig_glidein creation/info_glidein creation/lib/cgW* creation/web_base/factory*html creation/web_base/collector_setup.sh creation/web_base/condor_platform_select.sh creation/web_base/condor_startup.sh creation/web_base/create_mapfile.sh creation/web_base/gcb_setup.sh creation/web_base/glexec_setup.sh creation/web_base/glidein_startup.sh creation/web_base/job_submit.sh creation/web_base/local_start.sh creation/web_base/setup_x509.sh creation/web_base/validate_node.sh chksum.sh etc/checksum*"
./chksum.sh v%{version}-%{release}.osg etc/checksum.factory "CVS config_examples doc .git .gitattributes poolwatcher frontend/* creation/reconfig_glidein creation/lib/cgW* creation/web_base/factory*html creation/web_base/collector_setup.sh creation/web_base/condor_platform_select.sh creation/web_base/condor_startup.sh creation/web_base/create_mapfile.sh creation/web_base/gcb_setup.sh creation/web_base/glexec_setup.sh creation/web_base/glidein_startup.sh creation/web_base/job_submit.sh creation/web_base/local_start.sh creation/web_base/setup_x509.sh creation/web_base/validate_node.sh chksum.sh etc/checksum*"

%install
rm -rf $RPM_BUILD_ROOT

# Set the Python version
%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

# From http://fedoraproject.org/wiki/Packaging:Python
# Define python_sitelib
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#Change src_dir in reconfig_Frontend
sed -i "s/WEB_BASE_DIR=.*/WEB_BASE_DIR=\"\/var\/lib\/gwms-frontend\/web-base\"/" creation/reconfig_frontend
sed -i "s/STARTUP_DIR=.*/STARTUP_DIR=\"\/var\/lib\/gwms-frontend\/web-base\"/" creation/reconfig_frontend
sed -i "s/WEB_BASE_DIR=.*/WEB_BASE_DIR=\"\/var\/lib\/gwms-factory\/web-base\"/" creation/reconfig_glidein
sed -i "s/STARTUP_DIR =.*/STARTUP_DIR=\"\/var\/lib\/gwms-factory\/web-base\"/" creation/reconfig_glidein

# install the executables
install -d $RPM_BUILD_ROOT%{_sbindir}
# Find all the executables in the frontend directory
install -m 0500 frontend/checkFrontend.py $RPM_BUILD_ROOT%{_sbindir}/checkFrontend
install -m 0500 frontend/glideinFrontendElement.py $RPM_BUILD_ROOT%{_sbindir}/glideinFrontendElement.py
install -m 0500 frontend/glideinFrontend.py $RPM_BUILD_ROOT%{_sbindir}/glideinFrontend
install -m 0500 frontend/stopFrontend.py $RPM_BUILD_ROOT%{_sbindir}/stopFrontend
install -m 0500 creation/reconfig_frontend $RPM_BUILD_ROOT%{_sbindir}/reconfig_frontend

#install the factory executables
install -m 0500 factory/checkFactory.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/glideFactory.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/glideFactoryEntry.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/manageFactoryDowntimes.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 factory/stopFactory.py $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 creation/reconfig_glidein $RPM_BUILD_ROOT%{_sbindir}/
install -m 0500 creation/info_glidein $RPM_BUILD_ROOT%{_sbindir}/


# install the library parts
# FIXME: Need to create a subdirectory for vofrontend python files
install -d $RPM_BUILD_ROOT%{python_sitelib}
cp lib/*.py $RPM_BUILD_ROOT%{python_sitelib}
cp frontend/*.py $RPM_BUILD_ROOT/%{python_sitelib}
cp factory/*.py $RPM_BUILD_ROOT/%{python_sitelib}
cp creation/lib/*.py $RPM_BUILD_ROOT%{python_sitelib}


# Install the init.d
install -d  $RPM_BUILD_ROOT/%{_initrddir}
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/gwms-frontend
install -m 0755 %{SOURCE6} $RPM_BUILD_ROOT/%{_initrddir}/gwms-factory


# Install the web directory
install -d $RPM_BUILD_ROOT%{frontend_dir}
install -d $RPM_BUILD_ROOT%{web_base}
install -d $RPM_BUILD_ROOT%{web_dir}
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/
install -d $RPM_BUILD_ROOT%{web_dir}/stage/
install -d $RPM_BUILD_ROOT%{web_dir}/stage/group_main
install -d $RPM_BUILD_ROOT%{factory_dir}
install -d $RPM_BUILD_ROOT%{factory_web_base}
install -d $RPM_BUILD_ROOT%{factory_web_dir}
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/
install -d $RPM_BUILD_ROOT%{factory_web_dir}/stage/
install -d $RPM_BUILD_ROOT%{factory_dir}/lock
install -d $RPM_BUILD_ROOT%{condor_dir}


install -d $RPM_BUILD_ROOT%{web_dir}/monitor/lock
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/jslibs
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/total
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main/lock
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main/total
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/lock
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/jslibs
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/total
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/group_main
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/group_main/lock
install -d $RPM_BUILD_ROOT%{factory_web_dir}/monitor/group_main/total

install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{web_dir}/stage/nodes.blacklist
install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{web_dir}/stage/group_main/nodes.blacklist

# Install the logs
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/frontend
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/group_main
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory/server
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory/server/factory
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-factory/client
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gwms-factory/client-proxies


# Install frontend temp dir, for all the frontend.xml.<checksum>
install -d $RPM_BUILD_ROOT%{frontend_dir}/lock
#install -d $RPM_BUILD_ROOT%{frontend_dir}/monitor
#install -d $RPM_BUILD_ROOT%{frontend_dir}/monitor/group_main
install -d $RPM_BUILD_ROOT%{frontend_dir}/group_main
install -d $RPM_BUILD_ROOT%{frontend_dir}/group_main/lock
#install -d $RPM_BUILD_ROOT%{frontend_dir}/group_main/monitor

install -m 644 creation/web_base/frontendRRDBrowse.html $RPM_BUILD_ROOT%{web_dir}/monitor/frontendRRDBrowse.html
install -m 644 creation/web_base/frontendRRDGroupMatrix.html $RPM_BUILD_ROOT%{web_dir}/monitor/frontendRRDGroupMatrix.html  
install -m 644 creation/web_base/frontendStatus.html $RPM_BUILD_ROOT%{web_dir}/monitor/frontendStatus.html 
install -m 644 creation/web_base/frontend/index.html $RPM_BUILD_ROOT%{web_dir}/monitor/
install -m 644 creation/web_base/factory/index.html $RPM_BUILD_ROOT%{factory_web_dir}/monitor/
cp -arp creation/web_base/factory/images $RPM_BUILD_ROOT%{factory_web_dir}/monitor/
cp -arp creation/web_base/frontend/images $RPM_BUILD_ROOT%{web_dir}/monitor/

# Install the frontend config dir
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend/frontend.xml

# Install the factory config dir
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-factory
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-factory/glideinWMS.xml

# Install the web base
cp -r creation/web_base/* $RPM_BUILD_ROOT%{web_base}/
cp -r creation/web_base/* $RPM_BUILD_ROOT%{factory_web_base}/
rm -rf $RPM_BUILD_ROOT%{web_base}/CVS

# Install condor stuff
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor/certs
#make sure this (new) file exists, can be deprecated in gwms 2.7 or so
touch install/templates/90_gwms_dns.config
install -m 0644 install/templates/90_gwms_dns.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/00_gwms_general.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/00_gwms_factory_general.config
install -m 0644 install/templates/00_gwms_general.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/01_gwms_collectors.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/01_gwms_factory_collectors.config
install -m 0644 install/templates/01_gwms_collectors.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/02_gwms_factory_schedds.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/02_gwms_schedds.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/03_gwms_local.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/03_gwms_factory_local.config
install -m 0644 install/templates/03_gwms_local.config $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 install/templates/condor_mapfile $RPM_BUILD_ROOT%{_sysconfdir}/condor/certs/
install -m 0644 install/templates/privsep_config $RPM_BUILD_ROOT%{_sysconfdir}/condor/

sed -i "s/^COLLECTOR_NAME = .*$/COLLECTOR_NAME = wmscollector_service/" $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/01_gwms_factory_collectors.config
sed -i "s/^DAEMON_LIST.*=.*$//" $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/01_gwms_factory_collectors.config
sed -i 's/^COLLECTOR[0-9]*.\\//' $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/01_gwms_factory_collectors.config
echo 'DAEMON_LIST   = $(DAEMON_LIST),  COLLECTOR, NEGOTIATOR' >> $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/01_gwms_factory_collectors.config


#Install condor schedd dirs
for schedd in "schedd_glideins2" "schedd_glideins3" "schedd_glideins4" "schedd_glideins5" "schedd_jobs2"; do
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/execute
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/lock
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/procd_pipe
	install -d $RPM_BUILD_ROOT/var/lib/condor/$schedd/spool
done


# Install tools
install -d $RPM_BUILD_ROOT%{_bindir}
# Install the tools as the non-*.py filenames
for file in `ls tools/*.py`; do
   newname=`echo $file | sed -e 's/.*\/\(.*\)\.py/\1/'`
   cp $file $RPM_BUILD_ROOT%{_bindir}/$newname
done
for file in `find factory/tools -type f -maxdepth 1`; do
   newname=`echo $file | sed -e 's/\(.*\)\.py/\1/'`
   newname=`echo $newname | sed -e 's/.*\/\(.*\)/\1/'`
   cp $file $RPM_BUILD_ROOT%{_bindir}/$newname
done
cp factory/tools/lib/*.py $RPM_BUILD_ROOT%{python_sitelib}
cp tools/lib/*.py $RPM_BUILD_ROOT%{python_sitelib}
cp creation/create_condor_tarball $RPM_BUILD_ROOT%{_bindir}

# Install glidecondor
install -m 0755 install/glidecondor_addDN $RPM_BUILD_ROOT%{_sbindir}/glidecondor_addDN

# Install checksum file
install -m 0644 etc/checksum.frontend $RPM_BUILD_ROOT%{frontend_dir}/checksum.frontend
install -m 0644 etc/checksum.factory $RPM_BUILD_ROOT%{factory_dir}/checksum.factory

#Install web area conf
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/gwms-frontend.conf
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/gwms-factory.conf

%if %{v3_plus}
install -d $RPM_BUILD_ROOT%{web_base}/../creation
install -d $RPM_BUILD_ROOT%{web_base}/../creation/templates
install -d $RPM_BUILD_ROOT%{factory_web_base}/../creation
install -d $RPM_BUILD_ROOT%{factory_web_base}/../creation/templates
install -m 0644 creation/templates/factory_initd_startup_template $RPM_BUILD_ROOT%{factory_web_base}/../creation/templates/
install -m 0644 creation/templates/frontend_initd_startup_template $RPM_BUILD_ROOT%{web_base}/../creation/templates/
%endif

%post vofrontend-standalone
# $1 = 1 - Installation
# $1 = 2 - Upgrade
# Source: http://www.ibm.com/developerworks/library/l-rpm2/

fqdn_hostname=`hostname -f`
frontend_name=`echo $fqdn_hostname | sed 's/\./-/g'`_OSG_gWMSFrontend

sed -i "s/FRONTEND_NAME_CHANGEME/$frontend_name/g" %{_sysconfdir}/gwms-frontend/frontend.xml
sed -i "s/FRONTEND_HOSTNAME/$fqdn_hostname/g" %{_sysconfdir}/gwms-frontend/frontend.xml

/sbin/chkconfig --add gwms-frontend
ln -s %{web_dir}/monitor %{frontend_dir}/monitor

%post factory

fqdn_hostname=`hostname -f`
sed -i "s/FACTORY_HOSTNAME/$fqdn_hostname/g" %{_sysconfdir}/gwms-factory/glideinWMS.xml
if [ "$1" = "1" ] ; then
    ln -s %{factory_web_dir}/monitor %{factory_dir}/monitor
    ln -s %{_localstatedir}/log/gwms-factory %{factory_dir}/log
fi

%pre vofrontend-standalone

# Add the "frontend" user 
getent group frontend >/dev/null || groupadd -r frontend
getent passwd frontend >/dev/null || \
       useradd -r -g frontend -d /var/lib/gwms-frontend \
	-c "VO Frontend user" -s /sbin/nologin frontend

%pre factory
# Add the "gfactory" user 
getent group gfactory >/dev/null || groupadd -r gfactory
getent passwd gfactory >/dev/null || \
       useradd -r -g gfactory -d /var/lib/gwms-factory \
	-c "GlideinWMS Factory user" -s /sbin/nologin gfactory
getent group frontend >/dev/null || groupadd -r frontend
getent passwd frontend >/dev/null || \
       useradd -r -g frontend -d /var/lib/gwms-frontend \
	-c "VO Frontend user" -s /sbin/nologin frontend

%preun vofrontend-standalone
# $1 = 0 - Action is uninstall
# $1 = 1 - Action is upgrade

if [ "$1" = "0" ] ; then
    /sbin/chkconfig --del gwms-frontend
fi

if [ "$1" = "0" ]; then
    # Remove the symlinks
    rm -f %{frontend_dir}/frontend.xml
    rm -f %{frontend_dir}/monitor
    rm -f %{frontend_dir}/group_main/monitor

    # A lot of files are generated, but rpm won't delete those
#    rm -rf %{_datadir}/gwms-frontend
#    rm -rf %{_localstatedir}/log/gwms-frontend/*
fi

%preun factory
if [ "$1" = "0" ] ; then
    /sbin/chkconfig --del gwms-factory
fi
if [ "$1" = "0" ]; then
    rm -f %{factory_dir}/log
    rm -f %{factory_dir}/monitor
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files vofrontend
   
%files factory
%defattr(-,gfactory,gfactory,-)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/checkFactory.py
%attr(755,root,root) %{_sbindir}/stopFactory.py
%attr(755,root,root) %{_sbindir}/glideFactory.py
%attr(755,root,root) %{_sbindir}/glideFactoryEntry.py

%if %{?rhel}%{!?rhel:0} == 5
%attr(755,root,root) %{_sbindir}/checkFactory.pyc
%attr(755,root,root) %{_sbindir}/checkFactory.pyo
%attr(755,root,root) %{_sbindir}/glideFactory.pyc
%attr(755,root,root) %{_sbindir}/glideFactory.pyo
%attr(755,root,root) %{_sbindir}/glideFactoryEntry.pyc
%attr(755,root,root) %{_sbindir}/glideFactoryEntry.pyo
%attr(755,root,root) %{_sbindir}/manageFactoryDowntimes.pyc
%attr(755,root,root) %{_sbindir}/manageFactoryDowntimes.pyo
%attr(755,root,root) %{_sbindir}/stopFactory.pyc
%attr(755,root,root) %{_sbindir}/stopFactory.pyo
%endif
%attr(755,root,root) %{_sbindir}/glidecondor_addDN
%attr(755,root,root) %{_sbindir}/info_glidein
%attr(755,root,root) %{_sbindir}/manageFactoryDowntimes.py
%attr(755,root,root) %{_sbindir}/reconfig_glidein
%attr(-, root, root) %dir %{_localstatedir}/lib/gwms-factory
%attr(-, root, root) %{_localstatedir}/lib/gwms-factory/client-proxies
%attr(-, gfactory, gfactory) %{factory_web_dir}
%attr(-, gfactory, gfactory) %{factory_web_base}

%if %{v3_plus}
%attr(-, gfactory, gfactory) %{factory_web_base}/../creation
%endif
%attr(-, gfactory, gfactory) %{factory_dir}
%attr(-, gfactory, gfactory) %dir %{condor_dir}
%attr(-, root, root) %dir %{_localstatedir}/log/gwms-factory
%attr(-, root, root) %dir %{_localstatedir}/log/gwms-factory/client
%attr(-, gfactory, gfactory) %{_localstatedir}/log/gwms-factory/server
%{python_sitelib}/cWConsts.py
%{python_sitelib}/cWConsts.pyc
%{python_sitelib}/cWConsts.pyo
%{python_sitelib}/cWDictFile.py
%{python_sitelib}/cWDictFile.pyc
%{python_sitelib}/cWDictFile.pyo
%{python_sitelib}/cWParams.py
%{python_sitelib}/cWParams.pyc
%{python_sitelib}/cWParams.pyo
%{python_sitelib}/cgWConsts.py
%{python_sitelib}/cgWConsts.pyc
%{python_sitelib}/cgWConsts.pyo
%{python_sitelib}/cgWCreate.py
%{python_sitelib}/cgWCreate.pyc
%{python_sitelib}/cgWCreate.pyo
%{python_sitelib}/cgWDictFile.py
%{python_sitelib}/cgWDictFile.pyc
%{python_sitelib}/cgWDictFile.pyo
%{python_sitelib}/cgWParamDict.py
%{python_sitelib}/cgWParamDict.pyo
%{python_sitelib}/cgWParamDict.pyc
%{python_sitelib}/cgWParams.py
%{python_sitelib}/cgWParams.pyc
%{python_sitelib}/cgWParams.pyo
%{python_sitelib}/checkFactory.py
%{python_sitelib}/checkFactory.pyo
%{python_sitelib}/checkFactory.pyc
%{python_sitelib}/condorExe.py
%{python_sitelib}/condorExe.pyc
%{python_sitelib}/condorExe.pyo
%{python_sitelib}/condorLogParser.py
%{python_sitelib}/condorLogParser.pyc
%{python_sitelib}/condorLogParser.pyo
%{python_sitelib}/condorManager.py
%{python_sitelib}/condorMonitor.py
%{python_sitelib}/condorPrivsep.py
%{python_sitelib}/condorPrivsep.pyc
%{python_sitelib}/condorPrivsep.pyo
%{python_sitelib}/condorSecurity.py
%{python_sitelib}/condorSecurity.pyc
%{python_sitelib}/condorSecurity.pyo
%{python_sitelib}/exprParser.py
%{python_sitelib}/exprParser.pyo
%{python_sitelib}/exprParser.pyc
%{python_sitelib}/glideFactory.py
%{python_sitelib}/glideFactory.pyc
%{python_sitelib}/glideFactory.pyo
%{python_sitelib}/glideFactoryConfig.py
%{python_sitelib}/glideFactoryConfig.pyc
%{python_sitelib}/glideFactoryConfig.pyo
%{python_sitelib}/glideFactoryDowntimeLib.py
%{python_sitelib}/glideFactoryDowntimeLib.pyc
%{python_sitelib}/glideFactoryDowntimeLib.pyo
%{python_sitelib}/glideFactoryEntry.py
%{python_sitelib}/glideFactoryEntry.pyc
%{python_sitelib}/glideFactoryEntry.pyo
%{python_sitelib}/glideFactoryInterface.py
%{python_sitelib}/glideFactoryInterface.pyc
%{python_sitelib}/glideFactoryInterface.pyo
%{python_sitelib}/glideFactoryLib.py
%{python_sitelib}/glideFactoryLib.pyc
%{python_sitelib}/glideFactoryLib.pyo
%{python_sitelib}/glideFactoryLogParser.py
%{python_sitelib}/glideFactoryLogParser.pyc
%{python_sitelib}/glideFactoryLogParser.pyo
%{python_sitelib}/glideFactoryMonitorAggregator.py
%{python_sitelib}/glideFactoryMonitorAggregator.pyc
%{python_sitelib}/glideFactoryMonitorAggregator.pyo
%{python_sitelib}/glideFactoryMonitoring.py
%{python_sitelib}/glideFactoryMonitoring.pyo
%{python_sitelib}/glideFactoryMonitoring.pyc
%{python_sitelib}/glideFactoryPidLib.py
%{python_sitelib}/glideFactoryPidLib.pyc
%{python_sitelib}/glideFactoryPidLib.pyo
%{python_sitelib}/glideinCmd.py
%{python_sitelib}/glideinCmd.pyc
%{python_sitelib}/glideinCmd.pyo
%{python_sitelib}/glideinMonitor.py
%{python_sitelib}/glideinMonitor.pyc
%{python_sitelib}/glideinMonitor.pyo
%{python_sitelib}/glideinWMSVersion.py
%{python_sitelib}/glideinWMSVersion.pyc
%{python_sitelib}/glideinWMSVersion.pyo
%{python_sitelib}/hashCrypto.py
%{python_sitelib}/hashCrypto.pyc
%{python_sitelib}/hashCrypto.pyo
%{python_sitelib}/ldapMonitor.py
%{python_sitelib}/ldapMonitor.pyc
%{python_sitelib}/ldapMonitor.pyo
%{python_sitelib}/logSupport.py
%{python_sitelib}/logSupport.pyc
%{python_sitelib}/logSupport.pyo
%{python_sitelib}/manageFactoryDowntimes.py
%{python_sitelib}/manageFactoryDowntimes.pyc
%{python_sitelib}/manageFactoryDowntimes.pyo
%{python_sitelib}/pidSupport.py
%{python_sitelib}/pidSupport.pyc
%{python_sitelib}/pidSupport.pyo
%{python_sitelib}/pubCrypto.py
%{python_sitelib}/pubCrypto.pyc
%{python_sitelib}/pubCrypto.pyo
%{python_sitelib}/rrdSupport.py
%{python_sitelib}/rrdSupport.pyc
%{python_sitelib}/rrdSupport.pyo
%{python_sitelib}/stopFactory.py
%{python_sitelib}/stopFactory.pyc
%{python_sitelib}/stopFactory.pyo
%{python_sitelib}/symCrypto.py
%{python_sitelib}/symCrypto.pyc
%{python_sitelib}/symCrypto.pyo
%{python_sitelib}/subprocessSupport.py
%{python_sitelib}/subprocessSupport.pyc
%{python_sitelib}/subprocessSupport.pyo
%{python_sitelib}/test_advertize.py
%{python_sitelib}/test_advertize.pyc
%{python_sitelib}/test_advertize.pyo
%{python_sitelib}/test_cm.py
%{python_sitelib}/test_cm.pyc
%{python_sitelib}/test_cm.pyo
%{python_sitelib}/test_gfi.py
%{python_sitelib}/test_gfi.pyc
%{python_sitelib}/test_gfi.pyo
%{python_sitelib}/timeConversion.py
%{python_sitelib}/timeConversion.pyc
%{python_sitelib}/timeConversion.pyo
%{python_sitelib}/xmlFormat.py
%{python_sitelib}/xmlFormat.pyc
%{python_sitelib}/xmlFormat.pyo
%{python_sitelib}/xmlParse.py
%{python_sitelib}/xmlParse.pyc
%{python_sitelib}/xmlParse.pyo
%{python_sitelib}/analyze.py
%{python_sitelib}/analyze.pyc
%{python_sitelib}/analyze.pyo
%{python_sitelib}/gWftArgsHelper.py
%{python_sitelib}/gWftArgsHelper.pyc
%{python_sitelib}/gWftArgsHelper.pyo
%{python_sitelib}/gWftLogParser.py
%{python_sitelib}/gWftLogParser.pyc
%{python_sitelib}/gWftLogParser.pyo
%{_initrddir}/gwms-factory
%config(noreplace) %{_sysconfdir}/httpd/conf.d/gwms-factory.conf
%attr(-, gfactory, gfactory) %dir %{_sysconfdir}/gwms-factory
%attr(-, gfactory, gfactory) %config(noreplace) %{_sysconfdir}/gwms-factory/glideinWMS.xml
%if %{v3_plus}
%{python_sitelib}/classadSupport.py
%{python_sitelib}/classadSupport.pyc
%{python_sitelib}/classadSupport.pyo
%{python_sitelib}/cleanupSupport.py
%{python_sitelib}/cleanupSupport.pyc
%{python_sitelib}/cleanupSupport.pyo
%{python_sitelib}/encodingSupport.py
%{python_sitelib}/encodingSupport.pyc
%{python_sitelib}/encodingSupport.pyo
%{python_sitelib}/glideFactoryCredentials.py
%{python_sitelib}/glideFactoryCredentials.pyc
%{python_sitelib}/glideFactoryCredentials.pyo
%{python_sitelib}/glideinwms_tarfile.py
%{python_sitelib}/glideinwms_tarfile.pyc
%{python_sitelib}/glideinwms_tarfile.pyo
%{python_sitelib}/iniSupport.py
%{python_sitelib}/iniSupport.pyc
%{python_sitelib}/iniSupport.pyo
%{python_sitelib}/tarSupport.py
%{python_sitelib}/tarSupport.pyc
%{python_sitelib}/tarSupport.pyo
%endif

%files vofrontend-standalone
%defattr(-,frontend,frontend,-)
%attr(755,root,root) %{_bindir}/glidein_*
%attr(755,root,root) %{_bindir}/wms*
%attr(755,root,root) %{_sbindir}/checkFrontend
%attr(755,root,root) %{_sbindir}/glidecondor_addDN
%attr(755,root,root) %{_sbindir}/glideinFrontend
%attr(755,root,root) %{_sbindir}/glideinFrontendElement.py*
%attr(755,root,root) %{_sbindir}/reconfig_frontend
%attr(755,root,root) %{_sbindir}/stopFrontend
%attr(-, frontend, frontend) %dir %{_localstatedir}/lib/gwms-frontend
%attr(-, frontend, frontend) %{web_dir}
%attr(-, frontend, frontend) %{web_base}
%attr(-, frontend, frontend) %{frontend_dir}
%attr(-, frontend, frontend) %{_localstatedir}/log/gwms-frontend
%{python_sitelib}/cWConsts.py
%{python_sitelib}/cWConsts.pyc
%{python_sitelib}/cWConsts.pyo
%{python_sitelib}/cWDictFile.py
%{python_sitelib}/cWDictFile.pyc
%{python_sitelib}/cWDictFile.pyo
%{python_sitelib}/cWParams.py
%{python_sitelib}/cWParams.pyc
%{python_sitelib}/cWParams.pyo
%{python_sitelib}/checkFrontend.py
%{python_sitelib}/checkFrontend.pyc
%{python_sitelib}/checkFrontend.pyo
%{python_sitelib}/condorExe.py
%{python_sitelib}/condorExe.pyc
%{python_sitelib}/condorExe.pyo
%{python_sitelib}/condorLogParser.py
%{python_sitelib}/condorLogParser.pyc
%{python_sitelib}/condorLogParser.pyo
%{python_sitelib}/condorManager.py
%{python_sitelib}/condorManager.pyc
%{python_sitelib}/condorManager.pyo
%{python_sitelib}/condorMonitor.py
%{python_sitelib}/condorMonitor.pyc
%{python_sitelib}/condorMonitor.pyo
%{python_sitelib}/condorPrivsep.py
%{python_sitelib}/condorPrivsep.pyc
%{python_sitelib}/condorPrivsep.pyo
%{python_sitelib}/condorSecurity.py
%{python_sitelib}/condorSecurity.pyc
%{python_sitelib}/condorSecurity.pyo
%{python_sitelib}/cvWConsts.py
%{python_sitelib}/cvWConsts.pyc
%{python_sitelib}/cvWConsts.pyo
%{python_sitelib}/cvWCreate.py
%{python_sitelib}/cvWCreate.pyc
%{python_sitelib}/cvWCreate.pyo
%{python_sitelib}/cvWDictFile.py
%{python_sitelib}/cvWDictFile.pyc
%{python_sitelib}/cvWDictFile.pyo
%{python_sitelib}/cvWParamDict.py
%{python_sitelib}/cvWParamDict.pyc
%{python_sitelib}/cvWParamDict.pyo
%{python_sitelib}/cvWParams.py
%{python_sitelib}/cvWParams.pyc
%{python_sitelib}/cvWParams.pyo
%{python_sitelib}/exprParser.py
%{python_sitelib}/exprParser.pyc
%{python_sitelib}/exprParser.pyo
%{python_sitelib}/glideinCmd.py
%{python_sitelib}/glideinCmd.pyc
%{python_sitelib}/glideinCmd.pyo
%{python_sitelib}/glideinFrontend.py
%{python_sitelib}/glideinFrontend.pyc
%{python_sitelib}/glideinFrontend.pyo
%{python_sitelib}/glideinFrontendConfig.py
%{python_sitelib}/glideinFrontendConfig.pyc
%{python_sitelib}/glideinFrontendConfig.pyo
%{python_sitelib}/glideinFrontendInterface.py
%{python_sitelib}/glideinFrontendInterface.pyc
%{python_sitelib}/glideinFrontendInterface.pyo
%{python_sitelib}/glideinFrontendLib.py
%{python_sitelib}/glideinFrontendLib.pyc
%{python_sitelib}/glideinFrontendLib.pyo
%{python_sitelib}/glideinFrontendMonitorAggregator.py
%{python_sitelib}/glideinFrontendMonitorAggregator.pyc
%{python_sitelib}/glideinFrontendMonitorAggregator.pyo
%{python_sitelib}/glideinFrontendMonitoring.py
%{python_sitelib}/glideinFrontendMonitoring.pyc
%{python_sitelib}/glideinFrontendMonitoring.pyo
%{python_sitelib}/glideinFrontendPidLib.py
%{python_sitelib}/glideinFrontendPidLib.pyc
%{python_sitelib}/glideinFrontendPidLib.pyo
%{python_sitelib}/glideinFrontendPlugins.py
%{python_sitelib}/glideinFrontendPlugins.pyc
%{python_sitelib}/glideinFrontendPlugins.pyo
%{python_sitelib}/glideinMonitor.py
%{python_sitelib}/glideinMonitor.pyc
%{python_sitelib}/glideinMonitor.pyo
%{python_sitelib}/glideinWMSVersion.py
%{python_sitelib}/glideinWMSVersion.pyc
%{python_sitelib}/glideinWMSVersion.pyo
%{python_sitelib}/hashCrypto.py
%{python_sitelib}/hashCrypto.pyc
%{python_sitelib}/hashCrypto.pyo
%{python_sitelib}/ldapMonitor.py
%{python_sitelib}/ldapMonitor.pyc
%{python_sitelib}/ldapMonitor.pyo
%{python_sitelib}/logSupport.py
%{python_sitelib}/logSupport.pyc
%{python_sitelib}/logSupport.pyo
%{python_sitelib}/pidSupport.py
%{python_sitelib}/pidSupport.pyc
%{python_sitelib}/pidSupport.pyo
%{python_sitelib}/pubCrypto.py
%{python_sitelib}/pubCrypto.pyc
%{python_sitelib}/pubCrypto.pyo
%{python_sitelib}/rrdSupport.py
%{python_sitelib}/rrdSupport.pyc
%{python_sitelib}/rrdSupport.pyo
%{python_sitelib}/stopFrontend.py
%{python_sitelib}/stopFrontend.pyc
%{python_sitelib}/stopFrontend.pyo
%{python_sitelib}/subprocessSupport.py
%{python_sitelib}/subprocessSupport.pyc
%{python_sitelib}/subprocessSupport.pyo
%{python_sitelib}/symCrypto.py
%{python_sitelib}/symCrypto.pyc
%{python_sitelib}/symCrypto.pyo
%{python_sitelib}/xmlFormat.py
%{python_sitelib}/xmlFormat.pyc
%{python_sitelib}/xmlFormat.pyo
%{python_sitelib}/xmlParse.py
%{python_sitelib}/xmlParse.pyc
%{python_sitelib}/xmlParse.pyo
%{python_sitelib}/timeConversion.py
%{python_sitelib}/timeConversion.pyc
%{python_sitelib}/timeConversion.pyo
%{python_sitelib}/glideinFrontendElement.py*
%{_initrddir}/gwms-frontend
%config(noreplace) %{_sysconfdir}/httpd/conf.d/gwms-frontend.conf
%attr(-, frontend, frontend) %dir %{_sysconfdir}/gwms-frontend
%attr(-, frontend, frontend) %config(noreplace) %{_sysconfdir}/gwms-frontend/frontend.xml
%if %{v3_plus}
%attr(-, frontend, frontend) %{web_base}/../creation
%{python_sitelib}/classadSupport.py
%{python_sitelib}/classadSupport.pyc
%{python_sitelib}/classadSupport.pyo
%{python_sitelib}/cleanupSupport.py
%{python_sitelib}/cleanupSupport.pyc
%{python_sitelib}/cleanupSupport.pyo
%{python_sitelib}/encodingSupport.py
%{python_sitelib}/encodingSupport.pyc
%{python_sitelib}/encodingSupport.pyo
%{python_sitelib}/glideinwms_tarfile.py
%{python_sitelib}/glideinwms_tarfile.pyc
%{python_sitelib}/glideinwms_tarfile.pyo
%{python_sitelib}/iniSupport.py
%{python_sitelib}/iniSupport.pyc
%{python_sitelib}/iniSupport.pyo
%{python_sitelib}/tarSupport.py
%{python_sitelib}/tarSupport.pyc
%{python_sitelib}/tarSupport.pyo
%endif


%files factory-condor
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_factory_general.config
%config(noreplace) %{_sysconfdir}/condor/config.d/01_gwms_factory_collectors.config
%config(noreplace) %{_sysconfdir}/condor/config.d/02_gwms_factory_schedds.config
%config(noreplace) %{_sysconfdir}/condor/config.d/03_gwms_factory_local.config
%config(noreplace) %{_sysconfdir}/condor/privsep_config
%config(noreplace) %{_sysconfdir}/condor/certs/condor_mapfile
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins2
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins3
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins4
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_glideins5

%files usercollector
%attr(755,root,root) %{_sbindir}/glidecondor_addDN
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_general.config
%config(noreplace) %{_sysconfdir}/condor/config.d/01_gwms_collectors.config
%config(noreplace) %{_sysconfdir}/condor/config.d/03_gwms_local.config
%config(noreplace) %{_sysconfdir}/condor/config.d/90_gwms_dns.config
%config(noreplace) %{_sysconfdir}/condor/certs/condor_mapfile
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_jobs2

%files userschedd
%attr(755,root,root) %{_sbindir}/glidecondor_addDN
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_general.config
%config(noreplace) %{_sysconfdir}/condor/config.d/02_gwms_schedds.config
%config(noreplace) %{_sysconfdir}/condor/config.d/03_gwms_local.config
%config(noreplace) %{_sysconfdir}/condor/config.d/90_gwms_dns.config
%config(noreplace) %{_sysconfdir}/condor/certs/condor_mapfile
%attr(-, condor, condor) %{_localstatedir}/lib/condor/schedd_jobs2

%files minimal-condor
%attr(755,root,root) %{_sbindir}/glidecondor_addDN
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_general.config
%config(noreplace) %{_sysconfdir}/condor/config.d/03_gwms_local.config
%config(noreplace) %{_sysconfdir}/condor/config.d/90_gwms_dns.config
%config(noreplace) %{_sysconfdir}/condor/certs/condor_mapfile


%changelog
* Fri Jan 4 2013 Doug Strain <dstrain@fnal.gov> - 2.6.3-0.rc2.6
- Update to 2.6.3 rc2 release candidate
- Adding factory tools scripts and their python libraries
- Adding condor_create_tarball
- Adding frontend/factory index page.

* Thu Nov 8 2012 Doug Strain <dstrain@fnal.gov> - 2.6.2-2
- Improvements recommended by Igor to modularize glideinwms

* Wed Nov 2 2012 Doug Strain <dstrain@fnal.gov> - 2.6.2-1
- Glideinwms 2.6.2 Release

* Thu Sep 20 2012 Doug Strain <dstrain@fnal.gov> - 2.6.1-2
- Added GRIDMANAGER_PROXY_REFRESH_TIME to condor config

* Mon Aug 20 2012 Doug Strain <dstrain@fnal.gov> - 2.6.1-0.rc2
- Added JOB_QUEUE_LOG to the schedd condor configs
- updated to 2.6.1 release candidate

* Fri Aug 3 2012 Doug Strain <dstrain@fnal.gov> - 2.6.0-3
- Updating to new release 
- Changing the schedd configs to work with both wisc and osg condor rpms

* Wed Jun 13 2012 Doug Strain <dstrain@fnal.gov> - 2.6.0-rc1
- Updating to new release candidate

* Fri Apr 27 2012 Doug Strain <dstrain@fnal.gov> - 2.5.7-4
- Changed ownership of frontend.xml to frontend user
- Changed ownership of glideinwms.xml to gfactory user
- This allows writeback during upgrade reconfigs

* Fri Apr 27 2012 Doug Strain <dstrain@fnal.gov> - 2.5.7-3
- Changed frontend init.d script to reconfig as frontend user

* Mon Apr 9 2012 Doug Strain <dstrain@fnal.gov> - 2.5.7-2
- Updating sources for v2.5.7
- Splitting DAEMON LIST to appropriate config files

* Fri Mar 16 2012 Doug Strain <dstrain@fnal.gov> - 2.5.6-1
- Updating sources for v2.5.6

* Tue Feb 21 2012 Doug Strain <dstrain@fnal.gov> - 2.5.5-7alpha
- Adding factory RPM and v3 support
- Updating to also work on sl7
- Also added support for v3.0.0rc3 with optional define

* Thu Feb 16 2012 Doug Strain <dstrain@fnal.gov> - 2.5.5-1 
- Updating for v2.5.5 

* Tue Jan 10 2012 Doug Strain <dstrain@fnal.gov> - 2.5.4-7
- Adding condor_mapfile to minimal

* Mon Jan 9 2012 Doug Strain <dstrain@fnal.gov> - 2.5.4-6
- Changing directories per Igors request
-- changing directories to /var/lib
- Splitting condor config into separate package
- Fixing web-area httpd

* Thu Jan 5 2012 Doug Strain <dstrain@fnal.gov> - 2.5.4-2
- Updating for 2.5.4 release source and fixing eatures for BUG2310
-- Split directories so that the web area is in /var/www

* Thu Dec 29 2011 Doug Strain <dstrain@fnal.gov> - 2.5.4-1
- Using release source and fixing requested features for BUG2310
-- Adding user/group correctly
-- Substituting hostname name automatically

* Fri Dec 09 2011 Doug Strain <dstrain@fnal.gov> - 2.5.4-0.pre2
- Added glidecondor_addDN to vofrontend package

* Thu Nov 10 2011 Doug Strain <dstrain@fnal.gov> - 2.5.4-0.pre1 
- Update to use patched 2.5.3 
- Pushed patches upstream
- Made the package glideinwms with subpackage vofrontend

* Thu Nov 10 2011 Doug Strain <dstrain@fnal.gov> - 2.5.3-3
- Update to 2.5.3
- Updated condor configs to match ini installer
- Updated frontend.xml to not check index.html
- Updated init script to use "-xml" flag

* Mon Oct 17 2011 Burt Holzman <burt@fnal.gov> - 2.5.2.1-1
- Update to 2.5.2.1

* Tue Sep 06 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-5
- Fix reference to upstream tarball

* Tue Sep 06 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-4
- Add RPM to version number in ClassAd

* Tue Sep 06 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-3
- Fixed glideinWMS versioning advertisement

* Wed Aug 31 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-2
- Fixed file location for frontend_support.js

* Wed Aug 13 2011 Burt Holzman <burt@fnal.gov> - 2.5.2-1
- Update to glideinWMS 2.5.2

* Tue Aug 02 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 2.5.1-13
- Made vdt-repo compatible

* Tue Apr 05 2011 Burt Holzman 2.5.1-10
- Update frontend_startup script to better determine frontend name
- Move user-editable configuration items into 02_frontend-local.config

* Tue Mar 22 2011 Derek Weitzel 2.5.1-8
- Change condor config file name to 00_frontend.config
- Separated definition of collectors into 01_collectors.config

* Fri Mar 11 2011 Burt Holzman 	 2.5.1-1
- Include glideinWMS 2.5.1
- Made all the directories independent of the frontend name

* Mon Mar 10 2011 Derek Weitzel  2.5.0-11
- Changed the frontend.xml to correct the web stage directory

* Mon Mar 10 2011 Derek Weitzel  2.5.0-9
- Made the work, stage, monitor, and log directory independent of the frontend name.
- Frontend name is now generated at install time

* Mon Feb 13 2011 Derek Weitzel  2.5.0-6
- Made rpm noarch
- Replaced python site-packages more auto-detectable

* Mon Feb 09 2011 Derek Weitzel  2.5.0-5
- Added the tools to bin directory

* Mon Jan 24 2011 Derek Weitzel  2.5.0-4
- Added the tools directory to the release

* Mon Jan 24 2011 Derek Weitzel  2.5.0-3
- Rebased to official 2.5.0 release.

* Thu Dec 16 2010 Derek Weitzel  2.5.0-2
- Changed GlideinWMS version to branch_v2_4plus_igor_ucsd1

* Fri Aug 13 2010 Derek Weitzel  2.4.2-2
- Removed port from primary collector in frontend.xml
- Changed GSI_DAEMON_TRUSTED_CA_DIR to point to /etc/grid-security/certificates 
  where CA's are installed.
- Changed GSI_DAEMON_DIRECTORY to point to /etc/grid-security.  This is 
  only used to build default directories for other GSI_* 
  configuration variables.
- Removed the rm's to delete the frontend-temp and log directories at uninstall,
  they removed files when updating, not wanted.  Let RPM handle those.

