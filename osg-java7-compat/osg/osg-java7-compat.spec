Name:		osg-java7-compat
Version:	1.0
Release:	1%{?dist}
Summary:	Requires java >= 1:1.7.0 and provides java7
BuildArch:	noarch
Group:		Development/Tools
License:	ASL 2.0
Requires:	java >= 1:1.7.0
Provides:	java7 = 1:1.7.0

%description
This shim package requires java >= 1:1.7.0 and provides java7

It is intended to support osg packages that require java7, when the latest
available java package (eg, java-1.7.0-openjdk) may provide java = 1:1.7.0
but not java7.

%package -n osg-java7-devel-compat
Summary:	Requires java-devel >= 1:1.7.0 and provides java7-devel
Group:		Development/Tools
Requires:	java-devel >= 1:1.7.0
Provides:	java7-devel = 1:1.7.0

%description -n osg-java7-devel-compat
This shim package requires java-devel >= 1:1.7.0 and provides java7-devel

It is intended to support osg packages that require java7-devel, when the
latest available java-devel package (eg, java-1.7.0-openjdk-devel) may provide
java-devel = 1:1.7.0 but not java7-devel.

%package -n osg-java7-compat-openjdk
Summary:	Requires java-1.7.0-openjdk and provides java = 1:1.7.0
Group:		Development/Tools
Requires:	java-1.7.0-openjdk
Provides:	java = 1:1.7.0

%description -n osg-java7-compat-openjdk
This shim package requires java-1.7.0-openjdk and provides java = 1:1.7.0

It is intended to work around yum depsolving issues on platforms where the
latest available java package still provides java7 but not java = 1:1.7.0,
and where yum selects the osg-java7-compat package to satisfy a java7
requirement (for an osg package), instead of the actual java implementation.

In that undesirable case, yum would give up, not finding anything to provide
the java >= 1:1.7.0 required by osg-java7-compat.  This package forces
installing an actual java implementation (openjdk) and ensures that the
requirements of osg-java7-compat can always be met.

%package -n osg-java7-devel-compat-openjdk
Summary:	Requires java-1.7.0-openjdk-devel and provides java-devel = 1:1.7.0
Group:		Development/Tools
Requires:	java-1.7.0-openjdk-devel
Provides:	java-devel = 1:1.7.0

%description -n osg-java7-devel-compat-openjdk
This shim package requires java-1.7.0-openjdk-devel and provides java-devel = 1:1.7.0

It is intended to work around yum depsolving issues on platforms where the
latest available java-devel package still provides java7-devel but not
java-devel = 1:1.7.0, and where yum selects the osg-java7-devel-compat package
to satisfy a java7-devel requirement (for an osg package), instead of the
actual java-devel implementation.

In that undesirable case, yum would give up, not finding anything to provide
the java-devel >= 1:1.7.0 required by osg-java7-devel-compat.  This package
forces installing an actual java-devel implementation (openjdk-devel) and
ensures that the requirements of osg-java7-devel-compat can always be met.

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%files -n osg-java7-devel-compat
%files -n osg-java7-compat-openjdk
%files -n osg-java7-devel-compat-openjdk

%changelog
* Wed Dec 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0-1
- Initial release

