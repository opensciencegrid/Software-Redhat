# Have gitrev be the short hash or branch name if doing a prerelease build
#define gitrev

Name:           gridftp-hdfs
Version:        1.1.1
Release:        1.2%{?gitrev:.%{gitrev}git}%{?dist}
Summary:        HDFS DSI plugin for GridFTP
License:        ASL 2.0
URL:            https://github.com/opensciencegrid/gridftp_hdfs
# To create:
#   Release:
#     git archive --prefix=%{name}-%{version}/ v%{version} | gzip -n > %{name}-%{version}.tar.gz
#   Prerelease:
#     git archive --prefix=%{name}-%{version}/ %{gitrev} | gzip -n > %{name}-%{version}-%{gitrev}.tar.gz
Source0:        %{name}-%{version}%{?gitrev:-%{gitrev}}.tar.gz


BuildRequires: cmake

BuildRequires: java-devel >= 1:1.7.0
BuildRequires: jpackage-utils

BuildRequires: hadoop-libhdfs-devel
# globus-gridftp-server-devel-11 needed for 2436-enable-ordered-data.patch
BuildRequires: globus-gridftp-server-devel >= 11
BuildRequires: globus-common-devel

Requires: hadoop-libhdfs
Requires: hadoop-client >= 2.0.0+545
# ^ was getting "No FileSystem for scheme: hdfs" without this
# 6.14-2 added OSG plugin-style sysconfig instead of gridftp.conf.d
# 6.38-1.3 added /etc/gridftp.d
Requires: globus-gridftp-server-progs >= 6.38-1.3
Requires: xinetd
Requires: globus-gridftp-osg-extensions
Requires: java >= 1:1.7.0
Requires: jpackage-utils
# for ordered data support (SOFTWARE-2436):
BuildRequires: globus-ftp-control-devel >= 7.7
Requires: globus-ftp-control >= 7.7

Requires(pre): shadow-utils
Requires(preun): initscripts
Requires(postun): initscripts
Requires(postun): xinetd

%description
HDFS DSI plugin for GridFTP

%prep

%setup -q

%build

%cmake -DLIB_INSTALL_DIR=%{_libdir}

make %{?_smp_mflags}

%install

make DESTDIR=$RPM_BUILD_ROOT install

%post
/sbin/ldconfig

/sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :

%preun
if [ "$1" = "0" ] ; then
    /sbin/service xinetd condrestart >/dev/null 2>&1
    /sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
fi

%postun
/sbin/ldconfig
if [ "$1" -ge "1" ]; then
    /sbin/service xinetd condrestart >/dev/null 2>&1
    /sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_sbindir}/gridftp-hdfs-inetd
%{_bindir}/gridftp-hdfs-standalone
%{_libdir}/libglobus_gridftp_server_hdfs.so*
%{_datadir}/%{name}/%{name}-environment
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/gridftp-debug.conf
%config(noreplace) %{_sysconfdir}/%{name}/gridftp-inetd.conf
%config(noreplace) %{_sysconfdir}/%{name}/replica-map.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/gridftp.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/gridftp.d/%{name}.osg-extensions.conf
%{_datarootdir}/osg/sysconfig/globus-gridftp-server-plugin

%changelog
* Thu Jun 21 2018 Carl Edquist <edquist@cs.wisc.edu> - 1.1.1-1.2
- Rebuild against hadoop 2.6.0+cdh5 (SOFTWARE-3181)

* Tue Nov 14 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.1.1-1.1
- Merge OSG changes for version 1.1.1 (SOFTWARE-2999, SOFTWARE-2983)

* Thu Nov 09 2017 Carl Edquist <edquist@cs.wisc.edu> - 1.1-1.2
- Update hadoop build requirement (SOFTWARE-2983)

* Tue Nov 07 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 1.1.1-1
- Fix potential crash when requesting new checksum types.

* Thu Oct 26 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-1.1
- Merge OSG changes (osg-sysconfig.patch)

* Thu Oct 26 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 1.1-1
- Add support for CVMFS-style block checksums.
- Minor deadlock fixes contributed by JasonAlt.

* Tue Sep 05 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0-1.1
- Add osg-sysconfig.patch

* Thu Aug 24 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0-1
- Update to latest version from github (SOFTWARE-2856)
- Remove upstreamed patches

* Thu Dec 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-25.5
- Bump to rebuild against globus-gridftp-server 11.8 (SOFTWARE-2436)

* Fri Aug 26 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.5.4-25.4
- Add patch to enable ordered data (SOFTWARE-2436)
  - Adds dependency on globus-ftp-control >= 7.7
  - Adds build dependency on globus-gridftp-server >= 11

