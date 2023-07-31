Name:           osg-build-deps
Version:        3
Release:        2%{?dist}
Summary:        Dependencies for build tools for the OSG

License:        Apache 2.0
URL:            https://github.com/opensciencegrid/osg-build

BuildArch:      noarch

Source1:        install-osg-build.sh
Requires:       %{name}-base = %{version}
Requires:       %{name}-mock = %{version}
Requires:       %{name}-koji = %{version}

%if (0%{?fedora} >= 31 || 0%{?rhel} >= 8)
%define __python /usr/bin/python3
%else
%define __python /usr/bin/python2
%endif


%description
%{summary}
See %{url} for details.


%package base
%if 0%{?rhel} < 8
Requires:       git
%else
Requires:       git-core
%endif
Requires:       rpm-build
Requires:       quilt
Requires:       rpmlint
Requires:       subversion
Requires:       wget
Requires:       epel-rpm-macros
%if 0%{?rhel} < 8
Requires:       python >= 2.6
Requires:       python-six
%endif
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
Requires:       koji >= 1.13.0
Requires:       voms-clients-cpp
Requires:       grid-certificates
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
* Sun Jul 30 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3-2
- voms-proxy-init needs grid certificates

* Sun Jul 30 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3-1
- Fix creation of subpackages
- Add an install script

* Thu Jun 10 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 2-1
- Initial release, based on osg-build 1.18.0  (SOFTWARE-4659)

