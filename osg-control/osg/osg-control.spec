Name: osg-control
Version: 1.0.1
Release: 1%{?dist}
Summary: Wrapper for managing osg-configure services
Group: Grid
License: Apache 2.0
URL: https://vdt.cs.wisc.edu/svn/software/osg-control/
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Requires: python
Requires: osg-configure


%description
osg-control is a python wrapper script built on top of osg-configure to
manage the system services listed with "osg-configure --enabled-services"

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 osg-control $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sbindir}/osg-control

%changelog
* Thu Oct 23 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.1-1
- Update to 1.0.1 -- supports start/stop dependency order (SOFTWARE-1640)

* Mon Aug 26 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0-1
- 1.0 release

* Thu Aug 08 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.1-1
- Initial pre-release of osg-control

