Name:               gratia-probe
Summary:            Gratia OSG accounting system probes
Group:              Applications/System
Version:            1.07.02e
Release:            0.16.pre
License:            GPL
Group:              Applications/System
URL:                http://sourceforge.net/projects/gratia/
Vendor:             The Open Science Grid <http://www.opensciencegrid.org/>
%if %{?python:0}%{!?python:1}
BuildRequires:      python >= 2.3
BuildRequires:      python-devel >= 2.3
%endif

BuildRequires: gcc-c++

Patch0: change-folders.patch 
Patch1: change-imports.patch
Patch2: condor-probe-cron.patch
Patch3: gratiapy-change-imports.patch
Patch4: metric-imports.patch
Patch5: JobManagerGratia-dirs.patch
Patch6: dcache-transfer-locs.patch
Patch7: urCollector_defaults.patch
Patch8: gridftp-transfer-wrapper.patch
Patch9: gridftp_drive_imports.patch
Patch10: gridftp_netlogger.patch
Patch11: pbs-probe-locs.patch
Patch12: glexec-probe.patch
Patch13: sge-probe.patch
Patch14: dCache-storage-probe.patch
Patch15: dcache-transfer-main.patch
Patch16: gratia-core-home.patch

%global ProbeConfig_template_marker <!-- This probe has not yet been configured -->

%define default_prefix /usr/share

# Default probe configuration items for post-install.
%global default_collector_port 80
%global metric_port 8880
%global ssl_port 443

%global osg_collector gratia-osg-prod.opensciencegrid.org
%global osg_transfer_collector gratia-osg-transfer.opensciencegrid.org
%global osg_metric_collector rsv.grid.iu.edu

# Default ProbeName
%{!?meter_name: %global meter_name `hostname -f`}

%define customize_probeconfig(d:) sed -i "s#@PROBE_HOST@#%{meter_name}#" %{_sysconfdir}/gratia/%{-d*}/ProbeConfig

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

########################################################################
# Source and patch specifications
Source0: %{name}-common-%{version}.tar.bz2
Source1: %{name}-condor-%{version}.tar.bz2
Source2: %{name}-psacct-%{version}.tar.bz2
Source3: %{name}-pbs-lsf-%{version}.tar.bz2
Source5: %{name}-sge-%{version}.tar.bz2
Source6: %{name}-glexec-%{version}.tar.bz2
Source7: %{name}-metric-%{version}.tar.bz2

Source12: %{name}-dCache-transfer-%{version}.tar.bz2
Source13: %{name}-dCache-storage-%{version}.tar.bz2
Source14: %{name}-gridftp-transfer-%{version}.tar.bz2
Source15: %{name}-services-%{version}.tar.bz2
Source16: %{name}-hadoop-storage-%{version}.tar.bz2
Source17: %{name}-condor-events-%{version}.tar.bz2
Source18: %{name}-xrootd-transfer-%{version}.tar.bz2
Source19: %{name}-xrootd-storage-%{version}.tar.bz2
Source20: %{name}-bdii-status-%{version}.tar.bz2
Source30: 99_gratia.conf

# OSG-specific cron files
Source31: gratia-probe-gridftp-transfer.cron
Source32: gratia-probe-condor.cron
Source33: gratia-probe-sge.cron
Source34: gratia-probe-pbs-lsf.cron
Source35: gratia-probe-psacct.cron
Source36: gratia-probe-glexec.cron
Source37: gratia-probe-bdii-cese.cron
Source38: gratia-probe-bdii-subcluster.cron
Source39: gratia-probe-condor-events.cron
Source40: gratia-probe-hadoop-storage.cron
Source41: gratia-probe-dcache-storage.cron

Source42: ProbeConfigTemplate.osg
Source43: gratia-dcache-transfer.init
Source44: gratia-dcache-transfer

########################################################################

# Build settings.
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: /usr
Prefix: %{default_prefix}
Prefix: /etc

# Build preparation.
%prep
%setup -q -c
%setup -q -D -T -a 1
%setup -q -D -T -a 2
%ifnarch noarch
%setup -q -D -T -a 3
%endif
%setup -q -D -T -a 5
%setup -q -D -T -a 6
%setup -q -D -T -a 7
%setup -q -D -T -a 12
%setup -q -D -T -a 13
rm -f dCache-storage/test.xml
%setup -q -D -T -a 14
%setup -q -D -T -a 15
%setup -q -D -T -a 16
%setup -q -D -T -a 17
%setup -q -D -T -a 18
%setup -q -D -T -a 19
%setup -q -D -T -a 20

%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p0
%ifnarch noarch
%patch7 -p0
%patch11 -p0
%endif
%patch8 -p0
%patch9 -p0
%patch10 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0
%patch16 -p0

%build
%ifnarch noarch
cd pbs-lsf/urCollector-src
%{__make} clean
%{__make}
%endif

%install
# Setup
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_datadir}/gratia
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gratia

%ifarch noarch
  # Obtain files

%define noarch_packs common condor psacct sge glexec metric dCache-transfer dCache-storage gridftp-transfer services hadoop-storage condor-events xrootd-transfer xrootd-storage bdii-status

  cp -pR %{noarch_packs}  $RPM_BUILD_ROOT/%{_datadir}/gratia

  # Customize template for each probe
  for probe in %{noarch_packs}
  do
    PROBE_DIR=$RPM_BUILD_ROOT/%{_sysconfdir}/gratia/$probe
    install -d $PROBE_DIR
    install -m 644 %{SOURCE42} $PROBE_DIR/ProbeConfig
    echo "%{ProbeConfig_template_marker}" >> $PROBE_DIR/ProbeConfig
    mkdir -p $RPM_BUILD_ROOT/%{_datadir}/gratia/$probe/
    ln -s %{_sysconfdir}/gratia/$probe/ProbeConfig $RPM_BUILD_ROOT/%{_datadir}/gratia/$probe/ProbeConfig
    sed -i -e "s#@PROBE_NAME@#$probe#" $PROBE_DIR/ProbeConfig

    if [ $probe == *-transfer -o $probe == *-storage ]; then
      endpoint=%{osg_transfer_collector}:%{default_collector_port}
    elif [ $probe == metric ]; then
      endpoint=%{osg_metric_collector}:%{metric_port}
    else 
      endpoint=%{osg_collector}:%{default_collector_port}
    fi
    sed -i -e "s#@COLLECTOR_ENDPOINT@#$endpoint#" \
           -e "s#@SSL_ENDPOINT@#%{osg_collector}:%{ssl_port}#" \
           -e "s#@SSL_REGISTRATION_ENDPOINT@#$endpoint#" \
        $PROBE_DIR/ProbeConfig

    # Probe-specific customizations
    if [ $probe == "psacct" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#PSACCTFileRepository="/usr/share/gratia/var/account/" \
    PSACCTBackupFileRepository="/usr/share/gratia/var/backup/" \
    PSACCTExceptionsRepository="/var/log/gratia/exceptions/"#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "sge" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#SGEAccountingFile=""#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "glexec" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#gLExecMonitorLog="/var/log/glexec/glexec_monitor.log"#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "metric" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#metricMonitorLog="/var/log/metric/metric_monitor.log"#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "dCache-transfer" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#Summarize="0" \
    UpdateFrequency="120" \
    DBHostName="localhost" \
    DBLoginName="srmdcache" \
    DBPassword="srmdcache" \
    StopFileName="stopGratiaFeed" \
    DCacheServerHost="BILLING_HOST" \
    EmailServerHost="localhost" \
    EmailFromAddress="dCacheProbe@localhost" \
    EmailToList="" \
    AggrLogLevel="warn" \
    OnlySendInterSiteTransfers="true" \
    MaxBillingHistoryDays="31" \
    DBName="billing"#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "gridftp-transfer" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#GridftpLogDir="/var/log/"#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "dCache-storage" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#TitleDCacheStorage="dCache-storage-specific attributes" \
    InfoProviderUrl="http://DCACHE_HOST:2288/info" \
    ReportPoolUsage="0"#' $PROBE_DIR/ProbeConfig
    else
      sed -i -e 's#@PROBE_SPECIFIC_DATA@##' $PROBE_DIR/ProbeConfig
    fi

  done
  rm $RPM_BUILD_ROOT%{_sysconfdir}/gratia/common/ProbeConfig
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/common/ProbeConfig

  # dCache-transfer init script
  install -d $RPM_BUILD_ROOT/%{_initrddir}
  install -m 755 %{SOURCE43} $RPM_BUILD_ROOT%{_initrddir}/gratia-dcache-transfer
  rm -f "${RPM_BUILD_ROOT}%{_datadir}/gratia/dCache-transfer/gratia-dcache-transfer"
  install -m 755 %{SOURCE44} $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-transfer/gratia-dcache-transfer

  # Xrootd-storage init script
  install -m 755 "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-storage/gratia-xrootd-storage" "$RPM_BUILD_ROOT%{_initrddir}/gratia-xrootd-storage"
  rm -f "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-storage/gratia-xrootd-storage"

  # Xrootd-transfer init script
  install -m 755 "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-transfer/gratia-xrootd-transfer" "$RPM_BUILD_ROOT%{_initrddir}/gratia-xrootd-transfer"
  rm -f "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-transfer/gratia-xrootd-transfer"

  # gridftp-transfer unneeded file.
  rm -f "${RPM_BUILD_ROOT}%{_datadir}/gratia/gridftp-transfer/GridftpTransferProbe.sh"

  # Move python scripts
  mv $RPM_BUILD_ROOT%{_datadir}/gratia/condor-events/watchCondorEvents.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/condor-events/watchCondorEvents
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/condor-events/watchCondorEvents
  mv $RPM_BUILD_ROOT%{_datadir}/gratia/common/GetProbeConfigAttribute.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/common/GetProbeConfigAttribute
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/common/GetProbeConfigAttribute
  mv $RPM_BUILD_ROOT%{_datadir}/gratia/common/DebugPrint.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/common/DebugPrint
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/common/DebugPrint
  mv $RPM_BUILD_ROOT%{_datadir}/gratia/gridftp-transfer/GridftpTransferProbeDriver.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/gridftp-transfer/GridftpTransferProbeDriver
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/gridftp-transfer/GridftpTransferProbeDriver
  mv $RPM_BUILD_ROOT%{_datadir}/gratia/glexec/glexec_meter.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/glexec/glexec_meter
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/glexec/glexec_meter
  mv $RPM_BUILD_ROOT%{_datadir}/gratia/sge/sge_meter.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/sge/sge_meter
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/sge/sge_meter
  mv $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-storage/dCache_storage_probe.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-storage/dCache_storage_probe
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-storage/dCache_storage_probe

  mv $RPM_BUILD_ROOT%{_datadir}/gratia/hadoop-storage/storage.cfg \
     $RPM_BUILD_ROOT%{_sysconfdir}/gratia/hadoop-storage/storage.cfg
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/gridftp-transfer/netlogger

  # New cron files
  mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
  install -m 644 %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE35} \
     %{SOURCE36} %{SOURCE37} %{SOURCE38} %{SOURCE39} %{SOURCE40} %{SOURCE41} \
     $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/

