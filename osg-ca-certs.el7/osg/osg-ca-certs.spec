%define igtf_version 1.125
%define osg_version  1.116
%define release_num  1
%define vtag         %{osg_version}.igtf.%{igtf_version}-%{release_num}
%define enable_trusted_sha1_certs 0

Name:           osg-ca-certs
Version:        %{osg_version}
Release:        %{release_num}%{?dist}
Summary:        OSG Packaging of the IGTF CA Certs and OSG-specific CAs, in the OpenSSL 1.0.* format. 

License:        Unknown
URL:            http://repo.opensciencegrid.org/cadist/

Source0:        https://github.com/opensciencegrid/osg-certificates/archive/v%{vtag}/osg-certificates-%{vtag}.tar.gz
Source1:        https://dist.eugridpma.info/distribution/igtf/current/igtf-policy-installation-bundle-%{igtf_version}.tar.gz
Source2:        https://github.com/opensciencegrid/letsencrypt-certificates/archive/v0.3.2/letsencrypt-certificates.tar.gz
# can obtain latest letsencrypt-certificates.tar.gz with a github.source line:
# type=github repo=cilogon/letsencrypt-certificates tarball=letsencrypt-certificates.tar.gz tag=master hash=...

BuildArch:      noarch

BuildRequires:  openssl

BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Getopt::Long)

Provides:       grid-certificates = 7

Conflicts:      osg-ca-scripts

Obsoletes:      vdt-ca-certs
Obsoletes:      osg-ca-certs-experimental
Obsoletes:      osg-ca-certs-compat <= 1:1.37
RemovePathPostfixes: .trusted-cert

%description
For details about the current certificate release, see https://repo.opensciencegrid.org/cadist/ and change log at https://repo.opensciencegrid.org/cadist/CHANGES.

%package java
Summary: Java-compatible SHA1 certs for %{name}
BuildArch: noarch
Conflicts: osg-ca-scripts
RemovePathPostfixes: .java-cert

%description java
For details about the current certificate release, see https://repo.opensciencegrid.org/cadist/ and change log at https://repo.opensciencegrid.org/cadist/CHANGES.

%prep
%setup    -n osg-certificates-%{vtag}
%setup -D -n osg-certificates-%{vtag} -a 1
%setup -D -n osg-certificates-%{vtag} -a 2

%build
export IGTF_CERTS_VERSION=%{igtf_version}
export OSG_CERTS_VERSION=%{osg_version}
export OUR_CERTS_VERSION=${OSG_CERTS_VERSION}NEW
export CADIST=$PWD/certificates
export PKG_NAME=%{name}

./build-certificates-dir.sh

%if 0%{?enable_trusted_sha1_certs}
./add-trusted-sha1-certs.sh certificates trusted-cert java-cert
%else
# We still want to make the osg-ca-certs and osg-ca-certs-java RPMs
find certificates -name "*.pem" -exec cp '{}' '{}.java-cert' ';'
find certificates -name "*.pem" -exec mv '{}' '{}.trusted-cert' ';'
%endif

