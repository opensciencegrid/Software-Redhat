Name:           empty-ca-certs
Version:        1.0
Release:        4%{?dist}
Summary:        An empty grid CA cert package

License:        Unknown
URL:            http://vdt.cs.wisc.edu

BuildArch:      noarch

Provides:       grid-certificates = 7
Conflicts:      osg-ca-scripts
Conflicts:      osg-ca-certs
Conflicts:      osg-ca-certs-compat
Conflicts:      igtf-ca-certs
Conflicts:      igtf-ca-certs-compat
Obsoletes:      vdt-ca-certs

%description

This package is empty, but it "provides" grid-certificates. This
allows other packages that require Grid CA certificates to install
correctly when other mechanisms are used to provide Grid CA
certificates. It is assumed that people who use this package will
manage Grid CA certificates on their own, perhaps via installation on
a shared filesystem.

%prep

%build

%install

%files

%doc

%changelog
* Tue Jun 25 2024 Matt Westphall <westphall@wisc.edu> 1.0-4.osg
- Bump release to fix automated signing issue

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0-2.osg
- Provide grid-certificates = 7

* Thu Sep 19 2011 Alain Roy <roy@cs.wisc.edu> - 1.0-1
- Initial version
