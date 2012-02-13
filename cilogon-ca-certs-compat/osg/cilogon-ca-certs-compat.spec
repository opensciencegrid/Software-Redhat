Name:           cilogon-ca-certs-compat
Version:        1.0
Release:        2%{?dist}
Summary:        OSG Packaging of the CILogon CA Certs, in new OpenSSL 0.9.x format

Group:          System Environment/Base
License:        Unknown
URL:            http://ca.cilogon.org/downloads

Source0:        cilogon-ca-certificates-old.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Conflicts:      osg-ca-scripts

Obsoletes:      osg-ca-certs-cilogon

%description
%{summary}

%prep
%setup -q -n cilogon-ca

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/grid-security/certificates
install -m 0644 * $RPM_BUILD_ROOT/etc/grid-security/certificates/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,-)
%dir %attr(0755,root,root) /etc/grid-security/certificates
/etc/grid-security/certificates/*
%doc

%changelog
* Tue Oct 04 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.0-1
- Initial packaging of the CILogon CA certs (old format) from OSG.

