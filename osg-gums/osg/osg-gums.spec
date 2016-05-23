Name:      osg-gums
Summary:   OSG GUMS
Version:   3.3
Release:   3%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

Requires: grid-certificates >= 7
Requires: osg-version
Requires: osg-system-profiler
Requires: gums-service
Requires: gums-client
Requires: osg-gums-config
# Added for SOFTWARE-2331
Requires: vo-client
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif

%description
%{summary}
Provides GUMS and the default OSG GUMS configuration template

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files

%changelog
* Mon May 23 2016 Edgar Fajardo <emfajard@ucsd.edu> 3.3-3
- Added requirements of vo-client (SOFTWARE-2331)

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue Jul 23 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0.0-2
- Require fetch-crl (SOFTWARE-967)
* Sat Jun 23 2012 Alain Roy <roy@cs.wisc.edu> - 1.0.0-1
- First version

