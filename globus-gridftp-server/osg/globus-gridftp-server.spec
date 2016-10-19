%global _hardened_build 1

%{!?_initddir: %global _initddir %{_initrddir}}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gridftp-server
%global _name %(tr - _ <<< %{name})
Version:	10.4
Release:	1.4%{?dist}
Summary:	Globus Toolkit - Globus GridFTP Server

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://toolkit.globus.org/
Source:		http://toolkit.globus.org/ftppub/gt6/packages/%{_name}-%{version}.tar.gz
Source1:	%{name}
Source2:	globus-gridftp-sshftp
Source3:	globus-gridftp-password.8
Source5:	globus-gridftp-server.sysconfig
Source6:	globus-gridftp-server.osg-sysconfig
Source7:	globus-gridftp-server.logrotate
#		README file
Source8:	GLOBUS-GRIDFTP
#		Fix globus-gridftp-server-setup-chroot for kfreebsd and hurd
Patch0:		globus-gridftp-server-unames.patch
Patch1:		gridftp-conf-logging.patch
Patch2:         adler32.patch
Patch3:         do_not_destroy_log_handle.patch
Patch4:         Do-not-ignore-config.d-files-with-a-.-in-the-name.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-xio-gsi-driver%{?_isa} >= 2
%if %{?fedora}%{!?fedora:0} >= 20 || %{?rhel}%{!?rhel:0} >= 6
Requires:	globus-xio-udt-driver%{?_isa} >= 1
%endif
Requires:	globus-common%{?_isa} >= 16
Requires:	globus-xio%{?_isa} >= 5
Requires:	globus-gridftp-server-control%{?_isa} >= 4
Requires:	globus-ftp-control%{?_isa} >= 6
BuildRequires:	globus-common-devel >= 16
BuildRequires:	globus-xio-devel >= 5
BuildRequires:	globus-xio-gsi-driver-devel >= 2
BuildRequires:	globus-gfork-devel >= 3
BuildRequires:	globus-gridftp-server-control-devel >= 4
BuildRequires:	globus-ftp-control-devel >= 6
BuildRequires:	globus-authz-devel >= 2
BuildRequires:	globus-usage-devel >= 3
BuildRequires:	globus-gssapi-gsi-devel >= 10
BuildRequires:	globus-gss-assist-devel >= 9
BuildRequires:	globus-gsi-credential-devel >= 6
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	globus-io-devel >= 9
BuildRequires:	openssl-devel
# zlib-devel required for OSG adler32 patch
BuildRequires:  zlib-devel
#		Additional requirements for make check
BuildRequires:	openssl
BuildRequires:	fakeroot

%package progs
Summary:	Globus Toolkit - Globus GridFTP Server Programs
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
Conflicts:	gridftp-hdfs%{?_isa} < 0.5.4-6
Conflicts:	xrootd-dsi%{?_isa} < 3.0.4-9

%package devel
Summary:	Globus Toolkit - Globus GridFTP Server Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-common-devel%{?_isa} >= 16
Requires:	globus-xio-devel%{?_isa} >= 5
Requires:	globus-xio-gsi-driver-devel%{?_isa} >= 2
Requires:	globus-gfork-devel%{?_isa} >= 3
Requires:	globus-gridftp-server-control-devel%{?_isa} >= 4
Requires:	globus-ftp-control-devel%{?_isa} >= 6
Requires:	globus-authz-devel%{?_isa} >= 2
Requires:	globus-usage-devel%{?_isa} >= 3
Requires:	globus-gssapi-gsi-devel%{?_isa} >= 10
Requires:	globus-gss-assist-devel%{?_isa} >= 9
Requires:	globus-gsi-credential-devel%{?_isa} >= 6
Requires:	globus-gsi-sysconfig-devel%{?_isa} >= 5
Requires:	globus-io-devel%{?_isa} >= 9
Requires:	openssl-devel%{?_isa}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus GridFTP Server

%description progs
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-progs package contains:
Globus GridFTP Server Programs

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Globus GridFTP Server Development Files

%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p4
%patch4 -p1

%build
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags} -lz"

export GRIDMAP=/etc/grid-security/grid-mapfile
export GLOBUS_VERSION=6.0
%configure --disable-static \
	   --includedir='${prefix}/include/globus' \
	   --libexecdir='${datadir}/globus' \
	   --docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC \(.*-shared\) !CC \\\${wl}--as-needed \1 !' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

mv %{buildroot}%{_sysconfdir}/gridftp.conf.default \
   %{buildroot}%{_sysconfdir}/gridftp.conf
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
mv %{buildroot}%{_sysconfdir}/gridftp.xinetd.default \
   %{buildroot}%{_sysconfdir}/xinetd.d/gridftp
