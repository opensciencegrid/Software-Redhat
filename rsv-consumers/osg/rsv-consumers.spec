
Name:      rsv-consumers
Version:   3.4.9
Release:   1%{?dist}
Summary:   RSV Consumers Infrastructure

Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: gratia-probe-metric
Requires: httpd

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}


%pre
# Create the rsv user/group
getent group rsv >/dev/null || groupadd -r rsv
getent passwd rsv >/dev/null || useradd -r -g rsv -d /var/rsv -s /bin/sh -c "RSV monitoring" rsv


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Create the web areas
install -d $RPM_BUILD_ROOT%{_datadir}/rsv
install -d $RPM_BUILD_ROOT%{_datadir}/rsv/www

# Install the Apache configuration and index files
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -d $RPM_BUILD_ROOT%{_datadir}/osg/www.d/
install -m 0644 httpd/rsv.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
install -m 0644 httpd/rsv.site $RPM_BUILD_ROOT%{_datadir}/osg/www.d/

# Install executables
install -d $RPM_BUILD_ROOT%{_libexecdir}/rsv
cp -r libexec/consumers $RPM_BUILD_ROOT%{_libexecdir}/rsv/

# Install configuration
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta
cp -r etc/meta/consumers $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta/
cp -r etc/consumers $RPM_BUILD_ROOT%{_sysconfdir}/rsv/
cp etc/rsv-nagios.conf $RPM_BUILD_ROOT%{_sysconfdir}/rsv/

# Create the log dir
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/rsv/consumers

# Put log rotation in place
install -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 logrotate/rsv-consumers.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/rsv-consumers


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

# This package owns this directory and everything in it
%{_libexecdir}/rsv/consumers/

%config %{_sysconfdir}/rsv/meta/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/rsv-nagios.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsv-consumers

%config %{_sysconfdir}/httpd/conf.d/rsv.conf
%config %{_datadir}/osg/www.d/rsv.site

%attr(-,rsv,rsv) %{_datadir}/rsv
%attr(-,rsv,rsv) %{_datadir}/rsv/www
%attr(-,rsv,rsv) %{_localstatedir}/log/rsv/consumers

%changelog
* Thu Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Creating a first RPM for rsv-consumers
