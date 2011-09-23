Name:           osg-release
Version:        3.0 
Release:        10
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
Source5:        RPM-GPG-KEY-OSG

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:      redhat-release >=  5

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
install -pm 644 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OSG

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-OSG


%changelog
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

