Name:      xcache
Summary:   XCache scripts and configurations
Version:   3.7.0
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       https://opensciencegrid.org/docs/
Source0:   %{name}-%{version}.tar.gz
Source1:   https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/numpy-1.16.6-cp36-cp36m-manylinux1_x86_64.whl
Source2:   https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/cachetools-3.1.1-py2.py3-none-any.whl
Source3:   https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/awkward-0.12.22-py2.py3-none-any.whl
Source4:   https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/uproot_methods-0.7.4-py2.py3-none-any.whl
Source5:   https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/uproot-3.11.7-py2.py3-none-any.whl
Source6:   https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/xxhash-1.4.4-cp36-cp36m-manylinux1_x86_64.whl
Source7:   https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/lz4-2.2.1-cp36-cp36m-manylinux1_x86_64.whl

Source11:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/awkward-0.14.0-py2.py3-none-any.whl
Source12:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/awkward-2.0.7-py3-none-any.whl
Source13:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/awkward_cpp-8-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
Source14:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/cachetools-5.3.0-py3-none-any.whl
Source15:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/lz4-4.3.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
Source16:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/numpy-1.24.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
Source17:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/packaging-23.0-py3-none-any.whl
Source18:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/typing_extensions-4.4.0-py3-none-any.whl
Source19:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/uproot-5.0.2-py3-none-any.whl
Source20:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/uproot_methods-0.9.2-py3-none-any.whl
Source21:  https://vdt.cs.wisc.edu/upstream/xcache/3.0.0/python-deps/el9/xxhash-3.2.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl


BuildRequires: systemd
%{?systemd_requires}

%define __python /usr/bin/python3
BuildRequires: python3-devel
BuildRequires: python3-pip

# Necessary for daemon to report back to the OSG Collector.
BuildRequires: python3-condor
BuildRequires: python3-xrootd
Requires: python3-condor
Requires: python3-xrootd

Requires: voms-clients-cpp

# We use authz library appending syntax for SciTokens, which requires 5.1.0+ (SOFTWARE-4431)
Requires: xrootd-server >= 1:5.1.0

# Use common OSG XRootD configuration
Requires: osg-xrootd >= 3.6

Requires: grid-certificates >= 7
Requires: vo-client
Requires: fetch-crl
Requires: xrootd-scitokens

Provides: stashcache-daemon = %{name}-%{version}
Obsoletes: stashcache-daemon < 1.0.0

%description
%{summary}

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post xcache-reporter.service xcache-reporter.timer xrootd-renew-proxy.service xrootd-renew-proxy.timer
%preun
%systemd_preun xcache-reporter.service xcache-reporter.timer xrootd-renew-proxy.service xrootd-renew-proxy.timer
%postun
%systemd_postun_with_restart xcache-reporter.service xcache-reporter.timer xrootd-renew-proxy.service xrootd-renew-proxy.timer

########################################
%package -n xcache-consistency-check
Summary: Consistency check for root files
AutoReq: no
%global __provides_exclude ^libgfortran.*\\.so.*$|^libopenblasp.*\\.so.*$

Requires: xz
Requires: xrootd-server
%if 0%{?el9}
Requires: python3.9(x86-64)
%else
Requires: python36(x86-64)
%endif

%description -n xcache-consistency-check
%{summary}

%post -n xcache-consistency-check

/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post xcache-consistency-check.service xcache-consistency-check.timer
%preun -n xcache-consistency-check
%systemd_preun xcache-consistency-check.service xcache-consistency-check.timer
%postun -n xcache-consistency-check
%systemd_postun_with_restart xcache-consistency-check.service xcache-consistency-check.timer

########################################
%package -n stash-origin
Summary: The OSG Data Federation origin server

Requires: %{name} = %{version}
Requires: wget
Requires: xrootd-client

Provides: stashcache-origin-server = %{name}-%{version}
Obsoletes: stashcache-origin-server < 1.0.0
Conflicts: osg-xrootd-standalone

%description -n stash-origin
%{summary}

%post -n stash-origin
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post xrootd@stash-origin.service cmsd@stash-origin.service
%preun -n stash-origin
%systemd_preun xrootd@stash-origin.service cmsd@stash-origin.service
%postun -n stash-origin
%systemd_postun_with_restart xrootd@stash-origin.service cmsd@stash-origin.service

########################################
%package -n stash-cache
Summary: The OSG data federation cache server

