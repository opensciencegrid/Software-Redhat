Name:               gratia-probe
Summary:            Gratia OSG accounting system probes
Group:              Applications/System
Version:            1.14.2
Release:            3%{?dist}

License:            GPL
Group:              Applications/System
URL:                http://sourceforge.net/projects/gratia/
Vendor:             The Open Science Grid <http://www.opensciencegrid.org/>

BuildRequires:      python-devel

BuildRequires: gcc-c++

%define default_prefix /usr/share

# Default probe configuration items for post-install.
%global default_collector_port 80
%global metric_port 8880
%global ssl_port 443

%global osg_collector gratia-osg-prod.opensciencegrid.org
%global osg_transfer_collector gratia-osg-transfer.opensciencegrid.org
%global osg_metric_collector rsv.grid.iu.edu
%global enstore_collector dmscollectorgpvm01.fnal.gov

# Default ProbeName
%{!?meter_name: %global meter_name `hostname -f`}

%define customize_probeconfig(d:) sed -i "s#@PROBE_HOST@#%{meter_name}#" %{_sysconfdir}/gratia/%{-d*}/ProbeConfig

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

########################################################################
# Source and patch specifications
Source0:  %{name}-common-%{version}.tar.bz2
Source1:  %{name}-condor-%{version}.tar.bz2
Source2:  %{name}-psacct-%{version}.tar.bz2
Source3:  %{name}-pbs-lsf-%{version}.tar.bz2
Source5:  %{name}-sge-%{version}.tar.bz2
Source6:  %{name}-glexec-%{version}.tar.bz2
Source7:  %{name}-metric-%{version}.tar.bz2
Source8:  %{name}-dCache-transfer-%{version}.tar.bz2
Source9:  %{name}-dCache-storage-%{version}.tar.bz2
Source10: %{name}-gridftp-transfer-%{version}.tar.bz2
Source11: %{name}-services-%{version}.tar.bz2
Source12: %{name}-hadoop-storage-%{version}.tar.bz2
Source13: %{name}-condor-events-%{version}.tar.bz2
Source14: %{name}-xrootd-transfer-%{version}.tar.bz2
Source15: %{name}-xrootd-storage-%{version}.tar.bz2
Source16: %{name}-bdii-status-%{version}.tar.bz2
Source17: %{name}-onevm-%{version}.tar.bz2
Source18: %{name}-slurm-%{version}.tar.bz2
Source19: %{name}-common2-%{version}.tar.bz2
Source20: %{name}-enstore-transfer-%{version}.tar.bz2
Source21: %{name}-enstore-storage-%{version}.tar.bz2
Source22: %{name}-enstore-tapedrive-%{version}.tar.bz2
Source23: %{name}-dCache-storagegroup-%{version}.tar.bz2
Source24:  %{name}-lsf-%{version}.tar.bz2


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
%setup -q -D -T -a 8
%setup -q -D -T -a 9
%setup -q -D -T -a 10
%setup -q -D -T -a 11
%setup -q -D -T -a 12
%setup -q -D -T -a 13
%setup -q -D -T -a 14
%setup -q -D -T -a 15
%setup -q -D -T -a 16
%setup -q -D -T -a 17
%setup -q -D -T -a 18 
%setup -q -D -T -a 19
%setup -q -D -T -a 20
%setup -q -D -T -a 21
%setup -q -D -T -a 22
%setup -q -D -T -a 23
%setup -q -D -T -a 24

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

