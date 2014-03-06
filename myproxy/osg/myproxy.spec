%{!?_initddir: %global _initddir %{_initrddir}}

%if %{?fedora}%{!?fedora:0} >= 17 || %{?rhel}%{!?rhel:0} >= 7
%global with_sysv 0
%else
%global with_sysv 1
%endif

%ifarch aarch64 alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%global with_checks 0

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           myproxy
Version:        5.9
Release:        8.1%{?dist}
Summary:        Manage X.509 Public Key Infrastructure (PKI) security credentials

Group:          Applications/Internet
License:        NCSA and BSD and ASL 2.0
URL:            http://grid.ncsa.illinois.edu/myproxy/
Source0:        http://downloads.sourceforge.net/cilogon/myproxy-%{version}-gt5.2.tar.gz
Source1:        myproxy.init
Source2:        myproxy.sysconfig
Source4:        myproxy-server-tmpfiles.d.conf
Source5:        myproxy-server.service
Source3:        README.Fedora
#               Depend on GT5.2+ versions of globus packages
#               http://jira.globus.org/browse/GT-502
Patch0:         %{name}-deps.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  grid-packaging-tools >= 3.4
BuildRequires:  globus-core >= 8
BuildRequires:  globus-gsi-credential-devel >= 5
BuildRequires:  globus-gsi-callback-devel >= 4
BuildRequires:  globus-gss-assist-devel >= 8
BuildRequires:  globus-gsi-proxy-core-devel >= 6
BuildRequires:  globus-gssapi-gsi-devel >= 9
BuildRequires:  globus-gsi-cert-utils-devel >= 8
BuildRequires:  globus-gsi-sysconfig-devel >= 5
BuildRequires:  globus-common-devel >= 14
BuildRequires:  globus-usage-devel >= 3
BuildRequires:  doxygen
BuildRequires:  graphviz
%if "%{?rhel}" == "5"
BuildRequires:  graphviz-gd
%endif
BuildRequires:  ghostscript
BuildRequires:  tex(latex)
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 7
BuildRequires:  tex(fullpage.sty)
BuildRequires:  tex(multirow.sty)
BuildRequires:  tex(sectsty.sty)
BuildRequires:  tex(tocloft.sty)
BuildRequires:  tex(xtab.sty)
BuildRequires:  tex-ec
BuildRequires:  tex-courier
BuildRequires:  tex-helvetic
BuildRequires:  tex-times
BuildRequires:  tex-symbol
BuildRequires:  tex-rsfs
%endif
BuildRequires:  cyrus-sasl-devel
BuildRequires:  openldap-devel >= 2.3
BuildRequires:  pam-devel
BuildRequires:  voms-devel >= 1.9.12.1
%if %{?with_checks}
BuildRequires:  globus-proxy-utils
BuildRequires:  globus-gsi-cert-utils-progs
BuildRequires:  voms-clients
%endif
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       globus-proxy-utils
Requires:       voms-clients
Obsoletes:      %{name}-client < 5.1-3
Provides:       %{name}-client = %{version}-%{release}

%description
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

%package libs
Summary:        Manage X.509 Public Key Infrastructure (PKI) security credentials
Group:          System Environment/Libraries
Obsoletes:      %{name} < 5.1-3

%description libs
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

Package %{name}-libs contains runtime libs for MyProxy.

%package devel
Summary:        Develop X.509 Public Key Infrastructure (PKI) security credentials
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       globus-gsi-credential-devel%{?_isa} >= 5
Requires:       globus-gsi-callback-devel%{?_isa} >= 4
Requires:       globus-gss-assist-devel%{?_isa} >= 8
Requires:       globus-gsi-proxy-core-devel%{?_isa} >= 6
Requires:       globus-gssapi-gsi-devel%{?_isa} >= 9
Requires:       globus-core%{?_isa} >= 8
Requires:       globus-gsi-cert-utils-devel%{?_isa} >= 8
Requires:       globus-gsi-sysconfig-devel%{?_isa} >= 5
Requires:       globus-common-devel%{?_isa} >= 14
Requires:       globus-usage-devel%{?_isa} >= 3

%description devel
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

Package %{name}-devel contains development files for MyProxy.

%package server
Summary:        Server for X.509 Public Key Infrastructure (PKI) security credentials
Group:          System Environment/Daemons
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):    shadow-utils
%if %{?with_sysv}
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts
%else
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
%endif

%description server
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

Package %{name}-server contains the MyProxy server.