Requires: %{name} = %{version}
Requires: wget
Requires: xrdcl-http
Requires: xrootd-tcp-stats

Provides: stashcache-cache-server = %{name}-%{version}
Provides: stashcache-cache-server-auth = %{name}-%{version}
Obsoletes: stashcache-cache-server < 1.0.0
Obsoletes: stashcache-cache-server-auth < 1.0.0
Conflicts: osg-xrootd-standalone

%description -n stash-cache
%{summary}

%post -n stash-cache
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post xrootd@stash-cache.service stash-authfile@cache.service stash-authfile@cache.timer xrootd@stash-cache-auth.service
%preun -n stash-cache
%systemd_preun xrootd@stash-cache.service stash-authfile@cache.service stash-authfile@cache.timer xrootd@stash-cache-auth.service
%postun -n stash-cache
%systemd_postun_with_restart xrootd@stash-cache.service stash-authfile@cache.service stash-authfile@cache.timer xrootd@stash-cache-auth.service

########################################
%package -n atlas-xcache
Summary: The ATLAS data federation cache server

Requires: %{name} = %{version}
Requires: wget
Requires: xrootd-rucioN2N-for-Xcache

%description -n atlas-xcache
%{summary}

%post -n atlas-xcache
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post xrootd@atlas-xcache.service
%preun -n atlas-xcache
%systemd_preun xrootd@atlas-xcache.service
%postun -n atlas-xcache
%systemd_postun_with_restart xrootd@atlas-xcache.service

########################################
%package -n cms-xcache
Summary: The CMS data federation cache server

Requires: %{name} = %{version}
Requires: wget
%description -n cms-xcache
%{summary}
%post -n cms-xcache
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post xrootd@cms-xcache.service cmsd@cms-xcache.service
%preun -n cms-xcache
%systemd_preun xrootd@cms-xcache.service cmsd@cms-xcache.service
%postun -n cms-xcache
%systemd_postun_with_restart xrootd@cms-xcache.service cmsd@cms-xcache.service

%package -n xcache-redirector
Summary: The XCache redirector

Requires: %{name} = %{version}
%description -n xcache-redirector
%{summary}
%post -n xcache-redirector
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%systemd_post xrootd@xcache-redir.service cmsd@xcache-redir.service
%preun -n xcache-redirector
%systemd_preun xrootd@xcache-redir.service cmsd@xcache-redir.service
%postun -n xcache-redirector
%systemd_postun_with_restart xrootd@xcache-redir.service cmsd@xcache-redir.service 

%prep
%setup -n %{name}-%{version} -q

%install
#find . -type f -exec sed -ri '1s,^#!\s*(/usr)?/bin/(env )?python.*,#!%{__python},' '{}' +

mkdir -p %{buildroot}%{_sysconfdir}/xrootd
mkdir -p %{buildroot}/usr/lib/xcache-consistency-check
%if 0%{?el9}
for whl in %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} \
           %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20} \
           %{SOURCE21}
%else
for whl in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} \
           %{SOURCE7}
%endif
do
    %{__python} -m pip install -I --no-deps "$whl" --root %{buildroot}/usr/lib/xcache-consistency-check
done

make install DESTDIR=%{buildroot} PYTHON=%{__python}

# Create xrootd certificate directory
mkdir -p %{buildroot}%{_sysconfdir}/grid-security/xrd

%files
%{_libexecdir}/%{name}/xcache-reporter
%{_libexecdir}/%{name}/renew-proxy
%{python3_sitelib}/xrootd_cache_stats.py*
%{python3_sitelib}/__pycache__/xrootd_cache_stats.*
%{_unitdir}/xcache-reporter.service
%{_unitdir}/xcache-reporter.timer
%{_unitdir}/xrootd-renew-proxy.service
%{_unitdir}/xrootd-renew-proxy.timer
%config %{_sysconfdir}/xrootd/config.d/40-xcache-auth.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/90-xcache-logging.cfg
%config(noreplace) %{_sysconfdir}/xrootd/digauth.cfg
%attr(-, xrootd, xrootd) %{_sysconfdir}/grid-security/xrd
%attr(0755, xrootd, xrootd) %dir /run/xcache-auth
%{_tmpfilesdir}/xcache.conf

