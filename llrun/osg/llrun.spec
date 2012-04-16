Summary: Performs a test run for LCAS and/or LCMAPS
Name: llrun
Version: 0.1.3
Release: 1.3%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: Applications/System
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: lcmaps

%description
The llrun tool is meant to debug or test LCAS and/or LCMAPS configuration files.
It essentially does a full run, without any of the security settings and
precautions used by e.g. gLExec.

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
%{_sbindir}/llrun
%{_datadir}/man/man1/llrun.1*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Apr 16 2012 Dave Dykstra <dwd@fnal.gov> 0.1.3-1.3.osg
- Add lcmaps dependency

* Thu Mar 08 2012 Mischa Salle <msalle@nikhef.nl> 0.1.3-1.2.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Mon Mar 5 2012 Mischa Salle <msalle@nikhef.nl> 0.1.3-1.1.osg
- Imported to OSG

* Mon Mar 5 2012 Mischa Salle <msalle@nikhef.nl> 0.1.3-1
- Updating version
- do not install AUTHORS and LICENSE files.

* Sun Mar 4 2012 Mischa Salle <msalle@nikhef.nl> 0.1.2-1
- Initial version.