%else

  # PBS / LSF probe install
  cp -pR pbs-lsf $RPM_BUILD_ROOT%{_datadir}/gratia/
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/urCollector-src
  probe_dir=$RPM_BUILD_ROOT%{_sysconfdir}/gratia/pbs-lsf
  install -d $probe_dir
  cp -p common/ProbeConfigTemplate $probe_dir/ProbeConfig
  echo "%{ProbeConfig_template_marker}" >> $probe_dir/ProbeConfig
  mkdir -p $RPM_BUILD_ROOT/%{_datadir}/gratia/pbs-lsf/
  ln -s %{_sysconfdir}/gratia/pbs-lsf/ProbeConfig $RPM_BUILD_ROOT/%{_datadir}/gratia/pbs-lsf/ProbeConfig

  mv $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/pbs-lsf.py \
     $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/pbs-lsf
  chmod +x $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/pbs-lsf

  cd $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf
  cd - >/dev/null

  # Install urCollector softwarepbs-lsf/pbs-lsf
  cd pbs-lsf/urCollector-src
  cp -p urCreator urCollector.pl \
  "$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf"
  install -m 0644 LICENSE \
  "$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf"
  cp -p urCollector.conf-template \
  "$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/urCollector.conf"
  cp -p urCollector.conf-template \
  "$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/urCollector.conf-template"
  mkdir -p "$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/urCollector"
  cp -p urCollector/Common.pm \
  "$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/urCollector"
  cp -p urCollector/Configuration.pm \
  "$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/urCollector"
  cd - >/dev/null

  install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
  install -m 644 %{SOURCE34} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/

%endif

# Burn in the RPM version into the python files.
grep -rIle '%%%%%%RPMVERSION%%%%%%' $RPM_BUILD_ROOT%{_datadir}/gratia $RPM_BUILD_ROOT%{python_sitelib} | while read file; do \
  perl -wpi.orig -e 's&%%%%%%RPMVERSION%%%%%%&%{version}-%{release}&g' "$file" && \
    rm -fv "$file.orig"
done

%ifarch noarch
  # Set up var area
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/{tmp,data,logs}
  chmod 1777  $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/data

  # install psacct startup script.
  install -d "${RPM_BUILD_ROOT}%{_initrddir}"
  install -m 755 "${RPM_BUILD_ROOT}%{_datadir}/gratia/psacct/gratia-psacct" \
  "${RPM_BUILD_ROOT}%{_initrddir}"
%else
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/pbs-lsf/{lock,tmp/urCollector}
%endif

# Ok, now the real packaging

# Find python files, and put in site-packages/gratia/<package>/...
install -d $RPM_BUILD_ROOT%{python_sitelib}/gratia

# For each project in /usr/share/gratia/...
for dir in `ls $RPM_BUILD_ROOT%{_datadir}/gratia`; do
    project_initial=$RPM_BUILD_ROOT%{_datadir}/gratia/$dir
    python_dir=`echo $dir | tr '-' '_'`
    project_sitelib=$RPM_BUILD_ROOT%{python_sitelib}/gratia/$python_dir

    # Put the python files in site-packages/gratia
    install -d $project_sitelib
    touch $project_sitelib/__init__.py
    for file in `find $project_initial -name "*.py"`; do
        install -m 644 $file $project_sitelib
        rm -f $file
    done
done

# Some of the probes dont have python packages
rm -rf $RPM_BUILD_ROOT%{python_sitelib}/gratia/{hadoop_storage,xrootd_transfer,xrootd_storage,condor,condor_events,pbs_lsf,sge}

%ifarch noarch
touch $RPM_BUILD_ROOT%{python_sitelib}/gratia/__init__.py
cp $RPM_BUILD_ROOT%{python_sitelib}/gratia/common/Gratia.py $RPM_BUILD_ROOT%{python_sitelib}/Gratia.py
install -d $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM
install -m 644 $RPM_BUILD_ROOT%{_datadir}/gratia/common/GRAM/JobManagerGratia.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManagerGratia.pm
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d
install -m 644 %{SOURCE30} $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d/99_gratia.conf
%endif

install -d $RPM_BUILD_ROOT/%{_localstatedir}/log/gratia

# Remove the test stuff
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/condor/test
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/sge/test
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/test
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/test

# Remove remaining cruft
rm -f $RPM_BUILD_ROOT%{_datadir}/gratia/condor/condor_meter.pl.rej
rm  -f $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia.repo
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/gratia/common
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/condor/gram_mods
rm  -f $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-storage/SL4_init_script_patches
rm  -f $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-transfer/SL4_init_script_patches
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/GRAM
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/jlib
rm -f $RPM_BUILD_ROOT%{python_sitelib}/gratia/common/samplemeter.py
rm -f $RPM_BUILD_ROOT%{python_sitelib}/gratia/common/samplemeter_multi.py

%clean
rm -rf $RPM_BUILD_ROOT

%description
Probes for the Gratia OSG accounting system

%ifnarch noarch

%package pbs-lsf
Summary: Gratia OSG accounting system probe for PBS and LSF batch systems.
Group: Application/System
Requires: %{name}-common >= 0.12f
License: See LICENSE.

%description pbs-lsf
Gratia OSG accounting system probe for PBS and LSF batch systems.

