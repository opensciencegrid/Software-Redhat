Name: xrootd-lcmaps
Version: 1.2.0
Release: 1.1%{?dist}
Summary: LCMAPS plugin for xrootd

Group: System Environment/Daemons
License: BSD
URL: https://github.com/bbockelm/xrootd-lcmaps
Source0: %{name}-%{version}.tar.gz
Patch0: lcmaps-modules-path.patch
Patch1: CMakeLists.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: xrootd-devel >= 1:4.1.0
BuildRequires: xrootd-server-libs >= 1:4.1.0
BuildRequires: xrootd-server-devel >= 1:4.1.0
BuildRequires: lcmaps-interface
BuildRequires: lcmaps
BuildRequires: cmake


Requires: xrootd >= 1:4.1.0

Requires: lcas-lcmaps-gt4-interface

%description
%{summary}

%prep
%setup -q

%patch0 -p0
%patch1 -p1

%build
%cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo .

make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group xrootd >/dev/null || groupadd -r xrootd
getent passwd xrootd >/dev/null || \
       useradd -r -g xrootd -c "XRootD runtime user" \
       -s /sbin/nologin -d /etc/xrootd xrootd


%files
%defattr(-,root,root,-)
# We keep the .so here (and not in a -devel subpackage) because it is actually
# a shared library.
%{_libdir}/libXrdLcmaps.so
%{_libdir}/libXrdLcmaps.so.0
%{_libdir}/libXrdLcmaps.so.0.0.2
%defattr(644,root,root,-)
%config(noreplace) %{_sysconfdir}/xrootd/lcmaps.cfg

%changelog
* Thu Jan 14 2016 Edgar Fajardo <emfajard@ucsd.edu> - 1.2.0-1.1
- Bumped to 1.2.0
- Added patch to CMakeLists to build for rhel7

* Thu Jan 14 2016 Brian Bockelman <bbockelm@cse.unl.edu> - 1.2.0-1
- Have VOMS attributes forward to the xrootd credential.

* Tue Jan 12 2016 Edgar Fajardo <emfajard@ucsd.edu> 1.0.1-1
- Change to the CMakeList to make rhel7 builds work

* Wed Jan 6 2016 Edgar Fajardo <emfajard@ucsd.edu> 1.0.0-1
- Update to 1.0.0
- Support for HTTP Security extractor
- Removed the patch1 for xrootd4 linking

* Wed Feb 25 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.0.7-11.osg
- Patch to not require xrootd-compat-libs

* Tue Feb 24 2015 Edgar Fajardo <emfajard@ucsd.edu>  0.0.7-10
- The xrootd-compat-libs were only needed at built time not required during installation

* Mon Feb 23 2015 Edgar Fajardo <emfajard@ucsd.edu>  0.0.7-9
- Require xrootd-compat-libs for upgrade to xrootd4.1

* Fri Dec 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 0.0.7-8
- Require xrootd on EL7

* Mon Jul 14 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> 0.0.7-7
- Updated to require xrootd4.

* Thu Apr 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.7-5
- Explicitly Require and BuildRequire xrootd 3.3.1

* Wed Apr 03 2013 Matyas Selmeci <matyas@cs.wisc.edu> 0.0.7-4
- Fix lcmaps modules path in lcmaps.cfg
- Add lcas-lcmaps-gt4-interface as a dependency
- Rebuild with xrootd 3.3.1; adjust dependencies to match

* Tue Feb 12 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.7-3
- Bump to rebuild against xrootd-3.3.0-rc3

* Tue Nov 20 2012 Doug Strain <dstrain@fnal.gov> - 0.0.7-2
- Fix permissions of lcmaps.cfg

* Mon Nov 19 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.7-1
- Fix config parsing issues.

* Mon Nov 12 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.6-1
- Fix SL6 compilation issues.

* Mon Oct 22 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.5-1
- Switch to cmake.

* Mon Feb 13 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.4-1
- Various bugfixes from Matevz Tadel.

* Fri Sep 16 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.3-1
- Updated to match mapping callout found in Xrootd 3.1.

* Tue May 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.2-6
- Update RPM deps for CERN-based xrootd RPM.

* Wed Mar 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.2-5
- Update Koji for 32-bit build.

* Fri Dec 24 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.2-4
- Update sample config line based on xrootd 3.0.0 final plugin code.

* Mon Sep 20 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.2-3
- Update dependency info based on Mock/Koji errors.
- Added some forgotten plugin deps.

* Fri Sep 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.2-1
- Add the sample LCMAPS configuration.
- Updated to the new tarball.  Calls the LCMAPS library directly instead of via helpers.

* Fri Sep 17 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-4
- Recompile for new LCMAPS library.
- Try and fix C++ vs C linker issues.
- Link in all the required lcmaps libraries.

* Thu Sep 16 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-1
- Initial integration of LCMAPS into Xrootd.

