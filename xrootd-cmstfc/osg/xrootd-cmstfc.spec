Name: xrootd-cmstfc
Version: 1.5.2
Release: 9%{?dist}
Summary: CMS TFC plugin for xrootd

Group: System Environment/Daemons
License: BSD
URL: https://github.com/bbockelm/xrootd-cmstfc
# Generated from:
# git-archive master | gzip -7 > ~/rpmbuild/SOURCES/xrootd-lcmaps.tar.gz
Source0: %{name}.tar.gz
Patch0: buff_size.patch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?rhel} > 8
# EL 9 switched the default cmake invocation to do out-of-source builds;
# this causes the build to "cd" into a "redhat-linux-build" directory
# and then not find the Makefile.
# Go back to in-source builds.
%global __cmake_in_source_build 1
%endif

%define xrootd_current_major 5
%define xrootd_next_major 6

BuildRequires: xrootd-devel >= 1:%{xrootd_current_major}.0.0-1
BuildRequires: xrootd-devel <  1:%{xrootd_next_major}.0.0-1
BuildRequires: pcre-devel

BuildRequires: xerces-c-devel

BuildRequires: cmake
#BuildRequires: xrootd-compat-libs

Requires: /usr/bin/xrootd pcre xerces-c
#Requires: xrootd-compat-libs

#%if 0%%{?rhel} < 7
#Requires: xrootd4 >= 1:4.1.0
#%else
Requires: xrootd >= 1:%{xrootd_current_major}.0.0-1
Requires: xrootd <  1:%{xrootd_next_major}.0.0-1
#%endif

%package devel
Summary: Development headers and libraries for Xrootd CMSTFC plugin
Group: System Environment/Development

%description
%{summary}

%description devel
%{summary}

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p1
 
%build
cd %{name}-%{version}
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_LIBDIR=%{_lib} .
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libXrdCmsTfc.so
%if 0%{?rhel} < 8
%{_libdir}/libXrdCmsTfc.so.*
%endif
%files devel
%defattr(-,root,root,-)
%{_includedir}/XrdCmsTfc.hh

%changelog
* Wed Sep 24 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 1.5.2-9
- Bump to rebuild for x86_64 on EL10

* Wed Jun 4 2024 Matt Westphall <westphall@wisc.edu> - 1.5.2-8
- Bump release to test new build targets (SOFTWARE-5702)

* Fri Jul 28 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.5.2-7
- Fix cmake build fail on EL9 (SOFTWARE-5631)

* Thu Oct 22 2020 Diego Davila <didavila@ucsd.edu> - 1.5.2-6
- Build for el8 (software-4257)
- Adding patch: buff_size.patch to avoid compiling error
- Adding if around libXrdCmsTfc.so.* in the 'files' section

* Mon Apr 13 2020 Diego Davila <didavila@ucsd.edu> - 1.5.2-5
- Rebuild against xrootd 5.0.0-rc2 (SOFTWARE-3923)

* Thu Jul 18 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.5.2-4
- Rebuild against xrootd 4.10.0 (SOFTWARE-3697)

* Wed Apr 24 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.5.2-3
- Rebuild against xrootd 4.9.1 (SOFTWARE-3678)

* Wed Feb 27 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.5.2-2
- Rebuild against xrootd 4.9.0 (SOFTWARE-3485)

* Wed Sep 05 2018 Edgar Fajardo <emfajard@ucsd.edu> 1.5.2-1
- Small change to reduce the logging verbosity of this plugin for the DPM team.

* Tue Aug 08 2017 Brian Lin <blin@cs.wisc.edu> 1.5.1-11%{?dist}
- Build libraries into the appropriate shared lib arch path

* Mon Feb 23 2015 Edgar Fajardo <emfajard@ucsd.edu> 1.5.1-10%{?dist}
- Require xrootd (instead of xrootd4) for all builds

* Fri Dec 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.1-9%{?dist}
- Require xrootd (instead of xrootd4) on EL7

* Mon Jul 14 2014 Edgar Fakardo <efajardo@physics.ucsd.edu> - 1.5.1-8
- Rebuild against xrootd4 and fixed xrootd4 requirements

* Thu Apr 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.5.1-6
- Require and BuildRequire xrootd 3.3.1 explicitly

* Wed Apr 03 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.5.1-4
- Bump to rebuild against xrootd 3.3.1
- Rename xrootd-libs-devel dependency to match what 3.3.1 calls it

* Thu Nov 29 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.5.1-3
- Move module back into base RPM.

* Mon Nov 12 2012 Brian Bockelman - 1.5.1-1
- Fix SL6 compilation issues.

* Mon Oct 22 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.5-1
- Switch to cmake.
- Rebuild against Xrootd 3.3.

* Wed May 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.3-1
- Apply path matching only at the beginning of the path.

* Mon Mar 28 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.2-2
- Rebuild to reflect the updated RPM names.

* Wed Sep 29 2010 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.2-1
- Reduce verbosity of the logging.
- Fix for TFC parsing to better respect rule order; request from Florida.

* Tue Aug 24 2010 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.0-1
- Break xrootd-cmstfc off into its own standalone RPM.

