Summary:   Generate CAs and certificates for testing an OSG installation
Name:      osg-ca-generator
Version:   1.4.0
Release:   1%{?dist}
License:   Apache License, 2.0
Packager:  VDT <vdt-support@opensciencegrid.org>
Source0:   %{name}-%{version}.tar.gz
AutoReq:   yes
AutoProv:  yes
BuildArch: noarch

%if 0%{?rhel} >= 8
  %define __python /usr/libexec/platform-python
%else
  %if 0%{?fedora} >= 31
    %define __python /usr/bin/python3
  %else
    %define __python /usr/bin/python2
  %endif
%endif


Requires: openssl

%description
Create DigiCert-like CAs and certificates for testing an OSG Software installation

%prep
%setup -q

%install
find . -type f -exec sed -ri '1s,^#!/usr/bin/env python,#!%{__python},' '{}' +
make install DESTDIR=$RPM_BUILD_ROOT PYTHON=%{__python}

%files
%{_sbindir}/%{name}
%{python_sitelib}/cagen.py*
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30
%{python_sitelib}/__pycache__/*.pyc
%endif

%changelog
* Tue Jul 21 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.0-1
- Working Python 3/EL 8 support (SOFTWARE-4073)

* Tue Jan 23 2018 Brian Lin <blin@cs.wisc.edu> 1.3.2-1
- Use hostname for the fake VOMS URI

* Tue Jan 16 2018 Brian Lin <blin@cs.wisc.edu> 1.3.1-1
- Fix formatting of /etc/vomses (SOFTWARE-2976)

* Fri Dec 08 2017 Brian Lin <blin@cs.wisc.edu> 1.3.0-1
- Add ability to create VO lsc and vomses entry (SOFTWARE-2976)
- Create backups when writing files (SOFTWARE-2352)
- Drop DigiCert CA infrastracture mimicry
- Store CA private key in openssl folder

* Thu Aug 25 2016 Brian Lin <blin@cs.wisc.edu> 1.2.0-1
- Add ability to generate user certificate via CLI. Host certs no longer automatically generated (SOFTWARE-2417).

* Thu Jun 02 2016 Brian Lin <blin@cs.wisc.edu> 1.1.0-1
- Add option to generate CILogon-style CAs and certificates (--cilogon)

* Fri Feb 25 2016 Brian Lin <blin@cs.wisc.edu> 1.0.4-1
- Remove missed print statements from library (SOFTWARE-2204)

* Fri Feb 19 2016 Brian Lin <blin@cs.wisc.edu> 1.0.3-1
- Remove print statements from library (SOFTWARE-2204)

* Wed Jan 27 2016 Brian Lin <blin@cs.wisc.edu> 1.0.1-2
- Fix bug on EL5 where OpenSSL does not create the required folders

* Wed Jan 27 2016 Brian Lin <blin@cs.wisc.edu> 1.0.1-1
- Fix subject alternative name entry for generated certs
- Remove serial numbered copies of created certs in working dir (SOFTWARE-2174)

* Mon Jan 25 2016 Brian Lin <blin@cs.wisc.edu> 1.0.0-2
- Add openssl requirement

* Mon Jan 25 2016 Brian Lin <blin@cs.wisc.edu> 1.0.0-1
- Initial release
