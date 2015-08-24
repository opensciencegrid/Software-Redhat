%define osg 1

Name:           gridftp-hdfs
Version:        0.5.4
Release:        20%{?dist}
Summary:        HDFS DSI plugin for GridFTP
Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://twiki.grid.iu.edu/bin/view/Storage/HadoopInstallation
Source0:        %{name}-%{version}.tar.gz
Source1: globus-gridftp-server-plugin.osg-sysconfig
Source2: %{name}.conf
%if 0%{?osg} > 0
Patch0: osg-sysconfig.patch
%endif
Patch1: hadoop200.patch
Patch2: gridftp-hdfs-link.patch
# OSG: we do not want this patch; it changes the format of the sysconfig file
# such that it will no longer be a valid shell script.
#Patch3: gridftp-hdfs-config.patch
Patch4: gridftp-hdfs-rpath.patch
Patch5: gridftp-hdfs-read_t.patch
Patch6: gridftp-hdfs-readsize.patch
# OSG: don't want this patch either -- was getting weird 'No such file or
# directory' errors with it in
#Patch7: gridftp-hdfs-classpath.patch
Patch8: gridftp-hdfs-automake-modernize.patch
Patch9: gridftp-hdfs-libjvm.patch
Patch10: gridftp-hdfs-uninitialized-result.patch
Patch11: 1410-java-environment.patch
Patch12: 1412-gridftp_d.patch
Patch13: 1495-pthread-mutex.patch
Patch14: 1495-optimal-concurrency.patch
Patch15: 2006-gridftp-hdfs-get-checksum.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

BuildRequires: java-devel >= 1:1.7.0
BuildRequires: jpackage-utils

BuildRequires: hadoop-libhdfs
BuildRequires: globus-gridftp-server-devel
BuildRequires: globus-common-devel

BuildRequires: chrpath

Requires: hadoop-libhdfs
Requires: hadoop-client >= 2.0.0+545
# ^ was getting "No FileSystem for scheme: hdfs" without this
# 6.14-2 added OSG plugin-style sysconfig instead of gridftp.conf.d
# 6.38-1.3 added /etc/gridftp.d
Requires: globus-gridftp-server-progs >= 6.38-1.3
%if 0%{?osg} > 0
Requires: xinetd
%endif
Requires: java >= 1:1.7.0
Requires: jpackage-utils

Requires(pre): shadow-utils
Requires(preun): initscripts
%if 0%{?osg} == 0
Requires(preun): chkconfig
Requires(post): chkconfig
%endif
Requires(postun): initscripts
%if 0%{?osg} > 0
Requires(postun): xinetd
%endif

%description
HDFS DSI plugin for GridFTP

%prep

%setup -q
%if 0%{?osg} > 0
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
##patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
##patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

aclocal
libtoolize
automake --foreign -a
autoconf

%build

%configure --with-java=/etc/alternatives/java_sdk

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Remove rpaths
chrpath -d $RPM_BUILD_ROOT%{_libdir}/*.so

# Remove libtool turds
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.d

# Remove the init script - in GT5.2, this gets bootstrapped appropriately
rm $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{name}
rm $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gridftp.conf.d/%{name}-environment-bootstrap

%if 0%{?osg} > 0
mv $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gridftp.conf.d/%{name} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/gridftp.conf.d
rm $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-hdfs/gridftp.conf
mkdir -p $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/globus-gridftp-server-plugin
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/gridftp.d
%else
rm $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-hdfs/gridftp-debug.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-hdfs/gridftp-inetd.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-hdfs/gridftp.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/gridftp-hdfs/replica-map.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/gridftp-hdfs
rm $RPM_BUILD_ROOT%{_bindir}/gridftp-hdfs-standalone
rm $RPM_BUILD_ROOT%{_sbindir}/gridftp-hdfs-inetd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%if 0%{?osg} > 0
/sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
%else
/sbin/chkconfig --add %{name}
%endif

%preun
if [ "$1" = "0" ] ; then
%if 0%{?osg} > 0
    /sbin/service xinetd condrestart >/dev/null 2>&1
%endif
    /sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
fi

%postun
/sbin/ldconfig
if [ "$1" -ge "1" ]; then
%if 0%{?osg} > 0
    /sbin/service xinetd condrestart >/dev/null 2>&1
%endif
    /sbin/service globus-gridftp-server condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%if 0%{?osg} > 0
%{_sbindir}/gridftp-hdfs-inetd
%{_bindir}/gridftp-hdfs-standalone
%endif
%{_libdir}/libglobus_gridftp_server_hdfs.so*
%{_datadir}/%{name}/%{name}-environment
%if 0%{?osg} > 0
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/gridftp-debug.conf
%config(noreplace) %{_sysconfdir}/%{name}/gridftp-inetd.conf
%config(noreplace) %{_sysconfdir}/%{name}/replica-map.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/gridftp.d/%{name}.conf
/usr/share/osg/sysconfig/globus-gridftp-server-plugin
%else
%config(noreplace) %{_sysconfdir}/sysconfig/gridftp.conf.d/%{name}
%endif

%changelog
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

