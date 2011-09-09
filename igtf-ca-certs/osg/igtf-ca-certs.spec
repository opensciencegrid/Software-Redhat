Name:           igtf-ca-certs
Version:        1.40
Release:        5
Summary:        OSG Packaging of the IGTF CA Certs, in new OpenSSL 0.9.8/1.0.0 format

Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

# Note: currently, one needs a valid client certificate to access the source tarball
# https://osg-svn.rtinfo.indiana.edu/cadist/release/osg-certificates-1.20IGTFNEW.tar.gz
Source0:        osg-certificates-1.20IGTFNEW.tar.gz

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
install -m 0644 * $RPM_BUILD_ROOT/etc/grid-security/certificates/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,-)
%dir %attr(0755,root,root) /etc/grid-security/certificates
/etc/grid-security/certificates/*
%doc

%changelog
* Thu Sep 9 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.22-2
- Added osg-ca-certs-experimental in Obsoletes line

* Thu Sep 8 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.40-5
- Changed name from igtf-ca-certs-experimental to igtf-ca-certs

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-3
Fix conflicts line.

* Wed Aug 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-2
- Fix directory ownership issue.

* Mon Aug 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-1
- Initial packaging of the IGTF CA certs (new format) from OSG.

