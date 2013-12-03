Name:		java7-compat
Version:	0.1
Release:	1%{?dist}
Summary:	Requires java >= 1:1.7.0 and provides java7
BuildArch:	noarch
Group:		Development/Tools
License:	Freeware
Requires:	java >= 1:1.7.0
Provides:	java7 = 1:1.7.0

%description
%{summary}

%package -n java7-devel-compat
Summary:	Requires java-devel >= 1:1.7.0 and provides java7-devel
Group:		Development/Tools
Requires:	java-devel >= 1:1.7.0
Provides:	java7-devel = 1:1.7.0

%description -n java7-devel-compat
%{summary}

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%files -n java7-devel-compat

%changelog
* Mon Dec 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.1-1
- Initial version

