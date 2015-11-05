Name:           cilogon-openid-ca-cert
Version:        1.1
Release:        2%{?dist}
Summary:        OSG Packaging of the CILogon CA Certs, in new OpenSSL 0.9.8/1.0.0 format

Group:          System Environment/Base
License:        Unknown
URL:            http://ca.cilogon.org/downloads

Source0:        cilogon-openid-ca-certificates-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Conflicts:      osg-ca-scripts

Obsoletes:      osg-ca-certs-cilogon, osg-ca-certs-cilogon-osg

# Added the obsolete/provides after the cilogon-osg-ca-cert was moved out

Provides:      cilogon-ca-certs = %{version}-%{release}
Obsoletes:     cilogon-ca-certs < 1.1-2


%description
%{summary}

%prep
%setup -q -n cilogon-ca

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/grid-security/certificates
chmod 0644 *
mv * $RPM_BUILD_ROOT/etc/grid-security/certificates/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,-)
%dir %attr(0755,root,root) /etc/grid-security/certificates
/etc/grid-security/certificates/*
%doc

%changelog
* Thu Nov 05 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.1-2.osg
- Fix obsoletes for cilogon-ca-certs

* Wed Apr 22 2015 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1.1-2
- Changed name to cilogon-ca-certs
- Added provides/obsoletes for the name change


* Wed Apr 08 2015 Kevin Hill <kevinh@fnal.gov> - 1.1-1
- Added cilogon-osg ca cert and files.

* Mon Jun 30 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.0-5
- Removing cilogon basic CA since it is included in default package

* Thu Nov 28 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.0-3
- use mv instead of install to maintain symlink

* Tue Oct 04 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.0-1
- Initial packaging of the CILogon CA certs (new format) from OSG.

