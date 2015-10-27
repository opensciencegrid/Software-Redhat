Name:      stashcache-daemon
Summary:   Manage StashCache with HTCondor
Version:   0.3
Release:   3%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch
Source0:   %{name}-%{version}.tar.gz
Patch0: remove_2.6isms.patch
Patch1: update_central_collector.patch

Requires: xrootd-server
Requires: xrootd-python >= 1:4.2.0
Requires: condor-python >= 8.3.5

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
%patch0 -p3
%patch1 -p3

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
* Tue Jul 07 2015 Brian Lin <blin@cs.wisc.edu> 0.3-3
- Advertise stashcache startd and master ads to the central collector (SOFTWARE-1966)

* Tue Jun 30 2015 Brian Lin <blin@cs.wisc.edu> 0.3-2
- Restore ability for the daemon to run on EL5

* Thu Jun 25 2015 Brian Lin <blin@cs.wisc.edu> 0.3-1
- Update the cache query script

* Fri May 29 2015 Brian Lin <blin@cs.wisc.edu> 0.2-1
- Fix Python 2.6isms
- HTCondor heartbeats require at least condor-python 8.3.5

* Thu May 28 2015 Brian Lin <blin@cs.wisc.edu> 0.1-3
- Remove epoch from condor-python requirement

* Thu May 28 2015 Brian Lin <blin@cs.wisc.edu> 0.1-2.osg
- Updated requirements

* Wed May 27 2015 Brian Lin <blin@cs.wisc.edu> 0.1-1.osg
- Initial packaging
