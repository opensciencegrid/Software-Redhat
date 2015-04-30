Name:      osg-voms
Summary:   OSG VOMS
Version:   3.3
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#from vdt
Requires: voms-admin-server
Requires: voms-admin-client
Requires: osg-version
Requires: osg-system-profiler
#
# This metapackage requires a database _server_. voms-mysql-plugin only brings
# in the client.
%if 0%{?rhel} < 7
Requires: mysql-server
%else
Requires: mariadb-server
%endif
#from epel
Requires: voms-server

Requires: voms-mysql-plugin

%description
%{summary}
meta package to install voms-admin and voms-core packages


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files



%changelog
* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Wed Apr 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-3
- Use mariadb on el7

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-2
- Added dependencies on osg-version and osg-system-profiler

* Thu Jul 28 2011 Tanya Levshina <tlevshin.fnal.gov>
- Created an initial osg-voms RPM.

