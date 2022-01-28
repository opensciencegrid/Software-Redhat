Name:               gratia-probe
Summary:            Gratia OSG accounting system probes
Group:              Applications/System
Version:            2.5.1
Release:            2%{?dist}
License:            GPL
URL:                http://sourceforge.net/projects/gratia/
Vendor:             The Open Science Grid <http://www.opensciencegrid.org/>

BuildRequires:      python3

%if 0%{?rhel} < 8
BuildRequires:      git
%else
BuildRequires:      git-core
%endif

BuildArch: noarch

%define default_prefix /usr/share

# Default probe configuration items for post-install.
%global default_collector_port 80
%global ssl_port 443

%global osg_collector gratia-osg-prod.opensciencegrid.org
%global osg_transfer_collector gratia-osg-transfer.opensciencegrid.org
%global enstore_collector dmscollectorgpvm01.fnal.gov

# Default ProbeName
%{!?meter_name: %global meter_name `hostname -f`}

%define customize_probeconfig(d:) sed -i "s#@PROBE_HOST@#%{meter_name}#" %{_sysconfdir}/gratia/%{-d*}/ProbeConfig

%global __python /usr/bin/python3
%global condor_python   python3-condor
%global python_psycopg2 python3-psycopg2

%if 0%{?rhel} >= 8
%global python_openssl  python3-pyOpenSSL
%global python_mysql    python3-mysql
%global python_tz       python3-pytz
%else
%global python_openssl  python36-pyOpenSSL
%global python_mysql    python36-mysql
%global python_tz       python36-pytz
%endif

%global debug_package %{nil}

########################################################################
# Source and patch specifications
Source0: %{name}-%{version}.tar.gz

########################################################################

# Build settings.
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: /usr
Prefix: %{default_prefix}
Prefix: /etc

# _unitdir,_tmpfilesdir not defined on el6 build hosts
%{!?_tmpfilesdir: %global _tmpfilesdir %{_prefix}/lib/tmpfiles.d}

# Build preparation.
%prep
%setup -q

%build

%install
# Setup
rm -rf $RPM_BUILD_ROOT

find . -type f -exec \
    sed -ri '1s,^#!\s*(/usr)?/bin/(env *)?python.*,#!%{__python},' '{}' +

install -d $RPM_BUILD_ROOT/%{_datadir}/gratia
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/gratia

install -d  $RPM_BUILD_ROOT%{_tmpfilesdir}
mv common/tmpfiles.d/gratia.conf $RPM_BUILD_ROOT%{_tmpfilesdir}/gratia.conf


