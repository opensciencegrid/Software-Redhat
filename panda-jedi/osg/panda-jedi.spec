%define name panda-jedi
%define version 0.0.1.35
%define unmangled_version 0.0.1.35
%define release 1

Summary: JEDI Package
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Panda Team <atlas-adc-panda@cern.ch>
Packager: Panda Team <atlas-adc-panda@cern.ch>
Provides: panda-jedi
Requires: python panda-common panda-server
Url: https://twiki.cern.ch/twiki/bin/view/Atlas/PanDA

%description
This package contains JEDI components

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
