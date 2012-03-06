
Name:      osg-cleanup
Version:   1.0
Release:   1%{?dist}
Summary:   OSG cleanup scripts

Group:     System Environment/Base
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/Documentation/Release3/InstallCleanupScripts

Source0:   %{name}-%{version}.tar.gz

Requires: logrotate

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description
%{summary}


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Install executables
install -d $RPM_BUILD_ROOT%{_sbindir}/
install -d $RPM_BUILD_ROOT%{_libexecdir}/
install -d -m 0700 $RPM_BUILD_ROOT%{_libexecdir}/osg-cleanup/
install -m 0700 sbin/osg-cleanup $RPM_BUILD_ROOT%{_sbindir}/
install -m 0700 libexec/clean-globus-tmp $RPM_BUILD_ROOT%{_libexecdir}/osg-cleanup/
install -m 0700 libexec/clean-user-dirs $RPM_BUILD_ROOT%{_libexecdir}/osg-cleanup/

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
%attr(700,root,root) %{_libexecdir}/osg-cleanup

%{_sysconfdir}/rc.d/init.d/osg-cleanup-cron
%{_sysconfdir}/cron.d/osg-cleanup

%config(noreplace) %{_sysconfdir}/osg/osg-cleanup.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/osg-cleanup

%post
/sbin/chkconfig --add osg-cleanup-cron

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service osg-cleanup-cron stop >/dev/null 2>&1
    /sbin/chkconfig --del osg-cleanup-cron
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service osg-cleanup-cron condrestart >/dev/null 2>&1 || :
fi


%changelog
* Thu Jan 12 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 1.0-1
- Final bug fixes.  First version ready for testing.

* Thu Jan 12 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.3-2
- Fixed permissions on /usr/libexec/osg-cleanup to be 700

* Thu Jan 12 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.3-1
- Fixed clean script to work with Globus 5.2 locations

* Wed Jan 11 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.2-1
- Fixed bugs in osg-cleanup script.
- Fixed installation location of cleanup scripts.

* Wed Jan 11 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.1-2
- Register service with chkconfig

* Tue Jan 10 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.1-1
- Created an initial osg-cleanup RPM
