Summary: Process tracking plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-glexec-tracking
Version: 0.1.6
Release: 1%{?dist}
License: EGEE Middleware and ASL and Fermitools
Group: System Environment/Libraries
# The tarball was created from CVS using the following commands:
# cd /afs/cs.wisc.edu/p/vdt/public/html/upstream
# cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only export -d lcmaps-plugins-glexec-tracking-0.1.6 -r lcmaps-plugins-glexec-tracking_R_0_1_6 privilege/lcmaps-plugins-glexec-tracking
# mkdir lcmaps-plugins-glexec-tracking/0.1.6
# tar zcf lcmaps-plugins-glexec-tracking/0.1.6/lcmaps-plugins-glexec-tracking-0.1.6.tar.gz lcmaps-plugins-glexec-tracking-0.1.6/
# rm -rf lcmaps-plugins-glexec-tracking-0.1.6
Source0: %{name}-%{version}.tar.gz
BuildRequires: lcmaps-interface
BuildRequires: libtool automake autoconf
Requires: /usr/sbin/condor_procd
Requires: /usr/sbin/gidd_alloc
Requires: /usr/sbin/procd_ctl
Requires: python
Requires: lcmaps%{?_isa} >= 1.5.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This plugin utilizes the Condor procd to track the processes spawned
by glexec.

%prep
%setup -q -a0


%build
./bootstrap
%configure --disable-static --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/lcmaps/lcmaps_glexec_tracking.mod
%{_libdir}/lcmaps/liblcmaps_glexec_tracking.so
%{_sbindir}/glexec_monitor

%changelog
* Thu Feb 21 2013 Dave Dykstra <dwd@fnal.gov> 0.1.6-1.osg
- Pull in another upstream version which undoes the last version's changes
  because I found out those "unhelpful" messages were needed by the glexec
  gratia probe.

* Thu Jan 03 2013 Dave Dykstra <dwd@fnal.gov> 0.1.5-1.osg
- Pull in new upstream version which moves some unhelpful log NOTICE
  startup messages to INFO level

* Thu Dec 27 2012 Dave Dykstra <dwd@fnal.gov> 0.1.4-3.osg
- Remove %{_libdir}/modules symlink and corresponding %ghost files
- Change the Requires: lcmaps to be like the other lcmaps plugins and
    instead be Requires: lcmaps%{?_isa} >= 1.5.0

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 0.1.4-2.osg
- Rebuild after merging from branches/lcmaps-upgrade to trunk

* Thu Feb 09 2012 Dave Dykstra <dwd@fnal.gov> 0.1.4-1.osg
- Upgrade to upstream 0.1.4, which adds python option to ignore the
  deprecation warnings of using popen2 that otherwise print on sl6

* Fri Dec 30 2011 Dave Dykstra <dwd@fnal.gov> 0.1.3-1.osg
- Upgrade to upstream 0.1.3, which adds -log-facility option

* Wed Dec 28 2011 Dave Dykstra <dwd@fnal.gov> 0.1.2-1.osg
- Upgrade to upstream 0.1.2, which adds -log-level option and updates all
  log messages to be consistent with new lcmaps standard, and fixes a bug
  that prevented soft killing processes that outlive the main payload command
- Remove the *.so.0  and *.so.0.0.0 symlinks as has now been done for
  the other lcmaps plugins

* Mon Dec 12 2011 Dave Dykstra <dwd@fnal.gov> 0.1.1-1.osg
- Upgrade to upstream 0.1.1, which fixes a glexec hang when there are
  more than 5 open file descriptors passed in and fixes a problem with
  a debug log message that had newlines in it.
    http://jira.opensciencegrid.org/browse/SOFTWARE-423
    http://jira.opensciencegrid.org/browse/SOFTWARE-288

* Fri Dec 02 2011 Dave Dykstra <dwd@fnal.gov> 0.1.0-3.osg
- Add %ghost directories on the files in libdir/modules so rpm won't
   think it needs to remove them from a previous install

* Mon Nov 21 2011 Dave Dykstra <dwd@fnal.gov> 0.1.0-2.osg
- Move installed module from 'modules' libdir to 'lcmaps'

* Sun Nov 06 2011 Dave Dykstra <dwd@fnal.gov> 0.1.0-1.osg
 - Upgrade to upstream 0.1.0 which stops 2 significant race conditions
   in starting up condor_procd.
   http://jira.opensciencegrid.org/browse/SOFTWARE-337
   http://jira.opensciencegrid.org/browse/SOFTWARE-332

* Fri Oct 28 2011 Dave Dykstra <dwd@fnal.gov> 0.0.9-1
 - Upgrade to upstream 0.0.9 which fixes a significant bug where the
   tracking gid allocator process was killed too soon, making it possible
   for one glexec_monitor to kill the processes of a different glexec job.
   Also eliminates some scary-looking log messages that didn't indicate
   real problems.

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.8-2
- rebuilt

* Tue Oct 25 2011 Dave Dykstra <dwd@fnal.gov> 0.0.8-1
- Upgrade to upstream 0.0.8 which undoes a piece of the last patch in
  order to properly clean up orphaned processes, and also disconnects
  glexec_monitor from the process group and supplemental groups so it
  can survive batch system cleanups and nested glexec cleanups so it
  can stay around long enough to do its own cleanup as it should.
  See http://jira.opensciencegrid.org/browse/SOFTWARE-307 and
  http://jira.opensciencegrid.org/browse/SOFTWARE-283.

* Tue Aug 23 2011 Dave Dykstra <dwd@fnal.gov> 0.0.7-1
- Upgrade to upstream 0.0.7 which fixes process cleanup and exception
  handling.  It had been often leaving gidd_alloc processes around.
  Patch from Brian Bockelman.
- Remove glexec location patch that moves glexec.conf to /etc; no longer
  needed since it was put in upstream.

* Tue Aug 23 2011 Dave Dykstra <dwd@fnal.gov> 0.0.6-1
- Upgrade to upstream 0.0.6 which basically makes procd_ctl able to
  be in either bin or sbin whether or not -procddir is set

* Mon Jul 18 2011 Dave Dykstra <dwd@fnal.gov> 0.0.5-1
- Based on CVS with glexec-tracking name
- Make -procdir option default to '/usr', and if default is taken
  find procd_ctl in bin instead of sbin.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.4-2
- Include glexec_monitor in package.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.4-1
- Initial build.