* Thu Jul 21 2016 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-25.3
- Config file fixes for globus-gridftp-osg-extensions (SOFTWARE-2397)

* Wed Jul 20 2016 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-25.2
- Use globus-gridftp-osg-extensions (SOFTWARE-2397)

* Thu Jun 30 2016 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.4-25.1
- Fix bug with listing empty directories.

* Mon Feb 22 2016 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-25.osg
- Rebuild against hadoop-2.0.0+1612 (SOFTWARE-2161)

* Tue Dec 22 2015  Edgar Fajardo <emfajard@ucsd.edu> - 0.5.4-24.osg
- Update to include the patch (SOFTWARE-2107) to deal with mkdir and rename

* Tue Dec 8 2015 Edgar Fajardo <emfajard@ucsd.edu> - 0.5.4-23.osg
- Update to include the patch (SOFTWARE-2115) to deal with load limits

* Wed Sep 2 2015 Edgar Fajardo <emfajard@ucsd.edu> - 0.5.4-22.osg
- Update to the patch (SOFTWARE-2011) to correctly deal when replication errors

* Mon Aug 31 2015 Edgar Fajardo <emfajard@ucsd.edu> - 0.5.4-21.osg
- Applied patch to capture stderr to the gridftp-auth log (SOFTWARE-2011)

* Mon Aug 24 2015 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.5-1
- Fix checksum verification with gfal2.

* Mon Aug 24 2015 Edgar Fajardo <emfajard@ucsd.edu> - 0.5.4-20.osg
- Changed checksum names (adler32, md5, etc) to be case-insensitive (SOFTWARE-2006)

* Tue Sep 30 2014 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-19.osg
- Limit concurrency to 1 for no-parallelism transfers (SOFTWARE-1495)

* Thu Jun 19 2014 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-18.osg
- Mutex fix for GLOBUS_THREAD_MODEL="pthread" (SOFTWARE-1495)

* Wed May 21 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.5.4-17.osg
- Remove rpath (SOFTWARE-1394)

* Wed Apr 16 2014 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-15.osg
- Remove conflicting /etc/gridftp.d notion from non-osg builds (SOFTWARE-1439)

* Wed Apr 09 2014 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-14.osg
- Move hdfs-specific config into /etc/gridftp.d (SOFTWARE-1439)

* Thu Apr 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-13.osg
- Update globus-gridftp-server version requirement (SOFTWARE-1412)

* Thu Mar 27 2014 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-12.osg
- Add 1412-gridftp_d.patch to use /etc/gridftp.d config dir (SOFTWARE-1412)

* Tue Mar 04 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 0.5.4-11.osg
- Add 1410-environment.patch to fix problem with not finding libjsig.so in systems with OpenJDK (SOFTWARE-1410)

* Wed Jan 15 2014 Matyas Selmeci <matyas@cs.wisc.edu> - 0.5.4-10.osg
- Merged upstream changes as of GT 5.2.5 (SOFTWARE-1317)
- Remove gridftp-hdfs-config.patch
- Remove gridftp-hdfs-classpath.patch

* Fri May 31 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.5.4-9
- Add hadoop-client dependency

* Thu May 30 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.5.4-8
- Bump to rebuild against hadoop 2.0 built with OpenJDK 7

* Tue Feb 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.5.4-7
- Update to build with OpenJDK 7; require java7-devel + jpackage-utils

* Tue Feb 19 2013 Dave Dykstra <dwd@fnal.gov> - 0.5.4-6.osg
- Change sysconfig arrangement to use /usr/share/osg/sysconfig
  for OSG replaceable additions, and /etc/sysconfig/gridftp-hdfs
  for non-replaceable variables specific to gridftp-hdfs.
  Always include /usr/share/osg/sysconfig/globus-gridftp-server
  environment, which also pulls in hdfs-specific variables via
  a plugin file.

* Wed Jan 23 2013 Doug Strain <dstrain@fnal.gov> - 0.5.4-5
- Rebuild for Gridftp 6.14

* Wed Aug 1 2012 Doug Strain <dstrain@fnal.gov> - 0.5.4-4
- Added patch to LD_LIBRARY_PATH for /usr/lib/hadoop/lib/native

* Thu Jul 19 2012 Doug Strain <dstrain@fnal.gov> - 0.5.4-3
- Changing requirements to use any version of libhdfs
- Also updating hdfsDelete and gridftp-hdfs-environment
- In preparation of hadoop-2.0.0 upgrade

* Wed May 30 2012 Doug Strain <dstrain@fnal.gov> - 0.5.3-6
- Patch to hdfs stat so it actually finds uid and gid
- Also, delete function was missing, so I wrote a DELE function
- Fixed mkdir that was using the wrong path
- This fixes uberftp issues