git_commit_id=$(gzip -d < %{SOURCE0} | git get-tar-commit-id)


  # Obtain files

  packs=(
    common
    common2
    condor-ap
    htcondor-ce
    dCache-storagegroup
    dCache-transfer
    enstore-storage
    enstore-tapedrive
    enstore-transfer
    onevm
    osg-pilot-container
  )

  # PWD is the working directory, used to build
  # $RPM_BUILD_ROOT%{_datadir} are the files to package
  cp -pRL ${packs[@]} $RPM_BUILD_ROOT%{_datadir}/gratia

  install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
  install -d $RPM_BUILD_ROOT%{python_sitelib}
  mv common/gratia $RPM_BUILD_ROOT%{python_sitelib}
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia

  for probe in ${packs[@]}
  do
    # Install the cronjob
    if [[ -e $probe/gratia-probe-${probe,,}.cron ]]; then
      install -m 644 $probe/*.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/
    fi

    # Install the python modules
    if [ -e $probe/gratia ]; then
      mv $probe/gratia/* $RPM_BUILD_ROOT%{python_sitelib}/gratia
    fi

    # Common template customizations (same for all probes)
    PROBE_DIR=$RPM_BUILD_ROOT/%{_sysconfdir}/gratia/$probe
    install -d $PROBE_DIR
    install -m 644 common/ProbeConfigTemplate.osg $PROBE_DIR/ProbeConfig

    ## Probe-specific customizations
    # Replace @PROBE_SPECIFIC_DATA@ with ProbeConfig.add (if any)
    common/update-probeconfig.py $PROBE_DIR/ProbeConfig $probe/ProbeConfig.add

    # Collector strings
    case $probe in
    enstore-* | dCache-storagegroup )
      # must be first to catch enstrore-transfer/storage
      endpoint=%{enstore_collector}:%{default_collector_port}
      ssl_endpoint=%{enstore_collector}:%{ssl_port}
      ;;
    *-transfer | *-storage )
      endpoint=%{osg_transfer_collector}:%{default_collector_port}
      ssl_endpoint=%{osg_transfer_collector}:%{ssl_port}
      ;;
    * )
      endpoint=%{osg_collector}:%{default_collector_port}
      ssl_endpoint=%{osg_collector}:%{ssl_port}
      ;;
    esac
    sed -i -e "s#@PROBE_NAME@#$probe#" \
           -e "s#@COLLECTOR_ENDPOINT@#$endpoint#" \
           -e "s#@SSL_ENDPOINT@#$ssl_endpoint#" \
           -e "s#@SSL_REGISTRATION_ENDPOINT@#$endpoint#" \
        $PROBE_DIR/ProbeConfig

  done

  # Remove probe-specific items after install
  rm -f $RPM_BUILD_ROOT%{_datadir}/gratia/*/*.cron
  rm -f $RPM_BUILD_ROOT%{_datadir}/gratia/*/ProbeConfig.add
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/*/gratia

  # Remove test directories
  rm -rf $RPM_BUILD_ROOT%{_datadir}/gratia/*/test

  # common probe init script
  install -d $RPM_BUILD_ROOT/%{_initrddir}
  install -p -m 755 common/gratia-probes-cron.init $RPM_BUILD_ROOT%{_initrddir}/gratia-probes-cron
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/common/gratia-probes-cron.init

  # dCache-transfer init script
  install -d $RPM_BUILD_ROOT/%{_initrddir}
  install -m 755 dCache-transfer/gratia-dcache-transfer.init $RPM_BUILD_ROOT%{_initrddir}/gratia-dcache-transfer
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-transfer/gratia-dcache-transfer.init

  # Install condor-ap configuration snippet
  install -d $RPM_BUILD_ROOT/%{_datadir}/condor/config.d
  install -m 644 condor-ap/50-gratia-gwms.conf $RPM_BUILD_ROOT/%{_datadir}/condor/config.d/50-gratia-gwms.conf
  install -d $RPM_BUILD_ROOT/%{_sharedstatedir}/condor/gratia/{data,data/quarantine,tmp}
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/condor-ap/50-gratia-gwms.conf

  # Install the htcondor-ce configuration
  install -d $RPM_BUILD_ROOT/%{_datadir}/condor-ce/config.d
  install -m 644 htcondor-ce/50-gratia-ce.conf $RPM_BUILD_ROOT/%{_datadir}/condor-ce/config.d/50-gratia-ce.conf
  install -m 644 htcondor-ce/50-gratia-condor.conf $RPM_BUILD_ROOT/%{_datadir}/condor/config.d/50-gratia-condor.conf
  install -d $RPM_BUILD_ROOT/%{_sharedstatedir}/condor-ce/gratia/{data,data/quarantine,tmp}
  rm $RPM_BUILD_ROOT%{_datadir}/gratia/htcondor-ce/50-gratia-ce.conf \
     $RPM_BUILD_ROOT%{_datadir}/gratia/htcondor-ce/50-gratia-condor.conf

  # Remove remaining cruft
  rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/gratia/common
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/ProbeConfigTemplate.osg
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/samplemeter.py
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/samplemeter_multi.py
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/common/update-probeconfig.py
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/dCache-storagegroup/ProbeConfig.example
  rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/gratia/common2
  rm -f  $RPM_BUILD_ROOT%{_datadir}/gratia/*/README-xml.md
  rm     $RPM_BUILD_ROOT%{_datadir}/gratia/osg-pilot-container/Dockerfile

  # TODO: allow test directory, remove from RPM

  # Set up var area
  install -d $RPM_BUILD_ROOT%{_sharedstatedir}/gratia/
  install -d $RPM_BUILD_ROOT%{_sharedstatedir}/gratia/{tmp,data,data/quarantine,logs}
  chmod 1777  $RPM_BUILD_ROOT%{_sharedstatedir}/gratia/data
  install -d $RPM_BUILD_ROOT%{_sharedstatedir}/gratia/osg-pilot-container


