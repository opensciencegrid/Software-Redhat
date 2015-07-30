Name:           osg-release-itb
Version:        3.2
Release:        8%{?dist}
Summary:        OSG Software for Enterprise Linux repository configuration

Group:          System Environment/Base
License:        GPL
URL:            http://vdt.cs.wisc.edu/repos

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.


Source0:        generate-repo-files.sh
Source1:        repoinfo.txt
Source2:        template.repo.standard
Source3:        template.repo.basic
Source4:        template.repo.koji

Source40:       RPM-GPG-KEY-OSG

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
rm -rf $RPM_BUILD_ROOT

#GPG Key
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE40} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OSG

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

install -m 644 *.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG


%changelog
* Thu Jul 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.2-8
- Add goc-itb, goc repos (SOFTWARE-1969)

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