%package admin
# Create a sepeate admin clients package since they not needed for normal
# operation and pull in a load of perl dependencies.
Summary:        Server for X.509 Public Key Infrastructure (PKI) security credentials
Group:          Applications/Internet
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-server = %{version}-%{release}
Requires:       globus-gsi-cert-utils-progs

%description admin
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

Package %{name}-admin contains the MyProxy server admin commands.

%package doc
Summary:        Documentation for X.509 Public Key Infrastructure (PKI) security credentials
Group:          Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:      noarch
%endif
Requires:       %{name}-libs = %{version}-%{release}

%description doc
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

Package %{name}-doc contains the MyProxy documentation.

%prep
%setup -q
%patch0 -p1

%if %{?with_sysv}
cp -p %{SOURCE1} .   #myproxy.init
cp -p %{SOURCE2} .   #myproxy.sysconfig
%else
cp -p %{SOURCE4} .   #myproxy-server-tmpfiles.d.conf
cp -p %{SOURCE5} .   #myproxy-server.service
%endif
cp -p %{SOURCE3} .   #README.Fedora.

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

for f in `find . -name Makefile.am` ; do
  sed -e 's!^flavorinclude_HEADERS!include_HEADERS!' \
      -e 's!\(lib[a-zA-Z_]*\)_$(GLOBUS_FLAVOR_NAME)\.la!\1.la!g' \
      -e 's!^\(lib[a-zA-Z_]*\)___GLOBUS_FLAVOR_NAME__la_!\1_la_!' -i $f
done

unset GLOBUS_LOCATION
unset GPT_LOCATION
%{_datadir}/globus/globus-bootstrap.sh

%configure --disable-static --with-flavor=%{flavor} \
           --enable-doxygen --with-docdir=%{_pkgdocdir} \
           --with-openldap=%{_prefix} \
           --with-voms=%{_prefix} \
           --with-kerberos5=%{_prefix} \
           --with-sasl2=%{_prefix}

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

GLOBUSPACKAGEDIR=%{buildroot}%{_datadir}/globus/packages

# Remove libtool archives (.la files)
find %{buildroot}%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{name}/%{flavor}_dev.filelist

# Put documentation in Fedora defaults and alter GPT package lists.
mkdir -p %{buildroot}%{_pkgdocdir}/extras
for FILE in login.html myproxy-accepted-credentials-mapapp \
            myproxy-cert-checker myproxy-certificate-mapapp \
            myproxy-certreq-checker myproxy-crl.cron myproxy.cron \
            myproxy-get-delegation.cgi myproxy-get-trustroots.cron \
            myproxy-passphrase-policy myproxy-revoke ; do
   mv %{buildroot}%{_datadir}/%{name}/$FILE %{buildroot}%{_pkgdocdir}/extras
   shortpkgdocdir=`sed 's!^%{_prefix}!!' <<< %{_pkgdocdir}`
   sed -i "s!/share/%{name}/${FILE}!${shortpkgdocdir}/extras/${FILE}!" \
      $GLOBUSPACKAGEDIR/%{name}/noflavor_data.filelist
done

mkdir -p %{buildroot}%{_pkgdocdir}
for FILE in LICENSE LICENSE.* PROTOCOL README VERSION ; do
   mv %{buildroot}%{_datadir}/%{name}/$FILE %{buildroot}%{_pkgdocdir}
   shortpkgdocdir=`sed 's!^%{_prefix}!!' <<< %{_pkgdocdir}`
   sed -i "s!/share/%{name}/${FILE}!${shortpkgdocdir}/${FILE}!" \
      $GLOBUSPACKAGEDIR/%{name}/noflavor_data.filelist
done

# Remove irrelavent example configuration files.
for FILE in etc.inetd.conf.modifications etc.init.d.myproxy.nonroot \
            etc.services.modifications etc.xinetd.myproxy \
            etc.init.d.myproxy INSTALL ; do
   rm %{buildroot}%{_datadir}/%{name}/$FILE
   sed -i "/share\/%{name}\/$FILE/d" \
      $GLOBUSPACKAGEDIR/%{name}/noflavor_data.filelist
done

# Move example configuration file into place.
mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}%{_datadir}/%{name}/myproxy-server.config \
   %{buildroot}%{_sysconfdir}
sed -i "/share\/%{name}\/myproxy-server.config/d" \
   $GLOBUSPACKAGEDIR/%{name}/noflavor_data.filelist

%if %{with_sysv}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 755 myproxy.init %{buildroot}%{_initddir}/myproxy-server
install -p -m 644 myproxy.sysconfig \
   %{buildroot}%{_sysconfdir}/sysconfig/myproxy-server
%else
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 644 myproxy-server-tmpfiles.d.conf \
   %{buildroot}%{_sysconfdir}/tmpfiles.d/myproxy-server.conf
