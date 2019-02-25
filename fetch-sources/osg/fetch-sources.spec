# Instructions:
#
# After this is built and tested, tag it into dist-$el-build (where $el is el6
# or el7 or whatever other el is in use).  Then _untag it_ from the development
# repos you built it into and wait for kojira to regenerate all the build
# repos.  The untag step is important to prevent a stale fetch-sources in a
# development tag from overriding a newer fetch-sources in the dist-$el-build
# tag.

Summary:   Fetch sources from upstream (internal use)
Name:      fetch-sources
Version:   1.14.1
Release:   1%{?dist}
License:   Apache License, 2.0
Source0:   %{name}
BuildArch: noarch
BuildRequires: osg-build-base >= %{version}
Requires: git
Requires: python-six
Requires: subversion

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

%files
%{_bindir}/%{name}
/usr/share/fetch-sources

%changelog
* Mon Feb 25 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.14.1-1
- Rebuild against osg-build 1.14.1

* Wed Mar 14 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.12.2-1
- Rebuild against osg-build 1.12.2 (SOFTWARE-3172)
- Change version to match version of osg-build it's built against

* Wed Jan 24 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2.1-3
- Rebuild against osg-build 1.11.2

* Tue Jan 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2.1-2
- Rebuild against osg-build 1.11.1

* Tue Jan 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2.1-1
- Work around bug due to using relative paths

* Tue Jan 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2.0-1
- Rebuild based on osg-build 1.10.90 prerelease, with support for taking
  specfiles from git repos (SOFTWARE-2962)
- Add python-six dependency

* Tue May 09 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1.0-2
- Require git and subversion so that they're available in the buildSRPMFromSCM task
  (technically, subversion is already in there thanks to the Koji group, but better safe than sorry)

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

