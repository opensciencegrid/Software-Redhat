Name:      osg-gridftp
Summary:   Standalone OSG GridFTP with LCMAPS VOMS support
Version:   3.5
Release:   4%{?dist}
License:   Apache 2.0
URL:       http://www.opensciencegrid.org


Source1: udt-osg-gridftp.conf
# Add IPv6 enabled by default (SOFTWARE-2920)
Source2: ipv6.conf
Source3: logging.conf
# Increase transfer timeout (SOFTWARE-3241)
Source4: timeout.conf
Source5: globus-gridftp-server.logrotate
Source6: globus-gridftp-server.service
Source7: globus-gridftp-sshftp.service
Source8: globus-gridftp-server.osg-sysconfig
Source9: globus-gridftp-server.sysconfig
# SystemD helpers
Source10: globus-gridftp-server-start
Source11: globus-gridftp-sshftp-reconfigure
Source12: globus-gridftp-sshftp-start
Source13: globus-gridftp-sshftp-stop

Requires: osg-system-profiler
Requires: globus-gridftp-server-progs >= 13.20
Requires: vo-client
Requires: vo-client-lcmaps-voms
Requires: grid-certificates >= 7
Requires: gratia-probe-gridftp-transfer >= 1.17.0-1
Requires: fetch-crl
Requires: osg-configure-misc
Requires: osg-configure-gratia
Requires: globus-xio-udt-driver
%{systemd_requires}

Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)

# This should also pull in lcas, lcmaps, and various plugins
# (basic, proxy verify, posix, etc)

%description
This is a meta package for a standalone GridFTP server with
support for the LCMAPS VOMS authentication method.




%package xrootd
Summary: OSG GridFTP XRootD Storage Element package

Requires: %{name} = %{version}-%{release}
Requires: xrootd-dsi
Requires: xrootd-fuse >= 1:4.1.0
Requires: gratia-probe-xrootd-transfer >= 1.17.0-1
Requires: gratia-probe-xrootd-storage

%description xrootd
This is a meta-package for GridFTP with the underlying XRootD storage element
using the FUSE/DSI module.

%package hdfs
Summary: OSG GridFTP HDFS Storage Element package

Requires: %{name} = %{version}-%{release}
Requires: gridftp-hdfs >= 0.5.4-16

%description hdfs
This is a meta package for a standalone GridFTP server with 
HDFS and GUMS support.

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/gridftp.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/gridftp.d/udt-osg-gridftp.conf
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/gridftp.d/ipv6.conf
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/gridftp.d/logging.conf
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/gridftp.d/timeout.conf
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/globus-gridftp-server.logrotate
# systemd service files
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/globus-gridftp-server.service
install -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/globus-gridftp-sshftp.service
# OSG sysconfig
mkdir -p %{buildroot}%{_datarootdir}/osg/sysconfig
install -m 644 %{SOURCE8} %{buildroot}%{_datarootdir}/osg/sysconfig/globus-gridftp-server
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/globus-gridftp-server
# systemd startup helper scripts
mkdir -p %{buildroot}%{_libexecdir}
install -m 755 %{SOURCE10} %{buildroot}%{_libexecdir}/globus-gridftp-server-start
install -m 755 %{SOURCE11} %{buildroot}%{_libexecdir}/globus-gridftp-sshftp-reconfigure
install -m 755 %{SOURCE12} %{buildroot}%{_libexecdir}/globus-gridftp-sshftp-start
install -m 755 %{SOURCE13} %{buildroot}%{_libexecdir}/globus-gridftp-sshftp-stop


%pre
# Remove old init config when systemd is used
/sbin/chkconfig --del globus-gridftp-server > /dev/null 2>&1 || :
/sbin/chkconfig --del globus-gridftp-sshftp > /dev/null 2>&1 || :

%post
%systemd_post globus-gridftp-server.service globus-gridftp-sshftp.service
systemctl daemon-reload >/dev/null 2>&1 || :

%preun
%systemd_preun globus-gridftp-server.service globus-gridftp-sshftp.service

%postun
%systemd_postun_with_restart globus-gridftp-server.service globus-gridftp-sshftp.service
if [ $1 -eq 0 ]; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi



%files
%config(noreplace) %{_sysconfdir}/gridftp.d/udt-osg-gridftp.conf
%config(noreplace) %{_sysconfdir}/gridftp.d/ipv6.conf
%config(noreplace) %{_sysconfdir}/gridftp.d/logging.conf
%config(noreplace) %{_sysconfdir}/gridftp.d/timeout.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/globus-gridftp-server.logrotate
%config(noreplace) %{_sysconfdir}/sysconfig/globus-gridftp-server
%{_unitdir}/globus-gridftp-server.service
%{_unitdir}/globus-gridftp-sshftp.service
%{_datarootdir}/osg/sysconfig/globus-gridftp-server
%{_libexecdir}/globus-gridftp-server-start
%{_libexecdir}/globus-gridftp-sshftp-reconfigure
%{_libexecdir}/globus-gridftp-sshftp-start
%{_libexecdir}/globus-gridftp-sshftp-stop


%files xrootd
# This section intentionally left blank

%files hdfs
# This section intentionally left blank


%changelog
* Tue Dec 10 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.5-4
- Add configs and systemd files from OSG modifications of globus-gridftp-server (SOFTWARE-2996)
- Drop env var to disable SSLv3 (no longer needed)

* Fri Aug 16 2019 Brian Lin <blin@cs.wisc.edu> - 3.5-3
- Add HDFS sub-package

* Mon Aug 12 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.5-2
- Bump version to 3.5 (SOFTWARE-3761)

* Wed Mar 07 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4-7
- Add mistakenly dropped gratia-probe-xrootd-transfer requirement to
  osg-gridftp-xrootd (SOFTWARE-3141)

* Mon Feb 19 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4-6
- Combine packaging with osg-gridftp-xrootd (SOFTWARE-3141)

* Mon Jan 08 2018 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-5
- Remove osg-version from dependencies (SOFTWARE-2917)

* Wed Nov 15 2017 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.4-4
- Add osg-configure-gratia to dependencies (SOFTWARE-3019)

* Mon Jun 12 2017 Edgar Fajardo <emfajard@ucsd.edu> - 3.4-3
- Add osg-configure-misc to dependencies (SOFTWARE-2758)

* Mon Jun 05 2017 Brian Lin <blin@cs.wisc.edu> - 3.4-2
- Add vo-client-lcmaps-voms deps to osg-gridftp (SOFTWARE-2760)

* Tue May 23 2017 Brian Lin <blin@cs.wisc.edu> 3.4-1
- Rebuild for OSG 3.4

* Thu Aug 25 2016 Carl Edquist <edquist@cs.wisc.edu> - 3.3-3
- drop gums-client dependency (SOFTWARE-2398)
- remove rhel5-specific macros (OSG-3.2 EOL)

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue Apr 21 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.0.0-11_clipped
- Create clipped version for el7

* Thu Mar 13 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-9
- Add globus-xio-udt-driver dependency for el6, and enable by default in
  /etc/gridftp.d/ (SOFTWARE-1412)
