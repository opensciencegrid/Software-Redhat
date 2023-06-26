%global srcname nlohmann-json-devel
%global pkgname %{srcname}

Name:           %{pkgname}
Version:        3.11.2
Release:        1%{?dist}
Summary:        JSON Library for C++

License:        MIT
URL:            https://github.com/nlohmann/json

Source0:        %{pkgname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
A JSON library for C++ that attempts to make JSON a first-class type

%global debug_package %{nil}

%if 0%{?rhel} > 8
%global __cmake_in_source_build 1
%endif

%prep
%autosetup -n %{srcname}-%{version}

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
* Mon Jun 26 2023 Justin Hiemstra <jhiemstra@morgridge.org> - 3.11.2-1
- Initial RPM release