# Burn in the RPM version into the python files.
rpmver=%{version}-%{release}.${git_commit_id:0:7}
find $RPM_BUILD_ROOT%{_datadir}/gratia $RPM_BUILD_ROOT%{python_sitelib} \
  -type f -exec fgrep -ZIle '%%%%%%RPMVERSION%%%%%%' {} + | xargs -0 \
  sed -i "s&%%%%%%RPMVERSION%%%%%%&$rpmver&g"

install -d $RPM_BUILD_ROOT/%{_localstatedir}/log/gratia
install -d $RPM_BUILD_ROOT/%{_localstatedir}/log/condor/gratia
install -d $RPM_BUILD_ROOT/%{_localstatedir}/log/condor-ce/gratia
install -d $RPM_BUILD_ROOT/%{_localstatedir}/lock/gratia

%clean
rm -rf $RPM_BUILD_ROOT

%description
Probes for the Gratia OSG accounting system


%package common
Summary: Common files for Gratia OSG accounting system probes
Group: Applications/System
Requires: %{python_openssl}
Requires(post): chkconfig
Requires(preun): chkconfig
Obsoletes: gratia-probe-bdii-status < 1.18.2-1

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
%{_sharedstatedir}/gratia/
%attr(-,gratia,gratia) %{_localstatedir}/log/gratia/
%dir %{_sysconfdir}/gratia
%{_localstatedir}/lock/gratia/
%{python_sitelib}/gratia/__pycache__/
%{python_sitelib}/gratia/__init__.py*
%{python_sitelib}/gratia/common
%dir %{default_prefix}/gratia/common
%{default_prefix}/gratia/common/GratiaPing
%{default_prefix}/gratia/common/DebugPrint
%{default_prefix}/gratia/common/GetProbeConfigAttribute
%{default_prefix}/gratia/common/cron_check
#system.d tmp files
%{_tmpfilesdir}/gratia.conf
# %description common2
# Common files and examples for Gratia OSG accounting system probes. Version 2.

# %files common2
# %defattr(-,root,root,-)
%{_initrddir}/gratia-probes-cron
#%doc common2/README
%doc %{default_prefix}/gratia/common2/README
# this is in common: %%{python_sitelib}/gratia/__init__.py*
%{python_sitelib}/gratia/common2
# executables:
%dir %{default_prefix}/gratia/common2
# %%{default_prefix}/gratia/common2/alarm.py
# %%{default_prefix}/gratia/common2/checkpoint.py
# %%{default_prefix}/gratia/common2/uuid_replacement.py
# %%{default_prefix}/gratia/common2/meter.py
# %%{default_prefix}/gratia/common2/pginput.py
# %%{default_prefix}/gratia/common2/probeinput.py

%package condor-ap
Summary: A probe accounting for payload jobs on an HTCondor Access Point
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: condor
Requires: %{condor_python}
Provides: %{name}-glideinwms = %{version}-%{release}
Obsoletes: %{name}-glideinwms < 2.3.0
Conflicts: %{name}-htcondor-ce

%description condor-ap
The HTCondor access point probe for the Gratia OSG accounting system.

%files condor-ap
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/condor-ap/README
%dir %{default_prefix}/gratia/condor-ap
%{default_prefix}/gratia/condor-ap/condor_meter
%attr(0755,condor,condor) %dir %{_sharedstatedir}/condor/gratia
%attr(0755,condor,condor) %dir %{_sharedstatedir}/condor/gratia/data
%attr(0755,condor,condor) %dir %{_sharedstatedir}/condor/gratia/data/quarantine
%attr(0755,condor,condor) %dir %{_sharedstatedir}/condor/gratia/tmp
%attr(0755,condor,condor) %dir %{_localstatedir}/log/condor/gratia
%config %{_datadir}/condor/config.d/50-gratia-gwms.conf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/condor-ap/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-condor-ap.cron