This product includes software developed by The EU EGEE Project
(http://cern.ch/eu-egee/).

%files pbs-lsf
%defattr(-,root,root,-)
%dir %{_localstatedir}/lib/gratia/pbs-lsf/lock
%doc %{_datadir}/gratia/pbs-lsf/LICENSE
%doc %{_datadir}/gratia/pbs-lsf/urCollector.conf-template
%doc %{_datadir}/gratia/pbs-lsf/README
%dir %{_datadir}/gratia/pbs-lsf
%{_datadir}/gratia/pbs-lsf/ProbeConfig
%{_datadir}/gratia/pbs-lsf/pbs-lsf_meter.cron.sh
%{_datadir}/gratia/pbs-lsf/pbs-lsf_meter.pl
%{_datadir}/gratia/pbs-lsf/pbs-lsf
%{_datadir}/gratia/pbs-lsf/urCreator
%{_datadir}/gratia/pbs-lsf/urCollector.pl
%{_datadir}/gratia/pbs-lsf/urCollector/Common.pm
%{_datadir}/gratia/pbs-lsf/urCollector/Configuration.pm
%config(noreplace) %{_datadir}/gratia/pbs-lsf/urCollector.conf
%config(noreplace) %{_sysconfdir}/gratia/pbs-lsf/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-pbs-lsf.cron

%else

%package common
Summary: Common files for Gratia OSG accounting system probes
Group: Applications/System
Requires: python >= 2.3
Requires: pyOpenSSL

%description common
Common files and examples for Gratia OSG accounting system probes.

%files common
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/common/README
%doc %{default_prefix}/gratia/common/samplemeter.pl
%{_localstatedir}/lib/gratia/
%{_localstatedir}/log/gratia/
%{python_sitelib}/gratia/__init__.py*
%{python_sitelib}/gratia/common
%{python_sitelib}/Gratia.py*
%dir %{default_prefix}/gratia/common
%{default_prefix}/gratia/common/DebugPrint
%{default_prefix}/gratia/common/GetProbeConfigAttribute
%{default_prefix}/gratia/common/ProbeConfigTemplate
%{perl_vendorlib}/Globus/GRAM/JobManagerGratia.pm

%package psacct
Summary: A ps-accounting probe
Group: Applications/System
Requires: psacct
Requires: %{name}-common >= 0.12f

%description psacct
The psacct probe for the Gratia OSG accounting system.

# Anything marked "config" is something that is going to be changed in
# post or by the end user.
%files psacct
%defattr(-,root,root,-)
%doc psacct/README
%doc %{default_prefix}/gratia/psacct/README
%dir %{default_prefix}/gratia/psacct
%{default_prefix}/gratia/psacct/ProbeConfig
%config %{default_prefix}/gratia/psacct/facct-catchup
%config %{default_prefix}/gratia/psacct/facct-turnoff.sh
%config %{default_prefix}/gratia/psacct/psacct_probe.cron.sh
%config %{default_prefix}/gratia/psacct/gratia-psacct
%{python_sitelib}/gratia/psacct
%config(noreplace) %{_sysconfdir}/gratia/psacct/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-psacct.cron
%config %{_initrddir}/gratia-psacct

%post psacct
# /usr -> "${RPM_INSTALL_PREFIX0}"
# %{default_prefix} -> "${RPM_INSTALL_PREFIX1}"
# /etc -> "${RPM_INSTALL_PREFIX2}"

# Configure boot-time activation of accounting.
/sbin/chkconfig --add gratia-psacct

# Deal with legacy Fermilab psacct configuration:
if grep -e 'fiscal/monacct\.log' >/dev/null 2>&1; then
  tmpfile=`mktemp /tmp/gratia-probe-psacct-post.XXXXXXXXXX`
  crontab -l 2>/dev/null | \
  grep -v -e 'nite/acct\.log' \
        -e 'fiscal/monacct\.log' > "$tmpfile" 2>/dev/null
  crontab "$tmpfile" >/dev/null 2>&1
  echo "Shutting down facct service" 1>&2
  /sbin/chkconfig --del facct
fi

rm -f "$tmpfile"

%customize_probeconfig -d psacct

%package condor
Summary: A Condor probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: /usr/bin/condor_history

%description condor
The Condor probe for the Gratia OSG accounting system.

%files condor
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/condor/README
%dir %{default_prefix}/gratia/condor
%{default_prefix}/gratia/condor/ProbeConfig
%{default_prefix}/gratia/condor/condor_meter.cron.sh
%{default_prefix}/gratia/condor/condor_meter.pl
%config(noreplace) %{_sysconfdir}/condor/config.d/99_gratia.conf
%config(noreplace) %{_sysconfdir}/gratia/condor/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-condor.cron

%post condor
%customize_probeconfig -d condor

%package sge
Summary: An SGE probe
Group: Applications/System
%if %{?python:0}%{!?python:1}
Requires: python >= 2.3
%endif
Requires: %{name}-common >= %{version}-%{release}

%description sge
The SGE probe for the Gratia OSG accounting system.

%files sge
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/sge/README
%{default_prefix}/gratia/sge/ProbeConfig
%{default_prefix}/gratia/sge/sge_meter.cron.sh
%{default_prefix}/gratia/sge/sge_meter
%dir %{default_prefix}/gratia/sge
%config(noreplace) %{_sysconfdir}/gratia/sge/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-sge.cron

%post sge
%customize_probeconfig -d sge

%package glexec
Summary: A gLExec probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}

%description glexec
The gLExec probe for the Gratia OSG accounting system.

%files glexec
%defattr(-,root,root,-)
%{default_prefix}/gratia/glexec/ProbeConfig
%doc %{default_prefix}/gratia/glexec/README
%{default_prefix}/gratia/glexec/glexec_meter.cron.sh
%{default_prefix}/gratia/glexec/glexec_meter
%{python_sitelib}/gratia/glexec
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-glexec.cron
%config(noreplace) %{_sysconfdir}/gratia/glexec/ProbeConfig

%post glexec
%customize_probeconfig -d glexec

%package metric
Summary: A probe for OSG metrics
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}

%description metric
The metric probe for the Gratia OSG accounting system.

%files metric
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/metric/README
%{python_sitelib}/gratia/metric
%dir %{default_prefix}/gratia/metric
%{default_prefix}/gratia/metric/ProbeConfig
%config(noreplace) %{_sysconfdir}/gratia/metric/ProbeConfig

%post metric
%customize_probeconfig -d metric

%package dcache-transfer
Summary: Gratia OSG accounting system probe for dCache billing.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
Requires:  python-psycopg2
License: See LICENSE.

Obsoletes: dCache-transfer < 1.07.02e-15
Provides: dCache-transfer = %{version}-%{release}

%description dcache-transfer
Gratia OSG accounting system probe for dCache transfers.
Contributed by Greg Sharp and the dCache project.

%files dcache-transfer
%defattr(-,root,root,-)
%{_initrddir}/gratia-dcache-transfer
%doc %{default_prefix}/gratia/dCache-transfer/README-experts-only.txt
%doc %{default_prefix}/gratia/dCache-transfer/README
%{default_prefix}/gratia/dCache-transfer/ProbeConfig
%{default_prefix}/gratia/dCache-transfer/gratia-dcache-transfer
%{python_sitelib}/gratia/dCache_transfer
%dir %{default_prefix}/gratia/dCache-transfer
%config(noreplace) %{_sysconfdir}/gratia/dCache-transfer/ProbeConfig

%post dcache-transfer
/sbin/chkconfig --add gratia-dcache-transfer
%customize_probeconfig -d dCache-transfer

%package dcache-storage
Summary: Gratia OSG accounting system probe for dCache storage.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services
Requires: xalan-j2
License: See LICENSE.

Obsoletes: dCache-storage < 1.07.02e-15
Provides: dCache-storage = %{version}-%{release}

%description dcache-storage
Gratia OSG accounting system probe for available space in dCache.
Contributed by Andrei Baranovksi of the OSG Storage team. 

%files dcache-storage
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/dCache-storage/README.txt
%{python_sitelib}/gratia/dCache_storage
%dir %{default_prefix}/gratia/dCache-storage
%{default_prefix}/gratia/dCache-storage/ProbeConfig
%{default_prefix}/gratia/dCache-storage/create_se_record.xsl
%{default_prefix}/gratia/dCache-storage/dCache-storage_meter.cron.sh
%{default_prefix}/gratia/dCache-storage/dCache_storage_probe
%config(noreplace) %{_sysconfdir}/gratia/dCache-storage/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-dcache-storage.cron

%post dcache-storage
%customize_probeconfig -d dCache-storage

%package gridftp-transfer
Summary: Gratia OSG accounting system probe for gridftp transfers.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
License: See LICENSE.

%description gridftp-transfer
Gratia OSG accounting system probe for available space in dCache.
Contributed by Andrei Baranovski of the OSG storage team.

%files gridftp-transfer
%defattr(-,root,root,-)
%{python_sitelib}/gratia/gridftp_transfer
%{default_prefix}/gratia/gridftp-transfer/gridftp-transfer_meter.cron.sh
%dir %{default_prefix}/gratia/gridftp-transfer
%{default_prefix}/gratia/gridftp-transfer/ProbeConfig
%{default_prefix}/gratia/gridftp-transfer/GridftpTransferProbeDriver
%config(noreplace) %{_sysconfdir}/gratia/gridftp-transfer/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-gridftp-transfer.cron

%post gridftp-transfer
%customize_probeconfig -d gridftp-transfer

%package services
Summary: Gratia OSG accounting system probe API for services.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
License: See LICENSE.

%description services
Gratia OSG accounting system probe API for services.
Contributed by University of Nebraska Lincoln.

%files services
%defattr(-,root,root,-)
%{python_sitelib}/gratia/services
%{default_prefix}/gratia/services/ProbeConfig
%{default_prefix}/gratia/services/storageReport
%dir %{default_prefix}/gratia/services
%config(noreplace) %{_sysconfdir}/gratia/services/ProbeConfig

%post services
%customize_probeconfig -d services

%package hadoop-storage
Summary: HDFS Storage Probe for Gratia OSG accounting system.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services
License: See LICENSE.

%description hadoop-storage
HDFS Storage Probe for Gratia OSG accounting system.
Contributed by University of Nebraska Lincoln.

%files hadoop-storage
%defattr(-,root,root,-)
%{default_prefix}/gratia/hadoop-storage/hadoop_storage_probe
%{default_prefix}/gratia/hadoop-storage/ProbeConfig
%config(noreplace) %{_sysconfdir}/gratia/hadoop-storage/ProbeConfig
%config(noreplace) %{_sysconfdir}/gratia/hadoop-storage/storage.cfg
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-hadoop-storage.cron

%post hadoop-storage
%customize_probeconfig -d hadoop-storage

%package condor-events
Summary: Probe that emits a record for each event in the Condor system.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
License: See LICENSE.

%description condor-events
Condor Events Probe for Gratia OSG accounting system.
Contributed by University of Nebraska Lincoln.

%files condor-events
%defattr(-,root,root,-)
%{_datadir}/gratia/condor-events/watchCondorEvents
%{_datadir}/gratia/condor-events/ProbeConfig
%config(noreplace) %{_sysconfdir}/gratia/condor-events/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-condor-events.cron

%post condor-events
%customize_probeconfig -d condor-events

%package xrootd-transfer
Summary: Probe that emits a record for each file transfer in Xrootd.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
License: See LICENSE.

%description xrootd-transfer
Xrootd Transfer Probe for Gratia OSG accounting system.
Contributed by University of Nebraska Lincoln.

