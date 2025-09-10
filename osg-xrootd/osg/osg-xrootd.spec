Summary: OSG configuration files for XRootD
Name: osg-xrootd
Version: 25
Release: 1%{?dist}
License: ASL 2.0
BuildArch: noarch

Source1: ban-robots.txt
Source2: 10-common-site-local.cfg
Source3: 50-osg-http.cfg
Source4: 50-osg-monitoring.cfg
Source5: 50-osg-paths.cfg
Source6: 40-osg-standalone.cfg
Source7: 90-osg-standalone-paths.cfg
Source8: create_macaroon_secret
Source9: 50-osg-tpc.cfg
Source10: Authfile.example
Source11: 90-xrootd-logging.cfg
Source12: 10-osg-xrdvoms.cfg
Source13: 50-osg-xrdvoms.cfg
Source14: 50-osg-scitokens.cfg
Source15: scitokens.conf

Requires: xrootd >= 1:5.8.4

# Necessary for authentication
Suggests: osg-ca-certs
Requires: grid-certificates >= 7

Requires: vo-client
Requires: fetch-crl
Requires: xrootd-voms

%description
%{summary}

########################################
%package standalone
Summary: OSG configuration files for XRootD standalone installations
Requires: %{name} = %{version}-%release
Requires: xrootd-scitokens
Conflicts: stash-cache
Conflicts: stash-origin

%description standalone
%summary

%prep

%build

%install
install -m 755         -d $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/xrootd
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE12} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE13} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE14} $RPM_BUILD_ROOT/etc/xrootd/config.d
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/xrootd/
install -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT/%{_libexecdir}/xrootd/create_macaroon_secret
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/etc/xrootd/Authfile
install -m 644 %{SOURCE15} $RPM_BUILD_ROOT/etc/xrootd/scitokens.conf

%files
%config(noreplace) /etc/xrootd/config.d/10-common-site-local.cfg
%config(noreplace) /etc/xrootd/config.d/10-osg-xrdvoms.cfg
%config /etc/xrootd/config.d/50-osg-http.cfg
%config /etc/xrootd/config.d/50-osg-monitoring.cfg
%config /etc/xrootd/config.d/50-osg-paths.cfg
%config /etc/xrootd/config.d/50-osg-xrdvoms.cfg
%config /etc/xrootd/ban-robots.txt
%dir %_libexecdir/xrootd
%_libexecdir/xrootd/create_macaroon_secret

%files standalone
%config /etc/xrootd/config.d/40-osg-standalone.cfg
%config /etc/xrootd/config.d/50-osg-scitokens.cfg
%config(noreplace) /etc/xrootd/config.d/90-osg-standalone-paths.cfg
%config(noreplace) /etc/xrootd/config.d/90-xrootd-logging.cfg
%config /etc/xrootd/config.d/50-osg-tpc.cfg
%config(noreplace) /etc/xrootd/Authfile
%config(noreplace) /etc/xrootd/scitokens.conf

%post
if [ ! -e /etc/xrootd/macaroon-secret ]; then
    %_libexecdir/xrootd/create_macaroon_secret >/dev/null 2>&1 || :
fi
mkdir -p /etc/grid-security >/dev/null 2>&1 || :
[ -e /etc/grid-security/grid-mapfile ] || touch /etc/grid-security/grid-mapfile

%changelog
* Wed Sep 10 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 25-1
- Initial OSG 25 release; bump XRootD version to 5.8.4

* Thu Jan 9 2025 Matt Westphall <westphall@wisc.edu> - 24-3
- Add suggests: osg-ca-certs to satisfy grid-certificates (SOFTWARE-6051)

* Thu Oct 10 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 24-1
- Initial OSG 24 release

* Mon Mar 18 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 23-6
- Add GridMapfile and GmapOpt variables for controlling grid-mapfile mapping (SOFTWARE-5468)

* Fri Mar 01 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 23-5
- Log DNs of incoming certificates (SOFTWARE-5370); raise required XRootD version to 1:5.6.0 for the feature

* Fri Jan 23 2024 Matt Westphall <westphall@wisc.edu> - 23-4
- Enable HTTP directory listings for origins and auth caches (SOFTWARE-5586)

* Tue Aug 22 2023 Matt Westphall <westphall@wisc.edu> - 23-1
- Initial OSG 23 Release

* Tue Jun 27 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.6-20
- Allow create_macaroon_secret to be run as non-root user (SOFTWARE-5610)

* Thu Feb 16 2023 Carl Edquist <edquist@cs.wisc.edu> - 3.6-19
- Bump to rebuild for RPM GPG key (SOFTWARE-5457)

* Tue Jun 28 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-18
- Disable voms via XRD_DISABLE_VOMS env var (SOFTWARE-5106)

* Wed May 04 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.6-17
- Have standalone Conflict with stash-cache and -origin (SOFTWARE-4668)

* Mon Mar 07 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 3.6-16
- Don't turn on `http.secxtractor` for unauth caches/origins (SOFTWARE-5066)

