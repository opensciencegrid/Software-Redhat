Name:           osg-release
Version:        3.2
Release:        2%{?dist}
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

Source10:        osg-el6.repo
Source11:        osg-el6-development.repo
Source12:        osg-el6-testing.repo
Source13:        osg-el6-minefield.repo
Source14:        osg-el6-contrib.repo
Source15:        osg-el6-prerelease.repo

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
install -pm 644 $RPM_SOURCE_DIR/osg.repo $RPM_SOURCE_DIR/osg-[^e][^l][^6]*.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG


%changelog
* Tue Oct 29 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.1-2
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