%files xrootd-transfer
%defattr(-,root,root,-)
%{_initrddir}/gratia-xrootd-transfer
%{default_prefix}/gratia/xrootd-transfer/xrd_transfer_probe
%{default_prefix}/gratia/xrootd-transfer/ProbeConfig
%dir %{default_prefix}/gratia/xrootd-transfer
%config(noreplace) %{_sysconfdir}/gratia/xrootd-transfer/ProbeConfig

%post xrootd-transfer
%customize_probeconfig -d xrootd-transfer

%package xrootd-storage
Summary: Gratia probe to monitor Xrootd storage usage.
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services = %{version}-%{release}
License: See LICENSE.

%description xrootd-storage
Xrootd Transfer Probe for Gratia OSG accounting system.
Contributed by Brian Bockelman at University of Nebraska Lincoln.
Contributed as effort from OSG-Storage.

%files xrootd-storage
%defattr(-,root,root,-)
%{_initrddir}/gratia-xrootd-storage
%{default_prefix}/gratia/xrootd-storage/xrd_storage_probe
%{default_prefix}/gratia/xrootd-storage/ProbeConfig
%dir %{default_prefix}/gratia/xrootd-storage
%config(noreplace) %{_sysconfdir}/gratia/xrootd-storage/ProbeConfig

%post xrootd-storage
%customize_probeconfig -d xrootd-storage

%package bdii-status
Summary: Probes that emits records of BDII status
Group: Application/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services >= %{version}-%{release}
License: See LICENSE.

%description bdii-status
Records a BDII's status into the Gratia accounting system.
Creates a record for CEs, SEs, and Subcluster objects.
Contributed by University of Nebraska Lincoln.

%files bdii-status
%defattr(-,root,root,-)
%{default_prefix}/gratia/bdii-status/ProbeConfig
%{default_prefix}/gratia/bdii-status/bdii_subcluster_record
%{default_prefix}/gratia/bdii-status/bdii_cese_record
%dir %{default_prefix}/gratia/bdii-status
%{python_sitelib}/gratia/bdii_status
%config(noreplace) %{_sysconfdir}/gratia/bdii-status/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-bdii-cese.cron
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-bdii-subcluster.cron

%post bdii-status
%customize_probeconfig -d bdii-status

%endif # noarch

%changelog
* Wed Aug 24 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.07.02e-0.16.pre
Fix GratiaCore so it does not attempt to write into $HOME.

* Mon Aug 22 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.07.02e-0.15.pre
- Move probe customization into install section.

* Sun Aug 21 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.07.02e-0.14.pre
Restructure spec file to simplify, and remove as many things from the post script as possible.

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.07.02e-0.13.pre
- Fix directory locations for JobManagerGratia.  Remove empty extra-libs-arch-spec.

* Tue Aug 16 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.12.pre
Added user-vo-map to the default ProbeConfig

* Tue Aug 16 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.11.pre
- Updated the logging directory to /var/log/gratia

* Tue Aug 16 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.10.pre
- Fixed probe-preconfig macro for new directory
- Fixed system directory for dcache-transfer probeconfig

* Thu Aug 11 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.9.pre
- Removed requires on globus-scripts

* Thu Aug 11 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.8.pre
- Added JobManagerGratia.pm to perl sitelib

* Wed Aug 10 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.07.02e-0.7.pre
- Rebuild for noarch in Koji

* Wed Aug 03 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.6.pre
- Removed echo message from condor probe
- Added 99_gratia.conf to condor configuration

* Fri Jul 22 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.5.pre
- Changes to move things into FHS locations

* Thu Jun 2 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.4.pre
- Fixed hadoop probe for 0.20

* Wed May 25 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.07.02e-0.2pre
- Add support in the PBS probe for 'array jobs'
- Add support in the Condor probe for GlideinWMS jobs

* Thu May 5 2011 Neha Sharma <neha@fnal.gov> - 1.07.02d-2
- Updating release number as it wont generate the rpms correct otherwise

* Thu May 5 2011 Neha Sharma <neha@fnal.gov> - 1.07.02d-1
- The version number 1.09.01a is incorrect. There was some confusion.
- Fixing the version number now

* Wed May 4 2011 Neha Sharma <neha@fnal.gov> - 1.09.01a-1
- Noted that latest changes to DCacheAggregator.py and dCacheBillingAggregator.py
- did not make it into SVN. So, committed them again

* Mon May 2 2011 Neha Sharma <neha@fnal.gov> - 1.08.01a-1
- Modified gratia-probe.spec file to update Version and Release numbers
- Modified probe/build/README file to point to latest documentation on how to
- build probes

* Wed Apr 20 2011 Neha Sharma <neha@fnal.gov> 
- Removed SQLAlchemy and setup tools
- Removed obsolete parameter SOAPHost fro ProbeConfig
- modified the Build scripts, gratia-probe.spec file and README files to 
- remove dependencies/references on SQLAlchemy and setup tools
- Add upload of information about the amount of data still needing to be processed
  or uploaded to the Collector.
- Add new GratiaCore interface 'ResgisterEstimatedServiceBacklog' to let the probe 
  tell the system how much work is left to do.
- Avoid premature termination of the reprocessing (i.e. it will now reprocess all 
  the data before moving on)
- When compressing the xml data file into a tar file, make sure that the
  files are also removed from the current bundle ; thus avoiding a spurrious
  duplicate record when reprocessing.

* Tue Mar 08 2011 Philippe Canal <pcanal@fnal.gov> - 1.07.02b
- Update the use of ServiceLevel in the sge probe that prevent it from running properly.

* Thu Mar 04 2011 Philippe Canal <pcanal@fnal.gov> - 1.07.02a-2
- Backport to ancient python (2.3.4)

* Thu Mar 03 2011 Philippe Canal <pcanal@fnal.gov> - 1.07.02a-1
- Add support for CREAM Computing Element by adding support for extract
-  the cerfication information from the blahp.log files

* Thu Jan 20 2011 Christopher Green <greenc@gr6x1.fnal.gov> - 1.07.01a-2
- Correct bad preun for bdii-status.

* Mon Dec 20 2010 Brian Bockelman <bbockelm@cse.unl.edu> - 1.07.1a-1
- Increase buffer size on the server to make sure we get the full 
-  message from the xrootd daemon.
- Enhance detection of number of core in PBS and LSF accounting log 
-  (hence fixing the calculation for HTPC/whole node jobs)
- Since GratiaCore.py has a very efficient (tar.gz) way of keeping in 
-  store the record that can not be sent up to the collector, we now 
-  use this mechanism rather than keeping any input that is already in 
-  UsageRecord XML format.
- Addresses a security problem in which users can submit jobs that cause 
-  the gratia probe to execute arbitrary python code supplied by the user.  
- Reporting the number of processors is so that multi-core jobs (HTPC) on OSG 
-  condor sites will be correctly accounted.

* Mon Dec 20 2010 Brian Bockelman <bbockelm@cse.unl.edu> - 1.07.1-0.1.pre1
- First pre-release of 1.07, including the bdii-status probes.

* Mon Jun 21 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.16c-1
- Updated dCache-storage and dCache-transfer and README files from Neha.
- Remove unnecessary debug print from dCache-storage probe.

* Fri Jun 18 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.16b-1
- Fix daft typo in GratiaCore.py

* Thu Jun 17 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.16a-2
- Remove file entry for removed file xrootd-transfer/watchXrootdLogs.py.

* Thu Jun 17 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.16a-1
- Fix from Philippe for global variable scope issue.

* Thu Jun  3 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15p-1
- Hopefully final pre-release tweaks to dCache probe from Brian.

* Fri May 28 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15o-1
- Tweak ProbeConfig extra items for dCache-transfer probe.
- Reorganize GridFtpLogDir config item insertion..
- Sleep and configurable DB name for dCache-transfer probe from Brian.
- Core updates for HTTP timeout waiting for acknowledgement from
-  collector from Philippe.
- Improve connection timeout mesage to avoid confusion (from Philippe).

* Mon May 24 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15n-2
- Update dependencies.

* Mon May 24 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15n-1
- Correct import to GratiaCore in services.

* Fri May 21 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15m-1
- Improvements to xrootd probe from Brian.

* Wed May 19 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15l-1
- Fix from Philippe for staticmethod (make it work in 2.3).

* Fri May 14 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15k-1
- Build checkpoint for Andrew.

* Mon Mar 29 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15j-1
- Test release for storage group.

* Mon Mar 29 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15i-1
- Fix mechanism intended to avoid corruption caused by reading in-progress log.

* Mon Mar 15 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15h-1
- Robustness fix to GetNodeData function in Gratia.py.

* Mon Mar 15 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15g-1
- Fix for exception in debug statements in Gratia.py.
- Increase default BundleSize to 100 in ProbeConfigTemplate and Gratia.py.

* Mon Mar  8 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15f-2
- Remove unecessary dependencies from dCache-storage probe.

* Thu Mar  4 2010 Christopher Green <greenc@gr6x1.fnal.gov> - 1.06.15f-1
- EGEE-provided probe is now version-controlled instead of unpackaged
-  and patched from source.
- Unused GridftpTransfer.sh script removed prior to final packaging.
- Condor probe security fixes from Wisconsin.

* Wed Feb 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> - 1.06.15d-2
- Add gratia-probe-services as a dependency to the xrootd-storage probe

* Tue Feb  2 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.15d-1
- Fix from Andrew for CLASSPATH, etc.
- Fix to cron scripts for WorkingFolder discovery in dCache-storage and
-  gridftp-transfer cron scripts.