%post condor-ap
%customize_probeconfig -d condor-ap

%package dcache-transfer
Summary: Gratia OSG accounting system probe for dCache billing.
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{python_psycopg2}
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
%{default_prefix}/gratia/dCache-transfer/gratia-dcache-transfer
%{python_sitelib}/gratia/dcache_transfer
%dir %{default_prefix}/gratia/dCache-transfer
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/dCache-transfer/ProbeConfig

%post dcache-transfer
/sbin/chkconfig --add gratia-dcache-transfer
%customize_probeconfig -d dCache-transfer

%package onevm
Summary: Gratia OSG accounting system probe for OpenNebula VM accounting.
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: ruby
License: See LICENSE.

%description onevm
Gratia OSG accounting system probe for providing VM accounting.

%files onevm
%defattr(-,root,root,-)
%{python_sitelib}/gratia/onevm
%{default_prefix}/gratia/onevm/onevm_probe.cron.sh
%dir %{default_prefix}/gratia/onevm
%{default_prefix}/gratia/onevm/VMGratiaProbe
%{default_prefix}/gratia/onevm/query_one_lite.rb

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/onevm/ProbeConfig
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-onevm.cron

%post onevm
%customize_probeconfig -d onevm

%package osg-pilot-container
Summary: osg pilot container probe
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
#Requires: python-sqlite
Requires: %{condor_python}
License: See LICENSE.

%description osg-pilot-container
osg pilot container probe

%post osg-pilot-container
%customize_probeconfig -d osg-pilot-container

%files osg-pilot-container
%defattr(-,root,root,-)
%dir %{default_prefix}/gratia/osg-pilot-container
%{default_prefix}/gratia/osg-pilot-container/osgpilot_meter
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/osg-pilot-container/ProbeConfig
%dir %{_sharedstatedir}/gratia/osg-pilot-container
%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-osg-pilot-container.cron

%package htcondor-ce
Summary: A HTCondor-CE probe
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: htcondor-ce
License: See LICENSE.

%description htcondor-ce
The HTCondor-CE probe for the Gratia OSG accounting system

%files htcondor-ce
%defattr(-,root,root,-)
%dir %{default_prefix}/gratia/htcondor-ce
%doc %{default_prefix}/gratia/htcondor-ce/README
%{default_prefix}/gratia/htcondor-ce/condor_meter
%attr(0755,condor,condor) %dir %{_sharedstatedir}/condor-ce/gratia/data
%attr(0755,condor,condor) %dir %{_sharedstatedir}/condor-ce/gratia/data/quarantine
%attr(0755,condor,condor) %dir %{_sharedstatedir}/condor-ce/gratia/tmp
%attr(-,condor,condor) %dir %{_localstatedir}/log/condor-ce/gratia
%config %{_datadir}/condor/config.d/50-gratia-condor.conf
%config %{_datadir}/condor-ce/config.d/50-gratia-ce.conf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/htcondor-ce/ProbeConfig

%post htcondor-ce
%customize_probeconfig -d htcondor-ce


# Enstore probes: enstore-transfer, enstore-storage, enstore-tapedrive

%package enstore-transfer
Summary: Enstore transfer probe
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{python_psycopg2}
License: See LICENSE.

%description enstore-transfer
The Enstore transfer probe for the Gratia OSG accounting system.

%files enstore-transfer
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/enstore-transfer/README.html
%dir %{default_prefix}/gratia/enstore-transfer
%{default_prefix}/gratia/enstore-transfer/enstore-transfer

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/enstore-transfer/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-enstore-transfer.cron

%post enstore-transfer
%customize_probeconfig -d enstore-transfer

%package enstore-storage
Summary: Enstore storage probe
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-services = %{version}-%{release}
Requires: %{python_psycopg2}
License: See LICENSE.

%description enstore-storage
The Enstore storage probe for the Gratia OSG accounting system.

