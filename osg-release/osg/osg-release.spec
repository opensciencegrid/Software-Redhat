Name:           osg-release
Version:        3.0 
Release:        5
Summary:        OSG Software for Enterprise Linux repository configuration

Group:          System Environment/Base 
License:        GPL 
URL:            http://vdt.cs.wisc.edu/repos

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:	osg-repo.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:      redhat-release >=  5
Conflicts:     fedora-release

Obsoletes:     vdt-release

%description
This package contains the OSG Software for Enterprise Linux repository
configuration for yum.

%prep
%setup -q  -c -T
#install -pm 644 %{SOURCE0} .
#install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
#install -Dpm 644 %{SOURCE0} \
#    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL

# yum
#install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
#install -pm 644 %{SOURCE2} %{SOURCE3} %{SOURCE4} \
#    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
tar xzf %{SOURCE0}
mkdir -p $RPM_BUILD_ROOT
mv * $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
#%doc GPL
%config(noreplace) /etc/yum.repos.d/*
#/etc/pki/rpm-gpg/*


%changelog
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

* Tue Aug 10 2010 Seth Vidal <skvidal at fedoraproject.org> - 5-4
- conflict fedora-release so people don't indadvertently do something silly

* Fri Apr 25 2008 Matt Domsch <Matt_Domsch@dell.com> - 5-3
- use mirrorlists in epel-testing.repo
- use download.fedoraproject.org in (commented out) baseurls

* Mon Apr 02 2007 Michael Stahnke <mastahnke@gmail.com> - 5-2
- Missed a syntax correction in epel-testing.repo

* Mon Apr 02 2007 Michael Stahnke <mastahnke@gmail.com> - 5-1
- Hard coded version '5' in epel yum repo files. 

* Mon Apr 02 2007 Michael Stahnke <mastahnke@gmail.com> - 5-0
- Initial Package for RHEL 5
