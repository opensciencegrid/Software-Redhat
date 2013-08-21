Name:           condor-unified-repos
Version:        1.0
Release:        1%{?dist}
Summary:        Development repos for unified condor rpms

Group:          System Environment/Base 
License:        GPL 
URL:            http://vdt.cs.wisc.edu/repos

# This is an OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source5:        el5-condor-unified-development.repo
Source6:        el6-condor-unified-development.repo

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

%if 0%{?el6}
Requires:      redhat-release >=  6
%else
Requires:      redhat-release >=  5
%endif
Requires:      osg-release >= 3.0

%description
This package contains yum repositories required to install
development versions of the unified condor rpm.

%install
rm -rf $RPM_BUILD_ROOT

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%if 0%{?el6}
install -pm 644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
%else
install -pm 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*


%changelog
* Tue Aug 20 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0-1
- Initial release

