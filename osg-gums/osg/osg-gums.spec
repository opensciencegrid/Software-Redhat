Name:      osg-gums
Summary:   OSG GUMS
Version:   1.0.0
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

Requires: grid-certificates
Requires: osg-version
Requires: osg-system-profiler
Requires: gums-service
Requires: gums-client
Requires: osg-gums-config

%description
%{summary}
Provides GUMS and the default OSG GUMS configuration template

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files

%changelog
* Sat Jun 23 2012 Alain Roy <roy@cs.wisc.edu> - 1.0.0-1
- First version

