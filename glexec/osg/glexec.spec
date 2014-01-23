Summary: User identity switching tool based on grid credentials
Name: glexec
Version: 0.9.9
Release: 1.2%{?dist}
License: ASL 2.0
Group: Applications/System
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
Source1: glexec.conf
Source2: glexec.logrotate
Patch0: nowarn_allwhite.patch
Patch1: nowarn_sigchld.patch
Patch2: log_init.patch
%if %{?rhel}%{!?rhel:0} <= 5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif
BuildRequires: lcmaps-basic-interface >= 1.5.0
Requires: logrotate
# Since liblcmaps.so is dlopen'd we need this explicit requirement.
Requires: lcmaps%{?_isa} >= 1.5.0
Requires(pre): shadow-utils

Requires: lcmaps-plugins-glexec-tracking

%description
gLExec is a program that acts as a light-weight 'gatekeeper'. it takes
Grid credentials as input, and takes the local site policy into
account to authenticate and authorize the credentials. It will then
switch to a new execution sandbox and execute the given command as the
switched identity. gLExec is also capable of functioning as a
light-weight control point which offers a binary yes/no result in
logging-only mode.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p2

%build
%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
chmod u+r ${RPM_BUILD_ROOT}%{_sbindir}/glexec

# OSG default config
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/lcmaps
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/glexec.conf
cat %{SOURCE2} >>$RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/glexec

# glexec-configure doesn't work for OSG
rm $RPM_BUILD_ROOT%{_sbindir}/glexec-configure $RPM_BUILD_ROOT%{_datadir}/man/man8/glexec-configure.8*

%post
chown glexec:root %{_sysconfdir}/glexec.conf
chmod 600 %{_sysconfdir}/glexec.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE NEWS
%config(noreplace) %{_sysconfdir}/logrotate.d/glexec
%attr(600, glexec, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/glexec.conf
%{_datadir}/man/man5/glexec.conf.5*
%{_datadir}/man/man1/glexec.1*
%attr(4111, root, root) %{_sbindir}/glexec


# Add the glexec group and user (see http://fedoraproject.org/wiki/Packaging:UsersAndGroups)
%pre
getent group glexec >/dev/null || groupadd -r glexec
getent passwd glexec >/dev/null || \
    useradd -r -g glexec -d / -s /sbin/nologin \
    -c "gLExec user account to be used with %{_sbindir}/glexec" glexec
exit 0

%changelog
* Thu Jan 27 2013 Dave Dykstra <dwd@fnal.gov> 0.9.9-1.2.osg
- add patch from upstream to fix initialization of syslog so it
  can correctly redirect to a different facility

* Thu Nov 27 2013 Dave Dykstra <dwd@fnal.gov> 0.9.9-1.1.osg
- pull in new upstream version

* Mon Nov 11 2013 Mischa Salle <msalle@nikhef.nl> 0.9.9-1
- Adding NEWS file to doc
- only define buildroot on RHEL5
- updating version

* Thu Jan 04 2013 Dave Dykstra <dwd@fnal.gov> 0.9.8-1.2.osg
- Add a patch to move the log warning "Ignoring SIGCHLD from unknown
    finished child" from NOTICE to INFO level.  It is caused by
    the glexec_monitor detaching itself to run in the background.

* Thu Jan 03 2013 Dave Dykstra <dwd@fnal.gov> 0.9.8-1.1.osg
- pull in new upstream version

* Sun Nov 18 2012 Mischa Salle <msalle@nikhef.nl> 0.9.8-1
- updating version

* Tue Oct 23 2012 Mischa Salle <msalle@nikhef.nl> 0.9.7-1
- Remove explicit configure flags, they are defaults.
- Add architecture to lcmaps requirement.
- Update URL.
- updating version

* Fri Sep 21 2012 Dave Dykstra <dwd@fnal.gov> 0.9.6-1.2.osg
- Removed glexec-configure and its man page from OSG distribution since
  it doesn't work there

* Sun Apr  1 2012 Dave Dykstra <dwd@fnal.gov> 0.9.6-1.1.osg
- Reimported to OSG -- lowered loglevel of message if homedir of
  payload did not exist, and fixed bug that set wrong umask in
  non-linger mode

* Mon Mar 19 2012 Dave Dykstra <dwd@fnal.gov> 0.9.4-1.1.osg
- Reimported to OSG

* Fri Mar 16 2012 Mischa Salle <msalle@nikhef.nl> 0.9.4-1
- updating version

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 0.9.3-1.2.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Tue Feb 28 2012 Dave Dykstra <dwd@fnal.gov> 0.9.3-1.1.osg
- Upgraded upstream version

* Tue Feb 28 2012 Mischa Salle <msalle@nikhef.nl> 0.9.3-1
- fixing macros in ChangeLog and commented-out release
- updating version

* Mon Feb 27 2012 Mischa Salle <msalle@nikhef.nl> 0.9.2-1
- add manpage for glexec-configure
- updating version

* Tue Feb 21 2012 Dave Dykstra <dwd@fnal.gov> 0.9.1-2.1.osg
- Upgraded upstream version

* Mon Feb 20 2012 Mischa Salle <msalle@nikhef.nl> 0.9.1-2
- new install permissions on binary, should be chmod u+r in install phase
- updating version

* Mon Jan 16 2012 Dave Dykstra <dwd@fnal.gov> 0.9.0-1.3
- Rebuild to sign package

* Fri Jan 13 2012 Dave Dykstra <dwd@fnal.gov> 0.9.0-1.2
- Change default log levels in glexec.conf to 3 to align with NIKHEF's
  recommendation

* Fri Dec 30 2011 Dave Dykstra <dwd@fnal.gov> 0.9.0-1.1
- Import into OSG, including adding OSG's default glexec.conf, removing
  /etc/lcmaps/lcmaps-glexec.db, requiring lcmaps-plugins-glexec-tracking,
  and adding a logrotate for /var/log/glexec.log
- Add a patch to not warn in the log about all users being in the white list
- Explicitly set ownership & permissions on /etc/glexec.conf in the %post
  install because a %config(noreplace) won't change them on an existing file

* Wed Dec 14 2011 Mischa Salle <msalle@nikhef.nl> 0.9.0-1
- add installation of glexec-configure

* Mon Aug 15 2011 Mischa Salle <msalle@nikhef.nl> 0.8.12-3
- sbindir should have been _sbindir in useradd
- Need minimal lcmaps-basic-interface 1.4.31
- Format for testing release (commented-out)

* Thu Jul 21 2011 Mischa Salle <msalle@nikhef.nl> 0.8.11-2
- use the new --with-lcmaps-moduledir-sfx and --with-lcas-moduledir-sfx
  configure options instead of the --with-lcmaps-moduledir.

* Wed Jul 20 2011 Mischa Salle <msalle@nikhef.nl> 0.8.11-1
- use %%{_sysconfdir} instead of /etc in the %files list

* Thu Jul 14 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.10-2
- change lcmaps moduledir according to new schema
- fix the permissions of the configuration file
- create a glexec account on demand

* Wed Jun 29 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.8.10-1
- Remove Vendor tag

* Mon Mar 14 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.4-2a
- removed lcas.db
- updated sources

* Fri Mar 11 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.4-1
- new version including lcas/lcmaps db files

* Tue Mar  8 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.2-3
- setup config fiiles noreplace

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.2-2
- fixed configuration files and license string

* Fri Feb 25 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.
