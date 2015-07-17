Summary: Create the VOMS directory containing the LSC files
Name: osg-make-vomsdir
Version: 1.0.1
Release: 1%{?dist}
License: Apache License, 2.0
Group: Applications/Grid
Packager: VDT <vdt-support@opensciencegrid.org>
Source0: %{name}-%{version}.tar.gz
AutoReq: yes
AutoProv: yes
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
The tool creates the LSC files in the voms directory
by contacting all the VOMS servers listed
in a user-provided vomses file.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/%{name}

%changelog
* Wed Feb 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0.1-1
- Bugfix update: use ports specified in vomses file instead of hardcoded 8443
- Also, use --vomsdir from command line instead of hardcoded "vomsdir"

* Thu Jun 09 2011 Igor Sfiligoi - 1.0.0-1
- Initial spec file
