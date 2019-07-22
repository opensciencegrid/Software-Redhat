Summary: OSG config files for XRootD
Name: osg-xrootd
Version: 3.4
Release: 0.2%{?dist}
License: ASL 2.0
BuildArch: noarch

Source1: 40-osg-http.cfg
Source2: 40-osg-monitoring.cfg
Source3: 40-osg-paths.cfg
Source4: ban-robots.txt

%description
%{summary}

%prep

%build

%install
install -m 755         -d $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/xrootd/config.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/etc/xrootd

%files
%config(noreplace) /etc/xrootd/config.d/40-osg-http.cfg
%config(noreplace) /etc/xrootd/config.d/40-osg-monitoring.cfg
%config(noreplace) /etc/xrootd/config.d/40-osg-paths.cfg
%config(noreplace) /etc/xrootd/ban-robots.txt

%changelog
* Wed Feb 06 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-0.1
- Initial release (SOFTWARE-3520)

