Name:           glideinwms-vofrontend
Version:        2.5.1
Release:        11
Summary:        The VOFrontend for glideinWMS submission host

Group:          System Environment/Daemons
License:        Fermitools Software Legal Information (Modified BSD License)
URL:            http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/doc.v2/manual/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
#BuildRequires:  
#Requires:       
#BuildArchitectures: noarch 
Provides:	GlideinWMSFrontend = %{version}-%{release}
Obsoletes:	GlideinWMSFrontend < %2.5.1-11


#Source0:        http://www.uscms.org/SoftwareComputing/Grid/WMS/glideinWMS/glideinWMS_v2_5_1_frontend.tgz
#Source0:        GlideinWMSFrontend-2.5.1.tar.gz
Source0:	glideinWMS_v2_5_1_frontend.tgz

# How to build tar file
# cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only co -r v2_5 glideinWMS
# mv glideinWMS GlideinWMSFrontend-2.5.0
# tar czf GlideinWMSFrontend-2.5.0-3.tar.gz GlideinWMSFrontend-2.5.0/
# cp GlideinWMSFrontend-2.5.0-3.tar.gz ~/rpmbuild/SOURCES

Source1:        frontend_startup
Source2:        frontend.xml
Source3:        gwms-frontend.conf.httpd
Source4:        00_frontend.config
Source5:        01_collectors.config
Source6:	02_frontend-local.config
patch0:         reconfig_frontend.patch
patch1:         cvWParamDict.py.patch
patch2: 	cvWParams.py.patch

Requires: httpd
#Requires: condor
Requires: python-rrdtool
Requires: m2crypto
Requires: javascriptrrd
#Requires: vdt-vofrontend-essentials


Requires(post): /sbin/service
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig



%description
The purpose of the glideinWMS is to provide a simple way 
to access the Grid resources. GlideinWMS is a Glidein 
Based WMS (Workload Management System) that works on top of 
Condor. For those familiar with the Condor system, it is used 
for scheduling and job control. 



%prep
%setup -q -n glideinWMS
# Apply the patches
%patch -P 0
%patch -P 1 -R -p0
%patch -P 2 -p1

%build
#make %{?_smp_mflags}


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
# FIXME: Need to find macro for site-packages
# FIXME: Need to create a subdirectory for vofrontend python files
install -d $RPM_BUILD_ROOT%{python_sitelib}
cp lib/*.py $RPM_BUILD_ROOT%{python_sitelib}
cp frontend/*.py $RPM_BUILD_ROOT/%{python_sitelib}
cp creation/lib/*.py $RPM_BUILD_ROOT%{python_sitelib}
#install %{SOURCE4} $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages


# Install the init.d
install -d  $RPM_BUILD_ROOT/%{_initrddir}
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/frontend_startup

# Install the web directory
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/stage/
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/stage/group_main

# Bunch of Monitoring stuff
install -m 644 creation/web_base/frontendRRDBrowse.html $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/frontendRRDBrowse.html
install -m 644 creation/web_base/frontendRRDGroupMatrix.html $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/frontendRRDGroupMatrix.html  
install -m 644 creation/web_base/frontendStatus.html $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/frontendStatus.html 
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/lock
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/jslibs
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/total
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/group_main
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/group_main/lock
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/monitor/group_main/total

# staging stuff
install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/stage/nodes.blacklist
install -m 644 creation/web_base/nodes.blacklist $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/www/stage/group_main/nodes.blacklist

# Httpd configuration changes
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/gwms-frontend.conf

# Install the logs
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/frontend
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/gwms-frontend/group_main


# Install frontend temp dir, for all the frontend.xml.<checksum>
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/lock
#install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/monitor
#install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/monitor/group_main
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/group_main
install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/group_main/lock
#install -d $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/group_main/monitor


# Install the frontend config dir
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/gwms-frontend/frontend.xml

# Install the silly stuff, should be fixed in glideinWMS
cp -r creation/web_base/* $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/
rm -rf $RPM_BUILD_ROOT%{_datadir}/gwms-frontend/frontend-temp/CVS

# Make user frontend?


# Install condor stuff
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d
install -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/00_frontend.config
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/01_collectors.config
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/condor/config.d/02_frontend-local.config

# Install tools
install -d $RPM_BUILD_ROOT%{_bindir}
# Install the tools as the non-*.py filenames
for file in `ls tools/*.py`; do
   newname=`echo $file | sed -e 's/.*\/\(.*\)\.py/\1/'`
   cp $file $RPM_BUILD_ROOT%{_bindir}/$newname
done
cp tools/lib/*.py $RPM_BUILD_ROOT%{python_sitelib}

%post
# $1 = 1 - Installation
# $1 = 2 - Upgrade
# Source: http://www.ibm.com/developerworks/library/l-rpm2/

fqdn_hostname=`hostname -f`
frontend_name=`echo $fqdn_hostname | sed 's/\./-/g'`_OSG_gWMSFrontend


sed -i "s/FRONTEND_NAME_CHANGEME/$frontend_name/g" %{_sysconfdir}/gwms-frontend/frontend.xml

#mv %{_datadir}/gwms-frontend/www/stage/ %{_datadir}/gwms-frontend/www/stage/$frontend_name

/sbin/chkconfig --add frontend_startup
ln -s %{_sysconfdir}/gwms-frontend/frontend.xml %{_datadir}/gwms-frontend/frontend-temp/frontend.xml
ln -s %{_datadir}/gwms-frontend/www/monitor/ %{_datadir}/gwms-frontend/frontend-temp/monitor
ln -s %{_datadir}/gwms-frontend/www/monitor/group_main %{_datadir}/gwms-frontend/frontend-temp/group_main/monitor

%pre
# Add the "frontend" user 
/usr/sbin/useradd -c "VO Frontend User" \
	-s /sbin/nologin -r frontend 2> /dev/null || :

%preun
# $1 = 0 - Action is uninstall
# $1 = 1 - Action is upgrade


if [ "$1" = "0" ] ; then
    /sbin/chkconfig --del frontend_startup
fi

if [ "$1" = "0" ]; then
    # Remove the symlinks
    rm -f %{_datadir}/gwms-frontend/frontend-temp/frontend.xml
    rm -f %{_datadir}/gwms-frontend/frontend-temp/monitor
    rm -f %{_datadir}/gwms-frontend/frontend-temp/group_main/monitor

    # A lot of files are generated, but rpm won't delete those
#    rm -rf %{_datadir}/gwms-frontend
#    rm -rf %{_localstatedir}/log/gwms-frontend/*
fi

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,frontend,frontend,-)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(-, frontend, frontend) %{_datadir}/gwms-frontend
%attr(-, frontend, frontend) %{_localstatedir}/log/gwms-frontend
%{python_sitelib}
%{_initrddir}/frontend_startup
%config(noreplace) %{_sysconfdir}/httpd/conf.d/gwms-frontend.conf
%config(noreplace) %{_sysconfdir}/condor/config.d/00_frontend.config
%config(noreplace) %{_sysconfdir}/condor/config.d/01_collectors.config
%config(noreplace) %{_sysconfdir}/condor/config.d/02_frontend-local.config
%config(noreplace) %{_sysconfdir}/gwms-frontend/frontend.xml


%changelog
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

