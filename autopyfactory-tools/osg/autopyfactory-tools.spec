%define name autopyfactory-tools
%define version 1.0.3
%define unmangled_version 1.0.3
%define release 1

Summary: autopyfactory-tools package
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Jose Caballero <jcaballero@bnl.gov>
Packager: APF Team <autopyfactory-l@lists.bnl.gov>
Provides: autopyfactory-tools
#Requires: autopyfactory
Obsoletes: panda-autopyfactory-tools
Url: https://twiki.grid.iu.edu/bin/view/Documentation/Release3/AutoPyFactoryTools

%description
This package contains autopyfactory utils

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%pre
#!/bin/bash


%post
#!/bin/bash


%preun
#!/bin/bash


%files -f INSTALLED_FILES
%defattr(-,root,root)