install -p -m 644 myproxy-server.service \
   %{buildroot}%{_unitdir}/myproxy-server.service
mkdir -p %{buildroot}%{_localstatedir}/run
install -d -m 710 %{buildroot}%{_localstatedir}/run/myproxy-server
%endif

mkdir -p %{buildroot}%{_localstatedir}/lib/myproxy

# Create a directory to hold myproxy owned host certificates.
mkdir -p %{buildroot}%{_sysconfdir}/grid-security/myproxy

# Upstream now includes systemd files, good. Delete them for
# now and migrate to them shortly.
for FILE in myproxy-server.conf myproxy-server.service ; do
   rm %{buildroot}%{_datadir}/%{name}/$FILE
   sed -i "/share\/%{name}\/$FILE/d" \
      $GLOBUSPACKAGEDIR/%{name}/noflavor_data.filelist
done

# Remove myproxy-server-setup rhbz#671561
rm %{buildroot}%{_sbindir}/myproxy-server-setup
sed -i "/sbin\/myproxy-server-setup/d" \
   $GLOBUSPACKAGEDIR/%{name}/%{flavor}_pgm.filelist

%clean
rm -rf %{buildroot}

%check
%if %{?with_checks}
PATH=.:$PATH ./myproxy-test -startserver -generatecerts
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%pre server
# uid:gid 178:178 now reserved for myproxy. rhbz#733671
getent group myproxy >/dev/null || groupadd -g 178 -r myproxy
getent passwd myproxy >/dev/null || \
useradd -u 178 -r -g myproxy -d %{_localstatedir}/lib/myproxy \
    -s /sbin/nologin -c "User to run the MyProxy service" myproxy
exit 0

%if %{?with_sysv}
%post server
/sbin/chkconfig --add myproxy-server
%else
%post server
%systemd_post myproxy-server.service
%endif

%if %{?with_sysv}
%preun server
if [ $1 -eq 0 ] ; then
    /sbin/service myproxy-server stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del myproxy-server
fi
%else
%preun server
%systemd_preun myproxy-server.service
%endif

%if %{?with_sysv}
%postun server
if [ $1 -ge 1 ] ; then
    /sbin/service myproxy-server condrestart >/dev/null 2>&1 || :
fi
%else
%postun server
%systemd_postun_with_restart myproxy-server.service
%endif

%files
%{_bindir}/myproxy-change-pass-phrase
%{_bindir}/myproxy-destroy
%{_bindir}/myproxy-get-delegation
%{_bindir}/myproxy-get-trustroots
%{_bindir}/myproxy-info
%{_bindir}/myproxy-init
%{_bindir}/myproxy-logon
%{_bindir}/myproxy-retrieve
%{_bindir}/myproxy-store
%{_mandir}/man1/myproxy-change-pass-phrase.1*
%{_mandir}/man1/myproxy-destroy.1*
%{_mandir}/man1/myproxy-get-delegation.1*
%{_mandir}/man1/myproxy-info.1*
%{_mandir}/man1/myproxy-init.1*
%{_mandir}/man1/myproxy-logon.1*
%{_mandir}/man1/myproxy-retrieve.1*
%{_mandir}/man1/myproxy-store.1*

%files libs
%{_datadir}/globus/packages/%{name}
%{_libdir}/libmyproxy.so.*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/LICENSE*
%doc %{_pkgdocdir}/PROTOCOL
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/VERSION

%files devel
%{_includedir}/globus/myproxy.h
%{_includedir}/globus/myproxy_authorization.h
%{_includedir}/globus/myproxy_constants.h
%{_includedir}/globus/myproxy_creds.h
%{_includedir}/globus/myproxy_delegation.h
%{_includedir}/globus/myproxy_log.h
%{_includedir}/globus/myproxy_protocol.h
%{_includedir}/globus/myproxy_read_pass.h
%{_includedir}/globus/myproxy_sasl_client.h
%{_includedir}/globus/myproxy_sasl_server.h
%{_includedir}/globus/myproxy_server.h
%{_includedir}/globus/verror.h
%{_libdir}/libmyproxy.so
%{_libdir}/pkgconfig/myproxy.pc

