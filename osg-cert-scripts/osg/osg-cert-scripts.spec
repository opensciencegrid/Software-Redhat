# Define macros, source: http://fedoraproject.org/wiki/Packaging:Python
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           osg-cert-scripts
Version:        2.7.2
Release:        2%{?dist}
Summary:        Command-line interface to the DOEGrids CA web site, and more.

Group:          Grid
License:        Apache 2.0
URL:            http://vdt.cs.wisc.edu/components/cert-scripts.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       /usr/bin/ldapsearch
Requires:       /usr/bin/openssl
Requires:       grid-certificates >= 7
Requires:	perl(Crypt::SSLeay)
Requires: 	perl(LWP::UserAgent)
Requires: 	perl(Date::Format)
Requires: 	perl(Getopt::Long)

Source0:        osg-cert-scripts-2.7.2.tar.gz
# Patches incorporated to SVN since OSG is the upstream source
#Patch0:         change_awk_locations.patch  
#Patch1:         make_correct_python_module.patch

Provides:       ppdg-cert-scripts = %{version}-%{release}
Obsoletes:      ppdg-cert-scripts < 2.7-5

%description
The Certificate Scripts package provides two things: a command-line interface 
to the DOEGrids CA web site, and some extra utilities for dealing with X509 
Certificates. These scripts are part of the PPDG-Cert-Scripts package. It is 
named this way because it was originally donated by the PPDG Registration 
Authority (RA), but it is now maintained by the OSG RA.

%prep
# Annoying that the name of the tar is different than the package
%setup -q -n osg-cert-scripts
#%patch0 -p1 
#%patch1 -p1

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
* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 2.7.2-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Mon Feb 16 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 2.7.2-1
- Fix for Jira ticket 546

* Mon Feb 16 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 2.7.1-4
- Added dependency to perl(LWP::UserAgent), perl(Date::Format), perl(Getopt::Long)

* Mon Feb 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.7.1-3
- Added dist tag

* Mon Oct 10 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 2.7.1-2
- Added dependency to perl(Crypt::SSLeay)

* Mon Aug 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 2.7-5
- Rename RPM to use the osg- prefix.

* Wed Aug 10 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 2.7-4
- Require virtual dep grid-certificates, not actual package osg-ca-certs.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.7-3
- Rebuild using setup macro
- Mark as noarch

* Mon Jul 11 2011 Derek Weitzel <dweitzel@cse.unl.edu> 2.7-2
- Applied patch to look for awk files in /usr/share
- Applied patch to put python CertLib.py in the right directory

* Fri Jul 08 2011 Derek Weitzel <dweitzel@cse.unl.edu> 2.7-1
- Initial build of the ppdg-cert-scripts package.


