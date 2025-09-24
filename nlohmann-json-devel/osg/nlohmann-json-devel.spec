%global srcname nlohmann-json-devel
%global pkgname %{srcname}

Name:           %{pkgname}
Version:        3.12.0
Release:        2%{?dist}
Summary:        JSON Library for C++

License:        MIT
URL:            https://github.com/nlohmann/json

Source0:        json-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildArch: noarch

%description
A JSON library for C++ that attempts to make JSON a first-class type

%global debug_package %{nil}

%if 0%{?rhel} > 8
%global __cmake_in_source_build 1
%endif

%prep
%autosetup -n json-%{version}

%build
mkdir -p build
cd build
%cmake ..
%make_build

%install
cd build
%make_install

%files
%{_includedir}/nlohmann/
/usr/share/cmake/nlohmann_json/nlohmann_jsonConfig.cmake
/usr/share/cmake/nlohmann_json/nlohmann_jsonConfigVersion.cmake
/usr/share/cmake/nlohmann_json/nlohmann_jsonTargets.cmake
/usr/share/pkgconfig/nlohmann_json.pc

%changelog
* Wed Sep 24 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 3.12.0-2
- Build 3.12.0 as noarch

* Wed Sep 18 2024 Justin Hiemstra <jhiemstra@wisc.edu> - 3.11.2-2
- Bump release version for building against aarch64

* Mon Jun 26 2023 Justin Hiemstra <jhiemstra@morgridge.org> - 3.11.2-1
- Initial RPM release
