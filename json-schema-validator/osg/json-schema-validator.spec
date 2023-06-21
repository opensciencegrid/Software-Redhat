%global srcname json-schema-validator
%global pkgname %{srcname}

Name:           %{pkgname}
Version:        2.2.0
Release:        1%{?dist}
Summary:        JSON Schema Validator

License:        MIT
URL:            https://github.com/pboettch/json-schema-validator

Source0:        %{pkgname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
JSON Schema Validator is a library for validating JSON data against JSON Schema.

%prep
%autosetup -n %{srcname}-%{version}

%build
mkdir -p build
cd build
%cmake ..
%cmake_build

%install
cd build
%cmake_install

# Copy nlohmann/json headers
mkdir -p %{buildroot}/%{_includedir}/nlohmann
cp -r %{_builddir}/%{pkgname}-%{version}/third_party/nlohmann_json/single_include/nlohmann/* %{buildroot}/%{_includedir}/nlohmann/

%files
%license LICENSE
%{_includedir}/%{pkgname}/
%{_includedir}/nlohmann/

%changelog
* Sun Jun 21 2023 Your Name <your.email@example.com> - %{version}-%{release}
- Initial RPM release