mv %{buildroot}%{_sysconfdir}/gridftp.gfork.default \
   %{buildroot}%{_sysconfdir}/gridftp.gfork
mkdir -p %{buildroot}%{_sysconfdir}/gridftp.d

# No need for environment in conf files
sed '/ env /d' -i %{buildroot}%{_sysconfdir}/gridftp.gfork
sed '/^env /d' -i %{buildroot}%{_sysconfdir}/xinetd.d/gridftp

# Remove start-up scripts
rm -rf %{buildroot}%{_sysconfdir}/init.d

# Install start-up scripts
mkdir -p %{buildroot}%{_initddir}
install -p %{SOURCE1} %{SOURCE2} %{buildroot}%{_initddir}

# Install additional man pages
install -m 644 -p %{SOURCE3} %{buildroot}%{_mandir}/man8

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

mkdir -p $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}.logrotate

# Remove license file from pkgdocdir if licensedir is used
%{?_licensedir: rm %{buildroot}%{_pkgdocdir}/GLOBUS_LICENSE}

%check
make %{_smp_mflags} check VERBOSE=1

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post progs
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
    /sbin/chkconfig --add globus-gridftp-sshftp
fi

%preun progs
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del %{name}
    /sbin/chkconfig --del globus-gridftp-sshftp
    /sbin/service globus-gridftp-server stop
    /sbin/service globus-gridftp-sshftp stop
fi

%postun progs
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
    /sbin/service globus-gridftp-sshftp condrestart > /dev/null 2>&1 || :
fi

%files
%{_libdir}/libglobus_gridftp_server.so.*
%dir %{_sysconfdir}/gridftp.d
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%files progs
%{_sbindir}/gfs-dynbe-client
%{_sbindir}/gfs-gfork-master
%{_sbindir}/globus-gridftp-password
%{_sbindir}/globus-gridftp-server
%{_sbindir}/globus-gridftp-server-enable-sshftp
%{_sbindir}/globus-gridftp-server-setup-chroot
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}.logrotate
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/gridftp.conf
%config(noreplace) %{_sysconfdir}/gridftp.gfork
%config(noreplace) %{_sysconfdir}/xinetd.d/gridftp
/usr/share/osg/sysconfig/%{name}
%{_initddir}/%{name}
%{_initddir}/globus-gridftp-sshftp
%doc %{_mandir}/man8/globus-gridftp-password.8*
%doc %{_mandir}/man8/globus-gridftp-server.8*
%doc %{_mandir}/man8/globus-gridftp-server-setup-chroot.8*

