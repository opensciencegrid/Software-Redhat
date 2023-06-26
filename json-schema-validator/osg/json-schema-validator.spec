%global srcname json-schema-validator
%global pkgname %{srcname}

Name:           %{pkgname}
Version:        2.2.0
Release:        1%{?dist}
Summary:        JSON Schema Validator

License:        MIT
URL:            https://github.com/pboettch/json-schema-validator

Source0:        %{pkgname}-%{version}.tar.gz
Source1:        json.hpp

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  cmake-rpm-macros

%description
JSON Schema Validator is a library for validating JSON data against JSON Schema.

%prep
%autosetup -n %{srcname}-%{version}
cp %{SOURCE1} .

%build
mkdir -p build
cd build
%cmake ..
%make_build

%install
cd build
%make_install

%files
#%license LICENSE
%{_includedir}/%{pkgname}/
%{_includedir}/nlohmann/

%changelog
* Mon Jun 26 2023 Justin Hiemstra <jhiemstra@morgridge.org> - %{version}-%{release}
- Initial RPM release
