%define series 25

Name:           osg-release
Version:        %{series}
Release:        1%{?dist}
Summary:        OSG Software for Enterprise Linux repository configuration

License:        GPL
URL:            https://repo.osg-htc.org/

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.


Source0:        generate-repo-files.sh
Source1:        repoinfo.txt
Source2:        template.repo.standard
Source3:        template.repo.basic
Source4:        template.repo.kojira
Source5:        template.repo.direct
Source6:        template.repo.contrib
Source7:        template.repo.distrepo

Source41:       RPM-GPG-KEY-OSG-%{series}-auto
Source42:       RPM-GPG-KEY-OSG-%{series}-developer


BuildArch:      noarch

Requires:       redhat-release >= %{rhel}

%description
This package contains the OSG Software for Enterprise Linux repository
configuration for yum.

%prep
exit 0

%build
# generate .repo files for current rhel version
%{SOURCE0} %{SOURCE1} %{rhel}


%install

# GPG Key
install -D -pm 644 %{SOURCE41} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OSG-%{series}-auto
install -D -pm 644 %{SOURCE42} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OSG-%{series}-developer

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

install -m 644 *.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG-%{series}-auto
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG-%{series}-developer


%changelog
* Fri Sep 05 2025 Matt Westphall <westphall@wisc.edu> - 25-1
- Initial OSG 25 release (SOFTWARE-6054)

* Fri Jul 25 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 24-4
- Bump to rebuild

* Mon Sep 30 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 24-2
- Do not use "distrepo" repos for minefield (SOFTWARE-5985)

* Tue Sep 24 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 24-1
- Initial OSG 24 release (SOFTWARE-5985)

* Wed Oct 18 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 23-5
- Use 'auto' key for prerelease repo

* Thu Sep 28 2023 Matt Westphall <westphall@wisc.edu> - 23-4
- Prefix internal repos with 'osg-' (SOFTWARE-5691)

* Thu Aug 31 2023 Matt Westphall <westphall@wisc.edu> - 23-3
- Update with new OSG repo name conventions, add new GPG keys (SOFTWARE-5667)

* Fri Aug 18 2023 Brian Lin <blin@cs.wisc.edu> - 23-1
- Initial OSG 23 release (SOFTWARE-5503)

* Wed Dec 28 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.6-13
- rebuild

* Wed Dec 28 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.6-12
- Replace RPM-GPG-KEY-OSG-3 with RPM-GPG-KEY-OSG-4 (SOFTWARE-5424)

* Fri Dec 16 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-11
- Only distribute the relevant GPGKEY for each platform (SOFTWARE-5408)

* Mon Dec 12 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-10
- Drop RPM-GPG-KEY-OSG; teplate GPGKEY on EL# (SOFTWARE-5408)

* Mon Dec 12 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.6-9
- Replace RPM-GPG-KEY-OSG-3 with something that's accepted by rpm on both EL7 and EL9 (SOFTWARE-5408)

* Mon Dec 12 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-8
- Update domain name in uid for RPM-GPG-KEY-OSG-3 (SOFTWARE-5408)

* Fri Dec 09 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-7
- Bump for rpm signing (SOFTWARE-5408)

* Fri Dec 09 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-6
- Provide RPM-GPG-KEY-OSG-3 for .osg36.el9 (SOFTWARE-5408)

* Thu Apr 21 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-5
- Introduce osg-next repos (SOFTWARE-4509)

* Mon Dec 06 2021 Tim Theisen <tim@cs.wisc.edu> - 3.6-4
- Add devops-minefield repository (SOFTWARE-4681)

* Thu Feb 25 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.6-3
- Fix repo files to accept new signing key (SOFTWARE-3275)

* Wed Feb 24 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.6-2
- Add new signing key RPM-GPG-KEY-OSG-2 (SOFTWARE-3275)

* Thu Feb 04 2021 Brian Lin <blin@cs.wisc.edu> - 3.6-1
- Initial OSG 3.6 release (SOFTWARE-4465)

* Thu Jan 14 2021 Carl Edquist <edquist@cs.wisc.edu> - 3.5-5
- Use upcoming series to 3.5-upcoming (SOFTWARE-4420)

* Thu Aug 27 2020 Carl Edquist <edquist@cs.wisc.edu> - 3.5-4
- Drop failovermethod=priority from repo configs (SOFTWARE-4069)

* Mon Oct 14 2019 Diego Davila <didavila@ucsd.edu> - 3.5-3
- Changing "koji.chtc.wisc.edu" for "koji.opensciencegrid.org" (SOFTWARE-3863)
- Fixing date issue on changelog Fri Feb 08 2018 -> Thu