* Tue Feb  2 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.15c-2
- Remove erroneous ITB tag for services API package.

* Tue Feb  2 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.15c-1
- Better use of lock files in *_cron.sh.
- Fixes and updates to dCache-storage probe, including addition of
-  README file to package.

* Thu Jan 28 2010 Brian Bockelman <bbockelm@cse.unl.edu> - 1.06.15b-1
- Added redesigned xrootd-transfer probe
- Minor updates for the xrootd-storage probe found in testing.

* Tue Jan 26 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.15a-1
- Fix to condor probe for standalone (non-VDT) operation.

* Mon Jan 25 2010 Brian Bockelman <bbockelm@cse.unl.edu> - 1.06.14c-1
- Added new xrootd-storage probe
- Corrected dependency on non-existent gratia-probe-common-itb to
-  gratia-probe-common for condor-events and xrootd-transfer

* Tue Jan 19 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.14b-1
- Config template documentation.
- Add MaxBillingAgeDays to config file for dCache-transfer.

* Tue Jan 19 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.14a-1
- Fix bad comments after block restoration.

* Mon Jan 11 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.13c-1
- Fix logic problem with transfer record loop.

* Fri Jan  8 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.13b-1
- Fix incorrect error response detection in gridftp-transfer probe.

* Thu Jan  7 2010 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.13a-1
- Reactivate build of new storage probe.
- Improve detection of and response to down collector.
- Improve armoring against bad osg-user-vo-map.txt file.
- Use sourceforge gridftp-transfer probe source instead of old import from CVS.
- Use new sourceforge dCache-transfer probe source.
- Remove .orig_files after RPMVERSION substitution.

* Wed Dec  2 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.12-1
- Improvements to SGE probe for incomplete log lines.
- Condor probe detects and clean ups extra ClassAd file produced for WN BOINC probe. 
- Deal with extra-content X509USERPROXYSUBJECT if presented.
- Glexec probe ResourceType changed to BatchPilot.
- Quarantine bad XML files. Clean up regularly.
- Check for and deal with POST too large errors.
- Better handling of large backlogs.
- "Extraordinary" cleanup to handle disk space crunch.

* Wed Oct 21 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.7a-1
- Correct indentation of loop in DCacheBillingAggregator..

* Wed Oct 21 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.06.7-1
- Incorporate Philippe's improvements to DCacheBillingAggregator for long catchups.

* Tue Oct 20 2009 Brian Bockelman <bbockelm@cse.unl.edu> - 1.04.6-3
- Added the xrootd-transfer probe

* Mon Oct 12 2009 Brian Bockelman <bbockelm@cse.unl.edu> - 1.04.6-2
- Added the condor-events probe

* Sat Sep 26 2009 Brian Bockelman <bbockelm@cse.unl.edu> - 1.04.6-1
- Changed the hadoop-storage probe to properly pick up site name from ProbeConfig
- Changed the default collector for the services-based probes to OSG, not OSG-transfer

* Fri Sep 25 2009 Brian Bockelman <bbockelm@cse.unl.edu> - 1.04.6
- Added the hadoop-storage probe

* Thu Sep 10 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.5-1
- PBS probe now uploads to Gratia after every log file has been read.
- More improvements to Gratia.py output verbosity at low logging levels.
- More fixes to multi-processor handling for PBS.

* Thu Sep  3 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.4g-1
- Invoke Gratia from inside the urCollector part.
- Fix problems with PBS probe found during testing..
- Package services probe API at Brian's request.
- Include remaining dCache and Gratia.py backlog and server exception
-  handling improvements.
- PBS probe now handles account= directive and passes as UserVOName
-  (suitably handled by collector).
- Re-enable and improve the limit on the maximum number of records cached due to a
-  collector unavailability
- New ProbeConfig configuration value: MaxStagedArchives
- New location for the records, it is now
-  "WorkingFolder"/gratiafiles/subdir.[ProbeName].[CollectorHost]/outbox
- Once the outbox has "MaxPendingFiles", it is tar-ed and compressed in file
-  in "WorkingFolder"/gratiafiles/subdir.[ProbeName].[CollectorHost]/staged/store
- When the collector is again available, one of the tar file is uncompressed
-  in "WorkingFolder"/gratiafiles/subdir.[ProbeName].[CollectorHost]/staged/outbox
- The new limit of the number of records is 2*MaxPendingFiles + MaxStagedArchives*MaxPendingFiles
-  This results in only (2*MaxPendingFiles + MaxStagedArchives) files on disk with
-  no more than MaxPendingFiles in a single directory.
- New function Gratia.Maintenance to be called every once in a while by daemon/long 
-  lived probes
- Improve handling of reprocessing in case of time outs
- Re-write handling of reprocessing.
- Improve handling of send errors in dCache probe.
- Improve log level of some messages.
- Fix GratiaPing.py per pylint.
- Remove RegisterProbe.py -- obsolete and stale.

* Wed Aug 26 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.4e-1
- Improve PBS' ability to glean information about number of cores from log.
- SGE probe patch from Brian for number of cores.
- Gratia.py improvements for handling large numbers of files to reprocess.
- Gratia.py improvements for non-grid user -> group mappings.
- Gratia.py fix for misunderstanding multiupdate errors from old
-  collectors while bundling.

* Wed Aug 19 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.4d-1
- Update dCache-transfer package to include improvement to query.

* Wed Aug 19 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.4c-1
- Update dCache-transfer package to include fix for response handling under bundling.

* Wed Aug 19 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.4b-1
- Prepend 'OK' to successful bundling responses.

* Wed Aug 19 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.4a-1
- Fix to server-side error remediation while bundling.

* Tue Aug 11 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.3c-2
- Corrections for incorrect munging of new probe config template.

* Mon Jul 13 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.3c-1
- Fix daft typo.

* Mon Jul 13 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.3b-1
- Change probes to use DN rather than UserkKeyInfo.

* Tue Jul  7 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04.3a-1
- Fix backward compatibility for old MeterName.
- Update dCache transfer package to 0.2.8 incorporating query improvement from Brian.

* Fri Jun 26 2009 Christopher Green <greenc@gratia01.fnal.gov> - 1.04-1
- 1.04 release.
- Add files ProxyUtil.py, GratiaPing.py to common package.
- Secure upload to collector included self-signing.
- MeterName -> ProbeName (legacy name supported).
- SOAPHost -> CollectorHost (legacy name supported).
- Probe-side record bundling.
- Improve connection error handling.

* Mon Mar  2 2009 Christopher Green <greenc@fnal.gov> - 1.02.1a-1
- Do not create etc and libexec links.
- Add patches to remove reliance on existance of etc and libexec links.
- Fix multiple pychecker problems in Gratia.py.

* Wed Feb  4 2009 Christopher Green <greenc@fnal.gov> - 1.02.1-5
- Correct soaphost configs.

* Wed Feb  4 2009 Christopher Green <greenc@fnal.gov> - 1.02.1-4
- Correct soaphost configs.

* Wed Feb  4 2009 Christopher Green <greenc@fnal.gov> - 1.02.1-3
- Correct soaphost configs.

* Wed Feb  4 2009 Christopher Green <greenc@fnal.gov> - 1.02.1-2
- Correct soaphost configs.

* Wed Feb  4 2009 Christopher Green <greenc@fnal.gov> - 1.02.1-1
- Update to main release no.
- Update gridftp-transfer to v0.3 for bugfix from Andrei.

* Tue Jan 20 2009 Christopher Green <greenc@fnal.gov> - 1.00.5g-1
- Fix problem with walltime patch.

* Tue Jan 20 2009 Christopher Green <greenc@fnal.gov> - 1.00.5f-1
- Fix problem getting walltime and cputime if >100h.

* Fri Jan 16 2009 Christopher Green <greenc@fnal.gov> - 1.00.5e-1
- Update transfer probe to include Brian's latest fixes.
- Gratia.py now handles marking of batch records without certinfo files
-  as local.
- SuppressGridLocalRecords is no longer defaulted to true.

* Mon Dec 15 2008 Christopher Green <greenc@fnal.gov> - 1.00.5d-1
- Add patch to urCollector.pl to understand mppwidth directive in PBS log.
- Add facility to Gratia.py to extract the CVS revision from another file.
- Change glexec.py, pbs-lsf.py and condor_meter.pl to get their tag info
-  from the RPM packaging process rather than CVS' Name attribute.

* Mon Dec  8 2008 Christopher Green <greenc@fnal.gov> - 1.00.5c-2
- gridftp-transfer probe is not a dCache probe.
- gridftp-transfer probe requires python >= 2.3.

* Mon Dec  8 2008 Christopher Green <greenc@fnal.gov> - 1.00.5c-1
- Incorporate v0.2 of gridftp-transfer probe.

* Thu Nov 20 2008 Christopher Green <greenc@fnal.gov> - 1.00.5b-1
- Updated dCache-transfer/README from Tanya.

* Wed Nov 19 2008 Christopher Green <greenc@fnal.gov> - 1.00.5a-1
- GridftpLogDir moved to ProbeConfigTemplate for ease of translation.

* Wed Nov 19 2008 Christopher Green <greenc@fnal.gov> - 1.00.5-3
- gridftp-transfer probed does not need extra-libs.

