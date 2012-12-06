Version: 2.1.4
Name: pakiti
Release: 1.1%{?dist}

License: BSD
Source: http://pakiti.sourceforge.net/rpms/%{name}/%{name}-%{version}.tar.gz
Source1: pakiti2-client-init
Patch1: pakiti-client-os-1.patch
Patch2: osg-config.patch
Patch3: client-cron-lockfile.patch
Vendor: CESNET/CERN
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Packager: Michal Prochazka <michalp@ics.muni.cz>
Summary: Patching status monitoring tool.
Group: Utilities/System
Url: http://pakiti.sourceforge.net

%description 
Runs rpm -qa or dpkg -l on the hosts and sends results to the central server.

Central server then process the results and checks whether the packages are
installed in the recent version. Central server also provides web GUI where
all results can be seen.

%package client
Requires: openssl
Summary: Client for the Pakiti (patching status monitoring tool) using openssl or curl for transport.
Group: Utilities/System
BuildArch: noarch

%description client
Runs rpm -qa or dpkg -l, depends on the linux distro. Results are sent to the
central Pakiti server using openssl s_client or curl.

%package server
BuildArch: noarch
Requires: httpd, mysql-server, php , php-mysql, php-xml, grid-certificates, mod_ssl
Requires(post): policycoreutils
Requires(postun): policycoreutils
Summary: Pakiti server - Patching status system.
Group: Utilities/System

%description server
Server logic and web interface.

%prep

%setup

%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%clean
rm -rf %{buildroot}

%install 
install -D -m755  install/pakiti2-update.cron.daily        %{buildroot}/%{_sysconfdir}/cron.daily/pakiti2-server-update
install -D -m755  install/pakiti2-init                     %{buildroot}/%{_initrddir}/pakiti2
install -D -m640  install/pakiti2-server.conf              %{buildroot}/%{_sysconfdir}/pakiti2/pakiti2-server.conf
install -D -m640  client/pakiti2-client.conf               %{buildroot}/%{_sysconfdir}/pakiti2/pakiti2-client.conf
install -D -m755  client/pakiti2-client                    %{buildroot}/%{_sbindir}/pakiti2-client 
install -D -m755  client/pakiti2-client.update.cron.daily  %{buildroot}/%{_sysconfdir}/cron.daily/pakiti2-client-update
install -D -m755  %{SOURCE1}                               %{buildroot}/%{_initrddir}/pakiti2-client
#install -m644  README                                      %{buildroot}/README
#install -m622  pakiti.sql                                  %{buildroot}/pakiti.sql

install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/scripts
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/include
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/install
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/config
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/docs
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/www
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/img
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/www/feed
install -d %{buildroot}/%{_localstatedir}/lib/pakiti2/www/link
install -d %{buildroot}/%{_sysconfdir}/pakiti2

install -m644   scripts/backup_configuration.sh	           %{buildroot}/%{_localstatedir}/lib/pakiti2/scripts/backup_configuration.sh
install -m644   scripts/process_oval_rh.php	           %{buildroot}/%{_localstatedir}/lib/pakiti2/scripts/process_oval_rh.php
install -m644   scripts/process_oval_rh_php4.php	   %{buildroot}/%{_localstatedir}/lib/pakiti2/scripts/process_oval_rh_php4.php
install -m644   scripts/recalculate_vulnerabilities.php    %{buildroot}/%{_localstatedir}/lib/pakiti2/scripts/recalculate_vulnerabilities.php
install -m644   scripts/repository_updates.php             %{buildroot}/%{_localstatedir}/lib/pakiti2/scripts/repository_updates.php

install -m644   include/functions.php                      %{buildroot}/%{_localstatedir}/lib/pakiti2/include/functions.php
install -m644   include/process_rpm_pkgs_xmlreader.php     %{buildroot}/%{_localstatedir}/lib/pakiti2/include/process_rpm_pkgs_xmlreader.php
install -m644   include/process_rpm_pkgs_domxml.php        %{buildroot}/%{_localstatedir}/lib/pakiti2/include/process_rpm_pkgs_domxml.php
install -m644   include/gui.php                            %{buildroot}/%{_localstatedir}/lib/pakiti2/include/gui.php
install -m644   include/mysql_connect.php                  %{buildroot}/%{_localstatedir}/lib/pakiti2/include/mysql_connect.php

