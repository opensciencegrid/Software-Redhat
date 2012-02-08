Name:               gratia-probe
Summary:            Gratia OSG accounting system probes
Group:              Applications/System
Version:            1.10
Release:            0.5.pre%{?dist}
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
  install -d $RPM_BUILD_ROOT%{python_sitelib}
  mv common/gratia $RPM_BUILD_ROOT%{python_sitelib}
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia

  for probe in %{noarch_packs}
  do
    # Install the cronjob
    if [ -e $probe/gratia-probe-$probe.cron -o $probe == "dCache-storage" ]; then
      install -m 644 $probe/*.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
      rm $RPM_BUILD_ROOT%{_datadir}/gratia/$probe/*.cron
    fi

    # Install the python modules
    if [ -e $probe/gratia ]; then
      mv $probe/gratia/* $RPM_BUILD_ROOT%{python_sitelib}/gratia
      rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/$probe/gratia
    fi

    # Customize template for each probe
    PROBE_DIR=$RPM_BUILD_ROOT/%{_sysconfdir}/gratia/$probe
    install -d $PROBE_DIR
    install -m 644 common/ProbeConfigTemplate.osg $PROBE_DIR/ProbeConfig
    ln -s %{_sysconfdir}/gratia/$probe/ProbeConfig $RPM_BUILD_ROOT/%{_datadir}/gratia/$probe/ProbeConfig

    if [ $probe == "*-transfer" -o $probe == "*-storage" ]; then
      endpoint=%{osg_transfer_collector}:%{default_collector_port}
    elif [ $probe == metric ]; then
      endpoint=%{osg_metric_collector}:%{metric_port}
    else 
      endpoint=%{osg_collector}:%{default_collector_port}
    fi
    sed -i -e "s#@PROBE_NAME@#$probe#" \
           -e "s#@COLLECTOR_ENDPOINT@#$endpoint#" \
           -e "s#@SSL_ENDPOINT@#%{osg_collector}:%{ssl_port}#" \
           -e "s#@SSL_REGISTRATION_ENDPOINT@#$endpoint#" \
        $PROBE_DIR/ProbeConfig

    # Probe-specific customizations
    if [ $probe == "psacct" ]; then
      sed -i -e 's#@PROBE_SPECIFIC_DATA@#PSACCTFileRepository="/var/lib/gratia/account/" \
    PSACCTBackupFileRepository="/var/lib/gratia/backup/" \
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
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/condor/99_gratia.conf

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

  # Set up var area
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/
  install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/gratia/{tmp,data,logs}
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
Group: Application/System
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
%config(noreplace) %{_sysconfdir}/gratia/pbs-lsf/ProbeConfig
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
%config(noreplace) %{_sysconfdir}/gratia/psacct/ProbeConfig
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
%{default_prefix}/gratia/condor/ProbeConfig
%{default_prefix}/gratia/condor/condor_meter.cron.sh
%{default_prefix}/gratia/condor/condor_meter.pl
%{default_prefix}/gratia/condor/condor_meter
%config(noreplace) %{_sysconfdir}/condor/config.d/99_gratia.conf
%config(noreplace) %{_sysconfdir}/gratia/condor/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-condor.cron

%post condor
%customize_probeconfig -d condor

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
%config(noreplace) %{_sysconfdir}/gratia/sge/ProbeConfig
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
%{python_sitelib}/gratia/dcache_transfer
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
%{python_sitelib}/gratia/dcache_storage
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
%{default_prefix}/gratia/xrootd-transfer/gratia-xrootd-transfer
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
%{default_prefix}/gratia/xrootd-storage/gratia-xrootd-storage
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
%config(noreplace) %{_sysconfdir}/gratia/bdii-status/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-bdii-status.cron

%post bdii-status
%customize_probeconfig -d bdii-status

%endif # noarch

%changelog
* Wed Feb 08 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.10-0.5.pre
- Bumping to add noarch packages to el6 build

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

