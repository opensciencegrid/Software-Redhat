Summary:   Fetch sources from upstream (internal use)
Name:      fetch-sources
Version:   1.1.0
Release:   1%{?dist}
License:   Apache License, 2.0
Group:     Applications/Grid
Source0:   %{name}
BuildArch: noarch
BuildRequires: osg-build-base >= 1.8.92

%description
Fetches sources from upstream directory
For OSG internal use only.

%prep
exit 0

%install
mkdir -p $RPM_BUILD_ROOT/usr/share/fetch-sources/osgbuild
cp %{python_sitelib}/osgbuild/*.py $RPM_BUILD_ROOT/usr/share/fetch-sources/osgbuild/

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT/%{_bindir}/%{name}

# Put the build version into the script
osgbuild_version=$(osg-build --version)
sed -i -e "s|@OSGBUILDVERSION@|${osgbuild_version}|" $RPM_BUILD_ROOT/%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/%{name}
/usr/share/fetch-sources

%changelog
* Thu Apr 27 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1.0-1
- Bundle osg-build libraries so we aren't sensitive to new versions of osg-build in the development repos (SOFTWARE-2711)
- Improve logging

* Wed Apr 26 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.0-2
- Require osg-build instead of osg-build-base so we don't bring in mock (SOFTWARE-2642)

* Wed Apr 05 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.0-1
- Rewrite based on fetch_sources.py from osg-build (SOFTWARE-2642)

* Fri Jul 11 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.0.1-3
- Bump to rebuild

* Mon Feb 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.1-2
bumped

* Fri Dec 02 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.0.1-1
Created