* Wed Nov 19 2008 Christopher Green <greenc@fnal.gov> - 1.00.5-2
- Reorder some regex replacements in postconfig to allow late-entry
-  MAGIC_VDT_LOCATION to be subbed.

* Wed Nov 19 2008 Christopher Green <greenc@fnal.gov> - 1.00.5-1
- Packaged gridftp-transfer probe from Andrei.
- Bumped version number to match collector.

* Fri Nov 14 2008 Christopher Green <greenc@fnal.gov> - 1.00.4-1
- Version bump only to match collector.

* Thu Nov 13 2008 Christopher Green <greenc@fnal.gov> - 1.00.3c-1
- If the ProbeConfig is missing the SuppressGridLocalRecords attribute,
-  it defaults to true.

* Thu Nov 13 2008 Christopher Green <greenc@fnal.gov> - 1.00.3b-1
- Fix errors in Gratia.py found by pylint.
- Remove cruft around revision no. in condor_meter.pl.

* Fri Nov  7 2008 Christopher Green <greenc@fnal.gov> - 1.00.3a-1
- Proper version reporting for dCache and glexec probes.

* Thu Nov  6 2008 Christopher Green <greenc@fnal.gov> - 1.00.3-2
- Change template marker to allow VDT configuration script to spot pristine config files.

* Thu Nov  6 2008 Christopher Green <greenc@fnal.gov> - 1.00.3-1
- Add SuppressGridLocalRecords option to ProbeConfig and implementation
-  thereof in Gratia.py
- Include dCache-transfer v0.2.4 with latest patch for handling bad
-  billing DB data from Brian.

* Wed Oct 29 2008 Christopher Green <greenc@fnal.gov> - 1.00.1-1
- Include v0.2.3 of the dCache-transfer probe which has the
- not-earlier-than threshold from Brian.

* Mon Oct 20 2008 Philippe Canal <pcanal@fnal.gov> - 1.00
- Major overhaul in the way certinfo files are found and ambiguities
-  resolved, in particular improving run-time performance.
- Probe reports additional information about the probe library
-  and the batch job.
- Insure ProbeName is always set

* Thu Oct  2 2008 Christopher Green <greenc@fnal.gov> - 0.38b-2
- Correct erroneous minutes entry for glexec cron.

* Mon Sep 29 2008 Christopher Green <greenc@fnal.gov> - 0.38b-1
- Fix indentation problem in DebugPrint().
- Fix MeterName setting.

* Fri Sep 26 2008 Christopher Green <greenc@fnal.gov> - 0.38a-1
- Incorporate patch from Greg Quinn such that condor probe only updates
-  EndTime if CompletionDate >0.
- Downgrade some warning messages from condor probe.
- Provide early and explicit warning of ProbeConfig problems in all
-  probes.
- Gratia.py now defaults MeterName to auto:`hostname -f` if not set in
-  ProbeConfig.

* Mon Aug 25 2008 Christopher Green <greenc@fnal.gov> - 0.38a-1
- Glexec execution period set to 1h.
- Condor will batch sends so that a given python script will only
-  generate 500 records at max before sending.

* Wed Aug 20 2008 Christopher Green <greenc@fnal.gov> - 0.38-1
- Include transfer probe with fixed StartTime and new upload of IsNew
-  attribute.
- Include Condor probe with upload of ExitSignal attribute when present.

* Tue Jul 15 2008 Christopher Green <greenc@fnal.gov> - 0.36-1
- Fix certinfo / batch job matching for PBS jobs.

* Fri Jun  6 2008 Christopher Green <greenc@fnal.gov> - 0.34.9-1
- Fix problems with JobManagerGratia.pm.
- Fix typo in gratia-psacct init file (only affected status).
- Fix typo in glexec README file.

* Tue Jun  3 2008 Christopher Green <greenc@fnal.gov> - 0.34.8-2
- Fix bad mode on DebugPrint.py

* Mon Jun  2 2008 Christopher Green <greenc@fnal.gov> - 0.34.8-1
- Correct cleanup of no-longer-useful files in gratia/var/data.
- Improve DebugPrint.py in the case that input contains blank lines.
- Improve logic used in condor probe to decide whether we can use the absence
-  of the GratiaJobOrigin ClassAd attribute to infer that a job is local.
- Condor probe is now verbose but prints to main Gratia log.
- Condor probe only assigns grid=Local to jobs it's really sure are local.

* Fri May 16 2008 Christopher Green <greenc@fnal.gov> - 0.34.1-1
- Better exception handling in Gratia.py.
- Fix corner case handling certinfo for WS jobs with ID < 100.

* Mon May 12 2008 Christopher Green <greenc@fnal.gov> - 0.34b-1
- Fix stupidities triggered under strange circumstances.

* Fri May  9 2008 Christopher Green <greenc@fnal.gov> - 0.34a-1
- Updates to Gratia.py to handle cases where certinfo is present
-  but has nothing useful (WS).

* Fri May  9 2008 Christopher Green <greenc@fnal.gov> - 0.34-1
- Probe release for VDT:
-   Condor probe seriously updated to get data from anywhere it can.
-   Record upload failures due to (eg) 503 don't print the HTML error
-    source to the log file, just a short message.

* Mon May  5 2008 Christopher Green <greenc@fnal.gov> - 0.32.4-1
- dcache_transfer_probe_version to v0-1:
-   Fix transfer README.
- dcache_storage_probe_version to v0-1 (no change).

* Tue Apr 29 2008 Christopher Green <greenc@fnal.gov> - 0.32.3-2
- Correct configuration for ITB.

* Mon Apr 28 2008 Christopher Green <greenc@fnal.gov> - 0.32.3-1
- Merge ability to turn off dCache probe building from branch.
- dCache probes get sent to different host / port.
- dcache_transfer_probe_version to v0-1pre7.
- dcache_storage_probe_version to v0-1pre5.
- Gratia.py and glexec_meter.py now take advantage of new DN/FQAN
-  ability.

* Thu Mar 20 2008 Christopher Green <greenc@fnal.gov> - 0.32.2e-1
- dcache_transfer_probe_version -> v0-1pre6:
-   Add HOME to environment of init script if missing to allow python
-   logging to work (sheesh).

* Thu Mar 20 2008 Christopher Green <greenc@fnal.gov> - 0.32.2d-1
- dcache_transfer_probe_version -> v0-1pre5:
-   Fix import pkg_resource in DCacheAggregator.py.
- dcache_storage_probe_version -> v0-1pre3:
-   Fix PYTHONPATH in dCache-storage_meter.cron.sh.

* Thu Mar 20 2008 Christopher Green <greenc@fnal.gov> - 0.32.2c-1
- dcache_transfer_probe_version -> v0-1pre4:
-   Fix transfer probe import of string.

* Tue Mar 18 2008 Christopher Green <greenc@fnal.gov> - 0.32.2b-1
- dcache_transfer_probe_version -> v0-1pre3
-   README includes info about OnlySendInterSiteTransfers.

* Tue Mar 18 2008 Christopher Green <greenc@fnal.gov> - 0.32.2a-2
- Add OnlySendInterSiteTransfers to transfer ProbeConfig

* Tue Mar 18 2008 Christopher Green <greenc@fnal.gov> - 0.32.2a-1
- dcache_storage_probe_version -> v0-1pre2
-   Fix old python script references in cron script).
- dcache_probe_version -> dcache_transfer_probe_version (default value
- of OnlySendInterSiteTransfers should be true).
- dcache_transfer_probe_version -> v0-1pre2.
- Remove .orig and .bak files from post by request.

* Mon Mar 17 2008 Christopher Green <greenc@fnal.gov> - 0.32.2-1
- Transfer all dCache files (including READMEs) to dCache repository and
- go back to the tarball paradigm.

* Wed Mar 12 2008 Christopher Green <greenc@fnal.gov> - 0.32g-2
- Fix over-zealous scrubbing of crontab.

* Fri Mar  7 2008 Christopher Green <greenc@fnal.gov> - 0.32g-1
- Collector not yet ready for DN attribute.

* Thu Mar  6 2008 Christopher Green <greenc@fnal.gov> - 0.32f-2
- Fix uninitialized var problem for a particular code path in Gratia.py.

* Wed Mar  5 2008 Christopher Green <greenc@fnal.gov> - 0.32e-2
- Remove automatic requirement generation for the common package.

* Fri Feb 29 2008 Christopher Green <greenc@fnal.gov> - 0.32e-1
- Disable DN/FQAN special upload until collector improvements complete.

* Thu Feb 28 2008 Christopher Green <greenc@fnal.gov> - 0.32d-1
- Mirror glob improvement from transfer init script to storage cron script.

* Thu Feb 28 2008 Christopher Green <greenc@fnal.gov> - 0.32c-2
- Fix typo in ProbeConfig configure macro.

* Thu Feb 28 2008 Christopher Green <greenc@fnal.gov> - 0.32c-1
- Enable suppression of records without DN.
- Defined order of precendence for different sources of VO information.
- GLExec probe now saves FQAN.
- GLExec error output redirected to log.
- Remove some unneeded entries from ProbeConfig for dCache probe.
- GRAM patches appropriately named, with README.
- Fix unpackaged file problems.
- Improve SGE test file.
- SGE probe updates.

