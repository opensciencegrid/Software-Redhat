%ifarch aarch64 alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?_initddir: %global _initddir %{_initrddir}}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gatekeeper
%global _name %(tr - _ <<< %{name})
Version:	9.15
Release:	1.8%{?dist}
Summary:	Globus Toolkit - Globus Gatekeeper

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.5/packages/src/%{_name}-%{version}.tar.gz
Source2:	%{name}.README
#		README file
Source8:	GLOBUS-GRAM5
Source11:       globus-gatekeeper.osg-sysconfig
Patch3:         init.patch
Patch5:         logrotate-copytruncate.patch
Patch6:         GT-489-openssl-1.0.1-fix.patch
Patch7:         1250-init-priorities.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#		Keep providing globus-gatekeeper-setup until it is not needed
Provides:	%{name}-setup = 2.2
Requires:	globus-common%{?_isa} >= 14
Requires:	globus-gss-assist%{?_isa} >= 8
Requires:	globus-gssapi-gsi%{?_isa} >= 9
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
Requires:       /lib/lsb/init-functions
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-gss-assist-devel >= 8
BuildRequires:	globus-gssapi-gsi-devel >= 9
BuildRequires:	openssl-devel

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus Gatekeeper

%prep
%setup -q -n %{_name}-%{version}

%patch3 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0

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

%configure --disable-static --with-flavor=%{flavor} \
	   --with-docdir=%{_pkgdocdir} \
           --with-lsb \
	   --with-initscript-config-path=/etc/sysconfig/globus-gatekeeper \
	   --with-lockfile-path='${localstatedir}/lock/subsys/globus-gatekeeper'

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

GLOBUSPACKAGEDIR=%{buildroot}%{_datadir}/globus/packages

# Install post installation instructions
install -m 644 -p %{SOURCE2} \
  %{buildroot}%{_pkgdocdir}/README.Fedora

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | sed -e s!^!%{_prefix}! \
	-e 's!%{_prefix}%{_sysconfdir}!%config(noreplace) %{_sysconfdir}!' \
  > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' >> package.filelist

mkdir -p %{buildroot}/etc/grid-services
mkdir -p %{buildroot}/etc/grid-services/available

mkdir -p $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/%{name}

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files -f package.filelist
%{_sysconfdir}/init.d/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%dir %{_sysconfdir}/grid-services
%dir %{_sysconfdir}/grid-services/available
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/README.Fedora
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
/usr/share/osg/sysconfig/%{name}


%changelog
* Wed Jan 15 2014 Matyas Selmeci <matyas@cs.wisc.edu> 9.15-1.8.osg
- Add requirement for lsb init functions

* Fri Jan 10 2014 Matyas Selmeci <matyas@cs.wisc.edu> 9.15-1.7.osg
- Fix init script chkconfig priorities to run after netfs and autofs (SOFTWARE-1250)

* Thu Jan 09 2014 Matyas Selmeci <matyas@cs.wisc.edu> 9.15-1.5.osg
- Use LSB-style Globus init script

* Wed Jan 08 2014 Matyas Selmeci <matyas@cs.wisc.edu> 9.15-1.4.osg
- Do not override Globus-provided init script (which we patch for GT-489) with the EPEL-provided one

* Mon Dec 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 9.15-1.3.osg
- Bump and rebuild with OpenSSL 1.0.0

* Thu Dec 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 9.15-1.2.osg
- Add fork_and_proxy workaround patch for GT-489 (OpenSSL 1.0.1 compatibility issue)

* Mon Dec 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> 9.15-1.1.osg
- Merge OSG changes
- Drop patch GRAM-309.patch (fixed upstream)
- Trim patch init.patch (most of it fixed upstream except for an OSG-specific change)

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.15-1
- Update to Globus Toolkit 5.2.5
- Drop patch globus-gatekeeper-ac.patch (fixed upstream)

* Wed Sep 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.11.osg
- Avoid trigerring gatekeeper's own log rotation since we're using logrotate (SOFTWARE-1083)

* Wed Sep 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.10.osg
- Add copytruncate to logrotate (SOFTWARE-1083)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.14-5
- Implement updated packaging guidelines

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.14-4
- Add aarch64 to the list of 64 bit platforms
- Don't use AM_CONFIG_HEADER (automake 1.13)