#install -m644   install/pakiti2.sql                   %{buildroot}/%{_localstatedir}/lib/pakiti2/pakiti2.sql
install -m600   config/config.php                     %{buildroot}/%{_localstatedir}/lib/pakiti2/config/config.php

install -m644   www/pakiti/hosts.php                  %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/hosts.php
install -m644   www/pakiti/index.php                  %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/index.php
install -m644   www/pakiti/cves.php                   %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/cves.php
install -m644   www/pakiti/host.php                   %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/host.php
install -m644   www/pakiti/packages.php               %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/packages.php
install -m644   www/pakiti/settings.php               %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/settings.php
install -m644   www/pakiti/admin.php                  %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/admin.php
install -m644   www/pakiti/pakiti.css                 %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/pakiti.css

install -m644   www/pakiti/img/link.gif               %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/img/link.gif
install -m644   www/pakiti/img/mark.gif               %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/img/mark.gif
install -m644   www/pakiti/img/ok.gif                 %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/img/ok.gif
install -m644   www/pakiti/img/os_installed.gif       %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/img/os_installed.gif
install -m644   www/pakiti/img/os_not_installed.gif   %{buildroot}/%{_localstatedir}/lib/pakiti2/www/pakiti/img/os_not_installed.gif

install -m644   www/feed/index.php                    %{buildroot}/%{_localstatedir}/lib/pakiti2/www/feed/index.php

ln -s ../pakiti/cves.php www/link/cves.php
ln -s ../pakiti/packages.php www/link/packages.php
ln -s ../pakiti/pakiti.css www/link/pakiti.css

%files client
%defattr(-,root,root)
%attr(0755,root,root) %{_sysconfdir}/cron.daily/pakiti2-client-update
%attr(0755,root,root) %{_sbindir}/pakiti2-client
%attr(0775,root,root) %{_initrddir}/pakiti2-client
%config(noreplace)    %{_sysconfdir}/pakiti2/pakiti2-client.conf
%doc README
%doc client/pakiti2-client
%doc client/pakiti2-client.conf
%doc client/pakiti2-client.update.cron.daily
%doc client/README