%files -n xcache-consistency-check
%attr(0755, xrootd, xrootd) %{_bindir}/xcache-consistency-check
%dir %attr(0755, xrootd, xrootd) /var/lib/xcache-consistency-check
%{_unitdir}/xcache-consistency-check.service
%{_unitdir}/xcache-consistency-check.timer
%config(noreplace) %{_sysconfdir}/xrootd/xcache-consistency-check.cfg
/usr/lib/xcache-consistency-check/*

%files -n stash-origin
%config %{_sysconfdir}/xrootd/xrootd-stash-origin.cfg
%config %{_sysconfdir}/xrootd/xrootd-stash-origin-auth.cfg
%config %{_sysconfdir}/xrootd/config.d/50-stash-origin-authz.cfg
%config %{_sysconfdir}/xrootd/config.d/50-stash-origin-paths.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/10-origin-site-local.cfg
%{_libexecdir}/%{name}/authfile-update
%{_unitdir}/stash-authfile@.service
%{_unitdir}/stash-authfile@.timer
%{_unitdir}/xrootd@stash-origin.service.d/10-stash-origin-overrides.conf
%{_unitdir}/xrootd@stash-origin-auth.service.d/10-stash-origin-auth-overrides.conf
%{_unitdir}/xrootd-privileged@stash-origin-auth.service.d
%{_unitdir}/cmsd@stash-origin.service.d/10-stash-origin-overrides.conf
%{_unitdir}/cmsd@stash-origin-auth.service.d/10-stash-origin-auth-overrides.conf
%{_unitdir}/cmsd-multiuser@.service
%{_unitdir}/cmsd-privileged@stash-origin-auth.service.d/10-stash-origin-auth-overrides.conf
%{_tmpfilesdir}/stash-origin.conf
%attr(0755, xrootd, xrootd) %dir /run/stash-origin/
%attr(0755, xrootd, xrootd) %dir /run/stash-origin-auth/

%files -n stash-cache
%config(noreplace) %{_sysconfdir}/xrootd/Authfile-auth
%config(noreplace) %{_sysconfdir}/xrootd/xcache-robots.txt
%config %{_sysconfdir}/xrootd/xrootd-stash-cache.cfg
%config %{_sysconfdir}/xrootd/xrootd-stash-cache-auth.cfg
%config %{_sysconfdir}/xrootd/config.d/40-stash-cache-plugin.cfg
%config %{_sysconfdir}/xrootd/config.d/50-stash-cache-authz.cfg
%config %{_sysconfdir}/xrootd/config.d/50-stash-cache-paths.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/90-stash-cache-disks.cfg
%{_libexecdir}/%{name}/authfile-update
%{_unitdir}/stash-authfile@.service
%{_unitdir}/stash-authfile@.timer
%{_unitdir}/xrootd@stash-cache.service.d/10-stash-cache-overrides.conf
%{_unitdir}/xrootd@stash-cache-auth.service.d/10-stash-cache-auth-overrides.conf
%{_tmpfilesdir}/stash-cache.conf
%attr(0755, xrootd, xrootd) %dir /run/stash-cache/
%attr(0755, xrootd, xrootd) %dir /run/stash-cache-auth/

%files -n atlas-xcache
%config %{_sysconfdir}/xrootd/xrootd-atlas-xcache.cfg
%{_unitdir}/xrootd@atlas-xcache.service.d/10-atlas-xcache-overrides.conf
%{_unitdir}/xrootd-renew-proxy.service.d/10-atlas-refresh-proxy-overrides.conf
%config %{_sysconfdir}/xrootd/config.d/40-atlas-xcache-plugin.cfg
%config %{_sysconfdir}/xrootd/config.d/50-atlas-xcache-paths.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/90-atlas-xcache-disks.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/95-atlas-xcache-logging.cfg

%files -n cms-xcache
%config %{_sysconfdir}/xrootd/xrootd-cms-xcache.cfg
%config %{_sysconfdir}/xrootd/Authfile-cms-xcache
%{_unitdir}/xrootd@cms-xcache.service.d/10-cms-xcache-overrides.conf
%{_unitdir}/cmsd@cms-xcache.service.d/10-cms-xcache-overrides.conf
%{_unitdir}/xrootd-renew-proxy.service.d/10-cms-refresh-proxy-overrides.conf
%config %{_sysconfdir}/xrootd/config.d/30-cms-xcache-authz.cfg
%config %{_sysconfdir}/xrootd/config.d/40-cms-xcache-plugin.cfg
%config %{_sysconfdir}/xrootd/config.d/50-cms-xcache-paths.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/90-cms-xcache-disks.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/90-cms-xcache-local-redirector.cfg
%config(noreplace) %{_sysconfdir}/xrootd/config.d/95-cms-xcache-logging.cfg


%files -n xcache-redirector
%config %{_sysconfdir}/xrootd/xrootd-xcache-redir.cfg
%config %{_sysconfdir}/xrootd/config.d/03-redir-tuning.cfg

%changelog
* Fri Mar 22 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.7.0-1
- Make use of grid-mapfile downloaded from Topology.
  Requires osg-xrootd >= 3.6-24 (for OSG 3.6) or >= 23-6 (for OSG 23)

* Tue Dec 12 2023 Matt Westphall <westphall@wisc.edu> - 3.6.0-1
- Make redirector line in cache config customizable (SOFTWARE-5641)
- check for *.local files in /etc/xrootd in authfile-updater (SOFTWARE-5597)

* Thu Sep 28 2023 Brian Lin <blin@cs.wisc.edu> - 3.5.0-4
- Fix EL9 python dependency

* Fri Jun 23 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5.0-2
- Add xrdcl-http dependency for stash-cache (SOFTWARE-5606)

* Tue May 16 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5.0-1
- Have the authfile updater get a grid-mapfile from Topology for
  stash-cache-auth and stash-origin-auth (SOFTWARE-5467)

* Fri Feb 24 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4.0-3
- Merge changes for building on el9

* Fri Feb 24 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4.0-2
- Add python3-condor and python3-xrootd build dependencies so we don't build RPMs for repos
  which they can't be installed from.

* Fri Feb 03 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4.0-1
- Enable XRootD TCP Stats for stash-cache and stash-cache-auth (SOFTWARE-5373)

* Fri Feb 03 2023 Carl Edquist <edquist@cs.wisc.edu> - 3.3.0-1.1
- Add python3-pip build requirement for el9 (SOFTWARE-5416)

* Fri Dec 02 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3.0-1
- Remove X.509 proxy requirement for stash-cache xrootd instance (SOFTWARE-5366)

* Mon Oct 10 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.2.3-1
- Replace cmsd-multiuser overrides with cmsd-privileged (SOFTWARE-5338)

* Mon Sep 19 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.2.2-1
- Add scitokens.conf.local file support for caches too (SOFTWARE-5315)

* Thu Sep 15 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.2.1-1
- Allow specifying the xrootd instance (e.g. stash-cache, stash-origin-auth) to
  authfile-update (SOFTWARE-5028)
- Split stash-origin's "originexport" var into "PublicOriginExport" and
  "AuthOriginExport" (SOFTWARE-5303)
- Append contents of a "scitokens.conf.local" file to generated scitokens.conf (SOFTWARE-5315)
- Includes Fri Sep 02 2022 Carl Edquist <edquist@cs.wisc.edu>:
    - Generate authfile even if origin serves no public data (SOFTWARE-5028)
    - Refactor stash-authfile systemd files

* Fri May 13 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.1.0-1
- Drop GSI auth method (SOFTWARE-5121)
- Add --debug option to xcache-reporter (SOFTWARE-5119)

* Mon May 09 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.0.1-1.2
- Add Conflicts for osg-xrootd-standalone (SOFTWARE-4668)

* Wed Apr 20 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.0.1-2
- Fix python and python-xrootd requirements (SOFTWARE-5126)

* Thu Mar 24 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.0.1-1
- Fix PYTHONPATH in xcache-consistency-check service file

* Tue Mar 01 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.0.0-2
- Fix Python 3 bytes/str conversion errors (SOFTWARE-5019)
- Always use Python 3 scripts; update dependencies for xcache-consistency-check
- Fix xrootd_cache_stats.py library location issues (SOFTWARE-5019)

* Wed Oct 27 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.0.0-1
- Drop lcmaps config; use XrdVoms instead (from osg-xrootd 3.6)
- Add overrides for xrootd-privileged@stash-origin-auth, and add
  cmsd-multiuser@.service for running an auth stash-origin with multiuser (SOFTWARE-4792)
- Append contents of /run/stash-origin/Authfile.local and /run/stash-origin-auth/Authfile.local
  to generated /run/stash-origin/Authfile and /run/stash-origin-auth/Authfile,
  respectively

* Thu May 06 2021  <karo@cs.wisc.edu> - 2.0.1-3
- Packaging fixes for el7 (SOFTWARE-4476)

* Wed May 05 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.0.1-2
- Packaging fixes for el8 (SOFTWARE-4476)

* Tue May 04 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.0.1-1
- Add Python3 support for scripts (SOFTWARE-4476)

* Mon Feb 1 2021 Brian Lin <blin@cs.wisc.edu> - 2.0.0-1
- Add requirement for XRootD 5.1 (SOFTWARE-4431)

* Wed Jan 27 2021 Brian Lin <blin@cs.wisc.edu> - 1.5.5-1
- Fix ofs.authlib append syntax (SOFTWARE-4431)

* Tue Jan 26 2021 Brian Lin <blin@cs.wisc.edu> - 1.5.4-1
- Update configuration to append SciTokens to the auth list for XRootD
  5+ (SOFTWARE-4431)

* Wed Jan 13 2021 Brian Lin <blin@cs.wisc.edu> - 1.5.3-1
- Add default values for the number of blocks and threads used for
  writing in parallel
- Add new ATLAS XCache default values for the write queue, block size,
  and the number of prefetch blocks
- Disable additional ATLAS debugging by default

* Tue Nov 10 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.5.2-2
- Include xrootd-client in stash-origin since it's used for validation (SOFTWARE-4353)

* Fri Jul 31 2020 Edgar Fajardo <emfajard@ucsd.edu> - 1.5.2-1
- Fixing some bugs for el8 suppport (SOFTWARE-4158)

* Mon Jul 27 2020 Edgar Fajardo <emfajard@ucsd.edu> - 1.5.0-1
- Adding support for el8 installation (SOFTWARE-4158)
- Added SciTokens support (SOFTWARE-3562)

* Tue May 12 2020 Diego Davila <didavila@ucsd.edu> - 1.4.0-1
- Adding/Fixing functionality to the XCache Consistency Check tool (SOFTWARE-4047)

* Mon Jan 27 2020 Diego Davila <didavila@ucsd.edu> - 1.3.0-1
- Adding subpackage for consistency check (SOFTWARE-3976)

* Wed Dec 18 2019 Edgar Fajardo <emfajard@ucsd.edu> - 1.2.1-1
- Fixed bug in which cmsd filesystem was configured to be the cache (SOFTWARE-3952)

* Mon Sep 23 2019 Edgar Fajardo <emfajard@ucsd.edu> - 1.2.0-1
- Adding the subpackage for XCache redirector

* Mon Aug 19 2019 Brian Lin <blin@cs.wisc.edu> - 1.1.1-1
- Restore StashCache HTTP port to 8000

* Mon Aug 19 2019 Brian Lin <blin@cs.wisc.edu> - 1.1.0-1
- Use osg-xrootd (SOFTWARE-3558)

* Wed Aug 7 2019 Edgar Fajardo <emfajard@ucsd.edu> - 1.1.0-0.4
- Changing order of LCMAPS configuration files for CMS
- Fixing bug on refresh-proxy call for CMS and ATLAS proxies

* Mon Aug 5 2019 Edgar Fajardo <emfajard@ucsd.edu> - 1.1.0-0.3
- Adding ATLAS and CMS overides for the proxy generation
- Adding RucioN2N config for ATLAS Xcache (SOFTWARE-3784)

* Fri Aug 2 2019 Brian Lin <blin@cs.wisc.edu> - 1.1.0-0.2
- Changing auths options for lcmaps

* Wed Jul 31 2019 Edgar Fajardo <emfajard@ucsd.edu> - 1.1.0-0.1
- Add ATLAS and CMS XCache (SOFTWARE-3583, SOFTWARE-3584)

* Wed May 01 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.5-1
- Start services after network is up (SOFTWARE-3681)

* Mon Apr 08 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.3-1
- Fix *-overrides.conf syntax

* Thu Mar 14 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.2-1
- Add missing xrootd-lcmaps dependency for the origin
- Start and stop xrootd and cmsd together for the origin (SOFTWARE-3544)
- Drop workaround for LIGO not being part of the OSG Data Federation (SOFTWARE-3507)
- Start proxy renewal script for both unauth and auth cache and origin instances;
  only mandatory for auth cache
- Fix permissions in tmpfiles.d config for cache
- Add vo-client and voms-clients-cpp dependency
- Proxy renewal script now uses voms-proxy-init instead of grid-proxy-init
- "sitename" xrootd config variable in 10-common-site-local.cfg renamed to "resourcename"

* Wed Jan 30 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.1-1
- Config changes:
  - fix name of logging config and decrease verbosity
  - change default root dir from /stash to /mnt/stash
  - various other tweaks for understandability

* Mon Jan 14 2019 Brian Bockelman <brian.bockelman@cern.ch> - 1.0.0-1
- Final release of XCache 1.0.0.

* Fri Jan 11 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.0-0.rc2
- Auto-generate the origin authorization files as well.
- Fix configuration file syntax.

* Mon Jan 7 2019 Brian Bockelman <bbockelm@cse.unl.edu> - 1.0.0-0.rc1
- Overhaul configuration files to use new Xrootd 'continue' directive.
- Utilize systemd dependencies so all services start when XRootD does.
- Auto-generate the authorization files.

* Tue Oct 23 2018 Marian Zvada <marian.zvada@cern.ch> 0.10-1
- Remove condor daemon dependency from stats reporter
- Use systemd timer to periodically report stats
- Modify stats reporter to use python multiprocessing so ad won't expire
  during a long collection run
- Update XRootD cinfo parser to format v2

* Fri Sep 28 2018 Mátyás Selmeci <matyas@cs.wisc.edu> 0.9-1
- https://github.com/opensciencegrid/StashCache-Daemon/pull/8
  - Reduce the dependencies for the unauthenticated xrootd
  - Create the config and systemd unit files during the make install process
  - Tidy the stashcache configuration
    - Reduce the default disk usage of the cache to 90/95% to avoid
      accidentally filling filesystems too full
    - Move the certificate configuration inside the auth instance of xrootd
    - Set pfc.ram 7g to allow a bit of room for the OS on 8GB system
      (documented minimum RAM)
    - Added pss.origin redirector-itb as a commented line, rather than adding
      a separate itb config file

* Thu Aug 24 2017 Marian Zvada <marian.zvada@cern.ch> 0.8-1
- change homepage in origin server xrootd config file
- set proper redirector hostname in xrootd config files
- updated Makefile, replace properly VERSION in src/stashcache for make install target

* Thu Jun 1 2017 Marian Zvada <marian.zvada@cern.ch> 0.7-2
- added stanza so that we don't build StashCache for EL6
- no epoch of xrootd-lcmaps-1.3.3 for cache-server requirement

* Wed May 31 2017 Marian Zvada <marian.zvada@cern.ch> 0.7-1
- SOFTWARE-2295: restructure under opensciencegrid/StashCache-Daemon.git 

* Thu Feb 25 2016 Marian Zvada <marian.zvada@cern.ch> 0.6-2
- SOFTWARE-2196: redirector renamed to redirector.osgstorage.org, http export support
- SOFTWARE-2195: complete revamp of the origin server config using new redirector

* Tue Sep 29 2015 Brian Lin <blin@cs.wisc.edu> 0.6-1
- Bug fixes to xrootd service management

* Fri Sep 25 2015 Brian Lin <blin@cs.wisc.edu> 0.5-2
- Add systemd support

* Fri Sep 25 2015 Brian Lin <blin@cs.wisc.edu> 0.5-1
- Use FQDN instead of hostname in stashcache-daemon (SOFTWARE-2049)
- Refuse to start if missing host cert or key (SOFTWARE-2026)
- Fix log message if the xrootd service is already running

* Thu Aug 20 2015 Brian Lin <blin@cs.wisc.edu> 0.4-2
- Fix advertisement to central collector

* Thu Aug 20 2015 Brian Lin <blin@cs.wisc.edu> 0.4-1
- Advertise STASHCACHE_DaemonVersion in MasterAd (SOFTWARE-1971)
- Log daemon activity to /var/log/condor/StashcacheLog
- Use TCP to advertise StashCache ads

* Wed Jul 15 2015 Brian Lin <blin@cs.wisc.edu> 0.3-4
- Merge stashcache and stashcache-daemon packages

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

* Thu Apr 23 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.1-2.osg
- Renamed stashcache-server to stashcache-cache-server, and stashcache-origin
  to stashcache-origin-server; rename config files to match

* Wed Apr 22 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 0.1-1.osg
- Created metapackages with stub config files
