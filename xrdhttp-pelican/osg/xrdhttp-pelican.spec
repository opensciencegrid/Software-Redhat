
Name: xrdhttp-pelican
Version: 0.0.3
Release: 1.1%{?dist}
Summary: A Pelican-specific plugin for the XrdHttp server

Group: System Environment/Daemons
License: BSD
URL: https://github.com/pelicanplatform/xrdhttp-pelican
# Generated from:
# git archive --format tar.gz v%{version} --prefix=xrdhttp-pelican-%{version}/ > ~/rpmbuild/SOURCES/xrdhttp-pelican-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz
# https://github.com/PelicanPlatform/xrdhttp-pelican/pull/8
Patch: PelicanPlatform-8-versioninfo.patch

%define xrootd_current_major 5
%define xrootd_current_minor 7
%define xrootd_next_minor 8

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
* Tue Jan 14 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 0.0.3-1.1
- Add PelicanPlatform-8-versioninfo.patch to initialize version info in the plugin

* Mon Dec 23 2024 Brian Bockelman <bbockelman@morgridge.org> - 0.0.3-1
- First build of the xrdhttp-pelican plugin

