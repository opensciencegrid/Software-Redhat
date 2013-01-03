Summary: Environment wrapper scripts for gLExec
Name: glexec-wrapper-scripts
Version: 0.0.7
Release: 1.1%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: Applications/System
URL: http://wiki.nikhef.nl/grid/GLExec_Environment_Wrap_and_Unwrap_scripts
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: glexec

%description
Helper scripts to restore the environment variables previously wrapped into the
environment variable GLEXEC_ENV using the glexec_wrapenv.pl script.

%prep
%setup -q

%build
%configure

make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sbindir}/glexec_wrap.sh
%{_sbindir}/glexec_warp.sh
%{_sbindir}/glexec_wrapenv.pl
%{_sbindir}/glexec_unwrapenv.pl
%{_datadir}/man/man1/glexec_wrap.sh.1*
%{_datadir}/man/man1/glexec_warp.sh.1*
%{_datadir}/man/man1/glexec_wrapenv.pl.1*
%{_datadir}/man/man1/glexec_unwrapenv.pl.1*
%doc AUTHORS LICENSE README

%changelog
* Thu Jan 03 2013 Dave Dykstra <dwd@fnal.gov> 0.0.7-1.1.osg
- Update upstream version

* Wed Oct 24 2012 Mischa Salle <msalle@nikhef.nl> 0.0.7-1
- Update build procedure.
- Update files.
- Update URL.

* Tue Mar 27 2012 Mischa Salle <msalle@nikhef.nl> 0.0.6-2
- Make source location valid url

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 0.0.6-1.2.osg
- Rebuild after merging into trunk

* Mon Feb 27 2012 Dave Dykstra <dwd@fnal.gov> 0.0.6-1.1.osg
- Import into OSG

* Tue Jan 31 2012 Mischa Salle <msalle@nikhef.nl> 0.0.6-1
- Bump version

* Tue Dec 21 2011 Mischa Salle <msalle@nikhef.nl> 0.0.5-3
- Updating summary

* Tue Dec 20 2011 Mischa Salle <msalle@nikhef.nl> 0.0.5-2
- Updating Group

* Tue Dec 20 2011 Mischa Salle <msalle@nikhef.nl> 0.0.5-1
- Initial version.
