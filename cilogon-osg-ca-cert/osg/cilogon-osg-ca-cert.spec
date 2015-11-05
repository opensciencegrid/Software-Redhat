Name:           cilogon-osg-ca-cert
Version:        1.0
Release:        2%{?dist}
Summary:        Transitional dummy package; can be uninstalled

Group:          System Environment/Base
License:        Unknown
URL:            http://ca.cilogon.org/downloads

BuildArch:      noarch

%description
%{summary}

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files

%changelog
* Thu Nov 05 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.0-2
- The certs are in osg-ca-certs and igtf-ca-certs now, so dummying this out to prevent conflicts (SOFTWARE-2097)

* Wed Apr 22 2015 Edgar Fajardo <emfajard@ucsd.edu> 1.0-1
- First version of cilogon osg certs package (SOFTWARE-1885)


