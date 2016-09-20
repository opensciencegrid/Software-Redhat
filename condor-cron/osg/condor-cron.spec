Name:      condor-cron
Version:   1.1.1
Release:   2%{?dist}
Summary:   A framework to run cron-style jobs within Condor

Group:     Applications/System
License:   Apache 2.0
URL:       http://www.cs.wisc.edu/condor

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  condor
Requires:  which

%if 0%{?rhel} >= 7
%define systemd 1
Requires(post): systemd
Requires(preun): systemd
%else
%define systemd 0
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%endif

# _unitdir, _tmpfilesdir not defined on el6 build hosts
%{!?_unitdir: %global _unitdir %{_prefix}/lib/systemd/system}
%{!?_tmpfilesdir: %global _tmpfilesdir %{_prefix}/lib/tmpfiles.d}


%description
%{summary}


%pre
# Create the cndrcron user/group
getent group cndrcron >/dev/null || groupadd -r cndrcron
getent passwd cndrcron >/dev/null || useradd -r -g cndrcron -d /var/lib/condor-cron -s /sbin/nologin -c "Condor-cron service" cndrcron


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Copy wrappers into place
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_history $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_hold $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_q $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_qedit $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_release $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_rm $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_submit $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_version $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 wrappers/condor_cron_config_val $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 wrappers/condor_cron_master $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 wrappers/condor_cron_off $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 wrappers/condor_cron_restart $RPM_BUILD_ROOT%{_sbindir}/

# Copy config into place
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/config.d
install -m 0644 etc/condor_config $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/condor_config
touch $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/config.d/condor_ids
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/config.d/condor_ids

# Copy environment file into place 
install -d $RPM_BUILD_ROOT%{_libexecdir}/condor-cron
install -m 0755 libexec/condor-cron.sh $RPM_BUILD_ROOT%{_libexecdir}/condor-cron/

%if %systemd
# Copy systemd files into place
install -d $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 etc/condor-cron.service $RPM_BUILD_ROOT%{_unitdir}/
install -d $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 0644 etc/condor-cron-tmpfiles.conf $RPM_BUILD_ROOT%{_tmpfilesdir}/condor-cron.conf
%else
# Copy init script into place
install -d $RPM_BUILD_ROOT%{_initrddir}
install -m 0755 etc/condor.init $RPM_BUILD_ROOT%{_initrddir}/condor-cron
%endif

# Make working directories
install -d $RPM_BUILD_ROOT%{_localstatedir}/run/condor-cron
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/condor-cron
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/condor-cron
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/condor-cron/spool
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/condor-cron/execute
install -d $RPM_BUILD_ROOT%{_localstatedir}/lock/condor-cron

# Touch the ghost files
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
touch $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/condor-cron
touch $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/config.d/condor_location


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%{_bindir}/condor_cron_history
%{_bindir}/condor_cron_hold
%{_sbindir}/condor_cron_master
%{_sbindir}/condor_cron_off
%{_bindir}/condor_cron_q
%{_bindir}/condor_cron_qedit
%{_bindir}/condor_cron_release
%{_bindir}/condor_cron_rm
%{_sbindir}/condor_cron_restart
%{_bindir}/condor_cron_submit
%{_bindir}/condor_cron_version
%{_bindir}/condor_cron_config_val

%if %systemd
%{_unitdir}/condor-cron.service
%{_tmpfilesdir}/condor-cron.conf
%else
%{_initrddir}/condor-cron
%endif

%config %{_sysconfdir}/condor-cron/condor_config
%config %{_sysconfdir}/condor-cron/config.d/condor_ids

%{_libexecdir}/condor-cron/condor-cron.sh

%ghost %{_sysconfdir}/sysconfig/condor-cron
%ghost %{_sysconfdir}/condor-cron/config.d/condor_location

# Metric records will be placed in spool
%attr(-,cndrcron,cndrcron) %{_localstatedir}/run/condor-cron
%attr(-,cndrcron,cndrcron) %{_localstatedir}/log/condor-cron
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lib/condor-cron
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lib/condor-cron/spool
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lib/condor-cron/execute
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lock/condor-cron


%post
%if %systemd
systemctl enable condor-cron
%else
/sbin/chkconfig --add condor-cron
%endif

/sbin/ldconfig

# Need to put the uid/gid of cndrcron into the config file as CONDOR_IDS
CC_UID=`/usr/bin/id -u cndrcron`
CC_GID=`/usr/bin/id -g cndrcron`
echo "# This file is automatically generated.  Do not edit." > /etc/condor-cron/config.d/condor_ids
echo "CONDOR_IDS = $CC_UID.$CC_GID" >> /etc/condor-cron/config.d/condor_ids


%preun
if [ $1 = 0 ]; then
%if %systemd
  systemctl stop condor-cron >/dev/null 2>&1 || :
  systemctl disable condor-cron >/dev/null 2>&1 || :
%else
  /sbin/service condor-cron stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del condor-cron
%endif
fi


%postun
if [ "$1" -ge "1" ]; then
%if %systemd
  systemctl restart condor-cron >/dev/null 2>&1 || :
%else
  /sbin/service condor-cron condrestart >/dev/null 2>&1 || :
%endif
fi
/sbin/ldconfig




%changelog
* Tue Sep 20 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.1.1-2
- On EL7, use systemd commands in the scriptlets (SOFTWARE-2439)

* Thu Sep 15 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.1.1-1
- Add commands condor_cron_master, condor_cron_off, and condor_cron_restart (SOFTWARE-2439)
- Add tmpfiles.d config (SOFTWARE-2439)
- Remove init script from EL7 (SOFTWARE-2439)
- Ensure lockdir and rundir exist with correct permissions on startup (PR #4)

* Wed Jun 01 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 1.1.0-1
- Fix sending grid jobs to remote schedds (SOFTWARE-2267)

* Tue Dec 08 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.11-1
- Turn off BIND_ALL_INTERFACES (SOFTWARE-2133)

* Mon Dec 07 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.10-1
- Fix LIBEXEC path in config file (SOFTWARE-2126)
- Turn off shared port (SOFTWARE-2126)
- Remove SOFTWARE-1124 patch (upstream)

* Fri Jul 17 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0.9-4
- Add systemd .service file (SOFTWARE-1604)

* Fri Sep 19 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.9-3
- Require "which" package for init script (SOFTWARE-1611)

* Tue Jul 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.9-2
- Patch condor_config file to have more descriptive comments, and also remove
  the CONDOR_IDS line because /etc/condor-cron/config.d/condor_ids will set
  that anyway. (SOFTWARE-1124)

* Thu Jul 05 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.9-1
- Update to 1.0.9
- TECHONOLOGY-20 - patch for Condor-CE support

* Thu Mar 15 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.8-1
- Fix for SOFTWARE-588

* Fri Jan 20 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.6-2
- Fixed (harmless but unnecessary) duplicate entries in condor_ids file on updates

* Fri Jan 20 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.6-1
- Fixing to work with Condor installed in non-standard location

* Fri Sep 09 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.5-1
- Changed how we handle configuration

* Thu Aug 11 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.3-1
- Numerous fixes based on feedback

* Thu Aug 04 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Created an initial condor cron spec file