%install
mkdir -p $RPM_BUILD_ROOT/etc/grid-security/certificates
mv certificates/* $RPM_BUILD_ROOT/etc/grid-security/certificates/

%check
# TODO how do we sha256sum the files that will have their names changed during install?
# cd $RPM_BUILD_ROOT/etc/grid-security/certificates

# sha256sum -c cacerts_sha256sum.txt

%files
%defattr(0644,root,root,-)
%dir %attr(0755,root,root) /etc/grid-security/certificates
/etc/grid-security/certificates/*
%doc

%files java
%defattr(0644,root,root,-)
%dir %attr(0755,root,root) /etc/grid-security/certificates
/etc/grid-security/certificates/*
%doc

%changelog
* Wed Nov 29 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.116-1
- Update to IGTF 1.125; remove el9 cert changes (SOFTWARE-5764)

* Thu Nov 9 2023 Matt Westphall <westphall@wisc.edu> - 1.115-2
- Re-add el9 cert changes, create secondary package with original certs (SOFTWARE-5745)

* Tue Oct 31 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.115-1
- Update to IGTF 1.124 (SOFTWARE-5738)

* Fri Sep 08 2023 Matt Westphall <westphall@wisc.edu> - 1.114-2
- Bump version to remove el9 cert changes

* Tue Sep 05 2023 Matt Westphall <westphall@wisc.edu> - 1.114-1
- Update to IGTF 1.123 (SOFTWARE-5677)

* Mon Aug 07 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.113-1
- Update to IGTF 1.122 (SOFTWARE-5643)

* Fri Jun 16 2023 Matt Westphall <westphall@wisc.edu> - 1.112-1
- Update to IGTF 1.121 (SOFTWARE-5584)

* Wed May 31 2023 Matt Westphall <westphall@wisc.edu> - 1.111-1
- Update to IGTF 1.120 (SOFTWARE-5584)

* Mon Mar 13 2023 Tim Theisen <tim@cs.wisc.edu> - 1.110-1
- Update to IGTF 1.119 (SOFTWARE-5524)

* Tue Jan 03 2023 Carl Edquist <edquist@cs.wisc.edu> - 1.109-1.2
- Rebuild again for el9 rpm signing (SOFTWARE-5396)

* Mon Dec 19 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.109-1.1
- Rebuild for el9 rpm signing (SOFTWARE-5396)

* Mon Aug 29 2022 Tim Theisen <tim@cs.wisc.edu> - 1.109-1
- Update to IGTF 1.117 (SOFTWARE-5309)

* Mon Apr 25 2022 Tim Theisen <tim@cs.wisc.edu> - 1.106-1
- Update to IGTF 1.116 (SOFTWARE-5142)

* Wed Mar 30 2022 Tim Theisen <tim@cs.wisc.edu> - 1.105-1
- Update to IGTF 1.115 (SOFTWARE-5107)

* Wed Jan 19 2022 Tim Theisen <tim@cs.wisc.edu> - 1.104-1
- Update to IGTF 1.114 (SOFTWARE-4965)
- SOFTWARE-4965: Remove expired Let's Encrypt ROOT CA X3
- SOFTWARE-4965: Remove expired Let's Encrypt ROOT CA X4

* Mon Oct 04 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.100-1
- Update to IGTF 1.113 (SOFTWARE-4844)

* Wed Sep 29 2021 Tim Theisen <tim@cs.wisc.edu> - 1.99-1
- Remove expiring Let's Encrypt "DST Root X3 CA" (SOFTWARE-4836)

* Fri Aug 13 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.98-1
- Update to IGTF 1.112 (SOFTWARE-4745)

* Mon May 24 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.97-1
- Update to IGTF 1.111 (SOFTWARE-4631)

* Mon May 10 2021 Brian Lin <blin@cs.wisc.edu> - 1.96-1
- Add missing ISRG Root X1 to the DST Root CA X3 signing policy (SOFTWARE-4613)

* Wed Apr 28 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.95-1
- Update to IGTF 1.110 (SOFTWARE-4587)

* Wed Jan 27 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.94-1
- Bundle letsencrypt-certificates/lets-encrypt-r{3,4}.pem (SOFTWARE-4436)

* Wed Jan 27 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.93-2
- Rebuild with letsencrypt-certificates v0.3.1 (SOFTWARE-4436)

* Tue Jan 26 2021 Carl Edquist <edquist@cs.wisc.edu> - 1.93-1
- Add DST Root CA X3 Let's Encrypt root cert (SOFTWARE-4436)

* Tue Jan 19 2021 Brian Lin  <blin@cs.wisc.edu> - 1.92-1
- Update to IGTF 1.109 (SOFTWARE-4427)

* Mon Dec 14 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.91-1
- Update to IGTF 1.108 (SOFTWARE-4395)

* Wed Dec 9 2020 Brian Lin <blin@cs.wisc.edu> - 1.90-1
- Add new Let's Encrypt intermediate certificates (SOFTWARE-4387)

* Mon Aug 10 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.89-1
- Update to IGTF 1.107 (SOFTWARE-4215)

* Mon May 04 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.88-1
- Update to IGTF 1.106 (SOFTWARE-4085)

* Mon Mar 30 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.87-1
- Update to IGTF 1.105 (SOFTWARE-4046)

* Thu Feb 06 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.86-2
- Revamp build process (SOFTWARE-3977)

* Wed Jan 29 2020 Carl Edquist <edquist@cs.wisc.edu> - 1.86-1
- CA release corresponding to IGTF 1.104 (SOFTWARE-3985)
- Add back AddTrust-External-CA-Root

* Mon Jan 27 2020 Zalak Shah <zsshah@iu.edu> 1.85-1
- CA release corresponding to IGTF 1.103 release.

* Tue Oct 22 2019 Zalak Shah <zsshah@iu.edu> 1.84-1
- CA release corresponding to IGTF 1.102 release.
- Dropping MD5 checksum [SOFTWARE-3005]

* Mon Jun 24 2019 Zalak Shah <zsshah@iu.edu> 1.83-1
- CA release corresponding to IGTF 1.101 release.

* Tue May 28 2019 Zalak Shah <zsshah@iu.edu> 1.82-1
- CA release corresponding to IGTF 1.99 release.

* Mon Apr 29 2019 Zalak Shah <zsshah@iu.edu> 1.81-1
- CA release corresponding to IGTF 1.98 release.

* Tue Mar 26 2019 Zalak Shah <zsshah@iu.edu> 1.80-1
- CA release corresponding to IGTF 1.97 release.

* Wed Feb 27 2019 Zalak Shah <zsshah@iu.edu> 1.79-1
- CA release corresponding to IGTF 1.96 release.

* Tue Jan 8 2019 Zalak Shah <zsshah@iu.edu> 1.78-1
- CA release corresponding to IGTF 1.95 release.

* Fri Nov 16 2018 Zalak Shah <zsshah@iu.edu> 1.76-3
- CA release corresponding to IGTF 1.94 release.
- Renamed 1.77NEW to 1.76NEW_2 and 1.77IGTFNEW to 1.76IGTFNEW_2

* Tue Nov 06 2018 Zalak Shah <zsshah@iu.edu> 1.76-2
- CA release corresponding to IGTF 1.94 release.
- Included MD5 checksum again for certs

* Tue Oct 30 2018 Zalak Shah <zsshah@iu.edu> 1.76-1
- CA release corresponding to IGTF 1.94 release.

* Mon Sep 24 2018 Zalak Shah <zsshah@iu.edu> 1.75-1
- CA release corresponding to IGTF 1.93 release.

* Thu Jun 28 2018 Zalak Shah <zsshah@iu.edu> 1.74-1
- CA release corresponding to IGTF 1.92 release.

* Tue May 15 2018 Zalak Shah <zsshah@iu.edu> 1.73-1
- CA release corresponding to IGTF 1.91 release.

* Mon May 7 2018 Zalak Shah <zsshah@iu.edu> 1.72-1
- CA release corresponding to IGTF 1.90 release.
- Added root and intermediate certificates for Lets Encrypt CA (SOFTWARE-3249)

* Sun May 6 2018 Zalak Shah <zsshah@iu.edu> 1.71-1
- CA release corresponding to IGTF 1.90 release.
- Added LetsEncrypt CA (SOFTWARE-3249)

* Tue Mar 27 2018 Zalak Shah <zsshah@iu.edu> 1.70-1
- CA release corresponding to IGTF 1.90 release.

* Tue Jan 16 2018 Zalak Shah <zsshah@iu.edu> 1.69-2
- CA release corresponding to IGTF 1.89 release.
- Updated summary and description for osg-ca-certs (SOFTWARE-3097)
- Replaced repo.grid.iu.edu -> repo.opensciencegrid.org (SOFTWARE-3097)

* Wed Jan 10 2018 Zalak Shah <zsshah@iu.edu> 1.69-1
- CA release corresponding to IGTF 1.89 release.

* Mon Nov 27 2017 Zalak Shah <zsshah@iu.edu> 1.68-1
- CA release corresponding to IGTF 1.88 release.

* Mon Oct 30 2017 Zalak Shah <zsshah@iu.edu> 1.67-1
- CA release corresponding to IGTF 1.87 release.

* Mon Oct 9 2017 Zalak Shah <zsshah@iu.edu> 1.66-1
- CA release corresponding to IGTF 1.86 release.

* Wed Aug 2 2017 Zalak Shah <zsshah@iu.edu> 1.65-1
- CA release corresponding to IGTF 1.85 release.

* Thu Jul 6 2017 Zalak Shah <zsshah@iu.edu> 1.64-1
- CA release corresponding to IGTF 1.84 release.

* Wed Jun 7 2017 Zalak Shah <zsshah@iu.edu> 1.63-1
- CA release corresponding to IGTF 1.83 release.

* Mon Apr 3 2017 Zalak Shah <zsshah@iu.edu> 1.62-1
- CA release corresponding to IGTF 1.82 release.

* Mon Feb 27 2017 Zalak Shah <zsshah@iu.edu> 1.61-1
- CA release corresponding to IGTF 1.81 release.

* Fri Feb 10 2017 Zalak Shah <zsshah@iu.edu> 1.60-1
- CA release corresponding to IGTF 1.80 release.

* Tue Feb 7 2017 Edgar Fajardo <emfajard@ucsd.edu> 1.58-2
- Added the check for the md5sums of the certificates (SOFTWARE-2590)

* Wed Jan 11 2017 Zalak Shah <zsshah@iu.edu> 1.59-1
- CA release corresponding to IGTF 1.79 release.

* Thu Oct 13 2016 Anand Padmanabhan <apadmana@illinois.edu> 1.58-1
- CA release corresponding to IGTF 1.78 release.

* Mon Aug 1 2016 Anand Padmanabhan <apadmana@illinois.edu> 1.57-1
- CA release corresponding to IGTF 1.76 release.

* Tue Jul 5 2016 Anand Padmanabhan <apadmana@illinois.edu> 1.56-1
- CA release corresponding to IGTF 1.75 release.

* Thu May 19 2016 Anand Padmanabhan <apadmana@illinois.edu> 1.55-1
- CA release corresponding to IGTF 1.74 release.

* Thu Mar 31 2016 Anand Padmanabhan <apadmana@illinois.edu> 1.54-1
- CA release corresponding to IGTF 1.73 release.

* Tue Mar 1 2016 Anand Padmanabhan <apadmana@illinois.edu> 1.53-1
- CA release corresponding to IGTF 1.72 release.

* Wed Jan 27 2016 Anand Padmanabhan <apadmana@illinois.edu> 1.52-1
- CA release corresponding to IGTF 1.71 release.

* Mon Nov 30 2015 Jeny Teheran <jteheran@fnal.gov> 1.51-1
- CA release corresponding to IGTF 1.70 release.

* Thu Nov 05 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.50-3
- Remove obsoletes/provides for cilogon-osg-ca-cert, it was broken (SOFTWARE-2097)

* Thu Nov 05 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.50-2
- Add obsoletes/provides for cilogon-osg-ca-cert (SOFTWARE-2097)

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

* Fri Dec 07 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.32-3
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

* Mon Jun 11 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.29-2
- CA release corresponding to IGTF 1.48 

* Fri May 25 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.29-1
- CA release corresponding to IGTF 1.48 prerelease

* Mon May 07 2012 Kevin Hill <kevinh@fnal.gov> - 1.28-1
- CA release corresponding to IGTF 1.47 release

* Fri Mar 30 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.27-1
- CA release corresponding to IGTF 1.46 release
- Note version 1.45 is skipped since IGTF released 1.46 immediately due to problem with CRL from CESNET CA

* Wed Jan 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.26-2
- CA release corresponding to IGTF 1.44 release

* Wed Jan 18 2012 Anand Padmanabhan <apadmana@uiuc.edu> - 1.26-1
- CA release corresponding to IGTF 1.44 prerelease

* Wed Nov 30 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.25-1
- CA release corresponding to IGTF 1.43

* Mon Nov 28 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.24-3
- use mv instead of install to maintain symlink

* Tue Oct 11 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.24-1
- New CA release

* Tue Sep 27 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.23-1
- New CA release

* Fri Sep 09 2011 Anand Padmanabhan <apadmana@uiuc.edu> - 1.22-2
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

