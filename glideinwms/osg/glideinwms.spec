Name:           glideinwms
Version:        2.5.4
Release:        3%{?dist}
Summary:        The VOFrontend for glideinWMS submission host

Group:          System Environment/Daemons
License:        Fermitools Software Legal Information (Modified BSD License)
URL:            http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v2/manual/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%define web_dir %{_prefix}/share/gwms-frontend/web-area
%define web_base %{_localstatedir}/lib/gwms-frontend/web-base
%define frontend_dir %{_localstatedir}/lib/gwms-frontend/vofrontend

#Source0:        http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/glideinWMS_v2_5_1_frontend.tgz
Source:	glideinwms.tar.gz

# How to build tar file
# git clone http://cdcvs.fnal.gov/projects/glideinwms
# cd glideinwms
# git archive v2_5_2 --prefix='glideinWMS/' | gzip > ~/rpmbuild/SOURCES/glideinWMS_v2_5_2_frontend.tgz

Source1:        frontend_startup
Source2:        frontend.xml
Source3:        gwms-frontend.conf.httpd
Source4:        00_gwms_general.config
Source5:        01_gwms_collectors.config
Source6:	02_gwms_schedds.config
Source7:	03_gwms_local.config
Source8:	chksum.sh
patch0:         reconfig_frontend.patch
patch1:         cvWParamDict.py.patch
patch2: 	cvWParams.py.patch
patch3:		glideinwms_version.patch
%description
This is a package for the glidein workload management system.
Currently, only the vofrontend portion is supported

%package vofrontend
Summary:        The VOFrontend for glideinWMS submission host
Group:          System Environment/Daemons
Provides:	GlideinWMSFrontend = %{version}-%{release}
Obsoletes:	GlideinWMSFrontend < 2.5.1-11
Requires: httpd
# We require Condor 7.6.0 (and newer) to support 
# condor_advertise -multiple -tcp which is enabled by default
Requires: condor >= 7.6.0
Requires: python-rrdtool
Requires: m2crypto
Requires: javascriptrrd
Requires: osg-client
Requires: gwms-condor-config
#Requires: vdt-vofrontend-essentials

Requires(post): /sbin/service
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig


%description vofrontend
The purpose of the glideinWMS is to provide a simple way 
to access the Grid resources. GlideinWMS is a Glidein 
Based WMS (Workload Management System) that works on top of 
Condor. For those familiar with the Condor system, it is used 
for scheduling and job control. 


%package vofrontend-condor
Summary:        The VOFrontend condor config
Group:          System Environment/Daemons
Provides: gwms-condor-config

%description vofrontend-condor
This is a package including condor_config for a full one-node
install of vofrontend + userschedd + usercollector


%package minimal-condor
Summary:        The VOFrontend minimal condor config
Group:          System Environment/Daemons
Provides: gwms-condor-config

%description minimal-condor
This is an alternate condor config for just the minimal amount
needed for vofrontend.

%prep
%setup -q -n glideinwms
# Apply the patches
#%patch -P 0 -p1
#%patch -P 1 -p1
#%patch -P 2 -p1
#%patch -P 3 -p1

%build
cp %{SOURCE8} .
chmod 700 chksum.sh
./chksum.sh v%{version}-%{release}.osg etc/checksum.frontend "CVS config_examples doc .git .gitattributes poolwatcher factory/check* factory/glideFactory* factory/test* factory/manage* factory/stop* factory/tools creation/create_glidein creation/reconfig_glidein creation/info_glidein creation/lib/cgW* creation/web_base/factory*html creation/web_base/collector_setup.sh creation/web_base/condor_platform_select.sh creation/web_base/condor_startup.sh creation/web_base/create_mapfile.sh creation/web_base/gcb_setup.sh creation/web_base/glexec_setup.sh creation/web_base/glidein_startup.sh creation/web_base/job_submit.sh creation/web_base/local_start.sh creation/web_base/setup_x509.sh creation/web_base/validate_node.sh chksum.sh etc/checksum*"


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


# Apply the patches
#%patch -P 0
#%patch -P 1 -p3 

#Change src_dir in reconfig_Frontend
sed -i "s/WEB_BASE_DIR=.*/WEB_BASE_DIR=\"\/var\/lib\/gwms-frontend\/web-base\"/" creation/reconfig_frontend

# install the executables
install -d $RPM_BUILD_ROOT%{_sbindir}
# Find all the executables in the frontend directory
#find frontend -perm -u=x -type f -exec cp {} $RPM_BUILD_ROOT%{_sbindir} \;
install -m 0500 frontend/checkFrontend.py $RPM_BUILD_ROOT%{_sbindir}/checkFrontend
install -m 0500 frontend/glideinFrontendElement.py $RPM_BUILD_ROOT%{_sbindir}/glideinFrontendElement.py
install -m 0500 frontend/glideinFrontend.py $RPM_BUILD_ROOT%{_sbindir}/glideinFrontend
install -m 0500 frontend/stopFrontend.py $RPM_BUILD_ROOT%{_sbindir}/stopFrontend
install -m 0500 creation/reconfig_frontend $RPM_BUILD_ROOT%{_sbindir}/reconfig_frontend

