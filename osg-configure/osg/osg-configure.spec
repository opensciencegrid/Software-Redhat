Name: osg-configure
Summary: OSG configure script
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
%{summary}


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
%{_sysconfdir}/osg/config.ini
%config(noreplace) %{_sysconfdir}/osg/config.ini

%changelog
* Fri Jul  1 2011 Suchandra Thapa <sthapa@ci.uchicago.edu> 0.0.1-1
- Created an initial osg-configure RPM 

# vim:ft=spec
