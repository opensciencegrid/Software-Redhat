%ifarch aarch64 alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gram-job-manager
%global _name %(tr - _ <<< %{name})
Version:	13.53
Release:	1.3%{?dist}
Summary:	Globus Toolkit - GRAM Jobmanager

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.5/packages/src/%{_name}-%{version}.tar.gz
Source1:        globus-gram-job-manager-logging
Source2:        job-manager.rvf
#		README file
Source8:	GLOBUS-GRAM5

Patch0:         1418-broken-state-file-crash.patch
# OSG-specific patches
Patch9:         unlock_init.patch
Patch11:        null_old_jm.patch
Patch16:        description_service_tag.patch
Patch19:        load_requests_before_activating_socket.patch
Patch20:        fix-job-home-dir.patch
Patch22:        fix-job-lock-location.patch
Patch26:        allow-manager-restart.patch
Patch27:        recompute-stdio-on-restart.patch
Patch30:        logrotate-copytruncate.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#		Keep providing globus-gram-job-manager-setup until not needed
Provides:	%{name}-setup = 4.3
Requires:	globus-gsi-credential%{?_isa} >= 5
Requires:	globus-scheduler-event-generator%{?_isa} >= 4
Requires:	globus-xio-popen-driver%{?_isa} >= 2
Requires:	globus-xio%{?_isa} >= 3
Requires:	globus-gss-assist%{?_isa} >= 8
Requires:	globus-gsi-sysconfig%{?_isa} >= 5
Requires:	globus-callout%{?_isa} >= 2
Requires:	globus-gssapi-gsi%{?_isa} >= 10
Requires:	globus-gram-job-manager-callout-error%{?_isa} >= 2
Requires:	globus-gram-protocol%{?_isa} >= 11
Requires:	globus-common%{?_isa} >= 14
Requires:	globus-usage%{?_isa} >= 3
Requires:	globus-rsl%{?_isa} >= 9
Requires:	globus-gass-cache%{?_isa} >= 8
Requires:	globus-gass-transfer%{?_isa} >= 7
Requires:	globus-gram-protocol >= 11
Requires:	globus-gram-job-manager-scripts >= 4
Requires:	globus-gass-copy-progs >= 8
Requires:	globus-proxy-utils >= 5
Requires:	globus-gass-cache-program >= 5
Requires:	globus-gatekeeper >= 9
Requires:	psmisc
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8
BuildRequires:	globus-gsi-credential-devel >= 5
BuildRequires:	globus-scheduler-event-generator-devel >= 4
BuildRequires:	globus-xio-popen-driver-devel >= 2
BuildRequires:	globus-xio-devel >= 3
BuildRequires:	globus-gss-assist-devel >= 8
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	globus-callout-devel >= 2
BuildRequires:	globus-gssapi-gsi-devel >= 10
BuildRequires:	globus-gram-job-manager-callout-error-devel >= 2
BuildRequires:	globus-gram-protocol-devel >= 11
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-usage-devel >= 3
BuildRequires:	globus-rsl-devel >= 9
BuildRequires:	globus-gass-cache-devel >= 8
BuildRequires:	globus-gass-transfer-devel >= 7
BuildRequires:	globus-common-progs >= 14
BuildRequires:	globus-gram-protocol-doc >= 11
BuildRequires:	globus-common-doc >= 14
BuildRequires:	openssl-devel
BuildRequires:	libxml2-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	ghostscript
BuildRequires:	tex(latex)
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 7
BuildRequires:	tex(fullpage.sty)
BuildRequires:	tex(multirow.sty)
BuildRequires:	tex(sectsty.sty)
BuildRequires:	tex(tocloft.sty)
BuildRequires:	tex(xtab.sty)
BuildRequires:	tex-ec
BuildRequires:	tex-courier
BuildRequires:	tex-helvetic
BuildRequires:	tex-times
BuildRequires:	tex-symbol
BuildRequires:	tex-rsfs
%endif

%package doc
Summary:	Globus Toolkit - GRAM Jobmanager Documentation Files
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	%{name} = %{version}-%{release}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
GRAM Jobmanager

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
GRAM Jobmanager Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%patch0 -p0
%patch9 -p0
%patch11 -p0
%patch16 -p0
%patch19 -p0
%patch20 -p0
%patch22 -p0
%patch26 -p0

# This one is difficult.  Stdio stageout is not atomic - on restart,
# you need to either assume in-progress transfers "always fail" or
# "always succeed".  The patch below assumes "always fail".
# I think it's a better default, but am waiting on more info.
#%patch27 -p0

%patch30 -p0
sed 's!globus_gram_audit!globus/gram-audit!' -i configure.in

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

