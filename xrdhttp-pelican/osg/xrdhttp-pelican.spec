
Name: xrdhttp-pelican
Version: 0.0.4
Release: 1.1%{?dist}
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
%autosetup -p1

%build

%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo
pushd %__cmake_builddir
make VERBOSE=1 %{?_smp_mflags}
popd

%install
pushd %__cmake_builddir
make install DESTDIR=$RPM_BUILD_ROOT
popd

%files
%defattr(-,root,root,-)
%{_libdir}/libXrdHttpPelican-*.so

%changelog
* Thu Apr 17 2025 Matt Westphall <westphall@wisc.edu> - 0.0.4-1.1
- Update XRootD Dependency to 5.8.0 (SOFTWARE-6114)

* Sat Mar 1 2025 Brian Bockelman <bbockelman@morgridge.org> - 0.0.4-1
- Add ability to prestage and evict objects from cache.

* Mon Dec 23 2024 Brian Bockelman <bbockelman@morgridge.org> - 0.0.3-1
- First build of the xrdhttp-pelican plugin
