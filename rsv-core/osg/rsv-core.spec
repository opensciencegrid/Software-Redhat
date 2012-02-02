
Name:      rsv-core
Version:   3.6.8
Release:   2%{?dist}
Summary:   RSV Core Infrastructure

Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: /usr/bin/grid-proxy-info
Requires: /usr/bin/globus-job-run

# We require globus-common-progs to work around a missing dependency 
# in the globus-gram-client-tools RPM (which provides globus-job-run)
# In the future, we should be able to remove this
Requires: globus-common-progs

# We use shar files for globus-job-run
Requires: sharutils

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts


%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}


%pre
# Create the rsv user/group
getent group rsv >/dev/null || groupadd -r rsv
getent passwd rsv >/dev/null || useradd -r -g rsv -d /var/rsv -m -s /bin/sh -c "RSV monitoring" rsv


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Create the logging directories
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/rsv

# Create the temp file area
install -d $RPM_BUILD_ROOT%{_localstatedir}/tmp/rsv

# Install the executable
install -d $RPM_BUILD_ROOT%{_bindir}
install -m 0755 bin/rsv-control $RPM_BUILD_ROOT%{_bindir}/

install -d $RPM_BUILD_ROOT%{_libexecdir}/rsv
cp -r libexec/misc $RPM_BUILD_ROOT%{_libexecdir}/rsv/

# Install the init script
install -d $RPM_BUILD_ROOT%{_initrddir}
install -m 0755 init/rsv.init $RPM_BUILD_ROOT%{_initrddir}/rsv

# Install the configuration
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rsv
install -m 0644 etc/consumers.conf $RPM_BUILD_ROOT%{_sysconfdir}/rsv/
install -m 0644 etc/rsv.conf $RPM_BUILD_ROOT%{_sysconfdir}/rsv/

# Install python libraries
install -d $RPM_BUILD_ROOT%{python_sitelib}
cp -r lib/python/rsv $RPM_BUILD_ROOT%{python_sitelib}/

# Install the man page
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0644 share/man/man1/rsv-control.1 $RPM_BUILD_ROOT%{_mandir}/man1/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%attr(-,rsv,rsv) %{_localstatedir}/log/rsv
%attr(-,rsv,rsv) %{_localstatedir}/tmp/rsv

%{_bindir}/rsv-control
%{_libexecdir}/rsv/misc/

%{_initrddir}/rsv

%config(noreplace) %{_sysconfdir}/rsv/consumers.conf
%config(noreplace) %{_sysconfdir}/rsv/rsv.conf

%{python_sitelib}/rsv/*

%{_mandir}/man1/rsv-control.1*


%post
/sbin/chkconfig --add rsv
/sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  /sbin/service rsv stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del rsv
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service rsv restart >/dev/null 2>&1 || :
fi
/sbin/ldconfig


%changelog
* Thu Feb 02 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.8-2
- Use '%{localstatedir}/tmp' instead of %{_tmppath} when creating directories
- Add -m option when running useradd to make rsv user

* Fri Dec 30 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.8-1
- Bug fix for passing arguments on command line

* Wed Dec 28 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.6.7-1
- Added the ability to pass metric arguments on the command line.
- Fixed a bug in listing of probes with cron times. (JIRA 432)
- Improved error if uudecode is missing on remote CE.
- Other minor bug fixes.

* Wed Dec 07 2011 Alain Roy <roy@cs.wisc.edu> 3.6.6-2
- Added dependency on globus-common-progs

* Thu Oct 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.5.9-1
- Re-implemented globus-job-run submission (as a backup for Condor-G)

* Wed Oct 05 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.5.3-1
- rsv-control wrapper now uses system python

* Thu Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Creating a first RPM for rsv-core