unset GLOBUS_LOCATION
unset GPT_LOCATION
aclocal_includes="-I ." %{_datadir}/globus/globus-bootstrap.sh

%configure --disable-static --with-flavor=%{flavor} \
	   --enable-doxygen --with-docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

GLOBUSPACKAGEDIR=%{buildroot}%{_datadir}/globus/packages

# This library is opened using lt_dlopenext, so the libtool archive
# (.la file) can not be removed - fix the libdir and clear dependency_libs
# ... and move it to the main package
for lib in `find %{buildroot}%{_libdir} -name 'lib*.la'` ; do
  sed -e "s!^libdir=.*!libdir=\'%{_libdir}\'!" \
      -e "s!^dependency_libs=.*!dependency_libs=\'\'!" -i $lib
done
grep 'lib.*\.la$' $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Move license file to main package
grep GLOBUS_LICENSE $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist
sed /GLOBUS_LICENSE/d -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Move client and server man pages to main package
grep '.[18]$' $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist
sed '/.[18]$/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Fix doxygen glitches
for f in globus_gram_job_manager_configuration.3 \
	 globus_gram_job_manager_job_execution_environment.3 \
	 globus_gram_job_manager_rsl_validation_file.3 ; do
  sed 's/P\.RS/P\n.RS/' -i %{buildroot}%{_mandir}/man3/$f
done

# Devel package is redundant
rm %{buildroot}%{_libdir}/libglobus_seg_job_manager.so
rm $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist
rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_%{flavor}_dev.gpt

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | sed -e 's!/man/.*!&*!' -e s!^!%{_prefix}! \
        -e 's!%{_prefix}%{_sysconfdir}!%config(noreplace) %{_sysconfdir}!' \
  > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

# Add logging
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/globus
cat %{SOURCE1} >> $RPM_BUILD_ROOT%{_sysconfdir}/globus/globus-gram-job-manager.conf

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/globus
chmod 01777 $RPM_BUILD_ROOT%{_localstatedir}/log/globus 

# Add user-editable RVF file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram/job-manager.rvf

%clean
rm -rf %{buildroot}

%preun
if [[ $1 -ge 1 ]]; then # upgrade
    echo Killing job-managers
    killall -v globus-job-manager || /bin/true
fi

%post
/sbin/ldconfig
if [[ $1 -gt 1 ]]; then # upgrade
    echo Killing job-managers
    killall -v globus-job-manager || /bin/true
fi

%postun -p /sbin/ldconfig

%files -f package.filelist
%dir %{_datadir}/globus/%{_name}
%config(noreplace) %{_sysconfdir}/logrotate.d/globus-job-manager
%dir %{_localstatedir}/lib/globus
%dir %{_localstatedir}/lib/globus/gram_job_state
%dir %{_localstatedir}/log/globus
%config(noreplace) %{_sysconfdir}/globus/globus-gram-job-manager.conf
%config(noreplace) %{_sysconfdir}/globus/gram/job-manager.rvf
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README

%files -f package-doc.filelist doc
%dir %{_pkgdocdir}/html