* Thu Feb 10 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 3.6-15
- Remove nested if from config (SOFTWARE-5026)

* Thu Feb 10 2022 Diego Davila <didavila@ucsd.edu> 3.6-14
- Configure Xrootd to send caching monitoring data (SOFTWARE-5026)
- Make the ShovelerHostPort variable to use as the monitoring collector if there is a shoveler

* Tue Feb 08 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 3.6-13
- Ensure /etc/grid-security/grid-mapfile exists (SOFTWARE-5023)

* Mon Jan 03 2022 Mátyás Selmeci <matyas@cs.wisc.edu> 3.6-12
- Set grid-mapfile location (http.gridmap and -gridmap in sec.protocol gsi)
  to the standard location (SOFTWARE-4937)

* Tue Dec 14 2021 Brian Lin <blin@cs.wisc.edu> 3.5.upcoming-2
- Add files to the messages sent to xrd-mon (SOFTWARE-4931)

* Thu Oct 28 2021 Mátyás Selmeci <matyas@cs.wisc.edu> 3.6-10
- Load libXrdSec.so when doing Voms auth; load the ztn seclib so bearer tokens still work

* Tue Oct 26 2021 Mátyás Selmeci <matyas@cs.wisc.edu> 3.6-8
- Add sample scitokens.conf file (SOFTWARE-4790)
  based on https://github.com/xrootd/xrootd/blob/v5.3.2/src/XrdSciTokens/configs/scitokens.cfg
- Rename *-osg-vomsxrd.cfg to *-osg-xrdvoms.cfg (SOFTWARE-4495)
- Change XrdVoms config to fall back to using a hash of the user's DN as the username if the DN can't be found in the mapfile (SOFTWARE-4495)
- Replace deprecated http.* config with tls.* (SOFTWARE-4495)
- Require TLS when using SciTokens
- Move 50-osg-scitokens.cfg to osg-xrootd-standalone to avoid conflict with xcache packaging
- Move scitokens.conf to osg-xrootd-standalone and mark it %config(noreplace)
- Move xrootd-scitokens requirement to osg-xrootd-standalone since we don't distribute config for it in the base package

* Fri Aug 27 2021 Mátyás Selmeci <matyas@cs.wisc.edu> 3.6-4
- Fix vomsxrd in http (SOFTWARE-4495)
- Add missing authentication plugin packages
- Add SciTokens config

* Tue Jul 20 2021 Brian Lin <blin@cs.wisc.edu> 3.6-3
- Add vomsxrd configuration (SOFTWARE-4495)

* Tue Mar 30 2021 Brian Lin <blin@cs.wisc.edu> 3.6-2
- Update ofs.authlib directive to use new '++' append syntax (SOFTWARE-4544)

* Mon Mar 15 2021 Carl Edquist <edquist@cs.wisc.edu> - 3.6-1
- Release for OSG 3.6 / XRootD 5 (SOFTWARE-4495)
- Drop xrootd-lcmaps & vo-client-lcmaps-voms requirements

* Mon Jun 29 2020 Edgar Fajardo <emfajard@ucsd.edu> 3.5-13
- Adding logging information on its own file (SOFTWARE-4058)

* Fri Mar 06 2020 Edgar Fajardo <emfajard@ucsd.edu> 3.5-12
- The configuration on the standalone file shoudl be only for standalone (SOFTWARE-4027)

* Mon Jan 06 2020 Mátyás Selmeci <matyas@cs.wisc.edu> 3.5-10
- Add default Authfile to osg-xrootd-standalone (SOFTWARE-3951)

* Mon Dec 16 2019 Edgar Fajardo <emfajard@ucsd.edu> 3.5-9
- Should only enable macaroon by default and not scitokens (SOFTWARE-3931)

* Mon Dec 9 2019 Edgar Fajardo <emfajard@ucsd.edu> 3.5-8
- Enable Third party copy by default (SOFTWARE-3935)

* Mon Dec 9 2019 Edgar Fajardo <emfajard@ucsd.edu> 3.5-6
- Create a macaroon secret if non existent (SOFTWARE-3931)

* Mon Oct 21 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-4
- Add 'all.role server' to standalone xrootd config (SOFTWARE-3857)

* Wed Aug 21 2019 Brian Lin <blin@cs.wisc.edu> - 3.5-3
- Restore osg-configure requirement for standalone installations
  since they'll be using /etc/lcmaps.db instead of the LCMAPS configuration
  shipped with xrootd-lcmaps
- Ensure that XRootd/HTTP ports are the same

* Mon Aug 19 2019 Brian Lin <blin@cs.wisc.edu> - 3.5-2
- Opt into default configuration provided by xrootd-lcmaps-1.7.4 (SOFTWARE-3534)
- Remove osg-configure and redundant dependencies

* Mon Aug 19 2019 Brian Lin <blin@cs.wisc.edu> - 3.5-1
- Add packaging for OSG XRootD standalone installations
- Unify Stash Origin HTTP/S and XRootD ports (SOFTWARE-3558)

* Wed Feb 06 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-0.1
- Initial release (SOFTWARE-3520)