%files devel
%{_includedir}/globus/*
%{_libdir}/libglobus_gridftp_server.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Oct 19 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 10.4-1.4.osg
- Disable SSLv3 (SOFTWARE-2471)

* Wed Oct 19 2016 Brian Lin <blin@cs.wisc.edu> - 10.4-1.3.osg
- Fix exit code when determining service status (SOFTWARE-2470)

* Thu Sep 01 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 10.4-1.2.osg
- Do not ignore config.d files with a '.' in the name (SOFTWARE-2197)

* Wed Aug 10 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 10.4-1.1.osg
- Merge OSG changes

* Fri Jul 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 7.20-1.3.osg
- Add TRANSFER to log_level (SOFTWARE-2397)

* Mon Jun 27 2016 Brian Bockelman <bbockelm@cse.unl.edu> - 7.20-1.2.osg
- Avoid deadlocking when the gridftp server closes its log file. SOFTWARE-2377
- Add support for adler32 checksums. SOFTWARE-2379

* Thu May 19 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.4-1
- GT6 update
  - Fix broken remote_node auth without sharing (10.4)
  - Fix configuration for ipc_interface (10.3)
  - Fix remote_node connection failing when ipc_subject isn't used (10.3)

* Fri May 06 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-1
- GT6 update
  - Spelling (10.2)
  - Don't overwrite LDFLAGS (10.1) - Fix for regressions in 9.8 ans 9.9
  - Updates for https support (10.0)

* Mon May 02 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.9-1
- GT6 update
  - Fix crash when storattr is used without modify (9.7)
  - Add SITE WHOAMI command to return currently authenticated user (9.6)
  - Update manpage for -encrypt-data (9.5)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.4-1
- GT6 update (fix mem error when sharing)

* Tue Nov 24 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.3-1
- GT6 update
  - Add configuration to require encrypted data channels (9.3)
  - More robust cmp function (9.2)

* Fri Nov 06 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.1-1
- GT6 update
  - fix for thread race crash between sequential transfers
  - fix for partial stat punting when passed a single entry
  - fix for double free on transfer failure race

* Tue Oct 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.0-2
- Missing ? in _isa macro

* Tue Oct 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.0-1
- GT6 update (add SITE STORATTR command and associated DSI api)

* Fri Oct 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.9-1
- GT6 update (Home directory fixes)

* Wed Aug 26 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.7-1
- GT6 update (Improvements to globus-gridftp-server-setup-chroot)
- Man page for globus-gridftp-server-setup-chroot now provided by
  upstream, remove the one from the source rpm
- Add build requires on openssl and fakeroot needed for new tests

* Thu Aug 06 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.1-1
- GT6 update (GT-622: GridFTP server crash with sharing group permissions)
- Enable checks

* Mon Jul 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.0-1
- GT6 update
- Add update_bytes api that sets byte counters and range markers separately

* Sat Jun 20 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.26-1
- GT6 update (man pages updates)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.25-1
- GT6 update (Fix order of drivers when using netmgr)

* Sat Mar 28 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.24-1
- GT6 update
- Fix netmanager crash (7.24)
- Allow netmanager calls when taskid isn't set (7.24)
- Fix threads commandline arg processing (7.23)
- Prevent parse error on pre-init envs from raising assertion (7.23)
- Restrict sharing based on username or group membership (7.21)
- Don't enable udt without threads (7.21)
- Environrment and threading config not loaded from config dir (7.21)
- Ignore config.d files with a '.' in name (7.21)
- Always install udt driver (7.21) - F20+, EPEL6+

* Mon Feb 16 2015 Matyas Selmeci <matyas@cs.wisc.edu> - 7.20-1.1.osg
- Merge OSG changes

* Fri Jan 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.20-1
- Implement updated license packaging guidelines
- GT6 update (-help fix)

* Wed Jan 07 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.18-1
- GT6 update (net mgr support)

* Fri Dec 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.17-1
- GT6 update

* Thu Nov 13 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.15-1
- GT6 update
- Drop patch globus-gridftp-server-ipv6log.patch (fixed upstream)

* Mon Oct 27 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.12-1
- GT6 update
- Drop patch globus-gridftp-server-deps.patch (fixed upstream)

* Tue Sep 30 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.11-2
- Fix logging of IPv6 addresses

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.11-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata
- Activate hardening flags

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Brent Baude <baude@us.ibm.com> - 6.38-2
- Replace arch def of ppc64 with power64 macro for ppc64le enablement

* Wed Apr 02 2014 Carl Edquist <edquist@cs.wisc.edu> - 6.38-1.3.osg
- Provide config dir /etc/gridftp.d/ (SOFTWARE-1412)

* Fri Jan 10 2014 Matyas Selmeci <matyas@cs.wisc.edu> 6.38-1.2.osg
- Fix init script chkconfig priorities to run after netfs and autofs (SOFTWARE-1250)

* Tue Dec 10 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 6.38-1.1.osg
- Merge OSG changes

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.38-1
- Update to Globus Toolkit 5.2.5
- Drop patch globus-gridftp-server-ac.patch (fixed upstream)

* Tue Sep 10 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 6.14-5.osg
- Use copytruncate for log rotation (SOFTWARE-1083)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.19-4
- Implement updated packaging guidelines

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 6.19-3
- Perl 5.18 rebuild

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.19-2
- Add aarch64 to the list of 64 bit platforms
- Don't use AM_CONFIG_HEADER (automake 1.13)

* Wed Feb 20 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.19-1
- Update to Globus Toolkit 5.2.4

* Wed Feb 20 2013 Dave Dykstra <dwd@fnal.gov> - 6.14-4.osg
- Add gridftp-conf-logging.patch to add back logging options in gridftp.conf
  that were (apparently) accidentally dropped in 6.14-1.osg

* Tue Feb 19 2013 Dave Dykstra <dwd@fnal.gov> - 6.14-3.osg
- Switch the default LCMAPS_POLICY_NAME to authorize_only, so it will
  work with the -with-chroot option; it also works without -with-chroot

* Mon Feb 18 2013 Dave Dykstra <dwd@fnal.gov> - 6.14-2.osg
- Move most of the OSG-specific code out of /etc/sysconfig/%{name}
  to /usr/share/osg/sysconfig/%{name} so it can be more easily replaced.
- Instead of sourcing /etc/sysconfig/gridftp.conf.d/* if they exist,
  source /usr/share/osg/sysconfig/%{name}-plugin.
- Add Conflicts statements on older gridftp-hdfs and xrootd-dsi packages
  because need new versions that understand the new sysconfig layout.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.16-1
- Update to Globus Toolkit 5.2.3

* Sun Jul 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.14-1
- Update to Globus Toolkit 5.2.2
- Drop patch globus-gridftp-server-pw195.patch (was backport)
- Drop patch globus-gridftp-server-format.patch (fixed upstream)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.10-2
- Backport security fix for JIRA ticket GT-195

* Thu May 17 2012 Alain Roy <roy@cs.wisc.edu> 6.5-1.7.osg
- Added patch for GT-195.

* Fri Apr 27 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.10-1
- Update to Globus Toolkit 5.2.1
- Drop patches globus-gridftp-server-deps.patch,
  globus-gridftp-server-funcgrp.patch, globus-gridftp-server-pathmax.patch
  and globus-gridftp-server-compat.patch (fixed upstream)
- Drop globus-gridftp-server man page from packaging since it is now included
  in upstream sources
- Add additional contributed man pages

* Mon Apr 23 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.6.osg
- Remove variable in sysconfig for disabling voms certificate check;
  it is now the default

* Thu Mar 29 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.5.osg
- Reduce default lcmaps syslog level from 3 to 2

* Sat Mar 10 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-4
- Restore enum and struct member order for improved backward compatibility

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.4.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Mon Mar 05 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-3
- The last update broke backward compatibility and should have bumped
  the soname - so bump it now
- Add patch from upstream to reduce the chance of backward incompatible
  changes in the future

* Wed Jan 18 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-2
- Portability fixes
- Fix broken links in README file

* Fri Jan 6 2012 Dave Dykstra <dwd@fnal.gov> - 6.5-1.3
- Updated /etc/sysconfig/globus-gridftp-server for elimination of LCAS
  parameters and for new settings of lcas-lcmaps-gt4-interface parameters
  corresponding to the new upgrade of LCMAPS, including backward 
  compatibility with the old lcmaps.db where only the globus_gridftp_mapping
  policy worked.
- Eliminated need for separate sysconfig file for i386

* Tue Dec 27 2011 Doug Strain <dstrain@fnal.gov> - 6.5-1.2
- Changed LCMAPS_MOD_HOME to "lcmaps"
- For SOFTWARE-426 as per Dave Dykstra

* Mon Dec 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.5-1.1
- Merge OSG changes

* Wed Dec 14 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.5-1
- Update to Globus Toolkit 5.2.0
- Drop patches globus-gridftp-server-etc.patch,
  globus-gridftp-server-pathmax.patch and globus-gridftp-server-usr.patch
  (fixed upstream)

* Fri Nov 18 2011 Doug Strain <dstrain@fnal.gov> - 6.2-10
- Change sysconfig to add full file path

* Mon Nov 14 2011 Doug Strain <dstrain@fnal.gov> - 6.2-9
- Change sysconfig to source /var/lib/osg/globus-firewall

* Thu Nov 03 2011 Doug Strain <dstrain@fnal.gov> - 6.2-8
- Added logrotate for issue SOFTWARE-310
- Also fixed sysconfig issue for SOFTWARE-357

* Thu Nov 03 2011 Doug Strain <dstrain@fnal.gov> - 6.2-5
- Changed sysconfig to exclude sourcing files left behind by
- emacs, rpm, vi, etc

* Tue Oct 11 2011 Doug Strain <dstrain@fnal.gov> - 6.1-5
- Changes to sysconfig to 
-   1) get rid of a warning if nothing exists in gridftp.conf.d
-   2) Move the xrootd-dsi plugin stuff into the xrootd-dsi package.

* Sun Oct 02 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.33-2
- Update contributed manpage

* Fri Sep 30 2011 Jeff Dost <jdost@ucsd.edu> - 6.1-4
- Change sysconfig file to use correct globus_gridftp_mapping LCMAPS policy

* Tue Sep 27 2011 Doug Strain <dstrain@fnal.gov> - 6.1-3
- Re-Adding extra sysconfig directory and configurable conf file
- With new version of gridftp

* Fri Sep 23 2011 Joe Bester <bester@mcs.anl.gov> - 6.1-1
- GRIDFTP-184: Detect and workaround bug in start_daemon for LSB < 4

* Thu Sep 22 2011 Doug Strain <dstrain@fnal.gov> - 6.0-6
- Adding extra sysconfig directory and configurable conf file
- For different plugin supports

* Fri Sep 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.0-5
- Patched init script to work around an infinite loop caused by some versions of redhat-lsb

* Wed Sep 07 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 6.0-4
- Fix condition in post-script for progs

* Tue Aug 30 2011 Doug Strain <doug.strain@fnal.gov> - 5.4-4
- Updated to work on RHEL5
- Updated to patch conf to use log file options
- Updated to patch init script to source sysconfig
- Included sysconfig with lcas/lcmaps variables

* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.33-1
- Update to Globus Toolkit 5.0.4

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.28-3
- Add README file
- Add missing dependencies

* Tue Apr 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.28-2
- Add start-up script and man page for globus-gridftp-server

* Fri Feb 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.28-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.23-1
- Update to Globus Toolkit 5.0.2

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.21-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.19-1
- Update to Globus Toolkit 5.0.0

* Mon Oct 19 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.17-2
- Fix location of default config file

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.17-1
- Autogenerated