# install the library parts
# FIXME: Need to create a subdirectory for vofrontend python files
install -d $RPM_BUILD_ROOT%{python_sitelib}
cp lib/*.py $RPM_BUILD_ROOT%{python_sitelib}
cp frontend/*.py $RPM_BUILD_ROOT/%{python_sitelib}
cp creation/lib/*.py $RPM_BUILD_ROOT%{python_sitelib}


# Install the init.d
install -d  $RPM_BUILD_ROOT/%{_initrddir}
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/gwms-frontend

# Install the web directory
install -d $RPM_BUILD_ROOT%{frontend_dir}
install -d $RPM_BUILD_ROOT%{web_base}
install -d $RPM_BUILD_ROOT%{web_dir}
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/
install -d $RPM_BUILD_ROOT%{web_dir}/stage/
install -d $RPM_BUILD_ROOT%{web_dir}/stage/group_main


install -d $RPM_BUILD_ROOT%{web_dir}/monitor/lock
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/jslibs
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/total
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main/lock
install -d $RPM_BUILD_ROOT%{web_dir}/monitor/group_main/total

install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{web_dir}/stage/nodes.blacklist
install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{web_dir}/stage/group_main/nodes.blacklist

# Install the logs
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/frontend
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/group_main


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


# Install the frontend config dir
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend/frontend.xml

# Install the silly stuff, should be fixed in glideinWMS
cp -r creation/web_base/* $RPM_BUILD_ROOT%{web_base}/
rm -rf $RPM_BUILD_ROOT%{web_base}/CVS

# Install condor stuff
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/
install -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/

# Install tools
install -d $RPM_BUILD_ROOT%{_bindir}
# Install the tools as the non-*.py filenames
for file in `ls tools/*.py`; do
   newname=`echo $file | sed -e 's/.*\/\(.*\)\.py/\1/'`
   cp $file $RPM_BUILD_ROOT%{_bindir}/$newname
done
cp tools/lib/*.py $RPM_BUILD_ROOT%{python_sitelib}

# Install glidecondor
install -m 0755 install/glidecondor_addDN $RPM_BUILD_ROOT%{_sbindir}/glidecondor_addDN

# Install checksum file
install -m 0644 etc/checksum.frontend $RPM_BUILD_ROOT%{frontend_dir}/checksum.frontend

#Install web area conf
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/gwms-frontend.conf


%post vofrontend
# $1 = 1 - Installation
# $1 = 2 - Upgrade
# Source: http://www.ibm.com/developerworks/library/l-rpm2/

fqdn_hostname=`hostname -f`
frontend_name=`echo $fqdn_hostname | sed 's/\./-/g'`_OSG_gWMSFrontend


sed -i "s/FRONTEND_NAME_CHANGEME/$frontend_name/g" %{_sysconfdir}/gwms-frontend/frontend.xml
sed -i "s/FRONTEND_HOSTNAME/$fqdn_hostname/g" %{_sysconfdir}/gwms-frontend/frontend.xml

/sbin/chkconfig --add gwms-frontend
ln -s %{web_dir}/monitor %{frontend_dir}/monitor

%pre vofrontend

# Add the "frontend" user 
getent group frontend >/dev/null || groupadd -r frontend
getent passwd frontend >/dev/null || \
       useradd -r -g frontend -d %{_datadir}/gwms-frontend \
	-c "VO Frontend user" -s /sbin/nologin frontend

%preun vofrontend
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

%clean
rm -rf $RPM_BUILD_ROOT


%files vofrontend
%defattr(-,frontend,frontend,-)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(-, frontend, frontend) %{_localstatedir}/lib/gwms-frontend
%attr(-, frontend, frontend) %{web_dir}
%attr(-, frontend, frontend) %{web_base}
%attr(-, frontend, frontend) %{frontend_dir}
%attr(-, frontend, frontend) %{_localstatedir}/log/gwms-frontend
%{python_sitelib}
%{_initrddir}/gwms-frontend
%config(noreplace) %{_sysconfdir}/httpd/conf.d/gwms-frontend.conf
%config(noreplace) %{_sysconfdir}/gwms-frontend/frontend.xml

%files vofrontend-condor
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_general.config
%config(noreplace) %{_sysconfdir}/condor/config.d/01_gwms_collectors.config
%config(noreplace) %{_sysconfdir}/condor/config.d/02_gwms_schedds.config
%config(noreplace) %{_sysconfdir}/condor/config.d/03_gwms_local.config

%files minimal-condor
%config(noreplace) %{_sysconfdir}/condor/config.d/00_gwms_general.config


%changelog
* Thu Jan 5 2012 Doug Strain <dstrain@fnal.gov> - 2.5.4-3
- Changing directories per Igors request
-- changing directories to /var/lib
-- changing web directory back to /usr/share as per fedora guidelines
- Splitting condor config into separate package

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

