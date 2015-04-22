Name:      stashcache
Summary:   StashCache metapackages
Version:   0.1
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch
Source0:   xrootd-stashcache-origin.cfg.in
Source1:   xrootd-stashcache-server.cfg.in

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%define originhost_prod stash.opensciencegrid.org
%define originhost_itb  stash-itb.opensciencegrid.org

%description
%{summary}

%package origin
Group: Grid
Summary: Metapackage for the origin server

Requires: xrootd-server >= 1:4.1.0

%description origin
%{summary}

%package server
Group: Grid
Summary: Metapackage for a cache server

Requires: xrootd-server >= 1:4.1.0

%description server
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

%files origin
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-origin.cfg
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-origin-itb.cfg

%files server
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-server.cfg
%config(noreplace) %{_sysconfdir}/xrootd/xrootd-stashcache-server-itb.cfg

%changelog
* Wed Apr 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.1-1.osg
- Created metapackages with stub config files

