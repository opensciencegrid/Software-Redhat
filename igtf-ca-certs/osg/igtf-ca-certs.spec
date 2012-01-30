Name:           igtf-ca-certs
Version:        1.44
Release:        1%{?dist}
Summary:        OSG Packaging of the IGTF CA Certs, in new OpenSSL 0.9.8/1.0.0 format

Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

Source0:        osg-certificates-1.26ITBIGTFNEW.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       grid-certificates = 5

Conflicts:      osg-ca-scripts

Obsoletes:      vdt-ca-certs
Obsoletes:      igtf-ca-certs-experimental

%description
%{summary}

%prep
%setup -q -n certificates

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
* Thu Jan 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.44-1
- CA release corresponding to IGTF 1.44 release

* Thu Nov 30 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.43-1
- CA release corresponding to IGTF 1.43

* Thu Nov 28 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.42-3
- use mv instead of install to maintain symlink

* Thu Oct 11 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.42-1
- New CA release

* Thu Sep 27 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.41-1
- New CA release

* Thu Sep 9 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.40-6
- Added osg-ca-certs-experimental in Obsoletes line

* Thu Sep 8 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.40-5
- Changed name from igtf-ca-certs-experimental to igtf-ca-certs

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-3
Fix conflicts line.

* Wed Aug 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-2
- Fix directory ownership issue.

* Mon Aug 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-1
- Initial packaging of the IGTF CA certs (new format) from OSG.

