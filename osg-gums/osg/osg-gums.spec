Name:      osg-gums
Summary:   OSG GUMS
Version:   3.2
Release:   1%{?dist}
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
* Fri Jul 17 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.2-1
- Require grid-certificates >= 7 (SOFTWARE-1883)
- Change version to match release series

* Tue Jul 23 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0.0-2
- Require fetch-crl (SOFTWARE-967)

* Sat Jun 23 2012 Alain Roy <roy@cs.wisc.edu> - 1.0.0-1
- First version

