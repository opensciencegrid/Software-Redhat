%global _docdir_fmt %{name}
%global srcname jwt

Name:               python-jwt
Version:            1.6.1
Release:            1%{?dist}
Summary:            JSON Web Token implementation in Python
License:            MIT
URL:                https://github.com/jpadilla/pyjwt
Source0:            %{url}/archive/%{version}/pyjwt-%{version}.tar.gz
Patch0:             disable-coverage-and-runner.patch
BuildArch:          noarch

BuildRequires:      python2-devel
BuildRequires:      python2-setuptools
BuildRequires:      python2-cryptography >= 1.4.0
BuildRequires:      python2-pytest

BuildRequires:      python%{python3_pkgversion}-devel
BuildRequires:      python%{python3_pkgversion}-setuptools
BuildRequires:      python%{python3_pkgversion}-cryptography >= 1.4.0
BuildRequires:      python%{python3_pkgversion}-pytest

%global _description \
A Python implementation of JSON Web Token draft 01. This library provides a\
means of representing signed content using JSON data structures, including\
claims to be transferred between two parties encoded as digitally signed and\
encrypted JSON objects.

%description %{_description}

%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       python2-cryptography >= 1.4.0
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname} %{_description}

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
Requires:       python%{python3_pkgversion}-cryptography >= 1.4.0
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname} %{_description}

%prep
%autosetup -n pyjwt-%{version} -p 1
# prevent pulling in `addopts` for pytest run later
rm setup.cfg

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
py.test-%{python2_version} --verbose
py.test-%{python3_version} --verbose

%files -n python2-jwt
%doc README.rst AUTHORS
%license LICENSE
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/PyJWT-%{version}-py%{python2_version}.egg-info

%files -n python%{python3_pkgversion}-jwt
%doc README.rst AUTHORS
%license LICENSE
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/PyJWT-%{version}-py%{python3_version}.egg-info
%{_bindir}/pyjwt

%changelog
* Thu Apr 05 2018 Carl George <carl@george.computer> - 1.6.1-1
- Latest upstream
- Add patch0 to remove pytest-{cov,runner} deps
- Share doc and license dir between subpackages
- Enable EPEL PY3 build

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.5.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 16 2017 Kevin Fenzi <kevin@scrye.com> - 1.5.3-1
- Update to 1.5.3. Fixes bug #1488693
- 1.5.1 fixed CVE-2017-11424 Fixes bug #1482529

* Mon Aug 14 2017 Troy Dawson <tdawson@redhat.com> - 1.5.2-3
- Fixup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Kevin Fenzi <kevin@scrye.com> - 1.5.2-1
- Update to 1.5.2. Fixes bug #1464286

* Sat May 27 2017 Kevin Fenzi <kevin@scrye.com> - 1.5.0-1
- Update to 1.5.0. Fixes bug #1443792

* Mon Apr 17 2017 Kevin Fenzi <kevin@scrye.com> - 1.4.2-4
- Modernize spec and make sure to provide python2-jwt

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.4.2-2
- Rebuild for Python 3.6

* Mon Aug 15 2016 Kevin Fenzi <kevin@scrye.com> - 1.4.2-1
- Update to 1.4.2. Fixes bug #1356333

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 16 2015 Ralph Bean <rbean@redhat.com> - 1.4.0-1
- new version

* Wed Jun 17 2015 Ralph Bean <rbean@redhat.com> - 1.3.0-1
- new version
- start running the test suite.

* Fri Mar 27 2015 Ralph Bean <rbean@redhat.com> - 1.0.1-1
- new version

* Thu Mar 19 2015 Ralph Bean <rbean@redhat.com> - 1.0.0-1
- new version

* Fri Feb 20 2015 Ralph Bean <rbean@redhat.com> - 0.4.3-1
- Latest upstream.
- Expand the description as per review feedback.
- Add a comment about the test suite.
- Declare noarch.
- Declare _docdir_fmt

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 0.4.2-1
- initial package for Fedora.