* Thu Feb 22 2013 Dave Dykstra <dwd@fnal.gov> - 9.6-1.9.osg
- Change to using LCMAPS_POLICY_NAME=authorize_only so globus does the
  user id switch, since globus can do it and globus-gatekeeper was the
  last package having lcmaps do the user id switch

* Fri Feb 15 2013 Dave Dykstra <dwd@fnal.gov> - 9.6-1.8.osg
- Move osg-specific sysconfig settings to /usr/share/osg/sysconfig/%{name}
  instead of appending to the end of /etc/sysconfig/%{name}, in order to
  match the new OSG method of keeping non-replaceable environment variable
  settings out of /etc/sysconfig's %config(noreplace) files.
- Change LCMAPS_POLICY_NAME to just be osg_default and no longer
  include the backward-compatible globus_gridftp_mapping policy

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.14-2
- Specfile clean-up

* Sun Jul 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.14-1
- Update to Globus Toolkit 5.2.2
- Drop patch globus-gatekeeper-porting.patch (fixed upstream)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.11-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gatekeeper-deps.patch (fixed upstream)

* Mon Apr 23 2012 Dave Dykstra <dwd@fnal.gov> - 9.6-1.7.osg
- Remove variable in sysconfig for disabling voms certificate check;
  it is now the default

* Thu Mar 29 2012 Dave Dykstra <dwd@fnal.gov> - 9.6-1.6.osg
- Reduce default lcmaps syslog level from 3 to 2

* Thu Mar 15 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.5.osg
- Add patch for GRAM-309 (fixes startup failure on IPv4-only machines)

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> - 9.6-1.4.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Thu Feb 02 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.6-3
- Fix start-up script

* Mon Jan 20 2012 Alain Roy <roy@cs.wisc.edu> - 9.6-1.3.osg
- Updated sysconfig file to source firewall information if it exists.

* Wed Jan 18 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.6-2
- Portability fixes
- Fix broken links in README file

* Fri Jan 6 2012 Dave Dykstra <dwd@fnal.gov> - 9.6-1.2.osg
- Set LCMAPS_POLICY_NAME in /etc/sysconfig/globus-gatekeeper
  for improved backward compatibility; the bug that made it be ignored
  is getting fixed and for those who have an old lcmaps.db it will use a 
  broken policy without this change.  Try first globus_gridftp_mapping,
  that's one worked even though it used to be labeled for gridftp.  The
  old osg_default didn't work, although the new one does so try that
  next in case the globus_gridftp_mapping rule has been removed
- Set the sysconfig parameter to disable checking of voms certifications

* Thu Dec 29 2011 Dave Dykstra <dwd@fnal.gov> - 9.6-1.1.osg
- Change /etc/sysconfig/globus-gatekeeper parameters to reflect no more
  LCAS and new LCMAPS

* Mon Dec 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.0
- Merge OSG changes
- Removed unneeded OSG patches:
    increase_backlog.patch
    chkconfig-off.patch
    maybe child_signals.patch

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.6-1
- Update to Globus Toolkit 5.2.0

* Mon Dec 12 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 8.1-8
- Set LCMAPS_MOD_HOME in /etc/sysconfig/globus-gatekeeper to "lcmaps", the
  new supported value as of lcmaps-1.4.28-19 which came out on November 16.
  Leave LCAS_MOD_HOME alone for now, but LCAS will be removed in a future
  release.

* Wed Dec 9 2011 Alain Roy <roy@cs.wisc.edu> - 8.1-7
- Improved init script to provide better error messages.

* Wed Dec 7 2011 Alain Roy <roy@cs.wisc.edu> - 8.1-6
- Added log rotation.

* Mon Nov 14 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 8.1-5
- Default globus-gatekeeper service to off.

* Thu Nov 10 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 8.1-4
- Increase the backlog for the listening socket.  Done because the small default led to failures on the testbed setup.

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 7.3-2
- Port OSG patches to released gatekeeper.

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-4
- Add README file

* Tue Apr 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-3
- Add start-up script and README.Fedora file

* Mon Feb 28 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-2
- Fix typos in the setup patch

* Thu Feb 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.7-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-2
- Simplify directory ownership

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.5-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-1
- Update to Globus Toolkit 5.0.0

* Wed Jul 29 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-1
- Autogenerated
