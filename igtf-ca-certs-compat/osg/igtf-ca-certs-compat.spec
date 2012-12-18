Name:           igtf-ca-certs-compat
Version:        1.51
Release:        4%{?dist}
Summary:        OSG Packaging of the IGTF CA Certs, in the old OpenSSl 0.9.x format. For details what is in the current release, see the distribution site at http://software.grid.iu.edu/pacman/cadist/ and change log at http://software.grid.iu.edu/pacman/cadist/CHANGES.

Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

# Note: currently, one needs a valid client certificate to access the source tarball
# https://osg-svn.rtinfo.indiana.edu/cadist/release/osg-certificates-1.20IGTFOLD.tar.gz
Source0:        osg-certificates-1.32ITBIGTFOLD.tar.gz

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
* Tue Dec 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.51-4
- CA release corresponding to IGTF 1.51 release (ITB) + DOEGrids sha2

* Mon Dec 07 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.51-3
- CA release corresponding to IGTF 1.51 release

* Mon Dec 03 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.51-2
- CA release corresponding to IGTF 1.51 release  (ITB)

* Mon Nov 19 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.51-1
- CA release corresponding to IGTF 1.51 pre-release + DOEGRID/ESNET sha2

* Wed Oct 3 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.50-2
- CA release corresponding to IGTF 1.50

* Tue Sep 25 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.50-1
- CA release corresponding to IGTF 1.50

* Tue Aug 07 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.49-1
- CA release corresponding to IGTF 1.49

* Fri Jun 11 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.48-2
- CA release corresponding to IGTF 1.48

* Fri May 25 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.48-1
- CA release corresponding to IGTF 1.48 prerelease

* Mon May 07 2012 Kevin Hill <kevinh@fnal.gov> - 1.47-1
- CA release corresponding to IGTF 1.47 release

* Thu Mar 30 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.46-1
- CA release corresponding to IGTF 1.46 release
- Note version 1.45 is skipped since IGTF released 1.46 immediately due to problem with CRL from CESNET CA

* Thu Jan 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.44-1
- CA release corresponding to IGTF 1.44 release

* Thu Nov 30 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.43-1
- CA release corresponding to IGTF 1.43

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

