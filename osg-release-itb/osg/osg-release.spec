Name:           osg-release-itb
Version:        3.2
Release:        5%{?dist}
Summary:        OSG Software for Enterprise Linux repository configuration

Group:          System Environment/Base 
License:        GPL 
URL:            http://vdt.cs.wisc.edu/repos

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.


Source0:        osg.repo
Source1:        osg-development.repo
Source2:        osg-testing.repo
Source3:        osg-minefield.repo
Source4:        osg-contrib.repo
Source5:        osg-prerelease.repo
Source6:        osg-empty.repo

Source10:        osg-el6.repo
Source11:        osg-el6-development.repo
Source12:        osg-el6-testing.repo
Source13:        osg-el6-minefield.repo
Source14:        osg-el6-contrib.repo
Source15:        osg-el6-prerelease.repo
Source16:        osg-el6-empty.repo

Source20:        osg-upcoming.repo
Source21:        osg-upcoming-development.repo
Source22:        osg-upcoming-testing.repo
Source23:        osg-upcoming-minefield.repo
Source24:        osg-upcoming-prerelease.repo

Source30:        osg-el6-upcoming.repo
Source31:        osg-el6-upcoming-development.repo
Source32:        osg-el6-upcoming-testing.repo
Source33:        osg-el6-upcoming-minefield.repo
Source34:        osg-el6-upcoming-prerelease.repo

Source40:        RPM-GPG-KEY-OSG

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

%if 0%{?el6}
Requires:      redhat-release >=  6
%else
Requires:      redhat-release >=  5
%endif

Obsoletes:     vdt-release

%description
This package contains the OSG Software for Enterprise Linux repository
configuration for yum.

%prep
exit 0

%build
exit 0


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE40} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OSG

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%if 0%{?el6}
install -pm 644 $RPM_SOURCE_DIR/osg-el6*.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
%else
rm -f $RPM_SOURCE_DIR/osg-el6*.repo
install -pm 644 $RPM_SOURCE_DIR/osg*.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG


%changelog
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
