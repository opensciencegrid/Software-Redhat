
Name: xrootd-cmstfc
Version: 1.5.1
Release: 9%{?dist}
Summary: CMS TFC plugin for xrootd

Group: System Environment/Daemons
License: BSD
URL: https://github.com/bbockelm/xrootd-cmstfc
# Generated from:
# git-archive master | gzip -7 > ~/rpmbuild/SOURCES/xrootd-lcmaps.tar.gz
Source0: %{name}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: xrootd-devel >= 1:4.0.0
BuildRequires: xerces-c-devel pcre-devel
BuildRequires: cmake
Requires: /usr/bin/xrootd pcre xerces-c
%if 0%{?rhel} < 7
Requires: xrootd4 >= 1:4.0.0
%else
Requires: xrootd >= 1:4.0.0
%endif

%package devel
Summary: Development headers and libraries for Xrootd CMSTFC plugin
Group: System Environment/Development

%description
%{summary}

%description devel
%{summary}

%prep
%setup -q -c -n %{name}-%{version}

%build

%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libXrdCmsTfc.so.*
%{_libdir}/libXrdCmsTfc.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/XrdCmsTfc.hh

%changelog
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