%define noarch_packs common condor psacct sge glexec metric dCache-transfer dCache-storage gridftp-transfer services hadoop-storage condor-events xrootd-transfer xrootd-storage bdii-status onevm slurm common2 enstore-storage enstore-transfer enstore-tapedrive dCache-storagegroup lsf

  # PWD is the working directory, used to build
  # $RPM_BUILD_ROOT%{_datadir} are the files to package
  cp -pR %{noarch_packs}  $RPM_BUILD_ROOT%{_datadir}/gratia

  install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
  install -d $RPM_BUILD_ROOT%{python_sitelib}
  mv common/gratia $RPM_BUILD_ROOT%{python_sitelib}
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia

  for probe in %{noarch_packs}
  do
    # Install the cronjob
    if [ -e $probe/gratia-probe-$probe.cron -o $probe == "dCache-storage" -o $probe == "dCache-storagegroup" ]; then
      # wildcards not working in this test: if [ -e "$probe/gratia-probe-*.cron" ]; then
      install -m 644 $probe/*.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
      rm $RPM_BUILD_ROOT%{_datadir}/gratia/$probe/*.cron
    fi

    # Install the python modules
    if [ -e $probe/gratia ]; then
      mv $probe/gratia/* $RPM_BUILD_ROOT%{python_sitelib}/gratia
      rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/$probe/gratia
    fi

    # Common template customizations (same for all probes)
    PROBE_DIR=$RPM_BUILD_ROOT/%{_sysconfdir}/gratia/$probe
    install -d $PROBE_DIR
    install -m 644 common/ProbeConfigTemplate.osg $PROBE_DIR/ProbeConfig
    ln -s %{_sysconfdir}/gratia/$probe/ProbeConfig $RPM_BUILD_ROOT/%{_datadir}/gratia/$probe/ProbeConfig

    ## Probe-specific customizations
    # Probe template addon lines in ProbeConfig.add (in probe directory) added before @PROBE_SPECIFIC_DATA@ tag
    if [ -e "$probe/ProbeConfig.add" ]; then
      sed -i.bck "/@PROBE_SPECIFIC_DATA@/ {
          h
          r $probe/ProbeConfig.add
          g
          N
          }" "$PROBE_DIR/ProbeConfig"
      rm "$RPM_BUILD_ROOT%{_datadir}/gratia/$probe/ProbeConfig.add"
      rm "$PROBE_DIR/ProbeConfig.bck"
    fi

    # Collector strings
    if [ $probe == "enstore-*" -o $probe == "dCache-storagegroup" ]; then
      # must be first to catch enstrore-transfer/storage
      endpoint=%{enstore_collector}:%{default_collector_port}
      ssl_endpoint=%{enstore_collector}:%{ssl_port}
    elif [ $probe == "*-transfer" -o $probe == "*-storage" ]; then
      endpoint=%{osg_transfer_collector}:%{default_collector_port}
      ssl_endpoint=%{osg_transfer_collector}:%{ssl_port}
    elif [ $probe == metric ]; then
      endpoint=%{osg_metric_collector}:%{metric_port}
      ssl_endpoint=%{osg_metric_collector}:%{ssl_port}
    else
      endpoint=%{osg_collector}:%{default_collector_port}
      ssl_endpoint=%{osg_collector}:%{ssl_port}
    fi
    sed -i -e "s#@PROBE_NAME@#$probe#" \
           -e "s#@COLLECTOR_ENDPOINT@#$endpoint#" \
           -e "s#@SSL_ENDPOINT@#$ssl_endpoint#" \
           -e "s#@SSL_REGISTRATION_ENDPOINT@#$endpoint#" \
        $PROBE_DIR/ProbeConfig

    # Other Probe-specific customizations
    if [ $probe == "psacct" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#PSACCTFileRepository="/var/lib/gratia/account/" \
    PSACCTBackupFileRepository="/var/lib/gratia/backup/" \
    PSACCTExceptionsRepository="/var/log/gratia/exceptions/"#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "sge" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#SGEAccountingFile=""#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "glexec" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#gLExecMonitorLog="/var/log/messages"#' $PROBE_DIR/ProbeConfig
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
    elif [ $probe == "slurm" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#SlurmDbHost="db.cluster.example.edu" \
    SlurmDbPort="3306" \
    SlurmDbUser="slurm" \
    SlurmDbPasswordFile="/etc/gratia/slurm/pwfile" \
    SlurmDbName="slurm_acct_db" \
    SlurmCluster="mycluster"#' $PROBE_DIR/ProbeConfig
    elif [ $probe == "condor" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#NoCertinfoBatchRecordsAreLocal="0"#' $PROBE_DIR/ProbeConfig
    else
      sed -i -e 's#@PROBE_SPECIFIC_DATA@##' $PROBE_DIR/ProbeConfig
    fi

    # Remove cruft
    # dev and test directories
    [ -d "$RPM_BUILD_ROOT%{_datadir}/gratia/$probe/dev" ] && rm -rf "$RPM_BUILD_ROOT%{_datadir}/gratia/$probe/dev"
    [ -d "$RPM_BUILD_ROOT%{_datadir}/gratia/$probe/test" ] && rm -rf "$RPM_BUILD_ROOT%{_datadir}/gratia/$probe/test"

  done

  # Remove unnecessary links
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/condor/ProbeConfig
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/gridftp-transfer/ProbeConfig
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/glexec/ProbeConfig

  # common probe init script
  install -d $RPM_BUILD_ROOT/%{_initrddir}
  install -p -m 755 common/gratia-probes-cron.init $RPM_BUILD_ROOT%{_initrddir}/gratia-probes-cron
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia-probes-cron.init

  # dCache-transfer init script
  install -d $RPM_BUILD_ROOT/%{_initrddir}
  install -m 755 dCache-transfer/gratia-dcache-transfer.init $RPM_BUILD_ROOT%{_initrddir}/gratia-dcache-transfer
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-transfer/gratia-dcache-transfer.init

  # Xrootd-storage init script
  install -m 755 $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-storage/gratia-xrootd-storage.init $RPM_BUILD_ROOT%{_initrddir}/gratia-xrootd-storage
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-storage/gratia-xrootd-storage.init

  # Xrootd-transfer init script
  install -m 755 $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-transfer/gratia-xrootd-transfer.init $RPM_BUILD_ROOT%{_initrddir}/gratia-xrootd-transfer
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-transfer/gratia-xrootd-transfer.init

  # psacct init script
  install -m 755 $RPM_BUILD_ROOT%{_datadir}/gratia/psacct/gratia-psacct $RPM_BUILD_ROOT%{_initrddir}/gratia-psacct
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/psacct/gratia-psacct

  mv $RPM_BUILD_ROOT%{_datadir}/gratia/hadoop-storage/storage.cfg \
     $RPM_BUILD_ROOT%{_sysconfdir}/gratia/hadoop-storage/storage.cfg

  install -d $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM
  install -m 644 $RPM_BUILD_ROOT%{_datadir}/gratia/common/GRAM/JobManagerGratia.pm $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManagerGratia.pm

  # Install condor configuration snippet
  install -d $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d
  install -m 644 condor/99_gratia.conf $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d/99_gratia.conf
  install -m 644 condor/99_gratia-gwms.conf $RPM_BUILD_ROOT/%{_sysconfdir}/condor/config.d/99_gratia-gwms.conf
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/condor/99_gratia.conf
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/condor/99_gratia-gwms.conf

  # Remove the test stuff
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/condor/test
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/sge/test
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/test
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-storage/test.xml

  # Remove remaining cruft
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia.repo
  rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/gratia/common
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/condor/gram_mods
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/GRAM
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/ProbeConfigTemplate.osg
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/samplemeter.py
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/samplemeter.pl
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/samplemeter_multi.py
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/ProbeConfig
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/metric/samplemetric.py
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/xrootd-transfer/gratia-xrootd-transfer-alt
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-storagegroup/ProbeConfig.example
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common2/ProbeConfig
  rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/gratia/common2
  # TODO: allow test directory, remove from RPM

  # Set up var area
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/{tmp,data,data/quarantine,logs}
  chmod 1777  $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/data

%else

  # PBS / LSF probe
  PROBE_DIR=$RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf
  PROBE_ETC_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/gratia/pbs-lsf
  install -d -m 0755 $PROBE_DIR/urCollector
  install -d -m 0755 $PROBE_ETC_DIR
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/pbs-lsf/{lock,tmp/urCollector}
  install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/

  # Install Gratia executables and urCollector software
  install -m 0644 pbs-lsf/README $PROBE_DIR/README
  install -m 0755 pbs-lsf/{pbs-lsf,pbs-lsf_meter.cron.sh,pbs-lsf_meter.pl} $PROBE_DIR/
  pushd pbs-lsf/urCollector-src
    install -m 0755 urCreator urCollector.pl $PROBE_DIR
    install -m 0644 LICENSE $PROBE_DIR
    install -d -m 0755 $RPM_BUILD_ROOT%{perl_vendorlib}/urCollector/
    install -m 0644 urCollector/{Common,Configuration}.pm $RPM_BUILD_ROOT%{perl_vendorlib}/urCollector/
  popd

  # ProbeConfig customization
  install -m 0644 common/ProbeConfigTemplate.osg $PROBE_ETC_DIR/ProbeConfig
  install -m 0644 pbs-lsf/urCollector-src/urCollector.conf-template $PROBE_ETC_DIR/urCollector.conf
  endpoint=%{osg_collector}:%{default_collector_port}
  sed -i -e "s#@COLLECTOR_ENDPOINT@#$endpoint#" \
         -e "s#@SSL_ENDPOINT@#%{osg_collector}:%{ssl_port}#" \
         -e "s#@SSL_REGISTRATION_ENDPOINT@#$endpoint#" \
         -e 's#@PROBE_SPECIFIC_DATA@##' \
         -e "s#@PROBE_NAME@#pbs-lsf#" \
        $PROBE_ETC_DIR/ProbeConfig
  install -m 644 pbs-lsf/gratia-probe-pbs-lsf.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
  ln -sf %{_sysconfdir}/gratia/pbs-lsf/ProbeConfig $PROBE_DIR/ProbeConfig
  ln -s %{_sysconfdir}/gratia/pbs-lsf/urCollector.conf $PROBE_DIR/urCollector.conf

  # Remove test cruft
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/pbs-lsf/test

%endif

# Burn in the RPM version into the python files.
grep -rIle '%%%%%%RPMVERSION%%%%%%' $RPM_BUILD_ROOT%{_datadir}/gratia $RPM_BUILD_ROOT%{python_sitelib} | while read file; do \
  perl -wpi.orig -e 's&%%%%%%RPMVERSION%%%%%%&%{version}-%{release}&g' "$file" && \
    rm -fv "$file.orig"
done

install -d $RPM_BUILD_ROOT/%{_localstatedir}/log/gratia
install -d $RPM_BUILD_ROOT/%{_localstatedir}/lock/gratia

%clean
rm -rf $RPM_BUILD_ROOT

%description
Probes for the Gratia OSG accounting system

%ifnarch noarch

%package pbs-lsf
Summary: Gratia OSG accounting system probe for PBS and LSF batch systems.
Group: Applications/System
Requires: %{name}-common >= 0.12f
License: See LICENSE.

%description pbs-lsf
Gratia OSG accounting system probe for PBS and LSF batch systems.

This product includes software developed by The EU EGEE Project
(http://cern.ch/eu-egee/).

%post pbs-lsf
%customize_probeconfig -d pbs-lsf

%files pbs-lsf
%defattr(-,root,root,-)
%dir %{_localstatedir}/lib/gratia/pbs-lsf/lock
%doc %{_datadir}/gratia/pbs-lsf/LICENSE
%doc %{_datadir}/gratia/pbs-lsf/README
%dir %{_datadir}/gratia/pbs-lsf
%{_datadir}/gratia/pbs-lsf/ProbeConfig
%{_datadir}/gratia/pbs-lsf/urCollector.conf
%{_datadir}/gratia/pbs-lsf/pbs-lsf_meter.cron.sh
%{_datadir}/gratia/pbs-lsf/pbs-lsf_meter.pl
%{_datadir}/gratia/pbs-lsf/pbs-lsf
%{_datadir}/gratia/pbs-lsf/urCreator
%{_datadir}/gratia/pbs-lsf/urCollector.pl
%{perl_vendorlib}/urCollector/Common.pm
%{perl_vendorlib}/urCollector/Configuration.pm
%config(noreplace) %{_sysconfdir}/gratia/pbs-lsf/urCollector.conf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/pbs-lsf/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-pbs-lsf.cron

%else

%package common
Summary: Common files for Gratia OSG accounting system probes
Group: Applications/System
Requires: pyOpenSSL
Requires(post): chkconfig
Requires(preun): chkconfig

%description common
Common files and examples for Gratia OSG accounting system probes.

%pre common
getent group gratia >/dev/null || groupadd -r gratia
getent passwd gratia >/dev/null || \
       useradd -r -g gratia -c "gratia runtime user" \
       -s /sbin/nologin -d /etc/gratia gratia
%post 
/sbin/chkconfig --add gratia-probes-cron

%preun
if [ $1 = 0 ] ; then
     /sbin/service gratia-probes-cron stop >/dev/null 2>&1
     /sbin/chkconfig --del gratia-probes-cron
fi

%files common
%defattr(-,root,root,-)
%{_initrddir}/gratia-probes-cron
%doc %{default_prefix}/gratia/common/README
%{_localstatedir}/lib/gratia/
%attr(-,gratia,gratia) %{_localstatedir}/log/gratia/
%dir %{_sysconfdir}/gratia
%{_localstatedir}/lock/gratia/
%{python_sitelib}/gratia/__init__.py*
%{python_sitelib}/gratia/common
%dir %{default_prefix}/gratia/common
%{default_prefix}/gratia/common/GratiaPing
%{default_prefix}/gratia/common/DebugPrint
%{default_prefix}/gratia/common/GetProbeConfigAttribute
%{default_prefix}/gratia/common/ProbeConfigTemplate
%{default_prefix}/gratia/common/cron_check

# %description common2
# Common files and examples for Gratia OSG accounting system probes. Version 2.

# %files common2
# %defattr(-,root,root,-)
%{_initrddir}/gratia-probes-cron
#%doc common2/README
%doc %{default_prefix}/gratia/common2/README
%{_localstatedir}/lib/gratia/
%attr(-,gratia,gratia) %{_localstatedir}/log/gratia/
%dir %{_sysconfdir}/gratia
%{_localstatedir}/lock/gratia/
# this is in common: %{python_sitelib}/gratia/__init__.py*
%{python_sitelib}/gratia/common2
# executables:
%dir %{default_prefix}/gratia/common2
# %{default_prefix}/gratia/common2/alarm.py
# %{default_prefix}/gratia/common2/checkpoint.py
# %{default_prefix}/gratia/common2/uuid_replacement.py
# %{default_prefix}/gratia/common2/meter.py
# %{default_prefix}/gratia/common2/pginput.py
# %{default_prefix}/gratia/common2/probeinput.py

%package gram
Summary: GRAM extensions for Gratia OSG accounting system
Group: Applications/System

%description gram
%{summary}

%files gram
%{perl_vendorlib}/Globus/GRAM/JobManagerGratia.pm

%package psacct
Summary: A ps-accounting probe
Group: Applications/System
Requires: psacct
Requires: %{name}-common >= 0.12f

%description psacct
The psacct probe for the Gratia OSG accounting system.

%files psacct
%defattr(-,root,root,-)
%doc psacct/README
%doc %{default_prefix}/gratia/psacct/README
%dir %{default_prefix}/gratia/psacct
%{default_prefix}/gratia/psacct/ProbeConfig
%config %{default_prefix}/gratia/psacct/psacct_probe.cron.sh
%{default_prefix}/gratia/psacct/PSACCTProbe
%{python_sitelib}/gratia/psacct
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/psacct/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-psacct.cron
%config %{_initrddir}/gratia-psacct

%post psacct

# Configure boot-time activation of accounting.
/sbin/chkconfig --add gratia-psacct

%customize_probeconfig -d psacct

%package condor
Summary: A Condor probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: condor

%description condor
The Condor probe for the Gratia OSG accounting system.

%files condor
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/condor/README
%dir %{default_prefix}/gratia/condor
%{default_prefix}/gratia/condor/condor_meter
%config(noreplace) %{_sysconfdir}/condor/config.d/99_gratia.conf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/condor/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-condor.cron

%post condor
%customize_probeconfig -d condor

%package glideinwms
Summary: Configuration for Gratia GlideinWMS integration.
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-condor >= %{version}-%{release}

%description glideinwms
The Condor probe for the Gratia OSG accounting system.

%files glideinwms
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/condor/config.d/99_gratia-gwms.conf



%package sge
Summary: An SGE probe
Group: Applications/System
%if %{?python:0}%{!?python:1}
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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/sge/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-sge.cron

%post sge
%customize_probeconfig -d sge

%package glexec
Summary: A gLExec probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires:  /usr/bin/grid-proxy-info

%description glexec
The gLExec probe for the Gratia OSG accounting system.

%files glexec
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/glexec/README
%{default_prefix}/gratia/glexec/glexec_meter.cron.sh
%{default_prefix}/gratia/glexec/glexec_meter
%{python_sitelib}/gratia/glexec
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-glexec.cron
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/glexec/ProbeConfig

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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/metric/ProbeConfig

%post metric
%customize_probeconfig -d metric

%package dcache-transfer
Summary: Gratia OSG accounting system probe for dCache billing.
Group: Applications/System
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
%{python_sitelib}/gratia/dcache_transfer
%dir %{default_prefix}/gratia/dCache-transfer
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/dCache-transfer/ProbeConfig

%post dcache-transfer
/sbin/chkconfig --add gratia-dcache-transfer
%customize_probeconfig -d dCache-transfer

%package dcache-storage
Summary: Gratia OSG accounting system probe for dCache storage.
Group: Applications/System
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
%{python_sitelib}/gratia/dcache_storage
%dir %{default_prefix}/gratia/dCache-storage
%{default_prefix}/gratia/dCache-storage/ProbeConfig
%{default_prefix}/gratia/dCache-storage/create_se_record.xsl
%{default_prefix}/gratia/dCache-storage/dCache-storage_meter.cron.sh
%{default_prefix}/gratia/dCache-storage/dCache_storage_probe
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/dCache-storage/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-dCache-storage.cron

%post dcache-storage
%customize_probeconfig -d dCache-storage

%package gridftp-transfer
Summary: Gratia OSG accounting system probe for gridftp transfers.
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: netlogger 
License: See LICENSE.

%description gridftp-transfer
Gratia OSG accounting system probe for available space in dCache.
Contributed by Andrei Baranovski of the OSG storage team.

%files gridftp-transfer
%defattr(-,root,root,-)
%{python_sitelib}/gratia/gridftp_transfer
%dir %{default_prefix}/gratia/gridftp-transfer
%{default_prefix}/gratia/gridftp-transfer/GridftpTransferProbeDriver
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/gridftp-transfer/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-gridftp-transfer.cron

%post gridftp-transfer
%customize_probeconfig -d gridftp-transfer

%package services
Summary: Gratia OSG accounting system probe API for services.
Group: Applications/System
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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/services/ProbeConfig

%post services
%customize_probeconfig -d services

%package hadoop-storage
Summary: HDFS Storage Probe for Gratia OSG accounting system.
Group: Applications/System
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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/hadoop-storage/ProbeConfig
%config(noreplace) %{_sysconfdir}/gratia/hadoop-storage/storage.cfg
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-hadoop-storage.cron

%post hadoop-storage
%customize_probeconfig -d hadoop-storage

%package condor-events
Summary: Probe that emits a record for each event in the Condor system.
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
License: See LICENSE.

%description condor-events
Condor Events Probe for Gratia OSG accounting system.
Contributed by University of Nebraska Lincoln.

%files condor-events
%defattr(-,root,root,-)
%{_datadir}/gratia/condor-events/watchCondorEvents
%{_datadir}/gratia/condor-events/ProbeConfig
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/condor-events/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-condor-events.cron

%post condor-events
%customize_probeconfig -d condor-events

%package xrootd-transfer
Summary: Probe that emits a record for each file transfer in Xrootd.
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
License: See LICENSE.

%description xrootd-transfer
Xrootd Transfer Probe for Gratia OSG accounting system.
Contributed by University of Nebraska Lincoln.

%files xrootd-transfer
%defattr(-,root,root,-)
%{_initrddir}/gratia-xrootd-transfer
%{default_prefix}/gratia/xrootd-transfer/gratia-xrootd-transfer
%{default_prefix}/gratia/xrootd-transfer/ProbeConfig
%dir %{default_prefix}/gratia/xrootd-transfer
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/xrootd-transfer/ProbeConfig

%post xrootd-transfer
%customize_probeconfig -d xrootd-transfer

%package xrootd-storage
Summary: Gratia probe to monitor Xrootd storage usage.
Group: Applications/System
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
%{default_prefix}/gratia/xrootd-storage/gratia-xrootd-storage
%{default_prefix}/gratia/xrootd-storage/ProbeConfig
%dir %{default_prefix}/gratia/xrootd-storage
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/xrootd-storage/ProbeConfig

%post xrootd-storage
%customize_probeconfig -d xrootd-storage

%package bdii-status
Summary: Probes that emits records of BDII status
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services >= %{version}-%{release}
Requires: /usr/bin/ldapsearch
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
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/bdii-status/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-bdii-status.cron

%post bdii-status
%customize_probeconfig -d bdii-status

%package onevm
Summary: Gratia OSG accounting system probe for OpenNebula VM accounting.
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: ruby
License: See LICENSE.

%description onevm
Gratia OSG accounting system probe for providing VM accounting.

%files onevm
%defattr(-,root,root,-)
%{python_sitelib}/gratia/onevm
%{default_prefix}/gratia/onevm/onevm_probe.cron.sh
%dir %{default_prefix}/gratia/onevm
%{default_prefix}/gratia/onevm/ProbeConfig
%{default_prefix}/gratia/onevm/VMGratiaProbe
%{default_prefix}/gratia/onevm/query_one_lite.rb

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/onevm/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-onevm.cron

%post onevm
%customize_probeconfig -d onevm


%package slurm
Summary: A SLURM probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: slurm
Requires: MySQL-python
BuildRequires: python-devel
License: See LICENSE.

%description slurm
The SLURM probe for the Gratia OSG accounting system.

%files slurm
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/slurm/README.html
%dir %{default_prefix}/gratia/slurm
%{default_prefix}/gratia/slurm/SlurmProbe.py*
%{default_prefix}/gratia/slurm/slurm_meter
%{default_prefix}/gratia/slurm/slurm_meter_running
%{default_prefix}/gratia/slurm/ProbeConfig

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/slurm/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-slurm.cron

%post slurm
%customize_probeconfig -d slurm

# lsf probe, following the new format

%package lsf
Summary: A LSF probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
# Requires: lsf (can get the version form the configuration)
BuildRequires: python-devel
License: See LICENSE.

%description lsf
The alternative LSF probe for the Gratia OSG accounting system.

%files lsf
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/lsf/README
%dir %{default_prefix}/gratia/lsf
%{python_sitelib}/gratia/lsf
%{default_prefix}/gratia/lsf/lsf
%{default_prefix}/gratia/lsf/ProbeConfig

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/lsf/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-lsf.cron

%post lsf
%customize_probeconfig -d lsf


# Enstore probes: enstore-transfer, enstore-storage, enstore-tapedrive

%package enstore-transfer
Summary: Enstore transfer probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: python-psycopg2
BuildRequires: python-devel
License: See LICENSE.

%description enstore-transfer
The Enstore transfer probe for the Gratia OSG accounting system.

%files enstore-transfer
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/enstore-transfer/README.html
%dir %{default_prefix}/gratia/enstore-transfer
%{default_prefix}/gratia/enstore-transfer/enstore-transfer

%{default_prefix}/gratia/enstore-transfer/ProbeConfig
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/enstore-transfer/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-enstore-transfer.cron

%post enstore-transfer
%customize_probeconfig -d enstore-transfer

%package enstore-storage
Summary: Enstore storage probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services >= %{version}-%{release}
Requires: python-psycopg2
BuildRequires: python-devel
License: See LICENSE.

%description enstore-storage
The Enstore storage probe for the Gratia OSG accounting system.

%files enstore-storage
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/enstore-storage/README.html
%dir %{default_prefix}/gratia/enstore-storage
%{default_prefix}/gratia/enstore-storage/enstore-storage

%{default_prefix}/gratia/enstore-storage/ProbeConfig
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/enstore-storage/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-enstore-storage.cron

%post enstore-storage
%customize_probeconfig -d enstore-storage

%package enstore-tapedrive
Summary: Enstore tapedrive probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services >= %{version}-%{release}
Requires: python-psycopg2
BuildRequires: python-devel
License: See LICENSE.

%description enstore-tapedrive
The Enstore tape drive probe for the Gratia OSG accounting system.

%files enstore-tapedrive
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/enstore-tapedrive/README.html
%dir %{default_prefix}/gratia/enstore-tapedrive
%{default_prefix}/gratia/enstore-tapedrive/enstore-tapedrive

%{default_prefix}/gratia/enstore-tapedrive/ProbeConfig
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/enstore-tapedrive/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-enstore-tapedrive.cron

%post enstore-tapedrive
%customize_probeconfig -d enstore-tapedrive

# dCache storagegroup

%package dcache-storagegroup
Summary: dCache storagegroup probe
Group: Applications/System
Requires: %{name}-common >= %{version}-%{release}
Requires: %{name}-services >= %{version}-%{release}
Requires: python-psycopg2
BuildRequires: python-devel
License: See LICENSE.

%description dcache-storagegroup
The dCache storagegroup probe for the Gratia OSG accounting system.

%files dcache-storagegroup
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/dCache-storagegroup/README.html
%dir %{default_prefix}/gratia/dCache-storagegroup
%{default_prefix}/gratia/dCache-storagegroup/dcache-storagegroup

%{default_prefix}/gratia/dCache-storagegroup/ProbeConfig
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/dCache-storagegroup/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-dcache-storagegroup.cron

%post dcache-storagegroup
%customize_probeconfig -d dCache-storagegroup



%endif # noarch

%changelog
* Tue May 26 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.14.2-3
- rename gratia-probe-dCache-storagegroup to all-lowercase
- include common2 library in gratia-probe-common

* Fri May 1 2015 Marco Mambelli <marcom@fnal.gov> - 1.14.2-2
- fixed possible deadlock in enstore-tapedrive when dismount is lost and tape not used
- cleaned up code and docstrings to produce sphinx documentation 
- added script for local deployment to generate probe documentation via sphinx
- added to the repo a script to help rcover lsf quarantined files
 
* Thu Apr 30 2015 Marco Mambelli <marcom@fnal.gov> - 1.14.2-1
- added option to force manual execution also when a probe is disabled in the config file
- changed enstore-storage to support also fetching of current usage data 
- fixes to checkpoint for Enstore probes (GRATIA-173, GRATIA-174)
- fixed lsf probe to use start time in GlobalID (like pbs-lsf) and not handle correctly config file

* Tue Apr 21 2015 Kevin Retzke <kretzke@fnal.gov> - 1.14.1-1
- renamed dCache-storagegroup probe to all lowercase (GRATIA-172)
- added LogFileName option (GRATIA-165)
- missing HTCondor PER_JOB_HISTORY_DIR demoted to warning, not stopping the probe

* Tue Mar 24 2015 Marco Mambelli <marcom@fnal.gov> - 1.14.0-1
- merging of sample-probe branch into trunk. sample-probe development started in Summer 2014
- new common files in common2 module (base classes for probes)
- Adding dCache storagegroup probe
- Adding Enstore probes: transfer, storage, tape drive
- Adding LSF python probe 

* Mon Nov 3 2014 Marco Mambelli <marcom@fnal.gov> - 1.13.31-1
- Changed logic reporting VOName (GRATIA-156)
- certinfo files not checked for transfer probes (GRATIA-159)
- dCache transfer scalability improved (GRATIA-159)

* Tue Jul 15 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.13.30-3
- Fix syntax error in condor_meter

* Thu Jul 10 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.13.30-2
- Set NoCertinfoBatchRecordsAreLocal="0" by default (GRATIA-149)

* Thu Jul 10 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.13.30-1
- Bugfix for condor grid jobs incorrectly interpreted as Local (GRATIA-149)

* Tue Jun 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.13.29-1
- Bugfix for hadoop storage probe (GRATIA-137)

* Tue May 27 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.13.28-1
- Fix SGE probe startup check for other running pid (GRATIA-144)
- Update hadoop storage probe to use hadoop2 commands/paths (GRATIA-137)
- Disable globbing when removing unused certinfo files (GRATIA-140)

* Mon May 12 2014 Marco Mambelli <marcom@fnal.gov> -  1.13.27-1
- Fix for job probes not deleting certinfo files (GRATIA-140)

* Fri May 02 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.13.26-1
- Fix for pbs probe not detecting cores correctly (GRATIA-136)

* Wed Mar 19 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.13.25-1
- New version of SGE probe with support for log rotation (GRATIA-120)
- Fix for condor probe not deleting dagman job history (GRATIA-130)
- Fix for lsf probe reporting wrong cpu time (GRATIA-133)

* Fri Feb 7 2014 Tanya Levshina <tlevshin@fnal.gov> - 1.13.24-1
- Another attempt by Suchandra to fix GRATIA-111
- Also a fix for GRATIA-132

* Tue Feb 4 2014 Tanya Levshina <tlevshin@fnal.gov> - 1.13.23-1
- Suchandra's fixes for GRATIA-111
- Tanya's change of DebugLevel in psacct GRATIA-113
- Tanya's onevm changes for opennebula 4.4

* Sun Jan 26 2014 Tanya Levshina <tlevshin@fnal.gov> - 1.13.22-1
- Marco, Suchandra fixed double parsing regex (GRATIA-123)
- Suchandra added python's path comparision to verify that PER_JOB_HISTORY and DataFolder  are the same (GRATIA-126)

* Fri Jan 17 2014 Tanya Levshina <tlevshin@fnal.gov> - 1.13.21-1
- John/Derek fixes for slurm probe (SOFTWARE-1321/GRATIA-125,GRATIA-118,GRATIA-127)

* Wed Dec 11 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.20-1
- Suchandra's fixes for xml_utils.py(Fix certinfo patch to handle cases where vo_info is reset to None or isn't set at all)

* Fri Dec 6 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.19-1
- Disable certinfo* check for probes that do not need it (GRATIA-111)
- Add mapping options for gratia-dcache-transfer GRATIA-101
- Fixed deletion of old files from quarantine subdirectories
- Set limit on version length: GRATIA-128

* Fri Sep 20 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.18-1
- Add minor modification to log message related to invalid cpu duration (pbs-lsf and condor)

* Thu Sep 19 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.17-1
- Fix pbs-lsf probe - set to 0 CPUUserDuration if the value is too high (GRATIA-119)
- Add logging of invalid record with CPUSystem duration too high (SOFTWARE-1207)
- Add slurm patch provided by John Thiltges related to (GRATIA-118)
- Fix DebugPrint bug found by Matyas Selmeci (GRATIA-122)

* Wed Aug 9 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.16-1
- Fix psacct for sl6 (GRATIA-115)

* Wed Jul 31 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.15-1
- New patch to deal with condor problems (GRATIA-114/SOFTWARE-1132)

* Wed Jul 26 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.14-1
- Fixed typo in condor_meter , also fixed check for condor_setup GRATIA-110 ; all by Suchandra

* Wed Jul 26 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.13-1
- Temporary fix for condor_meter probe - (GRATIA-114/SOFTWARE-1132), condor ticket https://htcondor-wiki.cs.wisc.edu/index.cgi/tktview?tn=3814

* Wed Jul 3 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.12-1
- Fixed glexec probe bug GRATIA-99/SOFTWARE-1111

* Thu Jun 6 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.11-1
- Suchandra's fix for pbs probe efficiency SOFTWARE-1032 

* Tue Jun 4 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.10-2
- create /var/lib/data/quarantine directory

* Wed May 29 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.10-1
Have to modify ProbeConfigTemplate.osg
* Tue May 28 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.9-1
Added directory under quarantine

* Mon May 21 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.8-1
Added quarantine of Unknown VO records (Gratia-107)
PBS probe fixes SOFTWARE-1032

* Mon May 13 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.7-1
Added fixes for onvm probe: additional verification of onevm availability 
Modified gratia spec to supress verification of ProbeConfig (md5, size, modification time)

* Thu Apr 25 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.6-1
- even more condor-meter fixes: GRATIA-75,GRATIA-91 

* Mon Apr 22 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.5-1
- more condor-meter fixes: GRATIA-75,GRATIA-91 

* Fri Apr 19 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.4-1
- condor-meter changes: GRATIA-75,GRATIA-91 
- glexec probe changes: GRATIA-99

* Mon Mar 25 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.3-1
- build probe without checking out lsg changes

* Mon Mar 25 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.2-1
- dcache storage (GRATIA-94,95,96) and transfer (GRATIA-87) fixes, lsf probe (SOFTWARE-977) fixes

* Fri Feb 15 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.1-0
- onevm probe fixes

* Thu Jan 24 2013 John Thiltges <jthiltges2@unl.edu> - 1.13.0-3
- For SLURM probe, handle race in logging of job start time

* Thu Jan 17 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.0-2
restore slurm packaging for testing

* Thu Jan 17 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.0-1
Fixed xml_util and temporary commented slurm out to build production release

* Wed Dec 26 2012 John Thiltges <jthiltges2@unl.edu> - 1.12-11
- Added SLURM probe for SOFTWARE-746

* Thu Dec 20 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.12-10
Adding glideinwms configuration package. GRATIA-76

* Mon Oct  1 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.9
- minor fixes for onevm probe

* Thu Sep 27 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.9pre
- included onevm cloud accounting probe into trunk

* Fri Sep 7 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.8
condor_meter code merge (modification for xsede to include ProjectName from classad) 
changes provided by Derek and Brian

* Fri Aug 12 2012 Tanya Levshin <tlevshin@fnal.gov> - 1.12.7
Brian's common libs fixes: Added  more comments. Re-utilized the regexp objects, fixed the handling of IOError, 
and simplified the exception handling. 
* Fri Aug 03 2012 Tanya Levshin <tlevshin@fnal.gov> - 1.12.6
- fixed: sge probe, output messages produced py DebugPrint before ProbeConfig could be read
 
* Mon Jul 30 2012 Tanya Levshin <tlevshin@fnal.gov> - 1.12.5
- production release that includes Brian's code clean up, sge fixes etc

* Tue May 8 2012 Hyunwoo Kim <hyunwoo@fnal.gov> - 1.12-5pre
- Modified GratiaCore.py GenerateFilename to remove Config.getFilenameFragment()
- so that we can simplify temp filenames https://jira.opensciencegrid.org/browse/GRATIA-61

* Mon Apr 23  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12-1
- No changes production release with gratia service 1.12

* Mon Apr 16  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-11.pre
- Incorporated fix to PBS probe provided by Derek Weitzel  https://jira.opensciencegrid.org/browse/GRATIA-63

* Mon Apr  9  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-10.pre
- Incorporated changes to gratia-probes-cron proposed by Alain Roy  https://jira.opensciencegrid.org/browse/GRATIA-62

* Fri Mar 23  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.9
- release

* Wed Mar 21  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.9.pre
- Fixed debug message in condor_meter https://jira.opensciencegrid.org/browse/GRATIA-58

* Mon Mar 18  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.8.pre
- VOOverride feature for campus grid usage https://jira.opensciencegrid.org/browse/GRATIA-57 - Derek Weitzel
- cron_check header fix

* Mon Feb 20  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.7
- version for OSG production release

* Thu Feb 20  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.7.pre
- Fixed pbs probe that now supreesed generation of UserVOName attribute (https://jira.opensciencegrid.org/browse/GRATIA-53)
- Derek's fixes for pbs (https://jira.opensciencegrid.org/browse/GRATIA-44) 
- Brian's fixes for condor-meter

* Thu Feb 9  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.6.pre
- Fixed various bugs intoroduced in 1.10-0.4

* Thu Feb 3  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.4.pre
- Applied pacthes for pbs probes https://jira.opensciencegrid.org/browse/GRATIA-44 
- Implemented gratia-probes-cron to start/stop gratia probes that are ran as cronjob as a service (https://jira.opensciencegrid.org/browse/GRATIA-30)
- Added dist tag to release

* Wed Feb 1  2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.10-0.3.pre
- Update the GridFTP probe to use POSIX locking; removed wrapper script.
- Split out the GRAM module from the common RPM.

* Mon Jan 16 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.10-0.2.pre
- Rewrite of Condor probe into python.
- Added support for campus grids to Condor probe.
- Added support for CMS overflow to Condor probe.
- Addition of POSIX-style locking for Condor probe.

* Wed Nov 15 2011 Tanya Levshina <tlevshin@fnal.gov> - 1.09-1
- No changes from 1.09.08.pre - just official release

* Wed Nov 15 2011 Tanya Levshina <tlevshin@fnal.gov> - 1.09-08.pre
- Fixed psacct data dir location (removed them from /usr/share/gratia/var, and put them under /var/lib/gratia)
- Added ldapsearch dependency to bdii probe
- Fixed URCOLLECTOR_LOC  in pbs probe 

* Tue Nov 08 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.09-0.6.pre
 - Make pbs-lsf probe not write into /opt (GRATIA-24).
 - Fix FHS locations in hadoop-storage probe (GRATIA-22).
 - Fix path to gridftp-transfer probe (GRATIA-19).

* Mon Oct 31 2011 Tanya Levshina <tlevshin@fnal.gov> - 1.09-0.5.pre
- More fixes (https://jira.opensciencegrid.org/browse/GRATIA-16, 17, 20)

* Mon Oct 31 2011 Tanya Levshina <tlevshin@fnal.gov> - 1.09-0.5.pre
- Some small fixes (https://jira.opensciencegrid.org/browse/GRATIA-11, 13, 15)

* Thu Sep 29 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.09-0.4.pre
- Metrics fixes from Scot K.

* Fri Sep 09 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.09-0.3.pre
Updates to pbs-lsf and gridftp-transfer probe.

* Tue Sep 06 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.09-0.2.pre
- Create python modules in subversion.  Simplify install code.

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.08-0.1.pre
- Reset changelog for pre-release of new packaging

