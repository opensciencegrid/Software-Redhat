# Define macros, source: http://fedoraproject.org/wiki/Packaging:Python
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           ppdg-cert-scripts
Version:        2.7
Release:        3
Summary:        Command-line interface to the DOEGrids CA web site, and more.

Group:          Grid
License:        Apache 2.0
URL:            http://vdt.cs.wisc.edu/components/cert-scripts.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       /usr/bin/ldapsearch
Requires:       /usr/bin/openssl
Requires:       osg-ca-certs

Source0:        cert-scripts-2.7.tar.gz
Patch0:         change_awk_locations.patch  
Patch1:         make_correct_python_module.patch

%description
The Certificate Scripts package provides two things: a command-line interface 
to the DOEGrids CA web site, and some extra utilities for dealing with X509 
Certificates. These scripts are part of the PPDG-Cert-Scripts package. It is 
named this way because it was originally donated by the PPDG Registration 
Authority (RA), but it is now maintained by the OSG RA.

%prep
# Annoying that the name of the tar is different than the package
%setup -q -n cert-scripts
%patch0 -p1 
%patch1 -p1

%build


%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
cp bin/* $RPM_BUILD_ROOT/%{_bindir}

install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp lib/*awk $RPM_BUILD_ROOT/%{_datadir}/%{name}/

install -d -m 0755 $RPM_BUILD_ROOT/%{python_sitelib}/ppdg-cert
install -m 644 lib/CertLib.py $RPM_BUILD_ROOT/%{python_sitelib}/ppdg-cert/

install -d $RPM_BUILD_ROOT/%{perl_vendorlib}
install -m 644 lib/CertLib.pm $RPM_BUILD_ROOT/%{perl_vendorlib}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}
%{python_sitelib}/*
%{perl_vendorlib}/CertLib.pm



%changelog
* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.7-3
- Rebuild using setup macro
- Mark as noarch

* Mon Jul 11 2011 Derek Weitzel <dweitzel@cse.unl.edu> 2.7-2
- Applied patch to look for awk files in /usr/share
- Applied patch to put python CertLib.py in the right directory

* Fri Jul 08 2011 Derek Weitzel <dweitzel@cse.unl.edu> 2.7-1
- Initial build of the ppdg-cert-scripts package.



