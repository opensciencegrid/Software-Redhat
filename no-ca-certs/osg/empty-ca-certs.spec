Name:           empty-ca-certs
Version:        1.0
Release:        1
Summary:        An empty grid CA cert package

Group:          System Environment/Base
License:        Unknown
URL:            http://vdt.cs.wisc.edu

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       grid-certificates = 1
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

%clean

%files

%doc

%changelog
* Thu Sep 19 2011 Alain Roy <roy@cs.wisc.edu> - 1.0-1
- Initial version
