%define name panda-common
%define version 0.0.5.3
%define unmangled_version 0.0.5.3
%define release 0.3

Summary:  PanDA Common Package
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{unmangled_version}.tar.gz
Patch0: setup.patch
Patch1: templates.patch
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Panda Team <hn-atlas-panda-pathena@cern.ch>
Packager: Panda Team <hn-atlas-panda-pathena@cern.ch>
Provides: panda-common
Requires: python
Url: https://twiki.cern.ch/twiki/bin/view/Atlas/PanDA

%description
This package contains PanDA Common Components

%prep
%setup -n %{name}-%{unmangled_version}
%patch0 -p1
%patch1 -p1

%build
python setup.py build
#rename .rpmnew. . templates/*.rpmnew.template

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%config(noreplace) /etc/panda/panda_common.cfg