%files enstore-storage
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/enstore-storage/README.html
%dir %{default_prefix}/gratia/enstore-storage
%{default_prefix}/gratia/enstore-storage/enstore-storage

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/enstore-storage/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-enstore-storage.cron

%post enstore-storage
%customize_probeconfig -d enstore-storage

%package enstore-tapedrive
Summary: Enstore tapedrive probe
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-services = %{version}-%{release}
Requires: %{python_psycopg2}
License: See LICENSE.

%description enstore-tapedrive
The Enstore tape drive probe for the Gratia OSG accounting system.

%files enstore-tapedrive
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/enstore-tapedrive/README.html
%dir %{default_prefix}/gratia/enstore-tapedrive
%{default_prefix}/gratia/enstore-tapedrive/enstore-tapedrive

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/enstore-tapedrive/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-enstore-tapedrive.cron

%post enstore-tapedrive
%customize_probeconfig -d enstore-tapedrive

# dCache storagegroup

%package dcache-storagegroup
Summary: dCache storagegroup probe
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-services = %{version}-%{release}
Requires: %{python_psycopg2}
License: See LICENSE.

%description dcache-storagegroup
The dCache storagegroup probe for the Gratia OSG accounting system.

%files dcache-storagegroup
%defattr(-,root,root,-)
%doc %{default_prefix}/gratia/dCache-storagegroup/README.html
%dir %{default_prefix}/gratia/dCache-storagegroup
%{default_prefix}/gratia/dCache-storagegroup/dcache-storagegroup

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/gratia/dCache-storagegroup/ProbeConfig

%config(noreplace) %{_sysconfdir}/cron.d/gratia-probe-dcache-storagegroup.cron

%post dcache-storagegroup
%customize_probeconfig -d dCache-storagegroup

%package condor
Summary: Transitional dummy package to ease upgrades from OSG 3.5

%description condor
This is a transitional dummy package for gratia-probe-condor; it may safely be removed.

%files condor

%package lsf
Summary: Transitional dummy package to ease upgrades from OSG 3.5

%description lsf
This is a transitional dummy package for gratia-probe-lsf; it may safely be removed.

%files lsf

%package pbs-lsf
Summary: Transitional dummy package to ease upgrades from OSG 3.5

%description pbs-lsf
This is a transitional dummy package for gratia-probe-pbs-lsf; it may safely be removed.

%files pbs-lsf

%package sge
Summary: Transitional dummy package to ease upgrades from OSG 3.5

%description sge
This is a transitional dummy package for gratia-probe-sge; it may safely be removed.

%files sge

%package slurm
Summary: Transitional dummy package to ease upgrades from OSG 3.5

%description slurm
This is a transitional dummy package for gratia-probe-slurm; it may safely be removed.

%files slurm

%changelog
* Fri Jan 28 2022 Brian Lin <blin@cs.wisc.edu> - 2.5.1-2
- Add batch system dummy packages to ease upgrades

* Thu Jan 27 2022 Brian Lin <blin@cs.wisc.edu> - 2.5.1-1
- Fix HTCondor-CE configuration syntax

* Thu Jan 27 2022 Brian Lin <blin@cs.wisc.edu> - 2.5.0-1
- Fix record generation for HTCondor-CE with HTCondor batch systems
  (SOFTWARE-4978)
- Remove condor-batch probe (SOFTWARE-4978)

* Wed Jan 26 2022 Brian Lin <blin@cs.wisc.edu> - 2.4.0-1
- Add gratia-probe-condor-batch, formerly gratia-probe-condor (SOFTWARE-4978)
- Fix ownership of quarantine directories (SOFTWARE-4975)

* Wed Nov 10 2021 Brian Lin <blin@cs.wisc.edu> - 2.3.3-1
- Drop unnecessary trailing slash check for ProbeConfig DataFolder
  paths (SOFTWARE-4892)

* Thu Nov 04 2021 Brian Lin <blin@cs.wisc.edu> - 2.3.2-1
- Fix PER_JOB_HISTORY_DIR configuration for HTCondor AP (SOFTWARE-4846)
- Suppress payload job records by default for HTCondor APs (SOFTWARE-4846)

