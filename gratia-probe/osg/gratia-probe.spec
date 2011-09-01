Name:               gratia-probe
Summary:            Gratia OSG accounting system probes
Group:              Applications/System
Version:            1.09
Release:            0.1.pre
License:            GPL
Group:              Applications/System
URL:                http://sourceforge.net/projects/gratia/
Vendor:             The Open Science Grid <http://www.opensciencegrid.org/>

BuildRequires:      python-devel

BuildRequires: gcc-c++

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

  cp -pR %{noarch_packs}  $RPM_BUILD_ROOT%{_datadir}/gratia

  install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
  for probe in %{noarch_packs}
  do
    # Install the cronjob
    if [ -e $probe/gratia-probe-$probe.cron -o $probe == "bdii-status" -o $probe == "dCache-storage" ]; then
      install -m 644 $probe/*.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
      rm $RPM_BUILD_ROOT%{_datadir}/gratia/$probe/*.cron
    fi

    # Customize template for each probe
    PROBE_DIR=$RPM_BUILD_ROOT/%{_sysconfdir}/gratia/$probe
    install -d $PROBE_DIR
    install -m 644 common/ProbeConfigTemplate.osg $PROBE_DIR/ProbeConfig
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
  install -m 755 dCache-transfer/gratia-dcache-transfer.init $RPM_BUILD_ROOT%{_initrddir}/gratia-dcache-transfer
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-transfer/gratia-dcache-transfer.init

  # Xrootd-storage init script
  install -m 755 "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-storage/gratia-xrootd-storage" "$RPM_BUILD_ROOT%{_initrddir}/gratia-xrootd-storage"
  rm -f "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-storage/gratia-xrootd-storage"

  # Xrootd-transfer init script
  install -m 755 "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-transfer/gratia-xrootd-transfer" "$RPM_BUILD_ROOT%{_initrddir}/gratia-xrootd-transfer"
  rm -f "${RPM_BUILD_ROOT}%{_datadir}/gratia/xrootd-transfer/gratia-xrootd-transfer"

  # gridftp-transfer unneeded file.
  rm -f "${RPM_BUILD_ROOT}%{_datadir}/gratia/gridftp-transfer/GridftpTransferProbe.sh"

  mv $RPM_BUILD_ROOT%{_datadir}/gratia/hadoop-storage/storage.cfg \
     $RPM_BUILD_ROOT%{_sysconfdir}/gratia/hadoop-storage/storage.cfg

%else

  # PBS / LSF probe install
  cp -pR pbs-lsf $RPM_BUILD_ROOT%{_datadir}/gratia/
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/urCollector-src
  PROBE_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/gratia/pbs-lsf
  install -d $PROBE_DIR
  cp -p common/ProbeConfigTemplate.osg $PROBE_DIR/ProbeConfig
  echo "%{ProbeConfig_template_marker}" >> $PROBE_DIR/ProbeConfig

  sed -i -e "s#@PROBE_NAME@#$probe#" $PROBE_DIR/ProbeConfig

  endpoint=%{osg_collector}:%{default_collector_port}
  sed -i -e "s#@COLLECTOR_ENDPOINT@#$endpoint#" \
         -e "s#@SSL_ENDPOINT@#%{osg_collector}:%{ssl_port}#" \
         -e "s#@SSL_REGISTRATION_ENDPOINT@#$endpoint#" \
        $PROBE_DIR/ProbeConfig

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
  install -m 644 pbs-lsf/gratia-probe-pbs-lsf.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/*.cron
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

  # Remove test cruft
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/test
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

# Install condor configuration snippet
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d
install -m 644 condor/99_gratia.conf $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d/99_gratia.conf
rm $RPM_BUILD_ROOT%{_datadir}/gratia/condor/99_gratia.conf

# Remove the test stuff
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/condor/test
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/sge/test
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/test

# Remove remaining cruft
rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia.repo
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/gratia/common
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/condor/gram_mods
rm     $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-storage/SL4_init_script_patches
rm     $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-transfer/SL4_init_script_patches
rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/GRAM
rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/ProbeConfigTemplate.osg
rm     $RPM_BUILD_ROOT%{python_sitelib}/gratia/common/samplemeter.py
rm     $RPM_BUILD_ROOT%{python_sitelib}/gratia/common/samplemeter_multi.py
%endif

install -d $RPM_BUILD_ROOT/%{_localstatedir}/log/gratia

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
Requires: netlogger 
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
* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.08-0.1.pre
- Reset changelog for pre-release of new packaging

