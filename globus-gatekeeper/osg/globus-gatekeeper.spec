%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%if "%{?rhel}" == "5"
%global docdiroption "with-docdir"
%else
%global docdiroption "docdir"
%endif

Name:		globus-gatekeeper
%global _name %(tr - _ <<< %{name})
Version:	9.6
Release:	1.12%{?dist}
Summary:	Globus Toolkit - Globus Gatekeeper

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:         http://www.globus.org/ftppub/gt5/5.2/5.2.0/packages/src/%{_name}-%{version}.tar.gz

# OSG customizations
Source1:        globus-gatekeeper.osg-sysconfig
Patch3:         init.patch
Patch4:         GRAM-309.patch
Patch5:         logrotate-copytruncate.patch
Patch6:         GT-489-openssl-1.0.1-fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common >= 13.4
Requires:	globus-gss-assist%{?_isa} >= 8
Requires:	globus-gssapi-gsi%{?_isa} >= 9
Requires:       psmisc

Requires:       lsb
Requires(post): globus-common-progs >= 13.4
Requires(preun):globus-common-progs >= 13.4
BuildRequires:  lsb
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-gss-assist-devel%{?_isa} >= 8
BuildRequires:	globus-gssapi-gsi-devel%{?_isa} >= 9
BuildRequires:	globus-core%{?_isa} >= 8

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus Gatekeeper
Globus Gatekeeper Setup

%prep
%setup -q -n %{_name}-%{version}

%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} \
           --%{docdiroption}=%{_docdir}/%{name}-%{version} \
           --disable-static \
           --with-lsb \
	   --with-initscript-config-path=/etc/sysconfig/globus-gatekeeper \
           --with-lockfile-path='${localstatedir}/lock/subsys/globus-gatekeeper'

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | grep -v '^/etc' \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | grep '^/etc' >> package.filelist
mkdir -p $RPM_BUILD_ROOT/etc/grid-services
mkdir -p $RPM_BUILD_ROOT/etc/grid-services/available

mkdir -p $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del %{name}
    /sbin/service %{name} stop > /dev/null 2>&1 || :
fi

%postun
if [ $1 -eq 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%dir /etc/grid-services
%dir /etc/grid-services/available
%config(noreplace) /etc/sysconfig/globus-gatekeeper
%config(noreplace) /etc/logrotate.d/globus-gatekeeper
/usr/share/osg/sysconfig/%{name}

%changelog
* Wed Dec 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.12.osg
- Add fork_and_proxy workaround patch for GT-489 (OpenSSL 1.0.1 compatibility issue)

* Wed Sep 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.11.osg
- Avoid trigerring gatekeeper's own log rotation since we're using logrotate (SOFTWARE-1083)

* Wed Sep 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.10.osg
- Add copytruncate to logrotate (SOFTWARE-1083)

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

* Mon Apr 23 2012 Dave Dykstra <dwd@fnal.gov> - 9.6-1.7.osg
- Remove variable in sysconfig for disabling voms certificate check;
  it is now the default

* Thu Mar 29 2012 Dave Dykstra <dwd@fnal.gov> - 9.6-1.6.osg
- Reduce default lcmaps syslog level from 3 to 2

* Thu Mar 15 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 9.6-1.5.osg
- Add patch for GRAM-309 (fixes startup failure on IPv4-only machines)

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> - 9.6-1.4.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Mon Jan 20 2012 Alain Roy <roy@cs.wisc.edu> - 9.6-1.3.osg
- Updated sysconfig file to source firewall information if it exists. 

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

* Mon Dec 12 2011 Joseph Bester <bester@mcs.anl.gov> - 9.6-1
- init script fixes

* Mon Dec 12 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 8.1-8
- Set LCMAPS_MOD_HOME in /etc/sysconfig/globus-gatekeeper to "lcmaps", the
  new supported value as of lcmaps-1.4.28-19 which came out on November 16.
  Leave LCAS_MOD_HOME alone for now, but LCAS will be removed in a future
  release.

* Wed Dec 9 2011 Alain Roy <roy@cs.wisc.edu> - 8.1-7
- Improved init script to provide better error messages.

* Wed Dec 7 2011 Alain Roy <roy@cs.wisc.edu> - 8.1-6
- Added log rotation. 

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 9.5-3
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 9.5-2
- Last sync prior to 5.2.0

* Mon Nov 28 2011 Joseph Bester <bester@mcs.anl.gov> - 9.5-1
- GRAM-285: Set default gatekeeper log in native packages

* Mon Nov 28 2011 Joseph Bester <bester@mcs.anl.gov> - 9.4-1
- GRAM-287: Hang of globus-gatekeeper process

* Wed Nov 23 2011 Joseph Bester <bester@mcs.anl.gov> - 9.3-1
- Updated version numbers

* Tue Nov 15 2011 Joseph Bester <bester@mcs.anl.gov> - 9.2-1
- GRAM-276: Increase backlog for gatekeeper

* Mon Nov 14 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 8.1-5
- Default globus-gatekeeper service to off.

* Thu Nov 10 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 8.1-4
- Increase the backlog for the listening socket.  Done because the small default led to failures on the testbed setup.

* Mon Nov 07 2011 Joseph Bester <bester@mcs.anl.gov> - 9.1-1
- Add default chkconfig line

* Mon Nov 07 2011 Joseph Bester <bester@mcs.anl.gov> - 9.0-1
- GRAM-268: GRAM requires gss_export_sec_context to work

* Fri Oct 28 2011 Joseph Bester <bester@mcs.anl.gov> - 8.2-1
- GRAM-267: globus-gatekeeper uses inappropriate Default-Start in init script

* Fri Oct 21 2011 Joseph Bester <bester@mcs.anl.gov> - 8.1-2
- Fix %post* scripts to check for -eq 1
- Add explicit dependencies on >= 5.2 libraries

* Fri Sep 23 2011 Joe Bester <bester@mcs.anl.gov> - 8.1-1
- GRAM-260: Detect and workaround bug in start_daemon for LSB < 4

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 8.0-2
- Update for 5.1.2 release

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
