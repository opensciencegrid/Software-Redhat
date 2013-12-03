Name:		osg-java7-compat
Version:	0.1
Release:	3%{?dist}
Summary:	Requires java >= 1:1.7.0 and provides java7
BuildArch:	noarch
Group:		Development/Tools
License:	Freeware
Requires:	java >= 1:1.7.0
Provides:	java7 = 1:1.7.0

%description
%{summary}

%package -n osg-java7-devel-compat
Summary:	Requires java-devel >= 1:1.7.0 and provides java7-devel
Group:		Development/Tools
Requires:	java-devel >= 1:1.7.0
Provides:	java7-devel = 1:1.7.0

%description -n osg-java7-devel-compat
%{summary}

%package -n osg-java7-compat-openjdk
Summary:	Requires java-1.7.0-openjdk and provides java
Group:		Development/Tools
Requires:	java-1.7.0-openjdk
Provides:	java = 1:1.7.0

%description -n osg-java7-compat-openjdk
%{summary}

%package -n osg-java7-devel-compat-openjdk
Summary:	Requires java-1.7.0-openjdk-devel and provides java-devel
Group:		Development/Tools
Requires:	java-1.7.0-openjdk-devel
Provides:	java-devel = 1:1.7.0

%description -n osg-java7-devel-compat-openjdk
%{summary}

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%files -n osg-java7-devel-compat
%files -n osg-java7-compat-openjdk
%files -n osg-java7-devel-compat-openjdk

%changelog
* Tue Dec 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.1-3
- Scrap conflicts, which didn't help
- Add additional helper sub-packages to bring in openjdk/-devel

* Tue Dec 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.1-2
- Add Conflicts for java-1.7.0-openjdk versions that provide java7

* Mon Dec 02 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.1-1
- Initial version

