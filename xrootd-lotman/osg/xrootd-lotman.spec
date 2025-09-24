Name:           xrootd-lotman
Version:        0.0.5
Release:        1.1%{?dist}
Summary:        A purge plugin for XRootD that uses Lotman's tracking for informed cache disk management

License:        Apache-2.0
URL:            https://github.com/PelicanPlatform/xrootd-lotman
Source0:        https://github.com/PelicanPlatform/xrootd-lotman/archive/v%{version}/xrootd-lotman-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  lotman
BuildRequires:  nlohmann-json-devel
BuildRequires:  xrootd-server-devel >= 1:5.8

%description
This package provides a purge plugin for XRootD that uses Lotman's tracking for informed purges.

%prep
%setup -q -n xrootd-lotman-%version

%build

%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libXrdPurgeLotMan.so*
%{_includedir}/XrdPurgeLotMan.hh
%{_includedir}/XrdPurgeLotManUtils.hh

%changelog
* Wed Sep 24 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 0.0.5-1.1
- Bump to rebuild for x86_64 on EL10

* Mon Jul 14 2025 Justin Hiemstra <jhiemstra@wisc.edu> - 0.0.5-1
- Fix broken RPM (forgot to package new header files)

* Mon Jul 14 2025 Justin Hiemstra <jhiemstra@wisc.edu> - 0.0.4-1
- Add level-based logging and handle XRootD reporting negative blocks

* Fri Apr 18 2025 Justin Hiemstra <jhiemstra@wisc.edu> - 0.0.3-1
- Update included headers to reflect upstream changes

* Wed Apr 16 2025 Matyas Selmeci <mselmeci@wisc.edu> - 0.0.2-2
- Require XRootD 5.8 for the build

* Thu Sep 19 2024 Justin Hiemstra <jhiemstra@wisc.edu> - 0.0.2-1
- Fixes to packaging and better CMake error messages

* Tue Aug 27 2024 Justin Hiemstra <jhiemstra@wisc.edu> - 0.0.1-1
- Initial package
