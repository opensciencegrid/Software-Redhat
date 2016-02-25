%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c 'from distutils.sysconfig import get_python_lib; print get_python_lib(1)')}
%endif

Summary:   Generate CAs and certificates for testing an OSG installation
Name:      osg-ca-generator
Version:   1.0.4
Release:   1%{?dist}
License:   Apache License, 2.0
Group:     Applications/Grid
Packager:  VDT <vdt-support@opensciencegrid.org>
Source0:   %{name}-%{version}.tar.gz
AutoReq:   yes
AutoProv:  yes
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

Requires: openssl

%description
Create DigiCert-like CAs and certificates for testing an OSG Software installation

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/%{name}
%{python_sitelib}/cagen.py*

%changelog
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
