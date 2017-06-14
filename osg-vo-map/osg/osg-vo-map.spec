Name: osg-vo-map
Summary: OSG utilities for creating VO map files
Version: 0.0.2
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
* Mon Nov 14 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 0.0.2-1
- Fix month in log timestamps (SOFTWARE-2520)

* Fri Jul  1 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.1-1
- Created an initial osg-vo-map RPM for

# vim:ft=spec
