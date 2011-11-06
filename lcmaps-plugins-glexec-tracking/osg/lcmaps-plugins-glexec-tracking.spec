Summary: Process tracking plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-glexec-tracking
Version: 0.1.0
Release: 1%{?dist}
License: EGEE Middleware and ASL and Fermitools
Group: System Environment/Libraries
# The tarball was created from CVS using the following commands:
# cd /afs/cs.wisc.edu/p/vdt/public/html/upstream
# cvs -d :pserver:anonymous@cdcvs.fnal.gov:/cvs/cd_read_only export -d lcmaps-plugins-glexec-tracking-0.1.0 -r lcmaps-plugins-glexec-tracking_R_0_1_0 privilege/lcmaps-plugins-glexec-tracking
# mkdir lcmaps-plugins-glexec-tracking/0.1.0
# tar zcf lcmaps-plugins-glexec-tracking/0.1.0/lcmaps-plugins-glexec-tracking-0.1.0.tar.gz lcmaps-plugins-glexec-tracking-0.1.0/
# rm -rf lcmaps-plugins-glexec-tracking-0.1.0
Source0: %{name}-%{version}.tar.gz
BuildRequires: lcmaps-interface
BuildRequires: libtool automake autoconf
Requires: /usr/sbin/condor_procd
Requires: /usr/sbin/gidd_alloc
Requires: /usr/sbin/procd_ctl
Requires: python
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
mv $RPM_BUILD_ROOT/%{_libdir}/lcmaps $RPM_BUILD_ROOT/%{_libdir}/modules
ln -s liblcmaps_glexec_tracking.so $RPM_BUILD_ROOT/%{_libdir}/modules/liblcmaps_glexec_tracking.so.0
ln -s liblcmaps_glexec_tracking.so.0 $RPM_BUILD_ROOT/%{_libdir}/modules/liblcmaps_glexec_tracking.so.0.0.0
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/modules/lcmaps_glexec_tracking.mod
%{_libdir}/modules/liblcmaps_glexec_tracking.so
%{_libdir}/modules/liblcmaps_glexec_tracking.so.0
%{_libdir}/modules/liblcmaps_glexec_tracking.so.0.0.0
%{_sbindir}/glexec_monitor

%changelog
* Sun Nov 06 2011 Dave Dykstra <dwd@fnal.gov> 0.0.10-1.osg
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
