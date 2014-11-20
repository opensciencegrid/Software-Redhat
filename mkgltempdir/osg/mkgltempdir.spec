Summary: Create a directory owned by the gLExec target user
Name: mkgltempdir
Version: 0.0.4
Release: 1.1%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: Applications/System
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: glexec

%description
Helper script to create a secure temporary directory owned by the gLExec target
user for use by the payload.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%files
%defattr(-,root,root,-)
%{_sbindir}/mkgltempdir
%{_datadir}/man/man8/mkgltempdir.8*
%doc README AUTHORS LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Nov 20 2014 Jose Caballero <jcaballero@bnl.gov> - 0.0.4-1.1
  Bumped to 0.0.4-1

* Thu Jan 03 2013 Dave Dykstra <dwd@fnal.gov> 0.0.3-4.1
- Import into OSG

* Wed Oct 24 2012 Mischa Salle <msalle@nikhef.nl> 0.0.3-4
- Update URL field.

* Tue Mar 27 2012 Dennis van Dok <dennisvd@nikhef.nl> 0.0.3-3
- Make source into URL

* Wed Feb  1 2012 Dennis van Dok <dennisvd@nikhef.nl> 0.0.3-2
- Updated for autoconfigured package
- Added manpage and README

* Wed Dec 21 2011 Mischa Salle <msalle@nikhef.nl> 0.0.3-1
- Initial version.
