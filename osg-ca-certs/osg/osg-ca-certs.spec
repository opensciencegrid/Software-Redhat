Name:           osg-ca-certs
Version:        1.50
Release:        1%{?dist}
Summary:        OSG Packaging of the IGTF CA Certs and OSG-specific CAs, in the new OpenSSL 0.9.8/1.0.0 format.  The OSG CA Distribution contains:  1) IGTF Distribution of Authority Root Certificates (CAs accredited by the International Grid Trust Federation). Details of CAs in the OSG distribution can be found on twiki at https://twiki.grid.iu.edu/bin/view/Documentation/CaDistribution. For additional details what is in the current release, see the distribution site at http://software.grid.iu.edu/pacman/cadist/ and change log at http://software.grid.iu.edu/pacman/cadist/CHANGES. 


Group:          System Environment/Base
License:        Unknown
URL:            http://software.grid.iu.edu/pacman/cadist/

# Note: currently, one needs a valid client certificate to access the source tarball
# https://osg-svn.rtinfo.indiana.edu/cadist/release/osg-certificates-1.20NEW.tar.gz
Source0:        osg-certificates-1.50NEW.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Provides:       grid-certificates = 7

Conflicts:      osg-ca-scripts
Conflicts:      cilogon-ca-certs < 1.0-5

Obsoletes:      vdt-ca-certs
Obsoletes:      osg-ca-certs-experimental
Obsoletes:      osg-ca-certs-compat <= 1:1.37

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
* Mon Oct 26 2015 Jeny Teheran <jteheran@fnal.gov> - 1.50-1
- CA release corresponding to IGTF 1.69 release.

* Tue Oct 6 2015 Anand Padmanabhan <apadmana@uiuc.edu> - 1.49-1
- CA release corresponding to IGTF 1.68 release.

* Thu Sep 3 2015 Anand Padmanabhan <apadmana@uiuc.edu> - 1.48-1
- CA release corresponding to IGTF 1.67 release.

* Wed Jul 8 2015 Jeny Teheran <jteheran@fnal.gov> - 1.47-1
- CA release corresponding to IGTF 1.65 release.

* Wed Jul 1 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.46-2
- Obsolete osg-ca-certs-compat (SOFTWARE-1883)

* Mon Jun 1 2015 Kevin M. Hill <kevinh@fnal.gov> - 1.46-1
- CA release corresponding to IGTF 1.64 release.

* Mon Apr 6 2015 Anand Padmanabhan <apadmana@uiuc.edu> - 1.45-1
- CA release corresponding to IGTF 1.63 release.

* Mon Feb 23 2015 Anand Padmanabhan <apadmana@uiuc.edu> - 1.44-1
- CA release corresponding to IGTF 1.62 release.

* Wed Dec 3 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.43-1
- CA release corresponding to IGTF 1.61 release.

* Thu Oct 30 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.42-1
- CA release corresponding to IGTF 1.60 release.

* Wed Oct 1 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.41-1
- CA release corresponding to IGTF 1.59 release.

* Wed Jul 2 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.40-2
- Added conflict for cilogon-ca-certs < 1.0-5

* Mon Jun 30 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.40-1
- CA release corresponding to IGTF 1.58 release.
- IGTF Accredited IOTA (Identifier-Only Trust Assurance Services) profile CAs (e.g. cilogon-basic) will be included from this release. Details on this profile are at https://www.eugridpma.org/guidelines/IOTA/.

* Tue Jun 3 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.39-1
- CA release corresponding to IGTF 1.57 release.

* Wed Apr 2 2014 Anand Padmanabhan <apadmana@uiuc.edu> - 1.38-1
- CA release corresponding to IGTF 1.56 release. 
- PurdueCA and PurdueTeragridRA certificates have been removed.

* Wed Jan 29 2014 Kevin Hill <kevinh@fnal.gov> - 1.37-1
- SEEGRID CA had wrong hash filename in upstream igtf release. Fixed in old format (-compat), new version number for non-compat just to stay in sync. No other changes for new format release.

* Tue Dec 3 2013 Kevin Hill <kevinh@fnal.gov> - 1.36-1
- CA release corresponding to IGTF 1.55 release

* Mon Jul 1 2013 Anand Padmanabhan <apadmana@uiuc.edu> - 1.35-1
- CA release corresponding to IGTF 1.54 release

* Tue Jun 11 2013 Anand Padmanabhan <apadmana@uiuc.edu> - 1.34-1
- CA release corresponding to IGTF 1.53 release

* Mon Jan 28 2013 Anand Padmanabhan <apadmana@uiuc.edu> - 1.33-1
- CA release corresponding to IGTF 1.52 release

* Tue Dec 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.32-4
- CA release corresponding to IGTF 1.51 release (ITB) + DOEGrids sha2

* Mon Dec 07 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.32-3
- CA release corresponding to IGTF 1.51 release 

* Mon Dec 03 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.32-2
- CA release corresponding to IGTF 1.51 release (ITB)

* Mon Nov 19 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.32-1
- CA release corresponding to IGTF 1.51 pre-release + DOEGRID/ESNET sha2

* Wed Oct 3 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.31-2
- CA release corresponding to IGTF 1.50

* Tue Sep 25 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.31-1
- CA release corresponding to IGTF 1.50

* Tue Aug 07 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.30-1
- CA release corresponding to IGTF 1.49

* Fri Jun 11 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.29-2
- CA release corresponding to IGTF 1.48 

* Fri May 25 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.29-1
- CA release corresponding to IGTF 1.48 prerelease

* Mon May 07 2012 Kevin Hill <kevinh@fnal.gov> - 1.28-1
- CA release corresponding to IGTF 1.47 release

* Thu Mar 30 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.27-1
- CA release corresponding to IGTF 1.46 release
- Note version 1.45 is skipped since IGTF released 1.46 immediately due to problem with CRL from CESNET CA

* Thu Jan 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.26-2
- CA release corresponding to IGTF 1.44 release

* Thu Jan 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.26-1
- CA release corresponding to IGTF 1.44 prerelease

* Thu Nov 30 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.25-1
- CA release corresponding to IGTF 1.43

* Thu Nov 28 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.24-3
- use mv instead of install to maintain symlink

* Thu Oct 11 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.24-1
- New CA release

* Thu Sep 27 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.23-1
- New CA release

* Thu Sep 9 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.22-2
- Added osg-ca-certs-experimental in Obsoletes line 

* Thu Sep 8 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.22-1
- Released 1.22
- Changed name from osg-ca-certs-experimental to osg-ca-certs
- Added an Obsoletes line to vdt-ca-certs to make sure that there is an upgrade path for people using the VDT RPM

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.20-3
Fix conflicts line.

* Wed Aug 17 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.20-2
- Fix directory ownership issue.

* Mon Aug 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.20-1
- Initial version, based on osg-ca-certs spec file.