* Mon Feb 25 2008 Christopher Green <greenc@fnal.gov> - 0.32b-1
- Incorporate updates to Gratia.py:
- * Fix problem of upload to collector requiring workaround parsing of
-   POST arguments.
- * Probe can now read and upload certinfo files produced by a suitably
-   modified GRAM.
- GRAM mods to allow capture of DN / FQAN information.
- dCache probe fixes requested by Brian B.
- New README files to specify configuration information for dCache
  probes as installed by RPM or VDT; rename other README files to avoid
  confusion.
- Protect ProbeConfig files that are likely to have sensitive
  information (eg DB access information).

* Wed Feb 13 2008 Christopher Green <greenc@fnal.gov> - 0.32a-2
- Improve path setting in dCache-transfer init script.

* Wed Feb 13 2008 Christopher Green <greenc@fnal.gov> - 0.32a-1
- Incorporate Brian's files (NOP, but version bumped).

* Tue Jan 29 2008 Christopher Green <greenc@fnal.gov> - 0.32-1
- pexec should be global to get substituted in post properly.

* Tue Jan 29 2008 Christopher Green <greenc@fnal.gov> - 0.32-0%rtext
- Add override tar for dCache-transfer files.
- Remove python requires if python exec is overridden.
- glexec probe fixes ResourceType and ProbeName.

* Mon Jan 22 2008 Christopher Green <greenc@fnal.gov> - 0.30d-1
- Parser is a whole lot careful for LSF files, and more efficient for
  both PBS and LSF.
- Re-order unpacking of gratia/probe/dCache-storage vs the provided tar
  file to allow files to be overrwritten.
- Fix version matching in Condor jobmanager patches.

* Mon Jan 14 2008 Christopher Green <greenc@fnal.gov> - 0.30c-1
- Quick fix for last line in file missing newline due to race with batch
  system.

* Mon Jan  7 2008 Christopher Green <greenc@fnal.gov> - 0.30b-3
- Fix crontab removal problems in multiple preun statements.
- Add missing preun to gratia-storage.

* Fri Dec 14 2007 Christopher Green <greenc@fnal.gov> - 0.30b-2
- Remove debug statements from build.

* Fri Dec 14 2007 Christopher Green <greenc@fnal.gov> - 0.30b-1
- Allow for non-standard name of python exec.
- Fix directory problems in dCache-storage_meter.cron.sh.
- Fix cron install for dCache-storage.
- Add disclaimer to README file for dCache-transfer.

* Thu Dec 13 2007 Christopher Green <greenc@fnal.gov> - 0.30a-2
- Upon request, dCache probe is renamed to dCache-transfer.

* Mon Dec 10 2007 Christopher Green <greenc@fnal.gov> - 0.30a-1
- Better code reuse in scriptlets.
- Package dCache probes and associated third party libraries.
- Better method of naming temporary XML files prior to upload.

* Tue Oct 16 2007 Christopher Green <greenc@fnal.gov> - 0.27.5c-1
- Correct handling of suppressed records.

* Thu Oct  4 2007 Christopher Green <greenc@fnal.gov> - 0.27.5b-1
- Fix location of DebugPrint.py for PBS error conditions.

* Mon Sep 24 2007 Christopher Green <greenc@fnal.gov> - 0.27.5a-1
- Remove bad debug message in Gratia.py.
- Fix encoding behavior in Gratia.py.
- Fix dangerous behavior in debug mode in condor_meter.pl.

* Tue Sep 11 2007 Christopher Green <greenc@fnal.gov> - 0.27.3-1
- Match collector version bump.

* Mon Sep 10 2007 Christopher Green <greenc@fnal.gov> - 0.27.2a-1
- Better redirection of non-managed output.

* Mon Sep 10 2007 Christopher Green <greenc@fnal.gov> - 0.27.2-1
- Handshaking facility with collector.
- Gratia.py can handle larger numbers for time durations.
- URLencoding and XML escaping (backward compatible with old collectors).

* Mon Aug  6 2007 Christopher Green <greenc@fnal.gov> - 0.26.2b-1
- /bin/env -> /usr/bin/env in pound-bang line.

* Fri Aug  3 2007 Christopher Green <greenc@fnal.gov> - 0.26.2a-1
- Fix crontab entries to include user.
- Fix and improve DebugPring.py logging utility.
- Fix PBS probe logging.

* Thu Jul 19 2007 Christopher Green <greenc@fnal.gov> - 0.26-2
- Fix Grid assignment for psacct probe.

* Wed Jul 18 2007 Christopher Green <greenc@fnal.gov> - 0.26-1
- Configure Grid attribute appropriately in new ProbeConfig files.
- Fix Metric probe configuration of port.

* Wed Jul 11 2007 Christopher Green <greenc@fnal.gov> - 0.25a-1
- Correct Gratia.py to generate correct XML for Grid attribute.
- Take account of Gratia.py changes in Metric.py.
- Remove unnecessary Obsoletes clause from metric package.

* Tue Jul  3 2007 Christopher Green <greenc@fnal.gov> - 0.25-1
- First release of metric probe.

* Mon Jun 18 2007 Christopher Green <greenc@fnal.gov> - 0.24b-3
- Added define _unpackaged_files_terminate_build 0 to prevent python
-  files being byte-compiled without being put into the files list.

* Mon Jun 18 2007 Christopher Green <greenc@fnal.gov> - 0.24b-2
- Fix patch application.

* Mon Jun 18 2007 Christopher Green <greenc@fnal.gov> - 0.24b-1
- Remove accidental 'percent'global in changelog causing complaints.
- Patch xmlUtil.h to compile under gcc4.1's fixed friend injection rules.

* Fri Jun 15 2007 Christopher Green <greenc@fnal.gov> - 0.24a-1
- Fix problem with sge_meter_cron.sh per Shreyas Cholia

* Thu Jun 14 2007 Christopher Green <greenc@fnal.gov> - 0.24-1
- Sync with service release no.
- Incorporate latest changes to SGE probe from Shreyas.
- Fix URL in probe/sge/README per Shreyas.

* Thu Jun 14 2007 Christopher Green <greenc@fnal.gov> - 0.23b-1
- Extra safety checks on document integrity.
- Correct spelling of metricRecord.

* Wed Jun 13 2007 Christopher Green <greenc@fnal.gov> - 0.23a-1
- Fix various and sundry problems with abstractions of XML checking
 	routines.

* Wed Jun 13 2007 Christopher Green <greenc@fnal.gov> - 0.23-1
- Redirect urCollector.pl output to log file from pbs-lsf_meter.cron.sh.
- Gratia.py handles new "Grid" attribute.
- Updated release no.

* Tue Jun 12 2007 Christopher Green <greenc@fnal.gov> - 0.22d-4
- More variables declared global to fix funny behavior.
- glexec probe does not require python 2.3 -- erroneously copied from SGE.
- final_post_message only prints out if it's a ProbeConfig file.

* Fri May 25 2007 Christopher Green <greenc@fnal.gov> - 0.22d-1
- New utilites GetProbeConfigAttribute.py and DebugPrint.py.
- Cron scripts now check if they are enabled in ProbeConfig before
	running the probe.

* Thu May 24 2007 Christopher Green <greenc@fnal.gov> - 0.22c-1
- Correct minor problems with glexec probe.

* Thu May 24 2007 Christopher Green <greenc@fnal.gov> - 0.22b-2
- Swap to using /etc/cron.d and clean up root's crontab.

* Fri May 18 2007 Christopher Green <greenc@fnal.gov> - 0.22b-1
- Fix condor_meter.pl problems discovered during testing.
- uname -n => hostname -f.
- When installing in FNAL domain, default collector is FNAL.

* Thu May 17 2007 Christopher Green <greenc@fnal.gov> - 0.22a-2
- re-vamp post to handle FNAL-local collector configurations.

* Thu May 17 2007 Christopher Green <greenc@fnal.gov> - 0.22a-1
- Condor probe now looks in old history files if necessary.
- condor_history check only done once per invocation instead of once per job.

* Wed May  9 2007 Christopher Green <greenc@fnal.gov> - 0.20a-1
- Consolidation release.
- Addition of gLExec probe to suite.
- Yum repository config file.

* Wed Apr  4 2007 Christopher Green <greenc@fnal.gov> - 0.12k-0
- Pre-release for testing and emergency deployment only.

* Fri Feb  9 2007 Chris Green <greenc@fnal.gov> - 0.12i-1
- Fix reported problem with PBS probe.
- Make requested change to maximum backoff delay.

* Fri Feb  9 2007 Chris Green <greenc@fnal.gov> - 0.12h-1
- ResetAndRetry mechanism altered to geometric backoff delay up to 1
  hour.
- Suspension of reprocessing on connect failure now works as desired.
- Reprocessing gets re-done on successful re-connect.
- LICENSE file now part of main pbs-lsf directory as well as the docs.
- URL pointers to TWiki updated to new secure URLs.

* Wed Feb  7 2007 Chris Green <greenc@fnal.gov> - 0.12g-1
- Records now have a ResourceType: batch, rawCPU or storage.
- ResetAndRetry mechanism for continuously-running probes.
- Stats now include failed reprocess attempts.
- New naming scheme for backup files distinguishes different probes
  running on the same node.
- Fix minor internal problems with XML prefix parsing.
- VOName and ReportableVOName keys should not be in the XML record if
  they are empty.
- Preserve type of Record.XmlData

* Fri Feb  2 2007 Chris Green <greenc@fnal.gov> - 0.12f-1
- SGE probe requires python v2.3 or better -- put check in code as well
  as RPM requirements.
