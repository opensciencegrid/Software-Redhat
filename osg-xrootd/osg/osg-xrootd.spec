Summary: OSG configuration files for XRootD
Name: osg-xrootd
Version: 3.5
Release: 6%{?dist}
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
# We utilize a configuration directive (`continue`) introduced in XRootD 4.9.
Requires: xrootd >= 1:4.9.0

# Necessary for authentication
Requires: grid-certificates >= 7
Requires: vo-client
Requires: fetch-crl

%description
%{summary}

########################################
%package standalone
Summary: OSG configuration files for XRootD standalone installations
Requires: %{name} = %{version}-%release

# For LCMAPS VOMS authentication
Requires: osg-configure-misc
Requires: vo-client-lcmaps-voms
Requires: xrootd-lcmaps

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
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/xrootd/
install -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT/%{_libexecdir}/xrootd/create_macaroon_secret

%files
%config(noreplace) /etc/xrootd/config.d/10-common-site-local.cfg
%config /etc/xrootd/config.d/50-osg-http.cfg
%config /etc/xrootd/config.d/50-osg-monitoring.cfg
%config /etc/xrootd/config.d/50-osg-paths.cfg
%config /etc/xrootd/ban-robots.txt
%dir %_libexecdir/xrootd
%_libexecdir/xrootd/create_macaroon_secret

%files standalone
%config /etc/xrootd/config.d/40-osg-standalone.cfg
%config(noreplace) /etc/xrootd/config.d/90-osg-standalone-paths.cfg

%post
if [ ! -e /etc/xrootd/macaroon-secret ]; then
    %_libexecdir/xrootd/create_macaroon_secret >/dev/null 2>&1 || :
fi

%changelog
* Mon Dec 10 2019 Edgar Fajardo <emfajard@ucsd.edu> 3.5-6
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
