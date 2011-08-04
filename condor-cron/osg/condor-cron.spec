
Name:      condor-cron
Version:   1.0.2
Release:   1%{?dist}
Summary:   A framework to run cron-style jobs within Condor

Group:     Applications/System
License:   Apache 2.0
URL:       http://www.cs.wisc.edu/condor

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  mock
Requires:  rpm-build
Requires:  createrepo

Requires:  condor

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
cp wrappers/condor_cron_history $RPM_BUILD_ROOT%{_bindir}/
cp wrappers/condor_cron_hold $RPM_BUILD_ROOT%{_bindir}/
cp wrappers/condor_cron_q $RPM_BUILD_ROOT%{_bindir}/
cp wrappers/condor_cron_qedit $RPM_BUILD_ROOT%{_bindir}/
cp wrappers/condor_cron_release $RPM_BUILD_ROOT%{_bindir}/
cp wrappers/condor_cron_rm $RPM_BUILD_ROOT%{_bindir}/
cp wrappers/condor_cron_submit $RPM_BUILD_ROOT%{_bindir}/
cp wrappers/condor_cron_version $RPM_BUILD_ROOT%{_bindir}/

# Copy config into place
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron
cp etc/condor_config.local $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/
cp etc/condor-cron.sh $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/
touch $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/condor_config

# Copy init script into place
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
cp etc/condor.init $RPM_BUILD_ROOT%{_initrddir}/condor-cron

# Make working directories
mkdir -p $RPM_BUILD_ROOT%{_var}/run/condor-cron
mkdir -p $RPM_BUILD_ROOT%{_var}/log/condor-cron
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/condor-cron
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/condor-cron/spool
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/condor-cron/execute
mkdir -p $RPM_BUILD_ROOT%{_var}/lock/condor-cron

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

%{_initrddir}/condor-cron

%ghost %{_sysconfdir}/condor-cron/condor_config
%config %{_sysconfdir}/condor-cron/condor_config.local
%{_sysconfdir}/condor-cron/condor-cron.sh

# Metric records will be placed in spool
%attr(-,cndrcron,cndrcron) %{_var}/run/condor-cron
%attr(-,cndrcron,cndrcron) %{_var}/log/condor-cron
%attr(-,cndrcron,cndrcron) %{_var}/lib/condor-cron
%attr(-,cndrcron,cndrcron) %{_var}/lib/condor-cron/spool
%attr(-,cndrcron,cndrcron) %{_var}/lib/condor-cron/execute
%attr(-,cndrcron,cndrcron) %{_var}/lock/condor-cron


%post
/sbin/chkconfig --add condor-cron
/sbin/ldconfig

# Use the condor_config.generic file to make the base file
# WARNING: This command might pick up the wrong file if the wildcard picks
#          up more than one condor-* directory.
cp /usr/share/doc/condor-*/etc/examples/condor_config.generic $RPM_BUILD_ROOT%{_sysconfdir}/condor-cron/condor_config
# Update the local config file location
perl -pi -e's|^(LOCAL_CONFIG_FILE\s*=).+$|$1 /etc/condor-cron/condor_config.local|' /etc/condor-cron/condor_config

# Need to put the uid/gid of cndrcron into the config file as CONDOR_IDS
CC_UID=`/usr/bin/id -u cndrcron`
CC_GID=`/usr/bin/id -g cndrcron`
echo "CONDOR_IDS = $CC_UID.$CC_GID" >> /etc/condor-cron/condor_config.local


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
* Thu Aug 04 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Created an initial condor cron spec file
