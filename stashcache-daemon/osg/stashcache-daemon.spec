Name:      stashcache-daemon
Summary:   Manage StashCache with HTCondor
Version:   0.1
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch
Source0:   %{name}-%{version}.tar.gz

Requires: python
Requires: xrootd-server >= 1:4.2.0
Requires: condor >= 8.3.4

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
Provides scripts and configuration for an HTCondor installation that allows for
management of a StashCache cache.

%prep
%setup -q

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sbindir}/stashcache
%{_sysconfdir}/condor/config.d/01-stashcache.conf
%{python_sitelib}/xrootd_cache_stats.py*

%changelog
* Wed May 27 2015 Brian Lin <blin@cs.wisc.edu> 0.1-1.osg
- Initial packaging
