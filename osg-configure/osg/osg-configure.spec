%global name osg-configure
%global version 0.0.2
%global release 1%{?dist}

Summary: Package for configure-osg and associated scripts
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: Apache 2.0
Group: Grid
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Suchandra Thapa <sthapa@ci.uchicago.edu>
Url: http://www.opensciencegrid.org
Requires: python

%description
%{summary}

%prep
%setup

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/var/log/osg/
touch $RPM_BUILD_ROOT/var/log/osg/configure-osg.log

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%ghost /var/log/osg/configure-osg.log

%changelog
* Fri Jul  22 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.2-1
- Created initial configure-osg rpm using real source 

* Thu Jul  21 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.1-1
- Created an initial osg-configure RPM 
