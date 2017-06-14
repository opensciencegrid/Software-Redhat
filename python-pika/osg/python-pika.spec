%global srcname pika
%global srcurl  https://github.com/%{srcname}/%{srcname}
%global desc \
Pika is a pure-Python implementation of the AMQP 0-9-1 protocol that \
tries to stay fairly independent of the underlying network support \
library.

# FIXME some tests fail
%global nose_unit_excludes -e 'test_add_callbacks_.*' -e test_send_heartbeat_send_frame_called  
%{?rhel:%global nose_acceptance_excludes -e 'async_.*' }

# Enable Python 3 builds for Fedora + EPEL 7
%if 0%{?fedora} || 0%{?rhel} > 7
# If the definition isn't available for python3_pkgversion, define it
%{?!python3_pkgversion:%global python3_pkgversion 3}
%bcond_without  python3
%else
%bcond_with     python3
%endif

%bcond_without  builddoc

Name:           python-%{srcname}
Version:        0.10.0
Release:        10%{?dist}
Summary:        AMQP 0-9-1 client library for Python

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %{srcurl}/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch0:         github_pull_789.patch

BuildArch:      noarch

BuildRequires:  python-srpm-macros 
BuildRequires:  python-rpm-macros 
BuildRequires:  python2-rpm-macros 
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-mock

# python dependencies intentionally without version suffix, compatibility for epel
BuildRequires:  python-sphinx
BuildRequires:  python-nose
BuildRequires:  python-tornado

%if 0%{?fedora}
BuildRequires:  python2-twisted
%else
BuildRequires:  python-twisted-core
%endif

%if %{with python3}
# Required for Python 3 pkgversion macros to work
BuildRequires:  python3-pkgversion-macros

BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-nose

%if 0%{?fedora}
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-twisted
%endif

BuildRequires:  python%{python3_pkgversion}-tornado

%if 0%{?with_python3_other}
BuildRequires:  python%{python3_other_pkgversion}-setuptools
BuildRequires:  python%{python3_other_pkgversion}-devel
%endif
%endif

# for tests
BuildRequires:  rabbitmq-server
BuildRequires:  hostname
BuildRequires:  procps-ng

%description
%{desc}

#################################################################################
%package -n python2-%{srcname}
Summary:        AMQP 0-9-1 client library for Python 2
%{?python_provide:%python_provide python2-%{srcname}}

%if 0%{?fedora}
Recommends:     python2-tornado
Recommends:     python2-twisted
%endif

%description -n python2-%{srcname}
%{desc}

This package provides the Python 2 implementation.

%package -n python2-%{srcname}-doc
Summary:        Additional API documentation for python2-%{name}
%{?python_provide:%python_provide python2-%{srcname}-doc}

%description -n python2-%{srcname}-doc
%{sum}.

%if %{with python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        AMQP 0-9-1 client library for Python 3
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%if 0%{?fedora}
Recommends:     python3-tornado
Recommends:     python3-twisted
%endif

%description -n python%{python3_pkgversion}-%{srcname}
%{desc}

This package provides the Python 3 implementation.

%package -n python%{python3_pkgversion}-%{srcname}-doc
Summary:        Additional API documentation for python3-%{name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}-doc}

%description -n python%{python3_pkgversion}-%{srcname}-doc
%{sum}.

%if 0%{?with_python3_other}
%package -n python%{python3_other_pkgversion}-%{srcname}
Summary:        AMQP 0-9-1 client library for Python 3
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{srcname}}

%description -n python%{python3_other_pkgversion}-%{srcname}
%{desc}

This package provides the Python 3 implementation.
%endif
%endif

#################################################################################
%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p0

%build
%py2_build

%if %{with python3}
%py3_build

%if 0%{?with_python3_other}
%py3_other_build
%endif
%endif

%if %{with builddoc}
sphinx-build \
%if 0%{?fedora}
 %{?_smp_mflags} \
%endif
 -b html -d doctrees docs html
%if %{with python3}
%if 0%{?fedora}
# FIXME %%{?_smp_mflags} hangs sphinx-build-3
sphinx-build-%{python3_version} -b html -d 3/doctrees docs 3/html
%else
# FIXME sphinx is not available for epel7 and python3
# use files of python2, better that than nothing
mkdir 3
cp -av html 3
%endif
find . -name '.*' -print -delete
%endif


%install
%py2_install

%if %{with python3}
%py3_install

%if 0%{?with_python3_other}
%py3_other_install
%endif
%endif

#################################################################################
%files -n python2-%{srcname}
%{python2_sitelib}/%{srcname}*/*
%license LICENSE
%doc README.rst CHANGELOG.rst

%if %{with python3}
%files -n python%{python3_pkgversion}-%{srcname}
%{python3_sitelib}/%{srcname}*/*
%license LICENSE
%doc README.rst CHANGELOG.rst

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{srcname}
%{python3_other_sitelib}/%{srcname}*/*
%license LICENSE
%doc README.rst CHANGELOG.rst
%doc examples/ docs/
%endif
%endif

%if %{with builddoc}
%files -n python2-%{srcname}-doc
%license LICENSE
%doc examples/
%doc html/

%if %{with python3}
%files -n python%{python3_pkgversion}-%{srcname}-doc
%license LICENSE
%doc examples/
%doc 3/html/
%endif
%endif
%endif

#################################################################################
%changelog
* Thu Feb 16 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 0.10.0-10
- Include patch for encoded passwords #789

* Wed Feb 01 2017 Raphael Groner <projects.rg@smart.ms> - 0.10.0-9
- merge changelog

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-8.2
- Rebuild for Python 3.6

* Mon Dec 12 2016 Tuomo Soini <tis@foobar.fi> - 0.10.0-8.1
- Honor %%_smp_ncpus_max setting on testing

* Sat Dec 10 2016 Raphael Groner <projects.rg@smart.ms> - 0.10.0-7
- enable parallel testing with nose
- enable python-twisted-core and python-tornado on epel
- drop obsolete Group tag

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Jul 10 2016 Raphael Groner <projects.rg@smart.ms> - 0.10.0-5
- drop some duplications
- validate b0rken tests on epel7

* Sun Jul 03 2016 Raphael Groner <projects.rg@smart.ms> - 0.10.0-4
- add %%check with execution of both unit and acceptance tests
- enable adapters for both tornado and twisted
- generate additional documentation, split into subpackage

* Sun Feb 07 2016 Neal Gompa <ngompa13{%}gmail{*}com> - 0.10.0-3
- Fix builds by defining python3_pkgversion if it doesn't exist
- Add missing BRs for py3-other variant (for EPEL 7)

* Sat Feb 06 2016 Neal Gompa <ngompa13{%}gmail{*}com> - 0.10.0-2
- Actually make the python 3 bcond work

* Sat Feb 06 2016 Neal Gompa <ngompa13{%}gmail{*}com> - 0.10.0-1
- Upgrade to version 0.10.0
- Refactor to meet current Fedora guidelines
- Add Python 3 subpackage (with EPEL 7 compatibility)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 13 2012 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.9.5-3
- Bump pika release version to fix upgrade path for f17 -> f18

* Sun Feb 26 2012 Daniel Aharon <dan@danielaharon.com> - 0.9.5-2
- Patch pika/adapters/blocking_connection.py

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Apr 3 2011 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.9.5-1
- Upgrade to version 0.9.5

* Sun Mar 6 2011 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.9.4-1
- Upgrade to version 0.9.4

* Sat Feb 19 2011 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.9.3-1
- Upgrade to version 0.9.3

* Sat Oct 2 2010 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.5.2-1
- Initial Package

