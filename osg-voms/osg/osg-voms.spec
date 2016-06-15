Name:      osg-voms
Summary:   OSG VOMS
Version:   3.3
Release:   3%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#from vdt
%if 0%{?rhel} < 7
Requires: voms-admin-server
Requires: voms-admin-client
%else
Requires: grid-certificates >= 7
Requires: fetch-crl
%endif
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
%if 0%{?rhel} < 7
meta package to install voms-admin and voms-core packages
%else
meta package to install voms-core packages
%endif


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files



%changelog
* Wed Jun 15 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-3
- Add grid-certificates and fetch-crl requirements on EL7 (SOFTWARE-2356)

* Mon Jun 06 2016 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-2
- Remove voms-admin-client and voms-admin-server requirement on EL7 (SOFTWARE-2356)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Wed Apr 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-3
- Use mariadb on el7

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-2
- Added dependencies on osg-version and osg-system-profiler

* Thu Jul 28 2011 Tanya Levshina <tlevshin.fnal.gov>
- Created an initial osg-voms RPM.

