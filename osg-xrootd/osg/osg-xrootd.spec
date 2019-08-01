Summary: OSG configuration files for XRootD
Name: osg-xrootd
Version: 3.4
Release: 1%{?dist}
License: ASL 2.0
BuildArch: noarch

Source1: ban-robots.txt
Source2: 10-common-site-local.cfg
Source3: 50-osg-http.cfg
Source4: 50-osg-monitoring.cfg
Source5: 50-osg-paths.cfg

# We utilize a configuration directive (`continue`) introduced in XRootD 4.9.
Requires: xrootd >= 1:4.9.0

# Necessary for authentication
Requires: grid-certificates >= 7
Requires: vo-client
Requires: fetch-crl

%description
%{summary}

%prep

%build

%install
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/xrootd
install -m 755         -d $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/xrootd/config.d

%files
%config(noreplace) /etc/xrootd/10-osg-common-site-local.cfg
%config /etc/xrootd/config.d/50-osg-http.cfg
%config /etc/xrootd/config.d/50-osg-monitoring.cfg
%config /etc/xrootd/config.d/50-osg-paths.cfg
%config /etc/xrootd/ban-robots.txt

%changelog
* Thu Jul 25 2019 Brian Lin <blin@cs.wisc.edu> - 3.4-1
- Unify Stash Origin HTTP/S and XRootD ports (SOFTWARE-3558)

* Wed Feb 06 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-0.1
- Initial release (SOFTWARE-3520)