%changelog
* Thu Mar 13 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 13.53-1.3.osg
- Add fix for SOFTWARE-1418 / GT-520 (crashing issue with state files that
  don't have the client address in them)

* Mon Dec 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 13.53-1.2.osg
- Bump and rebuild with OpenSSL 1.0.0

* Wed Dec 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 13.53-1.1.osg
- Merge OSG changes
- Remove gt-286-missing-normalize.patch (fixed upstream)
- Remove gt-311-memory-leak.patch (fixed upstream)

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.53-1
- Update to Globus Toolkit 5.2.5

* Wed Sep 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 13.45-1.6.osg
- Don't trigger GRAM's own log rotation in logrotate (SOFTWARE-1083)

* Tue Sep 10 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 13.45-1.5.osg
- Change logrotate config to use copytruncate (SOFTWARE-1083)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.51-4
- Implement updated packaging guidelines

* Tue Jun 04 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 13.45-1.4.osg
- Add patch from GT-311 (memory leak)

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.51-3
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.51-1
- Update to Globus Toolkit 5.2.3

* Fri Nov 02 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.45-1.3.osg
- Add placeholder file for user-editable job-manager.rvf

* Wed Aug 15 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.45-1.2.osg
- Added patch from GT-268 (GRAM job manager seg module fails to replay first log of the month on restart)

* Sun Jul 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.48-1
- Update to Globus Toolkit 5.2.2
- Drop patch globus-gram-job-manager-porting.patch (fixed upstream)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Alain Roy <roy@cs.wisc.edu> - 13.45-1.1.osg
- Merged upstream changes from 13.45-1

    * Wed Jun 13 2012 Joseph Bester <bester@mcs.anl.gov> - 13.45-1
    - GT-225: GRAM5 skips some SEG events

    * Wed Jun 06 2012 Joseph Bester <bester@mcs.anl.gov> - 13.44-1
    - GT-157: Hash gram_job_state directory by user

    * Fri Jun 01 2012 Joseph Bester <bester@mcs.anl.gov> - 13.43-1
    - GT-214: Leaks in the job manager restart code

    * Thu May 24 2012 Joseph Bester <bester@mcs.anl.gov> - 13.42-1
    - GT-209: job manager crash in query

    * Tue May 22 2012 Joseph Bester <bester@mcs.anl.gov> - 13.41-1
    - GT-199: GRAM audit checks result username incorrectly
    - GT-192: Segfault in globus-gram-streamer

    * Fri May 18 2012 Joseph Bester <bester@mcs.anl.gov> - 13.40-1
    - GT-149: Memory leaks in globus-job-manager
    - GT-186: GRAM job manager leaks condor log path
    - GT-187: GRAM job manager leaks during stdio update
    - GT-189: GRAM job manager regular expression storage grows
    - GT-190: GRAM job manager leaks callback contact

* Mon Jun 4 2012 Alain Roy <roy@cs.wisc.edu> - 13.39-0.3.osg
- Added patches to fix memory leaks (from GT-214)

* Wed May 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.39-0.2.osg
- Remove duplicated line in globus-gram-job-manager.conf

* Tue May 22 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.39-0.1.osg
- New version with a fix for GT-149
- Remove unneeded osg patches

* Thu May 10 2012 Alain Roy <roy@cs.wisc.edu> - 13.35-0.4.osg
- Patch for GT-155 (Don't delete directories for jobs owned by other users)

* Thu May 10 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 13.35-0.3.osg
- Do not try to fast-shutdown the globus-job-manager.  See GT-156.

* Thu May 10 2012 Alain Roy <roy@cs.wisc.edu> - 13.35-0.2.osg
- Patched to fix GT-154 (Kill off idle Perl processes to save memory)

* Fri May 04 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.35-0.1.osg
- New version with a fix for GRAM-345

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.33-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gram-job-manager-deps.patch (fixed upstream)

* Wed Apr 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.34-0.1.osg
- New version with a real fix for GRAM-329
- Removed recreate-lockfile.patch, no longer applies
- Removed fix-poll-interval.patch, in upstream
- Removed close-rvf-file.patch, in upstream
- Removed condor-seg-nullptr.patch, in upstream

* Wed Apr 04 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.23-0.11.osg
- Add patch for GRAM-329

* Wed Mar 21 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 13.23-0.10.osg
- Attempt to fix null ptr deref in Condor SEG.

* Fri Mar 16 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 13.23-0.9.osg
Suppress Globus 129 for the client for now.

* Thu Mar 15 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.23-0.8.osg
- use killall instead of pkill for killing g-j-m processes

* Wed Mar 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.23-0.7.osg
- kill globus-job-manager processes on upgrade (SOFTWARE-561)

* Tue Mar 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.23-0.6.osg
- rebuilt

* Sun Mar 11 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 13.23-0.5.osg
- Allow globus-job-manager to restart taking jobs after a proxy expired.

* Fri Mar 09 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 13.23-0.4.osg
- Avoid filehandle leaks.

* Fri Mar 09 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 13.23-0.3.osg
- Restore functionality of the poll-interval-increase patch (GRAM-273).

* Thu Mar 08 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 13.23-0.2.osg
- Attempt to recreate missing locks if possible.

* Thu Mar 08 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 13.23-0.1.osg
- New version with a fix for GRAM-317
- Remove recvmsg_eagain.patch (in upstream)

* Mon Jan 30 2012 Alain Roy <roy@cs.wisc.edu> - 13.14-1.2.osg
- Fixed log rotation so there's no failure if the job manager isn't running. 

* Wed Jan 18 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.14-2
- Add missing BuildRequires: globus-common-progs and libxml2-devel
- Portability fixes
- Fix broken links in README file

* Mon Dec 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.14-1.1.osg
- Merge OSG changes
- Remove unneeded OSG patches:
  - condor-poll-GRAM-271.patch
  - GRAM-273-ignore-logs.patch
  - request-lock.patch
  - GRAM-275-logfile-names.patch
  - SOFTWARE-393.patch
  - GRAM-282-sigusr1_logrotate.patch
- Remove OSG-provided logrotate conf

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 13.14-1
- Update to Globus Toolkit 5.2.0
- Drop patches globus-gram-job-manager-doxygen.patch,
  globus-gram-job-manager.patch, globus-gram-job-manager-pathmax.patch and
  globus-gram-job-manager-undefined.patch (fixed upstream)

* Thu Dec 08 2011 Joseph Bester <bester@mcs.anl.gov> - 13.14-1
- Fix some cases of multiple submits of a GRAM job to condor

* Wed Dec 07 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-14.osg
- Remove watchdog timer patch; seems to be doing more harm than good in non-threaded mode.

* Wed Dec 07 2011  <bester@centos55.local> - 13.13-1
- GRAM-292: GRAM crashes when parsing partial condor log

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 13.12-2
- Update for 5.2.0 release

* Thu Dec 01 2011 Joseph Bester <bester@mcs.anl.gov> - 13.12-1
- GRAM-289: GRAM jobs resubmitted

* Wed Nov 30 2011 Alain Roy <roy@cs.wisc.edu> - 13.5-13.osg
- Updated logrotate to send SIGUSR1 to globus-job-manger processes

* Tue Nov 29 2011 Alain Roy <roy@cs.wisc.edu> - 13.5-12.osg
- Restart the jobmanagers state machine in a 'safe' state.
- Add hooks to job manager to handle log rotation
- Reduce default logging level

* Mon Nov 28 2011 Joseph Bester <bester@mcs.anl.gov> - 13.11-1
- GRAM-286: Set default jobmanager log in native packages
- Add gatekeeper and psmisc dependencies

* Tue Nov 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.5-11.osg
- Added patch to fix logfiles with garbage names getting created (GRAM-275)

* Mon Nov 21 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.5-10.osg
- Enabled logging by default.

* Mon Nov 21 2011 Alain Roy <roy@cs.wisc.edu> - 13.5-9.osg
- Added patch to fix lock confusion (update to fix from -8)
- Added patch to fix security context memory leak. 
- Configure logging

* Mon Nov 21 2011 Joseph Bester <bester@mcs.anl.gov> - 13.10-1
- GRAM-282: Add hooks to job manager to handle log rotation

* Sat Nov 19 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-8
- If holding the wrong lock file, make sure to close the fd.

* Mon Nov 14 2011 Joseph Bester <bester@mcs.anl.gov> - 13.9-1
- GRAM-271: GRAM Condor polling overpolls

* Sun Nov 13 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-7.osg
- Reduce the polling frequency and load of the condor job manager.

* Fri Nov 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-6.osg
- Make job home different from job lock dir.

* Wed Nov 09 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-5.osg
- No longer reload Condor logfiles every 5 seconds.

* Wed Nov 09 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-4.osg
- Fix the globus-job-dir option in the job manager.

* Mon Nov 07 2011 Joseph Bester <bester@mcs.anl.gov> - 13.8-1
- GRAM-268: GRAM requires gss_export_sec_context to work

* Fri Oct 28 2011 Joseph Bester <bester@mcs.anl.gov> - 13.7-1
- GRAM-266: Do not issue "Error locking file" warning if another jobmanager
  exists

* Wed Oct 26 2011 Joseph Bester <bester@mcs.anl.gov> - 13.6-1
- GRAM-265: GRAM logging.c sets FD_CLOEXEC incorrectly

* Mon Oct 24 2011 Joseph Bester <bester@mcs.anl.gov> - 13.5-2
- set aclocal_includes="-I ." prior to bootsrap

* Thu Oct 20 2011 Joseph Bester <bester@mcs.anl.gov> - 13.5-1
- GRAM-227: Manager double-locked

* Tue Oct 18 2011 Joseph Bester <bester@mcs.anl.gov> - 13.4-1
- GRAM-262: job manager -extra-envvars implementation doesn't match description

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 13.3-2
- Add explicit dependencies on >= 5.2 libraries

* Tue Oct 04 2011 Joseph Bester <bester@mcs.anl.gov> - 13.3-1
- GRAM-240: globus_xio_open in script code can recurse

* Thu Sep 22 2011  <bester@mcs.anl.gov> - 13.2-1
- GRAM-257: Set default values for GLOBUS_GATEKEEPER_*

* Thu Sep 22 2011 Joseph Bester <bester@mcs.anl.gov> - 13.1-1
- Fix: GRAM-250

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 13.0-2
- Update for 5.1.2 release
  
* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 12.10-2.osg
- Forward-port OSG patches.

* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.70-1
- Update to Globus Toolkit 5.0.4
- Fix doxygen markup

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.67-3
- Add README file

* Tue Apr 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.67-2
- Updated patch

* Thu Feb 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.67-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 18 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.59-2
- Move client and server man pages to main package

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.59-1
- Update to Globus Toolkit 5.0.2

* Sat Jun 05 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.42-2
- Additional portability fixes

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.42-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.17-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.15-1
- Autogenerated
