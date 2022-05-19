%global _hardened_build 1

%{!?_initddir: %global _initddir %{_initrddir}}

%if %{?fedora}%{!?fedora:0} >= 17 || %{?rhel}%{!?rhel:0} >= 7
%global with_sysv 0
%else
%global with_sysv 1
%endif

%global with_checks 1

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           myproxy
Version:        6.2.6
Release:        1.1%{?dist}
Summary:        Manage X.509 Public Key Infrastructure (PKI) security credentials

License:        NCSA and BSD and ASL 2.0
URL:            http://grid.ncsa.illinois.edu/myproxy/
Source:         https://repo.gridcf.org/gct6/sources/%{name}-%{version}.tar.gz
Source2:        myproxy-server-start
Source8:        README
Patch1:         Skip-.rpmsave-and-.rpmnew-files-in-etc-myproxy.d.patch
Patch2:         EL7-Use-myproxy-server-start-script.patch

BuildRequires:  gcc
BuildRequires:  globus-common-devel >= 15
BuildRequires:  globus-gssapi-gsi-devel >= 9
BuildRequires:  globus-gss-assist-devel >= 8
BuildRequires:  globus-gsi-sysconfig-devel >= 5
BuildRequires:  globus-gsi-cert-utils-devel >= 8
BuildRequires:  globus-gsi-proxy-core-devel >= 6
BuildRequires:  globus-gsi-credential-devel >= 5
BuildRequires:  globus-gsi-callback-devel >= 4
BuildRequires:  cyrus-sasl-devel
BuildRequires:  krb5-devel
BuildRequires:  openldap-devel >= 2.3
BuildRequires:  pam-devel
BuildRequires:  perl-generators
BuildRequires:  voms-devel >= 1.9.12.1
%if ! %{with_sysv}
BuildRequires:  systemd
%endif
%if %{?with_checks}
BuildRequires:  globus-proxy-utils
BuildRequires:  globus-gsi-cert-utils-progs
BuildRequires:  openssl
BuildRequires:  voms-clients
%endif

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}-client = %{version}-%{release}
Obsoletes:      %{name}-client < 5.1-3

%description
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

%package libs
Summary:        Manage X.509 Public Key Infrastructure (PKI) security credentials
Requires:       globus-proxy-utils
Requires:       globus-gssapi-gsi%{?_isa} >= 12
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
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

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
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Requires(pre):    shadow-utils
%if %{?with_sysv}
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts
%else
%{?systemd_requires}
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
# Create a separate admin clients package since they are not needed for normal
# operation and pull in a load of perl dependencies.
Summary:        Server for X.509 Public Key Infrastructure (PKI) security credentials
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

%package voms
Summary:        Manage X.509 Public Key Infrastructure (PKI) security credentials
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-libs < 6.1.6
Requires:       voms-clients

%description voms
MyProxy is open source software for managing X.509 Public Key Infrastructure
(PKI) security credentials (certificates and private keys). MyProxy
combines an online credential repository with an online certificate
authority to allow users to securely obtain credentials when and where needed.
Users run myproxy-logon to authenticate and obtain credentials, including
trusted CA certificates and Certificate Revocation Lists (CRLs).

Package %{name}-voms contains runtime libs for MyProxy to use VOMS.

%package doc
Summary:        Documentation for X.509 Public Key Infrastructure (PKI) security credentials
BuildArch:      noarch

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
%patch1 -p1
%patch2 -p1

%build
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

%configure --disable-static \
           --includedir=%{_includedir}/globus \
           --with-openldap=%{_prefix} \
           --with-voms=%{_prefix} \
           --with-kerberos5=%{_prefix} \
           --with-sasl2=%{_prefix}

# Reduce overlinking
sed 's!CC \(.*-shared\) !CC \\\${wl}--as-needed \1 !' -i libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

# Put documentation in Fedora default location
mkdir -p %{buildroot}%{_pkgdocdir}/extras
for FILE in login.html myproxy-accepted-credentials-mapapp \
            myproxy-cert-checker myproxy-certificate-mapapp \
            myproxy-certreq-checker myproxy-crl.cron myproxy.cron \
            myproxy-get-delegation.cgi myproxy-get-trustroots.cron \
            myproxy-passphrase-policy myproxy-revoke ; do
   mv %{buildroot}%{_datadir}/%{name}/$FILE %{buildroot}%{_pkgdocdir}/extras
done

mkdir -p %{buildroot}%{_pkgdocdir}
for FILE in LICENSE LICENSE.* PROTOCOL README.sasl REPOSITORY VERSION ; do
   mv %{buildroot}%{_datadir}/%{name}/$FILE %{buildroot}%{_pkgdocdir}
done

# Remove license files from pkgdocdir if licensedir is used
%{?_licensedir: rm %{buildroot}%{_pkgdocdir}/LICENSE*}

