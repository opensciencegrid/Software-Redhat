
Name: xrdhttp-pelican
Version: 0.0.7
Release: 1%{?dist}
Summary: A Pelican-specific plugin for the XrdHttp server

Group: System Environment/Daemons
License: BSD
URL: https://github.com/pelicanplatform/xrdhttp-pelican
# Generated from:
# git archive --format tar.gz v%{version} --prefix=xrdhttp-pelican-%{version}/ > ~/rpmbuild/SOURCES/xrdhttp-pelican-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

%define xrootd_current_major 5
%define xrootd_current_minor 8
%define xrootd_next_minor 9

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# Since we rely on the private headers, we don't want the plugin to cross
# unknown feature release versions.
BuildRequires: xrootd-devel >= 1:%{xrootd_current_major}.%{xrootd_current_minor}.0
BuildRequires: xrootd-devel <  1:%{xrootd_current_major}.%{xrootd_next_minor}.0
BuildRequires: xrootd-private-devel
BuildRequires: gcc-c++
BuildRequires: cmake

Requires: xrootd-client >= 1:%{xrootd_current_major}.%{xrootd_current_minor}
Requires: xrootd-client <  1:%{xrootd_current_major}.%{xrootd_next_minor}.0

%description
%{summary}

%prep
%setup -q

%build

%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo
pushd %__cmake_builddir
make VERBOSE=1 %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd %__cmake_builddir
make install DESTDIR=$RPM_BUILD_ROOT
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libXrdHttpPelican-*.so

%changelog
* Mon Jul 7 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 0.0.7-1
- Move authfile and SciTokens config file into the directories owned by xrootd user

* Thu Apr 24 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 0.0.6-1
- Fix EL8 builds

* Tue Apr 22 2025 Matyas Selmeci <mselmeci@wisc.edu> - 0.0.5-1
- Require XRootD 5.8
 
* Sat Mar 1 2025 Brian Bockelman <bbockelman@morgridge.org> - 0.0.4-1
- Add ability to prestage and evict objects from cache.

* Mon Dec 23 2024 Brian Bockelman <bbockelman@morgridge.org> - 0.0.3-1
- First build of the xrdhttp-pelican plugin
