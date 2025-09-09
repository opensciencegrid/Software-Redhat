Name:           osg-build-deps
Version:        6
Release:        1%{?dist}
Summary:        Dependencies for build tools for the OSG

License:        Apache 2.0
URL:            https://github.com/osg-htc/osg-build

BuildArch:      noarch

Source1:        install-osg-build.sh
Requires:       %{name}-base = %{version}
Requires:       %{name}-mock = %{version}
Requires:       %{name}-koji = %{version}

%define __python /usr/bin/python3


%description
%{summary}
See %{url} for details.


%package base
Requires:       git-core
Requires:       rpm-build
# quilt is not (yet) available on EL10
Recommends:     quilt
Requires:       rpmlint
Requires:       subversion
Requires:       wget
Requires:       epel-rpm-macros
Requires:       make
Summary:        osg-build-deps base package, not containing deps for mock or koji modules or koji-based tools

%description base
%{summary}
Installing this package will enable use of osg-build and osg-import-srpm.
osg-build will be able to do rpmbuilds and run the lint and quilt tasks.
osg-build-deps-mock is required to use the mock task, and
osg-build-deps-koji is required to use the koji task.


%package mock
Requires:       %{name}-base = %{version}
Requires:       mock >= 2.1
Summary:        osg-build-deps for the mock plugin, allows builds with mock

%description mock
%{summary}


%package koji
Requires:       %{name}-base = %{version}
Requires:       openssl
Requires:       koji >= 1.33.0
Requires:       krb5-workstation
Summary:        osg-build-deps for the Koji plugin and Koji-based tools

%description koji
%{summary}
Installing this package will enable the use of the 'osg-build koji' task
and the following tools:
- koji-blame
- koji-tag-diff
- osg-koji
- osg-promote



%install
install -d %{buildroot}/usr/sbin
install -m 0755 %{SOURCE1} %{buildroot}/usr/sbin/install-osg-build.sh



%files
%files base
/usr/sbin/install-osg-build.sh
%files mock
%files koji


%changelog
* Tue Jul 15 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 6-1
- Update requirements for kerberos-based auth
- Turn quilt into a soft dependency because it is not yet available on EL10

* Wed Jul 03 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 5-1
- Switch default osg-build branch in install script to V2-branch
- Remove el7 compat from spec file

* Tue Sep 19 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 4-1
- Allow selecting osg-build branch and repo in install script

* Sun Jul 30 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3-3
- voms-proxy-init needs grid certificates
- install script needs make

* Sun Jul 30 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3-1
- Fix creation of subpackages
- Add an install script

* Thu Jun 10 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 2-1
- Initial release, based on osg-build 1.18.0  (SOFTWARE-4659)