# Remove irrelevant example configuration files
for FILE in etc.inetd.conf.modifications etc.init.d.myproxy.nonroot \
            etc.services.modifications etc.xinetd.myproxy etc.init.d.myproxy \
            myproxy-server.service myproxy-server.conf ; do
   rm %{buildroot}%{_datadir}/%{name}/$FILE
done

# Move example configuration file into place
mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}%{_datadir}/%{name}/myproxy-server.config \
   %{buildroot}%{_sysconfdir}

# Always install myproxy.sysconfig (SOFTWARE-2471)
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 myproxy.sysconfig \
   %{buildroot}%{_sysconfdir}/sysconfig/myproxy-server
%if %{with_sysv}
mkdir -p %{buildroot}%{_initddir}
install -p -m 755 myproxy.init %{buildroot}%{_initddir}/myproxy-server
%else
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_tmpfilesdir}
install -p -m 644 systemd/myproxy-server.service %{buildroot}%{_unitdir}
install -p -m 644 systemd/myproxy-server.conf %{buildroot}%{_tmpfilesdir}
# Startup script used on EL7 to source sysconfig files (SOFTWARE-2471)
mkdir -p %{buildroot}%{_libexecdir}
install -p -m 755 %{SOURCE2} %{buildroot}%{_libexecdir}/myproxy-server-start
%endif

mkdir -p %{buildroot}%{_localstatedir}/lib/myproxy

# Create a directory to hold myproxy owned host certificates
mkdir -p %{buildroot}%{_sysconfdir}/grid-security/myproxy

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Remove myproxy-server-setup rhbz#671561
rm %{buildroot}%{_sbindir}/myproxy-server-setup

mkdir -p %{buildroot}%{_sysconfdir}/myproxy.d


%check
%if %{?with_checks}
make %{?_smp_mflags} check VERBOSE=1
%endif

%ldconfig_scriptlets libs

%pre server
# uid:gid 178:178 now reserved for myproxy. rhbz#733671
getent group myproxy > /dev/null || groupadd -g 178 -r myproxy
getent passwd myproxy > /dev/null || \
useradd -u 178 -r -g myproxy -d %{_localstatedir}/lib/myproxy \
    -s /sbin/nologin -c "User to run the MyProxy service" myproxy
exit 0

%if %{?with_sysv}
%post server
/sbin/chkconfig --add myproxy-server
%else
%post server
systemd-tmpfiles --create myproxy-server.conf > /dev/null 2>&1 || :
%systemd_post myproxy-server.service
%endif

%if %{?with_sysv}
%preun server
if [ $1 -eq 0 ] ; then
    /sbin/service myproxy-server stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del myproxy-server
fi
%else
%preun server
%systemd_preun myproxy-server.service
%endif

%if %{?with_sysv}
%postun server
if [ $1 -ge 1 ] ; then
    /sbin/service myproxy-server condrestart > /dev/null 2>&1 || :
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
%{_mandir}/man1/myproxy-get-trustroots.1*
%{_mandir}/man1/myproxy-info.1*
%{_mandir}/man1/myproxy-init.1*
%{_mandir}/man1/myproxy-logon.1*
%{_mandir}/man1/myproxy-retrieve.1*
%{_mandir}/man1/myproxy-store.1*

%files libs
%{_libdir}/libmyproxy.so.*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/PROTOCOL
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/README.sasl
%doc %{_pkgdocdir}/REPOSITORY
%doc %{_pkgdocdir}/VERSION
%{!?_licensedir: %doc %{_pkgdocdir}/LICENSE*}
%{?_licensedir: %license LICENSE*}

