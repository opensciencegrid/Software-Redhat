Summary: StashCache client tools
Name: stashcache-client
Version: 6.1.0
Release: 1%{?dist}
License: Apache 2.0
Url: https://github.com/opensciencegrid/StashCache
BuildArch: noarch
Source0: StashCache-%{version}.tar.gz
%if 0%{?rhel} < 8
BuildRequires: python2-setuptools
Requires: python2-setuptools
%else
BuildRequires: python3-setuptools
Requires: python3-setuptools
%endif
Requires: curl
Requires: xrootd-client
Provides: stashcp = %{version}-%{release}

%if 0%{?rhel} >= 8
%define __python /usr/bin/python3
%endif

%description
stashcp allows users to copy files out of the OSG StashCache data federation.

%prep
%autosetup -n StashCache-%{version}

%build
%if 0%{?rhel} < 8
%py2_build
%else
%py3_build
%endif

%install
%if 0%{?rhel} < 8
%py2_install
%else
%py3_install
%endif

%files
%if 0%{?rhel} < 8
%{python2_sitelib}/*
%else
%{python3_sitelib}/*
%endif
%{_bindir}/stashcp
%{_datarootdir}/stashcache/opensciencegrid.org.pub

%changelog
* Fri Sep 11 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.1.0-1
- Update to 6.1.0.  This release changes the behavior of stashcp to use
  multiple caches and never go back to the origin.  (SOFTWARE-4255)

* Thu Jul 16 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.0.0-1
- Update to 6.0.0.  This release adds Python 3 support and changes the
  statistics collector to collector.atlas-ml.org

* Thu May 14 2020 Dave Dykstra <dwd@fnal.gov> - 5.6.1-1
- Update to 5.6.1.  Add back support for /etc/stashcache/caches.json to
  override default list.

* Wed May 13 2020 Dave Dykstra <dwd@fnal.gov> - 5.6.0-1
- Update to 5.6.0.  Downloads lists of caches instead of having them
  included in the package.

* Thu Apr 23 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.5.0-3
- Build for EL 8 (SOFTWARE-4050)

* Fri Oct 11 2019 Diego Davila <didavila@ucsd.edu> - 5.5.0-2
- Adding "Requires: python2-setuptools" (SOFTWARE-3799)

* Wed Oct 2 2019 Diego Davila <didavila@ucsd.edu> - 5.5.0-1
- Update to 5.5.0
- Use python macros to install

* Wed Dec 12 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.2.0-1
- Update to 5.2.0

* Tue Dec 04 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-5
- Fix crash when we can't look up any caches with GeoIP

* Tue Oct 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-4
- Make a failure when querying the origin for the file size not fatal

* Tue Oct 23 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-3
- Rename to stashcache-client
- Add readme file for caches.json

* Fri Oct 12 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-2
- Package caches.json

* Thu Oct 11 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.1.0-1
- Initial packaging

