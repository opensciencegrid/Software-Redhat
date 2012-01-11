
Name:      osg-cleanup
Version:   0.1
Release:   1%{?dist}
Summary:   OSG cleanup scripts

Group:     System Environment/Base
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/Documentation/Release3/InstallCleanupScripts

Source0:   %{name}-%{version}.tar.gz

Requires: logrotate

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
%{summary}


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Install executables
install -d $RPM_BUILD_ROOT%{_sbindir}/
install -d $RPM_BUILD_ROOT%{_libexecdir}/
install -m 0700 sbin/osg-cleanup $RPM_BUILD_ROOT%{_sbindir}/
install -m 0700 libexec/clean-globus-tmp $RPM_BUILD_ROOT%{_libexecdir}/
install -m 0700 libexec/clean-user-dirs $RPM_BUILD_ROOT%{_libexecdir}/

# Install configuration
install -d $RPM_BUILD_ROOT%{_sysconfdir}/osg/
install -m 0600 etc/osg-cleanup.conf $RPM_BUILD_ROOT%{_sysconfdir}/osg/

# Install cron job
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/
install -m 755 init.d/osg-cleanup-cron $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/
install -m 644 cron.d/osg-cleanup $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/

# Log rotation
install -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 logrotate/osg-cleanup.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/osg-cleanup

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%{_sbindir}/osg-cleanup
%{_libexecdir}/clean-globus-tmp
%{_libexecdir}/clean-user-dirs

%{_sysconfdir}/rc.d/init.d/osg-cleanup-cron
%{_sysconfdir}/cron.d/osg-cleanup

%config(noreplace) %{_sysconfdir}/osg/osg-cleanup.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/osg-cleanup

%changelog
* Tue Jan 09 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.1-1
- Created an initial osg-cleanup RPM