%files server
%{_sbindir}/myproxy-server
%if %{?with_sysv}
%{_initddir}/myproxy-server
%config(noreplace) %{_sysconfdir}/sysconfig/myproxy-server
%else
%attr(0710,myproxy,root) %dir %{_localstatedir}/run/myproxy-server
%config(noreplace) %{_sysconfdir}/tmpfiles.d/myproxy-server.conf
%{_unitdir}/myproxy-server.service
%endif
%config(noreplace) %{_sysconfdir}/myproxy-server.config
# myproxy-server wants exactly 700 permission on its data
# which is just fine.
%attr(0700,myproxy,myproxy) %dir %{_localstatedir}/lib/myproxy
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/myproxy
%{_mandir}/man8/myproxy-server.8*
%{_mandir}/man5/myproxy-server.config.5*
%doc README.Fedora

%files admin
%{_sbindir}/myproxy-admin-addservice
%{_sbindir}/myproxy-admin-adduser
%{_sbindir}/myproxy-admin-change-pass
%{_sbindir}/myproxy-admin-load-credential
%{_sbindir}/myproxy-admin-query
%{_sbindir}/myproxy-replicate
%{_sbindir}/myproxy-test
%{_sbindir}/myproxy-test-replicate
%{_mandir}/man8/myproxy-admin-addservice.8*
%{_mandir}/man8/myproxy-admin-adduser.8*
%{_mandir}/man8/myproxy-admin-change-pass.8*
%{_mandir}/man8/myproxy-admin-load-credential.8*
%{_mandir}/man8/myproxy-admin-query.8*
%{_mandir}/man8/myproxy-replicate.8*

%files doc
%doc %{_pkgdocdir}/extras
%doc %{_pkgdocdir}/html
%doc %{_pkgdocdir}/refman.pdf

%changelog
* Thu Mar 06 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 5.9-8.1
- Disable %%check since it requires a locally running service and so does not work in the OSG build environment

* Fri Jan 31 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-8
- Fix broken postun scriptlet

* Thu Jan 23 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-7
- Depend on GT5.2+ versions of globus packages
- Use _pkgdocdir when defined
- Use non-ISA build dependencies
- Make license files part of the -libs package
- Make documentaion package noarch
- Use better Group tags

* Mon Aug 05 2013 Steve Traylen <steve.traylen@cern.ch> - 5.9-6
- rhbz926187 - Build on aarch64 also.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 5.9-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Steve Traylen <steve.traylen@cern.ch> - 5.9-2
- rpm .spec file parsing oddness.

* Mon Dec 17 2012 Steve Traylen <steve.traylen@cern.ch> - 5.9-1
- Update to 5.9, update TeX build requirements.
- remove myproxy-server-setup script, rhbz#671561.
- Switch to systemd scriptlet macros rhbz#850221.
- Use reserved uid:gid for myproxy user rhbz#733671

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Steve Traylen <steve.traylen@cern.ch> - 5.8-1
- Update to 5.8, source tar ball name change, drop
  myproxy-ssl1-tls.patch and myproxy-ssl1-2048bits.patch
  since upstream now.

* Tue May 15 2012 Steve Traylen <steve.traylen@cern.ch> - 5.6-4
- Add myproxy-ssl1-tls.patch and myproxy-ssl1-2048bits.patch.

* Mon Mar 05 2012 Steve Traylen <steve.traylen@cern.ch> - 5.6-3
- tmpfile.d configuration does not support comments and must
  be 0644

* Tue Feb 28 2012 Steve Traylen <steve.traylen@cern.ch> - 5.6-2
- Include Sources: for sysv and systemd always.
- Silly mistakes.

* Thu Feb 23 2012 Steve Traylen <steve.traylen@cern.ch> - 5.6-1
- Update myproxy to 5.6, remove addition ColocateLibraries="no"
  since added upstream.
- Support systemd for epel7 and fedora17 and up:
  http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=7240
- Switch from RPM_BUILD_ROOT to %%buildroot.

* Thu Feb 02 2012 Steve Traylen <steve.traylen@cern.ch> - 5.5-3
- Drop EPEL4 packaging since EOL.
- Adapt to Globus toolkit 5.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Steve Traylen <steve.traylen@cern.ch> - 5.5-1
- Update to version 5.5, drop myproxy-globus-7129.patch, pII, pIII,
  fixed upstream.
- No longer hard code /var/lib/myproxy since the default anyway now.

* Thu Sep 01 2011 Steve Traylen <steve.traylen@cern.ch> - 5.4-4
- Add myproxy-globus-7129-PartII.patch patch and
  myproxy-globus-7129-PartIII.patch patch.

* Wed Aug 31 2011 Steve Traylen <steve.traylen@cern.ch> - 5.4-3
- Add myproxy-globus-7129.patch patch.

* Tue May 31 2011 Steve Traylen <steve.traylen@cern.ch> - 5.4-2
- Rebuild for new voms api.