- SGE probe now uses DebugPrint instead of straight print.
- Use xml.dom for XML parsing where appropriate.
- Cope with multiple usage records in one XML packet.
- Optional suppression of records with no VOName.
- Python version checking and handling of libraries that behave
  differently in different versions.
- Psacct probe now more intelligent about memory use for large
  accounting files.

* Mon Jan 29 2007 Chris Green <greenc@fnal.gov> - 0.12e-1
- Keep track of suppressed, failed and successfully sent records
  separately.
- Better logging and error output.
- Public ProbeConfiguration.getConfigAttribute(attribute) method.
- New probe for SGE batch system.

* Fri Jan  5 2007 Chris Green <greenc@fnal.gov> - 0.12d-1
- Fix problems with user-vo-name lookup under pbs-lsf.
- Try to be more robust against not finding top of VDT distribution.
- Honor request for crontab to not redirect output; and for crontab line
   to be POSIX-compliant (/ notation for stepping is apparently a
   vixie-cron extension).
- Tweak ProbeConfigTemplate to suppress all but real errors in
  stdout/stderr.

* Thu Jan  4 2007 Chris Green <greenc@fnal.gov> - 0.12c-1
- Fix a couple of bugs affecting pbs-lsf.

* Thu Jan  4 2007 Chris Green <greenc@fnal.gov> - 0.12b-1
- README files now mainly vestigial and refer to TWiki.
- Fix various minor bugs in Gratia.py.
- Fix two annoying (but minor) bugs in condor_history capability check.
- Add db-find-job test script to common package.
- Removed unnecessary Clarens.py.
- Removed README-facct-migration (see TWiki docs for this information).

* Wed Dec 20 2006 Chris Green <greenc@fnal.gov> - 0.12a-1
- Upgrade version to match tag.
- Processing of backlog files is now much more efficient.
- Better handling of large backlog and MaxPendingFiles config option.
- New default value of MaxPendingFiles of 100K.
- Eliminate errors if we exit before full initialization.
- Reprocess is now done as part of initialization.

* Wed Dec 13 2006 Chris Green <greenc@fnal.gov> - 0.11f-2
- Better application of GRAM patches where gratia is not installed under
  $VDT_LOCATION.

* Wed Dec 13 2006 Chris Green <greenc@fnal.gov> - 0.11f-1
- Better correction to GRAM patches.

* Tue Dec 12 2006 Chris Green <greenc@fnal.gov> - 0.11e-1
- Correct GRAM patch problem.
- post install now corrects (but does not install) GRAM patches if appropriate.
- Gratia.py now supports automatic user->VO translation for those probes
  which allow Gratia.py routines to construct the XML (if it can find a
  reverse mapfile). This does not apply to probes which upload a pre-made XML
  blob such as the pbs-lsf probe.
- UserVOMapFile key added to ProbeConfigTemplate.
- Correct patch check.
- Probes don't require *exactly* the same version of the gratia-probe-common
  RPM, so this can be upgraded in isolation if necessary.

* Fri Dec  8 2006 Chris Green <greenc@fnal.gov> - 0.11d-1
- GRAM patches tweaked slightly.
- Gratia.py updated to offer VOfromUser(user) function, returning a
  [ voi, VOc ] pair based on a username -- uses a local copy of the
  grid3-user-vo-map.txt file.

* Mon Nov 20 2006 Chris Green <greenc@fnal.gov> - 0.11b-1
- Improve documentation for GRAM script patches.

* Mon Nov 20 2006 Chris Green <greenc@fnal.gov> - 0.11a-1
- New option UseSyslog.
- New option LogRotate.
- condor.pl only uses -backwards and -match options to condor_history if
  they are supported.
- More robust GRAM patches.

* Thu Oct 19 2006 Chris Green <greenc@fnal.gov> - 0.10c-2
- Change escaping of site_name macro internally for more robustness.

* Thu Oct 19 2006 Chris Green <greenc@fnal.gov> - 0.10c-1
- Remove unnecessary VDTSetup line from psacct ProbeConfig file.
- Remove version no. from README files.
- new doc README-facct-migration for psacct.

* Wed Oct 18 2006 Chris Green <greenc@fnal.gov> - 0.10b-2
- meter_name and site_name are now configurable macros.

* Mon Oct 16 2006 Chris Green <greenc@fnal.gov> - 0.10a-1
- Robustness updates for connection handling.

* Wed Oct 11 2006  <greenc@fnal.gov> - 0.10-1
- Make sure that the end time is correct even when processing more than
one day worth of raw data (PSACCTProbeLib.py).

* Fri Oct  6 2006  <greenc@fnal.gov> - 0.9m-1
- Separate routines out of urCollector into Perl Modules, and use them
in a perl Gratia probe for pbs-lsf.
- Remove gratia-addin patch: call Gratia probe from outside
urCollector.pl and use perl modules to read configuration file.

* Wed Oct  4 2006  <greenc@fnal.gov> - 0.9l-2
- Processor count set to 1 if it's not anything else.

* Wed Oct  4 2006  <greenc@fnal.gov> - 0.9l-1
- urCollector now looks at nodect in addition to neednodes.

* Fri Sep 29 2006  <greenc@fnal.gov> - 0.9k-1
- Add method to Gratia.py to set VOName in the record.
- Remove debug statements printing direct to screen in Gratia.py.
- Disconnect at exit using sys.exitfunc in Gratia.py.
- Remove obsolete reference to jclarens in disconnect debug message in
Gratia.py.

* Fri Sep 22 2006  <greenc@fnal.gov> - 0.9j-1
- Fix problem with StartTime / EndTime in ps-accounting probe.

* Fri Sep 22 2006  <greenc@fnal.gov> - 0.9i-1
- Gratia.py had some strange response code logic for non-default
transaction methods: added automatic setting of code based on message if
supplied code is -1.
- Fix thinko in ProbeConfigTemplate.

* Thu Sep 21 2006  <greenc@fnal.gov> - 0.9h-1
- Turn off soap for non-SSL connections.

* Thu Sep 21 2006  <greenc@fnal.gov> - 0.9g-2
- Add patch to fix timezone problem for createTime in urCollector.pl.

* Wed Sep 20 2006  <greenc@fnal.gov> - 0.9g-1
- Update version number for improved condor probe.
- Only replace MAGIC_VDT_LOCATION in VDTSetup.sh if vdt_loc was
explicitly set.

* Tue Sep 19 2006  <greenc@fnal.gov> - 0.9f-3
- SiteName should be pretty (not the node name), so use OSG_SITE_NAME.

* Mon Sep 18 2006  <greenc@fnal.gov> - 0.9f-2
- Allow for build-time setting of VDT location.
- Set MeterName and SiteName in post for fresh installs.

* Fri Sep 15 2006  <greenc@fnal.gov> - 0.9f-1
- Moved psacct-specific items out of ProbeConfigTemplate and into post.
- Fixed sundry minor problems in psacct_probe.cron.sh: missing export of
PYTHONPATH, typo (psaact -> psacct). Also only attempt to copy old
PSACCT admin file if it exists, and assume gratia/var/data already
exists (in common RPM).
- SOAPHost changes in post need enclosing quotes

* Thu Sep 14 2006  <greenc@fnal.gov> - 0.9e-2
- Correct typo in psacct post-install message.

* Wed Sep 13 2006  <greenc@fnal.gov> - 0.9e-1
- Reprocess() and __disconnect() were at the wrong indent level --
should be outside the loop.

* Wed Sep 13 2006  <greenc@fnal.gov> - 0.9d-2
- Split post-install sections for configuring urCollector.conf and
ProbeConfig.
- Changed jobPerTimeInterval and timeInterval to make catching up on a
backlog much faster.

* Mon Sep 11 2006  <greenc@fnal.gov> - 0.9d-1
- ITB-specific RPMS with preconfigured port.
- Updated README files.
- Replaced as many UNIX commands as possible with %%{__cmd} macros
 
* Fri Sep  8 2006  <greenc@fnal.gov> - 0.9c-2
- Patch to urCollector for parsing corner cases (work with Rosario).

* Wed Sep  6 2006  <greenc@fnal.gov> - 0.9c-1
- New patch for urCollector to invoke gratia probe.
- Gratia.py enhancements to handle pre-made XML files.
- Cron script for pbs-lsf probe.
- Fix preun scripts for hysteresis problem during RPM upgrades.

* Wed Aug 30 2006  <greenc@fnal.gov> - 0.9b-4
- Condor probe should run every 15 minutes, not once per day.

* Tue Aug 29 2006  <greenc@fnal.gov> - 0.9b-3
- Revised doc entries and simplified (!) install section.
- Corrected path in log_to_gratia check in condor post.
- Corrected handling of /etc/rc.d/init.d/gratia-psacct in file list and
post.
- Improved description for pbs-lsf probe.

* Mon Aug 28 2006 <greenc@fnal.gov> - 0.9b-2
- Specfile revised for arch-specific pbs-lsf package adapted from EGEE's
urCollector package. NOTE double build now required with and without
"--target noarch" option

* Wed Aug 23 2006  <greenc@fnal.gov> - 0.9b-1
- Documentation updates
- Minor change to condor_meter.pl from Philippe

* Tue Aug 15 2006  <greenc@fnal.gov> - 0.9a-1
- Initial build.