* Thu Nov 04 2021 Brian Lin <blin@cs.wisc.edu> - 2.3.1-1
- Fix SchedD cron path to HTCondor AP probe (SOFTWARE-4846)
- Fix ownership of HTCondor AP directories (SOFTWARE-4846)
- Fix case of Lockfile config name for HTCondor-CE and HTCondor AP
  probes (SOFTWARE-4621, SOFTWARE-4846)
- Remove OSPool specific configuration in HTCondor AP ProbeConfig
  (SOFTWARE-4846)

* Wed Oct 06 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.3.0-1
- Consolidate condor and old glideinwms probe into condor-ap (SOFTWARE-4846)
- Add support for running HTCondor access point probe as a SchedD cron (SOFTWARE-4846)

* Mon Sep 27 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.2.1-1
- Update htcondor-ce WorkingFolder to match hosted-ce container (SOFTWARE-4806)

* Mon Sep 20 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.2.0-1
- Drop xrootd-transfer probe (SOFTWARE-4520)
- Update directory configuration for htcondor-ce probe (SOFTWARE-4621)

* Fri Jul 23 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.1.0-1
- Get VO info from AuthToken (SciToken) attrs (SOFTWARE-4615)
- Lock Version-Release across sub-packages (SOFTWARE-4667)
- Move 99_gratia-ce.conf to /usr/share location (SOFTWARE-4611)
- Fix exception handling in condor_meter (SOFTWARE-4711)
- Fix missing log level (#107)
- Add GHA workflow (SOFTWARE-4684)

* Tue May 25 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.0.1-2
- Fix paren syntax in certinfo.py (SOFTWARE-4638)

* Tue Mar 02 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.23.2-1
- Fix attribute list handling for QueueTime (#94) (SOFTWARE-4521)
- Fix python3 int division in niceNum (#92)

* Thu Feb 25 2021 Brian Lin <blin@cs.wisc.edu> - 2.0.0-2
- Ensure that HTCondor-CE DataFolder exists (SOFTWARE-4490)

* Wed Feb 24 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.0.0-1
- Drop lots of probes for OSG 3.6 (SOFTWARE-4467)
- Support running htcondor-ce probe under schedd cron (SOFTWARE-4490)
- Fix python3 int division in niceNum
- Fix QueueTime attribute handling

* Wed Feb 10 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.23.1-1
- Add python2/3 compat for sge probe (SOFTWARE-4286)
- Add 'QueueTime' collection (SOFTWARE-4479)
- Add 'GratiaVersion' to UsageRecords (SOFTWARE-4455)

* Tue Jan 19 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.22.3-1
- Fix re.split warning for el8 (SOFTWARE-4283)

* Thu Jan 07 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.22.2-1
- Fix duration formatting in xml for python3 (SOFTWARE-4416)
- Report partial jobs for osg pilot container probe (SOFTWARE-4404)

* Tue Dec 22 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.22.1-1
- Add multi-site handling for osg-pilot-container probe (SOFTWARE-4386)
- More python3 packaging fixes for el8 (SOFTWARE-4398)

* Wed Dec 16 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.22.0-3
- Fix python3 packaging deps for el7 vs el8 (SOFTWARE-4398)

* Wed Dec 16 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.22.0-2
- Fix python3 packaging deps (SOFTWARE-4398)

* Mon Nov 30 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.22.0-1
- Initial release of osg-container-pilot probe (SOFTWARE-4169)
- More el8 / python3 build fixes (SOFTWARE-4348)
- Fix bug in cmd.communicate() handling of stderr (SOFTWARE-4348)

* Tue Nov 17 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.21.1-2
- More el7 / python3 build fixes (SOFTWARE-4348)

* Wed Nov 11 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.21.1-1
- Add python2/3 compat for common2 to fix el7 build (SOFTWARE-4348)

* Tue Nov 10 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.21.0-3
- Fix condor-python requirement for python3
- Require python3 explicitly for el7, too (SOFTWARE-4348)

* Thu Nov 05 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.21.0-2
- Build fix: specify python3 explicitly for el8 (SOFTWARE-4348)

* Wed Nov 04 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.21.0-1
- Add python3 support (SOFTWARE-4285, 4287, 4288, 4283)
- Add docker testing container (SOFTWARE-4313)

* Fri Jul 31 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.20.14-1
- Fix unquoted cluster names in slurm probe sql (SOFTWARE-4189)
- Detect condor vs htcondor-ce probe config (SOFTWARE-4195)

* Tue May 05 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.20.13-1
- Fix bug for slurm version < 18 (SOFTWARE-4055)
- Fix handling of non-word characters in slurm cluster name (SOFTWARE-4032)

* Fri Dec 13 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.20.12-1
- Quarantine files with parse errors, log unhandled errors (SOFTWARE-3877)

* Tue Oct 01 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.20.11-1
- Slurm probe SQL fixes (backtick quotes for identifiers) (SOFTWARE-3724)

* Mon Jul 29 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.20.10-1
- Slurm probe SQL fixes (SOFTWARE-3724, SOFTWARE-3765)

* Wed Jun 19 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.20.9-1
- Packaging revamp (SOFTWARE-3546)
- Document probe xml records (SOFTWARE-3609, SOFTWARE-3641)
- Cleanup init script (SOFTWARE-2503)
- Fix Exception string construction (#37)
- Support slurm v18 schema (SOFTWARE-3724)

* Mon Jan 14 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.20.8-1
- Avoid setting processors twice in slurm probe (SOFTWARE-3475)
- Add travis-ci infrastructure, add condor unit tests (#43)
- Default to 0 processors in condor probe (SOFTWARE-3474, SOFTWARE-3476)

* Tue Sep 11 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.20.7-1
- Fix handling of ExtraAttributes in condor probe (SOFTWARE-3415)

* Wed Aug 22 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.20.5-1
- Log unhandled exceptions in slurm probe (SOFTWARE-2456)

* Tue Jul 24 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.20.4-1
- Avoid missing records due to lag in slurm probe (SOFTWARE-3347)

* Wed Jun 20 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.20.3-2
- Fix htcondor-ce probe's condor_config_val queries (SOFTWARE-2629)
- Update pbs/lsf latest timestamp for empty logfiles (SOFTWARE-3041)

* Tue Jun 05 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.20.2-1
- Remove TWiki links from README files (SOFTWARE-3211)

* Mon Apr 16 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.20.1-1
- Handle raw seconds in walltime / cput in pbs probe (SOFTWARE-3221)

* Tue Apr 10 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.20.0-1
- Drop glexec probe & old GRAM code (SOFTWARE-3105)
- Fix handling of SlurmLocation in slurm probe (SOFTWARE-2795)
- Make ProjectName case insensitive in condor probe (SOFTWARE-3017)

* Wed Jan 24 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.19.1-1
- Always use classad lib in condor probe (SOFTWARE-3017)

* Thu Dec 21 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.19.0-1
- Add GPU support to common probe code (SOFTWARE-3084)

* Thu Nov 09 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.18.2-2
- Add Obsoletes for bdii-status probe (SOFTWARE-2660)

* Mon Oct 30 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.18.2-1
- Drop bdii-status probe (SOFTWARE-2660)
- Fix transfer collector strings in ProbeConfig (SOFTWARE-2560)

* Mon Jun 26 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.18.1-1
- Add support for WholeNodeJobs for HTCondor-CE (SOFTWARE-2783)

* Mon Jun 12 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.18.0-1
- Include arbitrary ClassAd attributes in Gratia usage records (SOFTWARE-2714)

* Mon Apr 24 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.17.5-1
- fix eval call in condor probe (SOFTWARE-2636)

* Mon Feb 20 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.17.4-1
- fall back to 1 if no cpus attributes specified in classad (SOFTWARE-2587)

* Wed Feb 15 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.17.3-1
- fall back to RequestCpus if MachineAttrCpus0 not in classad (SOFTWARE-2587)

* Tue Dec 20 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.2-1
- Use rpm version instead of $Revision$ svn:keyword (SOFTWARE-2538)
- Include OSG patches (SOFTWARE-2551, SOFTWARE-2532)

* Thu Dec 15 2016 Brian Lin <blin@cs.wisc.edu> - 1.17.0-2.7
- Populate Gratia record Host Description for local jobs (SOFTWARE-2551)

* Tue Nov 15 2016 Brian Lin <blin@cs.wisc.edu> - 1.17.0-2.6
- Suppress locally run payload job records (SOFTWARE-2532)

* Thu Oct 20 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.1-1
- Include OSG patches (SOFTWARE-2454, SOFTWARE-2171, SOFTWARE-2463,
                       SOFTWARE-2484)

* Fri Oct 14 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.0-2.5
- Only apply PBS patch for arch builds (SOFTWARE-2484)

* Thu Oct 13 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.0-2.4
- Count all allocated CPUs for whole-node PBS jobs (SOFTWARE-2484)

* Fri Sep 23 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.0-2.3
- Provide default for CondorCEHistoryFolder in code (SOFTWARE-2463)

* Wed Sep 21 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.0-2.2
- Add patch from Derek W to handle next slurm version (SOFTWARE-2171)

* Mon Sep 19 2016 Edgar Fajardo <emfajard@ucsd.edu> - 1.17.0-2.1
- Added tmpfiles.d configuration (SOFTWARE-2454)

* Fri Aug 26 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.0-2
- add versioned dependency on globus-gridftp-server-progs (SOFTWARE-2398)

* Wed Aug 24 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.17.0-1
- new gridftp-transfer probe to remove need for gums-host-cron (GRATIA-191,
                                                                SOFTWARE-2398)

* Fri Apr 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.16.0-1
- modify condor probe for HTCondor-CE (SOFTWARE-2257)
- filter results by probe name in condor_meter (GRATIA-188)

* Thu Feb 18 2016 Carl Edquist <edquist@cs.wisc.edu> - 1.15.0-1
- drop psacct probe (GRATIA-184)
- fix GridJobId parsing in condor_ce.py (GRATIA-185)
- eliminate file glob searches from certinfo file lookup (GRATIA-186)
- in dCache-transfer probe, read from Group file for mapping and get file name
  from ProbeConfig

* Thu Jun 11 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.14.2-6
- slurm probe bugfix for previous patch (goc/25834)

* Wed Jun 03 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.14.2-5
- Work around noarch probes not building on el7 by making them all arch-specific on el7

* Tue May 26 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.14.2-4
- slurm probe fix for mysql/mariadb 5.5 (goc/24516)

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

* Fri Aug 9 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.16-1
- Fix psacct for sl6 (GRATIA-115)

* Wed Jul 31 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.15-1
- New patch to deal with condor problems (GRATIA-114/SOFTWARE-1132)

* Fri Jul 26 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.14-1
- Fixed typo in condor_meter , also fixed check for condor_setup GRATIA-110 ; all by Suchandra

* Fri Jul 26 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.13-1
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

* Tue May 21 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.8-1
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

* Sun Aug 12 2012 Tanya Levshin <tlevshin@fnal.gov> - 1.12.7
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

* Sun Mar 18  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.8.pre
- VOOverride feature for campus grid usage https://jira.opensciencegrid.org/browse/GRATIA-57 - Derek Weitzel
- cron_check header fix

* Mon Feb 20  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.7
- version for OSG production release

* Mon Feb 20  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.7.pre
- Fixed pbs probe that now supreesed generation of UserVOName attribute (https://jira.opensciencegrid.org/browse/GRATIA-53)
- Derek's fixes for pbs (https://jira.opensciencegrid.org/browse/GRATIA-44) 
- Brian's fixes for condor-meter

* Thu Feb 9  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.6.pre
- Fixed various bugs intoroduced in 1.10-0.4

* Fri Feb 3  2012 Tanya Levshina <tlevshin@fnal.gov> - 1.10-0.4.pre
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

* Tue Nov 15 2011 Tanya Levshina <tlevshin@fnal.gov> - 1.09-1
- No changes from 1.09.08.pre - just official release

* Tue Nov 15 2011 Tanya Levshina <tlevshin@fnal.gov> - 1.09-08.pre
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
