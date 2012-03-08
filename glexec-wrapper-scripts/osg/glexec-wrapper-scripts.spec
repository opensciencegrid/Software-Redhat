Summary: Environment wrapper scripts for gLExec
Name: glexec-wrapper-scripts
Version: 0.0.6
Release: 1.2%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: Applications/System
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

%description
Helper scripts to restore the environment variables previously wrapped into the
environment variable GLEXEC_ENV using the glexec_wrapenv.pl script.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 *.pl *.sh $RPM_BUILD_ROOT%{_sbindir}
ln -s -f glexec_wrap.sh $RPM_BUILD_ROOT%{_sbindir}/glexec_warp.sh

%files
%defattr(-,root,root,-)
%{_sbindir}/glexec_wrap.sh
%{_sbindir}/glexec_warp.sh
%{_sbindir}/glexec_wrapenv.pl
%{_sbindir}/glexec_unwrapenv.pl
%doc README_glexecwrappers

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
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
