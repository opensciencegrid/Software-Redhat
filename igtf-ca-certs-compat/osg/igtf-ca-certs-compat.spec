Name:           igtf-ca-certs-compat
Version:        1.42
Release:        1
Summary:        OSG Packaging of the IGTF CA Certs, in the old OpenSSl 0.9.x format

Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

# Note: currently, one needs a valid client certificate to access the source tarball
# https://osg-svn.rtinfo.indiana.edu/cadist/release/osg-certificates-1.20IGTFOLD.tar.gz
Source0:        osg-certificates-1.24IGTFOLD.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       grid-certificates = 4

Conflicts:      osg-ca-scripts
Obsoletes:      vdt-ca-certs < 61

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
* Thu Oct 11 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.42-1
- New CA release

* Thu Sep 27 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.41-1
- New CA release

* Thu Sep 8 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.40-5
- Changed name from igtf-ca-certs to igtf-ca-certs-compat

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-4
Fix conflicts and obsoletes.

* Wed Aug 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-3
- Fix directory ownership issue.

* Mon Aug 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-2
- Version the virtual provides.  Fix directory permissions

* Wed Aug 10 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.40-1
- Initial packaging of the IGTF CA certs from OSG.

