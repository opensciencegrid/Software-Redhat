Summary: Create the VOMS directory containing the LSC files
Name: osg-make-vomsdir
Version: 1.0.0
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
* Thu Jun 09 2011 Igor Sfiligoi - 1.0.0-1
- Initial spec file
