Name:           osg-ca-certs-cilogon
Version:        1.21
Release:        2%{?dist}
Summary:        OSG CA Certs, plus the unaccredited CILogon CAs

Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

# From: 
# http://software-itb.grid.iu.edu/pacman/cadist/1.21ITBEXPT/osg-certificates-1.21ITBEXPT.tar.gz
Source0:        osg-certificates-1.21ITBEXPT.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       grid-certificates = 6

Conflicts:      osg-ca-scripts

%description
%{summary}

%prep
%setup -q -n certificates

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
* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.21-2
Fix conflicts line and virtual provides version.

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.21-1
- Create cert package with cilogon.