* Mon Aug 05 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-2
- Rename goc repos -> devops (SOFTWARE-3291)

* Fri Aug 02 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-1
- New OSG 3.5 repos (SOFTWARE-3761)

* Tue May 14 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-8
- Use https for koji repos (SOFTWARE-3653)

* Wed Feb 13 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-7
- Add rolling release for upcoming (SOFTWARE-3465)

* Mon Feb 11 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-6
- Add rolling release repo (SOFTWARE-3465)

* Wed May 02 2018 Carl Edquist <edquist@cs.wisc.edu> - 3.4-5
- Drop consider_as_osg from *.repo files (SOFTWARE-3204)

* Wed Mar 07 2018 Brian Lin <blin@cs.wisc.edu> - 3.4-4
- Revert HTTP -> HTTPS testing for Koji repositories due to certificate verification failures

* Thu Feb 08 2018 Brian Lin <blin@cs.wisc.edu> - 3.4-3
- Change references from repo.grid.iu.edu to repo.opensciencegrid.org

* Wed Sep 13 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4-2
- Generate goc repos as 'direct' (no mirror) (SOFTWARE-2890)

* Wed May 10 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-1
- Release OSG 3.4

* Mon Feb 22 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-5
- Use koji.chtc.wisc.edu instead of koji-hub.batlab.org for minefield repos

  (SOFTWARE-2220)
* Thu Jul 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-4
- Add goc-itb, goc repos (SOFTWARE-1969)

* Thu Jul 16 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-2
- Disable gpgcheck for minefield repos since some packages are unsigned

* Fri May 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Make osg-3.3 version

* Tue Sep 30 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.2-7
- Rename debug repos to *-debuginfo (SOFTWARE-1622)

* Thu Jul 17 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.2-6
- Use .repo file templates and support el7 (SOFTWARE-1541)

* Thu Dec 12 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2-5
- Bugfix for el5; glob to exclude el6 packages was also excluding osg-empty

* Mon Dec 09 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2-4
- Add osg-empty repos (SOFTWARE-1237)

* Thu Oct 31 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2-3
- Update prerelease repos to new koji tags

* Tue Oct 29 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2-2
- Update minefield repos to new koji tags

* Tue Oct 22 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.1-2
- Update minefield repos to new koji tags

* Wed Oct 16 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2-1
- Update to osg/3.2 (SOFTWARE-1221)

* Wed Oct 16 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.1-1
- Update from old 3.0 repo layout to new osg/3.1 layout (SOFTWARE-1221)

* Thu Feb 07 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0-22
- Add *upcoming* repos

* Thu Apr 26 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-21
- Changing Requires back to redhat-release > [5|6]

* Thu Apr 26 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-20
- Fixing el5 and el6 requires

* Thu Apr 26 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-19
- Changing requires so only el5 on el5, el6 on el6

* Tue Apr 10 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0-18
- Also fixed baseurl entries in the el5 repo files

* Mon Apr 09 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0-17
- Fixed baseurl entries in the el6 repo files

* Thu Feb 16 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-16
- Turning off el6 minefield

* Mon Feb 13 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-15
- Fixing sources for el5 version of osg-release

* Tue Jan 31 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-14
- Changing mirror urls for el6

* Thu Jan 19 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-13
- Adding preliminary el6 support

* Mon Nov 28 2011 Neha Sharma <neha@fnal.gov> - 3.0-12
- Added consider_as_osg=yes to all osg repo files

* Mon Nov 14 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0-11
- Added osg-prerelease repo

* Fri Sep 23 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0-10
- Previous improvements to debug and source repos were previously not applied to the contrib repo.

* Mon Sep 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0-9
- Added commented-out baseurl line to the .repo files so people have a fallback
  if there is a problem with the mirrors
- Added -debug repositories (disabled by default) for the debuginfo packages
  for development, testing, and release.

* Fri Sep 16 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0-8
- Added RPM signing public key
- Changed all repo files to require gpg check

* Fri Sep 09 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0-7
- Add in stub for the osg-contrib repository.

* Fri Sep 2 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0-6
- Files changed to point to GOC repos
- Removed conflict with fedora-release

* Mon Aug 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-5
- Corrected the source repos

* Thu Aug 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0-4
- Added minefield repository, which reads directly from Koji.

* Thu Aug 04 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0-3
- Rename from VDT-* to OSG-*.

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3.0-2
- Changed vdt-development so that it doesn't force gpg checks

* Wed Jul 06 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3-1
- Adapted EPEL release rpm for use with the VDT