* Sun Apr 24 2011 Steve Traylen <steve.traylen@cern.ch> - 5.4-1
- Drop myproxy-vomsc-vomsapi.patch since upstream.
- Drop myproxy-test-non-inter.patch since not needed.
- Drop myproxy-double-free-globus-7135.patch since upstream.
- Drop myproxy-test-home2tmp.patch since upstream.
- Update to 5.4

* Tue Mar 01 2011 Steve Traylen <steve.traylen@cern.ch> - 5.3-7
- Add myproxy-test-home2tmp.patch to avoid %%script
  writing in home.

* Mon Feb 28 2011 Steve Traylen <steve.traylen@cern.ch> - 5.3-6
- Remove myproxy-test-disables-globus-7135.patch since
  checks now run with a clean CA/grid-security directory
  and work.
- Add myproxy-double-free-globus-7135.patch to
  remove double free in myproxy-creds.ch. globus bug #7135.

* Sat Feb 26 2011 Steve Traylen <steve.traylen@cern.ch> - 5.3-5
- Globus bug #7135 only applies to myproxy-test in .spec files so
  patch private copy in RPM rather than eventual deployed
  myproxy-test.

* Thu Feb 24 2011 Steve Traylen <steve.traylen@cern.ch> - 5.3-4
- Remove useless gpt filelists check from %%check.
- Add useful check myproxy-test to %%check.

* Tue Feb 22 2011 Steve Traylen <steve.traylen@cern.ch> - 5.3-3
- myproxy-vomsc-vomsapi.patch to build against vomsapi rather
  than vomscapi.
- Add _isa rpm macros to build requires on -devel packages.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Steve Traylen <steve.traylen@cern.ch> - 5.3-1
- New upstream 5.3.

* Wed Jun 23 2010 Steve Traylen <steve.traylen@cern.ch> - 5.2-1
- New upstream 5.2.
- Drop blocked-signals-with-pthr.patch patch.

* Sat Jun 12 2010 Steve Traylen <steve.traylen@cern.ch> - 5.1-3
- Add blocked-signals-with-pthr.patch patch, rhbz#602594
- Updated init.d script rhbz#603157
- Add myproxy as requires to myproxy-admin to install clients.

* Sat May 15 2010 Steve Traylen <steve.traylen@cern.ch> - 5.1-2
- rhbz#585189 rearrange packaging.
  clients moved from now obsoleted -client package
  to main package.
  libs moved from main package to new libs package.

* Tue Mar 09 2010 Steve Traylen <steve.traylen@cern.ch> - 5.1-1
- New upstream 5.1
- Remove globus-globus-usage-location.patch, now incoperated
  upstream.

* Fri Dec 04 2009 Steve Traylen <steve.traylen@cern.ch> - 5.0-1
- Add globus-globus-usage-location.patch
  https://bugzilla.mcs.anl.gov/globus/show_bug.cgi?id=6897
- Addition of globus-usage-devel to BR.
- New upstream 5.0
- Upstream source hosting changed from globus to sourceforge.

* Fri Nov 13 2009 Steve Traylen <steve.traylen@cern.ch> - 4.9-6
- Add requires globus-gsi-cert-utils-progs for grid-proxy-info
  to myproxy-admin package rhbz#536927
- Release bump to F13 so as to be newer than F12.

* Tue Oct 13 2009 Steve Traylen <steve.traylen@cern.ch> - 4.9-3
- Glob on .so.* files to future proof for upgrades.

* Tue Oct 13 2009 Steve Traylen <steve.traylen@cern.ch> - 4.9-1
- New upstream 4.9.

* Tue Oct 13 2009 Steve Traylen <steve.traylen@cern.ch> - 4.8-5
- Disable openldap support for el4 only since openldap to old.

* Wed Oct 07 2009 Steve Traylen <steve.traylen@cern.ch> - 4.8-4
- Add ASL 2.0 license as well.
- Explicitly add /etc/grid-security to files list
- For .el4/5 build only add globus-gss-assist-devel as requirment
  to myproxy-devel package.

* Thu Oct 01 2009 Steve Traylen <steve.traylen@cern.ch> - 4.8-3
- Set _initddir for .el4 and .el5 building.

* Mon Sep 21 2009 Steve Traylen <steve.traylen@cern.ch> - 4.8-2
- Require version of voms with fixed ABI.

* Thu Sep 10 2009 Steve Traylen <steve.traylen@cern.ch> - 4.8-1
- Increase version to upstream 4.8
- Remove voms-header-location.patch since fixed upstream now.
- Include directory /etc/grid-security/myproxy

* Mon Jun 22 2009 Steve Traylen <steve.traylen@cern.ch> - 4.7-1
- Initial version.
