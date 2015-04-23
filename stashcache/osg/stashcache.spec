Name:      stashcache
Summary:   StashCache metapackages
Version:   0.1
Release:   2%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch
Source0:   xrootd-stashcache-origin-server.cfg.in
Source1:   xrootd-stashcache-cache-server.cfg.in

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%define originhost_prod stash.opensciencegrid.org
%define originhost_itb  stash-itb.opensciencegrid.org

%description
%{summary}

%package origin-server
Group: Grid
Summary: Metapackage for the origin server

Requires: xrootd-server >= 1:4.1.0

%description origin-server
%{summary}

%package cache-server
Group: Grid
Summary: Metapackage for a cache server

Requires: xrootd-server >= 1:4.1.0

%description cache-server
%{summary}


%install
mkdir -p %{buildroot}%{_sysconfdir}/xrootd
for src in "%{SOURCE0}" "%{SOURCE1}"; do
    dst=$(basename "$src" .cfg.in)
    sed -i -e "s#@LIBDIR@#%{_libdir}#" "$src"
    sed -e "s#@ORIGINHOST@#%{originhost_prod}#" \
        "$src" > "%{buildroot}%{_sysconfdir}/xrootd/${dst}.cfg"
    sed -e "s#@ORIGINHOST@#%{originhost_itb}#" \
        "$src" > "%{buildroot}%{_sysconfdir}/xrootd/${dst}-itb.cfg"
done

%clean
rm -rf %{_buildroot}

%files origin-server
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-origin-server.cfg
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-origin-server-itb.cfg

%files cache-server
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-cache-server.cfg
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-cache-server-itb.cfg

%changelog
* Thu Apr 23 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.1-2.osg
- Renamed stashcache-server to stashcache-cache-server, and stashcache-origin
  to stashcache-origin-server; rename config files to match

* Wed Apr 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.1-1.osg
- Created metapackages with stub config files

