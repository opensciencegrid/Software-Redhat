%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?_initddir: %global _initddir %{_initrddir}}
%if "%{?rhel}" == "5"
%global docdiroption "with-docdir"
%else
%global docdiroption "docdir"
%endif

Name:		globus-gridftp-server
%global _name %(tr - _ <<< %{name})
Version:	6.14
Release:	4%{?dist}
Summary:	Globus Toolkit - Globus GridFTP Server

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.2/packages/src/%{_name}-%{version}.tar.gz
Source1:	%{name}
Source2:	globus-gridftp-sshftp
Source3:	globus-gridftp-password.8
Source4:	globus-gridftp-server-setup-chroot.8
Source5:	globus-gridftp-server.sysconfig
Source6:	globus-gridftp-server.osg-sysconfig
Source7:	globus-gridftp-server.logrotate
#		README file
Source8:	GLOBUS-GRIDFTP
# can't use %patch0 macro because this patch works on Source files and
#  not on files in the tarball like normal
Patch0:		osg-sysconfig.patch
Patch1:		gridftp-conf-logging.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-xio%{?_isa} >= 3
Requires:	globus-authz%{?_isa} >= 2
Requires:	globus-gfork%{?_isa} >= 3
Requires:	globus-ftp-control%{?_isa} >= 4
Requires:	globus-gridftp-server-control%{?_isa} >= 2
Requires:	globus-common%{?_isa} >= 14
Requires:	globus-xio-gsi-driver%{?_isa} >= 2
Requires:	globus-usage%{?_isa} >= 3
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core%{?_isa} >= 8
BuildRequires:	globus-xio-devel%{?_isa} >= 3
BuildRequires:	globus-authz-devel%{?_isa} >= 2
BuildRequires:	globus-gfork-devel%{?_isa} >= 3
BuildRequires:	globus-ftp-control-devel%{?_isa} >= 4
BuildRequires:	globus-gridftp-server-control-devel%{?_isa} >= 2
BuildRequires:	globus-common-devel%{?_isa} >= 14
BuildRequires:	globus-xio-gsi-driver-devel%{?_isa} >= 2
BuildRequires:	globus-usage-devel%{?_isa} >= 3
BuildRequires:	openssl-devel%{?_isa}

%package progs
Summary:	Globus Toolkit - Globus GridFTP Server Programs
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-xio-gsi-driver%{?_isa} >= 2
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
Requires:	globus-xio-devel%{?_isa} >= 3
Requires:	globus-authz-devel%{?_isa} >= 2
Requires:	globus-gfork-devel%{?_isa} >= 3
Requires:	globus-ftp-control-devel%{?_isa} >= 4
Requires:	globus-gridftp-server-control-devel%{?_isa} >= 2
Requires:	globus-common-devel%{?_isa} >= 14
Requires:	globus-xio-gsi-driver-devel%{?_isa} >= 2
Requires:	globus-usage-devel%{?_isa} >= 3
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
%patch1 -p1
# apply Patch0 to SOURCE1 & SOURCE2 files
(cd `dirname %{SOURCE1}`;patch -p0 <%{PATCH0})

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache
unset GLOBUS_LOCATION
unset GPT_LOCATION

%{_datadir}/globus/globus-bootstrap.sh

export GRIDMAP=/etc/grid-security/grid-mapfile
%configure --with-flavor=%{flavor} --sysconfdir=/etc/%{name} \
           --%{docdiroption}=%{_docdir}/%{name}-%{version} \
           --disable-static

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Remove libtool archives (.la files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

mv $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.conf.default \
   $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d
mv $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.xinetd.default \
   $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/gridftp
mv $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.gfork.default \
   $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.gfork
rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_noflavor_data.gpt
rm $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist

# No need for environment in conf files
sed '/ env /d' -i $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.gfork
sed '/^env /d' -i $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/gridftp

# Remove start-up scripts
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/init.d
sed '/init\.d/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist

# Install start-up scripts
mkdir -p $RPM_BUILD_ROOT%{_initddir}
install -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_initddir}

# Move server man pages to progs package
grep '.[18]$' $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist
sed '/.[18]$/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Install additional man pages
install -m 644 -p %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8

# Install README file
install -m 644 -p %{SOURCE8} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

mkdir -p $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}.logrotate

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' >> package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' > package-progs.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist

%clean
rm -rf $RPM_BUILD_ROOT

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

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README

%files -f package-progs.filelist progs
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}.logrotate
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/gridftp.conf
%config(noreplace) %{_sysconfdir}/gridftp.gfork
%config(noreplace) %{_sysconfdir}/xinetd.d/gridftp
/usr/share/osg/sysconfig/%{name}
%{_initddir}/%{name}
%{_initddir}/globus-gridftp-sshftp
%doc %{_mandir}/man8/globus-gridftp-password.8*
%doc %{_mandir}/man8/globus-gridftp-server-setup-chroot.8*


%files -f package-devel.filelist devel
%defattr(-,root,root,-)

%changelog
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

* Sun Jul 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.14-1
- Update to Globus Toolkit 5.2.2
- Drop patch globus-gridftp-server-pw195.patch (was backport)
- Drop patch globus-gridftp-server-format.patch (fixed upstream)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.10-2
- Backport security fix for JIRA ticket GT-195

 Thu May 17 2012 Alain Roy <roy@cs.wisc.edu> 6.5-1.7.osg
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

* Mon Dec 12 2011 Joseph Bester <bester@mcs.anl.gov> - 6.5-1
- init script fixes

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 6.4-3
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 6.4-2
- Last sync prior to 5.2.0

* Fri Nov 18 2011 Doug Strain <dstrain@fnal.gov> - 6.2-10
- Change sysconfig to add full file path

* Mon Nov 14 2011 Doug Strain <dstrain@fnal.gov> - 6.2-9
- Change sysconfig to source /var/lib/osg/globus-firewall

* Fri Nov 11 2011 Joseph Bester <bester@mcs.anl.gov> - 6.3-1
- GRIDFTP-190: add in config dir loading

* Thu Nov 03 2011 Doug Strain <dstrain@fnal.gov> - 6.2-8
- Added logrotate for issue SOFTWARE-310
- Also fixed sysconfig issue for SOFTWARE-357

* Thu Nov 03 2011 Doug Strain <dstrain@fnal.gov> - 6.2-5
- Changed sysconfig to exclude sourcing files left behind by
- emacs, rpm, vi, etc

* Mon Oct 24 2011 Joseph Bester <bester@mcs.anl.gov> - 6.2-2
- Add explicit dependencies on >= 5.2 libraries
- Add backward-compatibility aging
- Fix %post* scripts to check for -eq 1

* Tue Oct 11 2011 Doug Strain <dstrain@fnal.gov> - 6.1-5
- Changes to sysconfig to 
-   1) get rid of a warning if nothing exists in gridftp.conf.d
-   2) Move the xrootd-dsi plugin stuff into the xrootd-dsi package.

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

* Wed Aug 31 2011 Joseph Bester <bester@mcs.anl.gov> - 6.0-3
- Add more config files for xinetd or gfork startup
- Update to Globus Toolkit 5.1.2

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
