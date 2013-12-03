Name:		osg-java7-compat
Version:	0.1
Release:	2%{?dist}
Summary:	Requires java >= 1:1.7.0 and provides java7
BuildArch:	noarch
Group:		Development/Tools
License:	Freeware
Requires:	java >= 1:1.7.0
Provides:	java7 = 1:1.7.0
Conflicts:	java-1.7.0-openjdk < 1.7.0.45-2.4.3.3
#Conflicts:	java7-1.7.0 > 1:1.7.0

%description
%{summary}

%package -n osg-java7-devel-compat
Summary:	Requires java-devel >= 1:1.7.0 and provides java7-devel
Group:		Development/Tools
Requires:	java-devel >= 1:1.7.0
Provides:	java7-devel = 1:1.7.0
Conflicts:	java-1.7.0-openjdk-devel < 1.7.0.45-2.4.3.3
#Conflicts:	java7-1.7.0 > 1:1.7.0

%description -n osg-java7-devel-compat
%{summary}

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%files -n osg-java7-devel-compat

%changelog
* Tue Dec 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.1-2
- Add Conflicts for java-1.7.0-openjdk versions that provide java7

* Mon Dec 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.1-1
- Initial version

