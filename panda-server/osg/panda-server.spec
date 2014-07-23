%define name panda-server
%define version 0.0.20.28
%define unmangled_version 0.0.20.28.mysql
%define release 1

Summary:  PanDA Server Package
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
Packager: Panda Team <hn-atlas-panda-pathena@cern.ch>
Provides: panda-server
Requires: python panda-common
Url: https://twiki.cern.ch/twiki/bin/view/Atlas/PanDA

%description
This package contains PanDA Server Components

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