%files devel
%{_includedir}/globus/*
%{_libdir}/libmyproxy.so
%{_libdir}/pkgconfig/myproxy.pc

%files server
%{_sbindir}/myproxy-server
# Always install myproxy.sysconfig (SOFTWARE-2471)
%config(noreplace) %{_sysconfdir}/sysconfig/myproxy-server
%if %{?with_sysv}
%{_initddir}/myproxy-server
%else
%{_unitdir}/myproxy-server.service
%{_tmpfilesdir}/myproxy-server.conf
# Startup script used on EL7 to source sysconfig files (SOFTWARE-2471)
%{_libexecdir}/myproxy-server-start
# Own the runtime directory, which is managed by tmpfiles
%ghost %{_localstatedir}/run/myproxy-server
%endif
%config(noreplace) %{_sysconfdir}/myproxy-server.config
# myproxy-server wants exactly 700 permission on its data
# which is just fine.
%attr(0700,myproxy,myproxy) %dir %{_localstatedir}/lib/myproxy
%dir %{_sysconfdir}/grid-security/myproxy
%{_mandir}/man8/myproxy-server.8*
%{_mandir}/man5/myproxy-server.config.5*
%doc README.Fedora
%dir %{_sysconfdir}/myproxy.d

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

%files voms
%{_libdir}/libmyproxy_voms.so

%files doc
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/extras
%{!?_licensedir: %doc %{_pkgdocdir}/LICENSE*}
%{?_licensedir: %license LICENSE*}

%changelog
* Tue Sep 17 2019 Carl Edquist <edquist@cs.wisc.edu> - 6.2.6-1.1
- Merge OSG changes (SOFTWARE-3828)

* Fri Aug 30 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.6-1
- Clean up old GPT references (6.2.5)
- Install myproxy-get-trustroots man page (6.2.5)
- Remove LICENSE.globus file - usage statistics collection (6.2.6)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.2.4-1.1.osg
- Merge OSG changes
- Drop 00-osg-environment (unnecessary)

* Wed Feb 27 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.4-1
- Remove usage statistics collection support

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 13 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.3-1
- Switch upstream to Grid Community Toolkit
- First Grid Community Toolkit release (6.2.0)
  - Disable usage statistics reporting by default
  - Fix option parsing bug
- Merge GT6 update 6.1.29 into GCT (6.2.1)
- Use 2048 bit CA key for myproxy tests (6.2.2)
- Merge GT6 update 6.1.30 into GCT (6.2.3)

* Sat Sep 01 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.31-1
- GT6 update: Use 2048 bit keys to support openssl 1.1.1
- Drop patch myproxy-2048-bits.patch (accepted upstream)

* Sun Aug 26 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.30-3
- Use 2048 bit CA key for myproxy tests

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.30-1
- Update to 6.1.30: Remove macro overquoting

* Thu May 03 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.29-1
- Update to 6.1.29: Fix -Werror=format-security errors

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.28-1
- Update to 6.1.28
  - Fix error check (6.1.26)
  - Remove legacy SSLv3 support (6.1.27)

* Mon Mar 27 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.25-3
- EPEL 5 End-Of-Life specfile clean-up
  - Remove Group and BuildRoot tags
  - Remove _pkgdocdir and _initddir macro definitions
  - Drop redundant Requires corresponding to autogenerated pkgconfig Requires
  - Don't clear the buildroot in the install section
  - Remove the clean section
  - Drop the myproxy-openssl098.patch

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.25-1
- Update to 6.1.25 (Fixes for OpenSSL 1.1.0)

* Fri Nov 18 2016 Tim Cartwright <cat@cs.wisc.edu> - 6.1.18-1.4.osg
- Declare ownership of /var/run/myproxy-server, managed by systemd tmpfiles

* Thu Oct 20 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.1.18-1.3.osg
- Skip .rpmsave and .rpmnew files in /etc/myproxy.d
- Source sysconfig files on EL7 (SOFTWARE-2471)

* Wed Oct 19 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.1.18-1.2.osg
- Disable SSLv3 (SOFTWARE-2471)

* Fri Sep 02 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.19-1
- Update to 6.1.19 (update myproxy debug/error msgs for accepted_peer_names
  type change)

* Wed Aug 31 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 6.1.18-1.1.osg
- Patch to fix debug/error messages for accepted_peer_names (PR #70)
    require globus-gssapi-gsi >= 12 due to the API change that caused this

* Fri May 06 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.18-1
- Update to 6.1.18 (spelling)

* Tue Mar 15 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.17-1
- Update to 6.1.17 (handle error returns from OCSP_parse_url)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 10 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.16-1
- Update to 6.1.16 (handle invalid proxy_req type)

* Wed Oct 21 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.15-2
- Generate temporary directory in post install scriptlet

* Wed Jul 29 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.15-1
- Update to 6.1.15
- GT-616: Myproxy uses resolved IP address when importing names

* Sat Jun 20 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.14-1
- Update to 6.1.14 (RFC2818 name handling)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.13-1
- Update to 6.1.13 (underallocation of memory)

* Thu Jan 15 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.12-1
- Update to 6.1.12
- Implement updated license packaging guidelines

* Thu Dec 18 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.10-1
- Update to 6.1.10
- Drop patches myproxy-tls.patch and myproxy-liblink.patch (fixed upstream)

* Wed Nov 19 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1.6-1
- Update to 6.1.6
- Drop patch myproxy-deps.patch (fixed upstream)
- Upstream source moved from sourceforge to the Globus Toolkit github repo
- Use source tarball published by Globus
- Use upstream's init scripts and systemd unit files
- New binary package myproxy-voms (voms support split out as a plugin)

* Sat Sep 20 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.0-2
- Use larger patch instead of running autoreconf (fixes EPEL5)

* Sat Sep 20 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.0-1
- Update to 6.0, adapt to Globus Toolkit 6
- Drop GPT build system and GPT packaging metadata
- Activate hardening flags

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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
