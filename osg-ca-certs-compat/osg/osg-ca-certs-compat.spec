Name:           osg-ca-certs-compat
Version:        1.22
Release:        1
Epoch:          1
Summary:        OSG Packaging of the IGTF CA Certs and OSG-specific CAs in old format. Compatible only with openssl 0.9.x.

Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

# Note: currently, one needs a valid client certificate to access the source tarball
# https://osg-svn.rtinfo.indiana.edu/cadist/release/osg-certificates-1.20.tar.gz
Source0:        osg-certificates-1.22.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       grid-certificates = 6

Conflicts:      osg-ca-scripts

Obsoletes:      vdt-ca-certs

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
* Thu Sep 8 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1:1.22-1
- Released 1.22
- Changed name from osg-ca-certs to osg-ca-certs-compat
- Added an Obsoletes line to vdt-ca-certs to make sure that there is an upgrade path for people using the VDT RPM

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1:1.20-3
Fix conflicts line.

* Wed Aug 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1:1.20-2
- Fixed ownership issue.

* Mon Aug 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.20-1
- Update to use the package from osg-security.  Bumped epoch number to prevent confusion with old versioning.

* Fri Jul 22 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3-2
- Add provdes grid-certificates

* Fri Jul 08 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3-1
- Initial creation of RPM to pull in vdt-ca-certs.

