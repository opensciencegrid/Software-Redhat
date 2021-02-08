Name:           osg-release-itb
Version:        3.6
Release:        2%{?dist}
Summary:        OSG Software for Enterprise Linux repository configuration

License:        GPL
URL:            https://repo-itb.opensciencegrid.org/

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.


Source0:        generate-repo-files.sh
Source1:        repoinfo.txt
Source2:        template.repo.standard
Source3:        template.repo.basic
Source4:        template.repo.koji
Source5:        template.repo.direct

Source40:       RPM-GPG-KEY-OSG


BuildArch:      noarch

Requires:       redhat-release >= %{rhel}

Obsoletes:      vdt-release

%description
This package contains the OSG Software for Enterprise Linux repository
configuration for yum.

%prep
exit 0

%build
# generate .repo files for current rhel version
%{SOURCE0} %{SOURCE1} %{rhel}


%install

#GPG Key
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE40} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OSG

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

install -m 644 *.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
sed -i -e 's/gpgcheck=1/gpgcheck=0/' $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/*-minefield.repo

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG


%changelog
* Mon Feb 08 2021 Brian Lin <blin@cs.wisc.edu> - 3.6-2
- Rebuild for DevOps repo (SOFTWARE-4465)

* Mon Feb 08 2021 Brian Lin <blin@cs.wisc.edu> - 3.6-1
- New OSG 3.6 repos (SOFTWARE-4465)

* Mon Aug 05 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-2
- Rename goc repos -> devops (SOFTWARE-3291)

* Fri Aug 02 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-1
- New OSG 3.5 repos (SOFTWARE-3761)

* Wed Feb 13 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-7
- Add rolling release for upcoming (SOFTWARE-3465)

* Mon Feb 11 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-6
- Add rolling release repo (SOFTWARE-3465)

* Wed May 02 2018 Carl Edquist <edquist@cs.wisc.edu> - 3.4-5
- Drop consider_as_osg from *.repo files (SOFTWARE-3204)

* Wed Mar 07 2018 Brian Lin <blin@cs.wisc.edu> - 3.4-4
- Revert HTTP -> HTTPS testing for Koji repositories due to certificate verification failures

* Fri Feb 08 2018 Brian Lin <blin@cs.wisc.edu> - 3.4-3
- Use HTTPS for repo URLs

* Wed Sep 13 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4-2
- Generate goc repos as 'direct' (no mirror) (SOFTWARE-2890)

* Wed May 10 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-1
- Release OSG 3.4

* Mon Feb 22 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-5
- Use koji.chtc.wisc.edu instead of koji-hub.batlab.org for minefield repos
  (SOFTWARE-2220)

* Thu Jul 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-4
- Add goc-itb, goc repos (SOFTWARE-1969)

* Thu Jul 16 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-2
- Disable gpgcheck for minefield repos since some packages are unsigned

* Mon May 04 2015 Carl Edquist <edquist@cs.wisc.edu> - 3.3-1
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

* Tue Oct 29 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2-1
- Update to osg-3.2, and new style koji tags for minefield repos

* Tue Oct 01 2013  <edquist@cs.wisc.edu> - 3.0-23
- Update .repo files to point to new directory layout

* Wed Sep 11 2013 Brian Lin <blin@cs.wisc.edu> - 3.0-22
- Create osg-release-itb
