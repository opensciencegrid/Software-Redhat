%{?suse_version:%define dist .suse%suse_version}

Summary: CernVM File System Authz Helper
Name: cvmfs-x509-helper
Version: 2.2
# The release_prefix macro is used in the OBS prjconf, don't change its name
%define release_prefix 3
Release: %{release_prefix}%{?dist}
Source0: https://ecsft.cern.ch/dist/cvmfs/%{name}-%{version}.tar.gz
Group: Applications/System
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: globus-common-devel
BuildRequires: globus-gsi-callback-devel
BuildRequires: globus-gsi-cert-utils-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: globus-gsi-sysconfig-devel
BuildRequires: libuuid-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: voms-devel
BuildRequires: scitokens-cpp-devel

Requires: cvmfs >= 2.6.0

%if 0%{?rhel} > 8
%global __cmake_in_source_build 1
%endif

%description
Authorization helper to verify X.509 proxy certificates, VOMS membership, and scitokens for
the CernVM-FS client.
See http://cernvm.cern.ch
Copyright (c) CERN

%prep
%setup -q

%build
%ifarch i386 i686
export CXXFLAGS="`echo %{optflags}|sed 's/march=i386/march=i686/'`"
export CFLAGS="`echo %{optflags}|sed 's/march=i386/march=i686/'`"
%endif

%if 0%{?suse_version}
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr .
%else
%cmake .
%endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
/usr/libexec/cvmfs/authz/cvmfs_x509_helper
/usr/libexec/cvmfs/authz/cvmfs_x509_validator
/usr/lib64/libcvmfs_scitoken_helper.so
/usr/libexec/cvmfs/authz/cvmfs_scitoken_helper
%doc COPYING AUTHORS README ChangeLog

%changelog
* Tue Mar 21 2023 Matyas Selmeci <matyas@cs.wisc.edu> - 2.2-3
- Fix build failure on EL9 by doing an in-source build

* Mon Aug 23 2021 Dave Dykstra <dwd@fnal.gov> - 2.2-2
- Forgot to reset the revision to 1; now make it match

* Mon Aug 23 2021 Dave Dykstra <dwd@fnal.gov> - 2.2-1
- Prevent exiting after the first token authentication
- Close token file descriptor after use
- Enable token debug messages
- Implement WLCG bearer token discovery standard
- Add libscitokens-dev build dependency on debian

* Thu Sep 19 2019 Dave Dykstra <dwd@fnal.gov> - 2.1-2
- Change cvmfs requirement to >= 2.6.0 for SciTokens support

* Thu Sep 12 2019 Dave Dykstra <dwd@fnal.gov> - 2.1-1
- Fix bug preventing from running unprivileged

* Tue May 14 2019 Derek Weitzel <dweitzel@unl.edu> - 2.0-1
- Add SciTokens support

* Sat Jul 28 2018 Brian Bockelman <bbockelm@cse.unl.edu> - 1.1-1
- Fix file descriptor leak.

* Fri Nov 03 2017 Dave Dykstra <dwd@fnal.gov> - 1.0-2
- Add %release_prefix macro to support openSUSE Build System

* Thu Apr 06 2017 Dave Dykstra <dwd@fnal.gov> - 1.0-1
- Use the same root / $CWD as the target process.  Without this, the
  authz process may utilize the incorrect file for target processes
  that are in a chroot or provide a relative path for the X509 proxy.

* Fri Apr 22 2016 Jakob Blomer <jblomer@cern.ch> - 0.9-1
- Initial packaging
