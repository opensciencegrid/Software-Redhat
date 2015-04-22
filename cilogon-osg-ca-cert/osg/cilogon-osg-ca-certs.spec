Name:           cilogon-osg-ca-certs
Version:        1.0
Release:        1%{?dist}
Summary:        OSG Packaging of the CILogon OSG CA Certs, in new OpenSSL 0.9.8/1.0.0 format

Group:          System Environment/Base
License:        Unknown
URL:            http://ca.cilogon.org/downloads

Source0:        cilogon-osg-ca-cert-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Conflicts:      osg-ca-scripts

#Obsoletes:      osg-ca-certs-cilogon, osg-ca-certs-cilogon-osg

%description
%{summary}

%prep
%setup -q -n cilogon-osg-ca

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
* Wed Apr 22 2015 Edgar Fajardo <emfajard@ucsd.edu> 1.0-1
- First version of cilogon osg certs package (SOFTWARE-1885)