* Wed May 9 2012 Doug Strain <dstrain@fnal.gov> - 0.5.3-5
- Added new LCMAPs options to sysconfig
- Changed location of sysconfig information in standalone+inetd scripts

* Fri Apr 13 2012 Doug Strain <dstrain@fnal.gov> - 0.5.3-2
- Added dist tag
- Switched to using jdk for SL6

* Tue Dec 06 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.3-1
- Initial support for GlobusOnline.

* Sat Nov 19 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.2-1
- Implement checksum support for gridftp-hdfs.

* Sat Oct 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.1-1
Migrate as much of the RPM as possible to the OSG-style of gridftp initialization while maintaining GT 52 compatibility.

* Sat Sep 24 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.5.0-1
- Redo gridftp to allow either xinetd or init startup; link with GT 5.2.

* Mon Jun 6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.4.0-2
- Decrease logging verbosity.
- Make sure we always finish up the transfer.

* Mon Jun 6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.4.0-1
- Rewrite of send/recv to clean up logic and error handling.
- Should improve multithreaded performance.

* Thu Jun 2 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.2-2
- Remove dependency on gratia probe.

* Thu May 26 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.2-1
- Attempt to fix the race issue for closing files.

* Tue Apr 26 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.1-1
- Fix listing of empty directories; error is now higher in the globus stack
- Fix listed modes in stat.
- Make everything friendly to dumping cores.
- On segfaults, inetd now spews Java mess back to the client.

* Mon Apr 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.0-1
- Re-organize code and tighten up visibility rules.

* Mon Apr 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.4-1
- Implement "ls" on directories.

* Mon Apr 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-8
- Fix generation of debuginfo RPM.

* Fri Apr 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-7
- Destroy HDFS handle only if it was initialized.  Fixes segfault on auth failure.

* Wed Mar 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-6
- Add explicit dep for globus-common
- Rebuild to trigger a 32-bit build in Koji.

* Mon Jan 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-4
- Purposefully leak file handle due to lifetime and synchronization issues.

* Fri Dec 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.3-2
- Protect against a double-free if only one block is read.

* Wed Dec 15 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.2-1
- Update the bootstrapping scripts for the correct HADOOP_HOME
  and exporting CLASSPATH

* Sun Oct 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.1-2
- Update the bootstrapping scripts to include the JVM paths.
- Fix library names for flavourless-Globus

* Fri Oct 15 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.0-3
- Rebuild to create new Koji build.

* Tue Sep 28 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.0-2
- Update configurations to use GT5 GridFTP server from Fedora
- Include environment variables for LCMAPS/LCAS support

* Mon May 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.2.0-1
- Adjust build to depend on hadoop-0.20 RPM layout.
- Commit patches to upstream source.

* Fri Apr 9 2010 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-16
- Add extra debugging lines for file buffer creation to help diagnose
  mmap() failures.  Clean up file buffer if mmap() fails.
- Use MAP_SHARED instead of MAP_PRIVATE to ensure that changes are
  written to disk and memory is not exhausted.

* Wed Feb 10 2010 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-15
- Fix library name on 32-bit arch

* Fri Aug 21 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-14
- Add logrotate configuration file

* Mon Aug 17 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-13
- Add Requires: for osg-ca-certs and fetch-crl
- New upstream source fixing a potential seg fault

* Mon Jul 27 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-12
- Additional debugging lines.
- Add dependency on gratia probes

* Thu Jul 23 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-11
- New upstream sources with syslog fixes

* Sat Jul 4 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-10
- Add GRIDFTP_REPLICA_MAP env var for setting per-file replicas

* Thu Jul 2 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-9
- Move config files to /etc
- Allow local env settings in /etc/gridftp-hdfs/gridftp-hdfs-local.conf

* Thu Jul 2 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-8
- Restart xinetd after installing, but only if xinetd was already running

* Thu Jun 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-7
- Add hadoop environment setup to xinetd scripts

* Thu Jun 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-6
- Update to latest tarball that contains fixes for the so name

* Thu Jun 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-5
- Fix bug in postun
- Add Requires: prima

* Wed Jun 24 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-4
- Add Requires: gpt-postinstall so we know where the globus libraries are
  located
- Update source tarball to pick up xinetd service name change.

* Wed Jun 24 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-3
- Fix paths in inetd scripts
- Add explicit dependency on hadoop

* Wed Jun 24 2009 Michael Thomas <thomas@hep.caltech.edu> 0.1.0-2
- spec file cleanup

* Thu Jun 18 2009 Brian Bockelman <bbockelm@cse.unl.edu> 0.1.0-1
- Creation of GridFTP/HDFS plugin

