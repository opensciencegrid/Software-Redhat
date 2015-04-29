Name: osg-vo-map
Summary: OSG utilities for creating VO map files
Version: 0.0.1
License: Apache 2.0
Release: 1%{?dist}
Group: Grid
URL: http://www.opensciencegrid.org
BuildArch: noarch
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: perl

%description
Package with the OSG utilities to generate and check VO map files. 


%prep
%setup -q

%build
exit 0


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sbindir}/check-vo-map
%{_sbindir}/generate-vo-map
%doc %{_docdir}/%{name}/README

%changelog
* Fri Jul  1 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.1-1
- Created an initial osg-vo-map RPM for 

# vim:ft=spec
