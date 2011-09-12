
Name:      condor-cron
Version:   1.0.5
Release:   3%{?dist}
Summary:   A framework to run cron-style jobs within Condor

Group:     Applications/System
License:   Apache 2.0
URL:       http://www.cs.wisc.edu/condor

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  condor

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts


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

# Copy config into place
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron
install -d $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/config.d
install -m 0644 etc/condor_config $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/condor_config
touch $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/config.d/condor_ids
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/config.d/condor_ids

# Copy environment file into place 
install -d $RPM_BUILD_ROOT%{_libexecdir}/condor-cron
install -m 0755 libexec/condor-cron.sh $RPM_BUILD_ROOT%{_libexecdir}/condor-cron/

# Copy init script into place
install -d $RPM_BUILD_ROOT%{_initrddir}
install -m 0755 etc/condor.init $RPM_BUILD_ROOT%{_initrddir}/condor-cron

# Make working directories
install -d $RPM_BUILD_ROOT%{_localstatedir}/run/condor-cron
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/condor-cron
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/condor-cron
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/condor-cron/spool
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/condor-cron/execute
install -d $RPM_BUILD_ROOT%{_localstatedir}/lock/condor-cron

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%{_bindir}/condor_cron_history
%{_bindir}/condor_cron_hold
%{_bindir}/condor_cron_q
%{_bindir}/condor_cron_qedit
%{_bindir}/condor_cron_release
%{_bindir}/condor_cron_rm
%{_bindir}/condor_cron_submit
%{_bindir}/condor_cron_version
%{_bindir}/condor_cron_config_val

%{_initrddir}/condor-cron

%config %{_sysconfdir}/condor-cron/condor_config
%config %{_sysconfdir}/condor-cron/config.d/condor_ids

%{_libexecdir}/condor-cron/condor-cron.sh

# Metric records will be placed in spool
%attr(-,cndrcron,cndrcron) %{_localstatedir}/run/condor-cron
%attr(-,cndrcron,cndrcron) %{_localstatedir}/log/condor-cron
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lib/condor-cron
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lib/condor-cron/spool
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lib/condor-cron/execute
%attr(-,cndrcron,cndrcron) %{_localstatedir}/lock/condor-cron


%post
/sbin/chkconfig --add condor-cron
/sbin/ldconfig

# Need to put the uid/gid of cndrcron into the config file as CONDOR_IDS
CC_UID=`/usr/bin/id -u cndrcron`
CC_GID=`/usr/bin/id -g cndrcron`
echo "CONDOR_IDS = $CC_UID.$CC_GID" >> /etc/condor-cron/config.d/condor_ids


%preun
if [ $1 = 0 ]; then
  /sbin/service condor-cron stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del condor-cron
fi


%postun
if [ "$1" -ge "1" ]; then
  /sbin/service condor-cron condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig




%changelog
* Fri Sep 09 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.5-1
- Changed how we handle configuration

* Thu Aug 11 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0.3-1
- Numerous fixes based on feedback

* Thu Aug 04 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Created an initial condor cron spec file