%files server
%defattr(-,root,root)
%attr(0664,root,root) %{_localstatedir}/lib/pakiti2/scripts/*

%attr(0640,root,apache) %{_localstatedir}/lib/pakiti2/config/config.php

%attr(0664,root,root) %{_localstatedir}/lib/pakiti2/include/*.php

%attr(0664,root,root) %{_localstatedir}/lib/pakiti2/www/pakiti/*.php
%attr(0664,root,root) %{_localstatedir}/lib/pakiti2/www/pakiti/pakiti.css
%attr(0664,root,root) %{_localstatedir}/lib/pakiti2/www/pakiti/img/*.gif

%attr(0664,root,root) %{_localstatedir}/lib/pakiti2/www/feed/index.php

%attr(0775,root,root) %{_initrddir}/pakiti2

%attr(0775,root,root) %{_sysconfdir}/cron.daily/pakiti2-server-update
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/pakiti2/pakiti2-server.conf

%doc install/pakiti2.sql 
%doc install/pakiti2.apache2
%doc README

%post server
/sbin/chkconfig --add pakiti2
# set selinux contexts
if selinuxenabled; then
    semanage fcontext -a -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2
    semanage fcontext -a -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/config
    semanage fcontext -a -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/include
    semanage fcontext -a -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www
    semanage fcontext -a -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www/feed
    semanage fcontext -a -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www/pakiti
    semanage fcontext -a -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www/pakiti/img
    restorecon %{_localstatedir}/lib/pakiti2
    restorecon %{_localstatedir}/lib/pakiti2/config
    restorecon %{_localstatedir}/lib/pakiti2/include
    restorecon %{_localstatedir}/lib/pakiti2/www
    restorecon %{_localstatedir}/lib/pakiti2/www/feed
    restorecon %{_localstatedir}/lib/pakiti2/www/pakiti
    restorecon %{_localstatedir}/lib/pakiti2/www/pakiti/img
fi

%preun server
/sbin/chkconfig --del pakiti2

%postun server
if [ $1 -eq 0 ]; then # final removal
    if selinuxenabled; then
        semanage fcontext -d -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2
        semanage fcontext -d -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/config
        semanage fcontext -d -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/include
        semanage fcontext -d -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www
        semanage fcontext -d -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www/feed
        semanage fcontext -d -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www/pakiti
        semanage fcontext -d -t httpd_sys_content_t %{_localstatedir}/lib/pakiti2/www/pakiti/img
    fi
fi
    

%post client
/sbin/chkconfig --add pakiti2-client

%preun client
/sbin/chkconfig --del pakiti2-client

%changelog
* Wed Dec 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.1.4-1.1
- Set SELinux contexts for server

* Mon Dec 03 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.1.4-1.0.4
- Add init script for client
- Changed 'webserver' requirement to 'httpd' so the package doesn't bring in two webservers
- Use Kevin Hill's apache conf

* Tue Nov 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.1.4-1.0.3
- Add mod_ssl dependency to server

* Mon Nov 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.1.4-1.0.2
- Add grid-certificates dependency
- Fix example apache conf.d file and default client config to work in an OSG environment
- Fix perms on init script

* Tue Oct 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.1.4-1.0.1
- Fixed chkconfig in server
- Merged client and client-manual

* Tue Sep 25 2012 Kevin Hill <kevin@fnal.gov>
- First OSG release. 
- added back client side os if we can figure it out.

* Thu Sep 16 2010 Michal Prochazka <michalp@ics.muni.cz>
- Pakiti 2.1.4 release
- bug fixes
- added support for proxy servers
- RPM based repositories can be defined also by repomd.xml file
- accepts repository definition files in bz2 compression
- added force option to the repository_updates.php script
- autorization accepts both REMOTE_USER and SSL_CLIENT_S_DN
- performance optimizations
- unused OSes can be deleted
- Pakiti client
    - automatic detection of transport mechanism
    - errors are printed to the stderr
    - OS detection only for Debian based systems other are detected on the server side
    - added option that enables statisctics of the reports
    - added command line option -c which specifies configuration file

* Fri Jun 11 2010 Michal Prochazka <michalp@ics.muni.cz>
- Pakiti 2.1.3 release
- bug fixes
- little changes in the DB scheme
- added support for interface selection in the pakiti2-client

* Thu May 12 2010 Michal Prochazka <michalp@ics.muni.cz>
- bug fixes
- support for authZ
- performance imporovements
- add support for proxy clients

* Fri Mar 21 2010 Michal Prochazka <michalp@ics.muni.cz>
- serious bug fix
- statistics in all hosts views

* Fri Mar 19 2010 Michal Prochazka <michalp@ics.muni.cz>
- Pakiti 2.1.1-2 release
- bug fixes
- added full support for the PHP4
- added asynchronous mode
- added anonymous links
- added optional report - outdated packages (thanks to Catalin Dumitrescu)

* Tue Jan 26 2010 Michal Prochazka <michalp@ics.muni.cz>
- Pakiti 2.1-2 release
- function process_rpm_pkgs is now split into two parts, the first one using
  XLMReader and the second one using DOMXML. PHP4 doesn't have XMLReader

* Tue Jan 11 2010 Michal Prochazka <michalp@ics.muni.cz>
- Pakiti 2.1-1 release
- checking the arch for the packages from RPM repositories
- fixed wrong unique key in act_version table
- fixed parsing the responce from Debian and RH systems

* Mon Nov 30 2009 Michal Prochazka <michalp@ics.muni.cz>
- Initial Pakiti 2.1 release


