%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global _hardened_build 1

Name:		voms
Version:	2.0.11
%global tagver %(tr . _ <<< %{version})
Release:	2.3%{?dist}
Summary:	Virtual Organization Membership Service

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		https://wiki.italiangrid.it/VOMS
#Source0:	https://github.com/italiangrid/%{name}/archive/%{tagver}.tar.gz
Source0:        2_0_11.tar.gz
#		Post-install setup instructions:
Source1:	%{name}.INSTALL
#		Don't use embedded gsoap sources
Patch0:		%{name}-gsoap.patch
Patch1:         sha2-proxy.patch
Patch2:		handle-dns-failures.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	globus-gssapi-gsi-devel
BuildRequires:	globus-gss-assist-devel
BuildRequires:	openssl-devel
BuildRequires:	expat-devel
BuildRequires:	gsoap-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	libxslt
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	tex(latex)
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 7
BuildRequires:	tex(sectsty.sty)
BuildRequires:	tex(tocloft.sty)
BuildRequires:	tex(xtab.sty)
BuildRequires:	tex(multirow.sty)
BuildRequires:	tex-ec
BuildRequires:	tex-courier
BuildRequires:	tex-helvetic
BuildRequires:	tex-times
BuildRequires:	tex-symbol
BuildRequires:	tex-rsfs
%endif

%description
In grid computing, and whenever the access to resources may be controlled
by parties external to the resource provider, users may be grouped to
Virtual Organizations (VOs). This package provides a VO Membership Service
(VOMS), which informs on that association between users and their VOs:
groups, roles and capabilities.

This package offers libraries that applications using the VOMS functionality
will bind to.

%package devel
Summary:	Virtual Organization Membership Service Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	openssl-devel%{?_isa}
Requires:	automake

%description devel
In grid computing, and whenever the access to resources may be controlled
by parties external to the resource provider, users may be grouped to
Virtual Organizations (VOs). This package provides a VO Membership Service
(VOMS), which informs on that association between users and their VOs:
groups, roles and capabilities.

This package offers header files for programming with the VOMS libraries.

%package doc
Summary:	Virtual Organization Membership Service Documentation
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for the Virtual Organization Membership Service.

%package clients
Summary:	Virtual Organization Membership Service Clients
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description clients
In grid computing, and whenever the access to resources may be controlled
by parties external to the resource provider, users may be grouped to
Virtual Organizations (VOs). This package provides a VO Membership Service
(VOMS), which informs on that association between users and their VOs:
groups, roles and capabilities.

This package provides command line applications to access the VOMS
services.

%package server
Summary:	Virtual Organization Membership Service Server
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}

Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description server
In grid computing, and whenever the access to resources may be controlled
by parties external to the resource provider, users may be grouped to
Virtual Organizations (VOs). This package provides a VO Membership Service
(VOMS), which informs on that association between users and their VOs:
groups, roles and capabilities.

The service can be understood as an account database, which serves the
information in a special format (VOMS credential). The VO manager can
administrate it remotely using command line tools or a web interface.

%prep
%setup -q -n %{name}-%{tagver}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Remove embedded gsoap sources
rm src/server/stdsoap2.c src/server/stdsoap2.h src/server/soap*

# rebootstrap
./autogen.sh

install -m 644 %{SOURCE1} README.Fedora

%build
%configure --disable-static --enable-docs --disable-parser-gen

make %{?_smp_mflags}

( cd doc/apidoc/api/VOMS_C_API/latex ; make )
( cd doc/apidoc/api/VOMS_CC_API/latex ; make )

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*.la

mkdir -p %{buildroot}%{_sysconfdir}/grid-security/vomsdir
mkdir -p %{buildroot}%{_sysconfdir}/grid-security/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# Turn off default enabling of the service
mkdir -p %{buildroot}%{_initrddir}
sed -e 's/\(chkconfig: \)\w*/\1-/' \
    -e '/Default-Start/d' \
    -e 's/\(Default-Stop:\s*\).*/\10 1 2 3 4 5 6/' \
    -i %{buildroot}%{_initrddir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
echo VOMS_USER=voms > %{buildroot}%{_sysconfdir}/sysconfig/%{name}

mkdir -p %{buildroot}%{_pkgdocdir}
install -m 644 -p AUTHORS LICENSE README.md %{buildroot}%{_pkgdocdir}

mkdir -p %{buildroot}%{_pkgdocdir}/VOMS_C_API
cp -pr doc/apidoc/api/VOMS_C_API/html %{buildroot}%{_pkgdocdir}/VOMS_C_API
rm -f %{buildroot}%{_pkgdocdir}/VOMS_C_API/html/installdox
install -m 644 doc/apidoc/api/VOMS_C_API/latex/refman.pdf \
   %{buildroot}%{_pkgdocdir}/VOMS_C_API

mkdir -p %{buildroot}%{_pkgdocdir}/VOMS_CC_API
cp -pr doc/apidoc/api/VOMS_CC_API/html %{buildroot}%{_pkgdocdir}/VOMS_CC_API
rm -f %{buildroot}%{_pkgdocdir}/VOMS_CC_API/html/installdox
install -m 644 doc/apidoc/api/VOMS_CC_API/latex/refman.pdf \
   %{buildroot}%{_pkgdocdir}/VOMS_CC_API

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%posttrans
# Recover /etc/vomses...
if [ -r %{_sysconfdir}/vomses.rpmsave -a ! -r %{_sysconfdir}/vomses ] ; then
   mv %{_sysconfdir}/vomses.rpmsave %{_sysconfdir}/vomses
fi

%pre server
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} \
    -d %{_sysconfdir}/%{name} -s /sbin/nologin -c "VOMS Server Account" %{name}
exit 0

%post server
if [ $1 = 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun server
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi

%postun server
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_libdir}/libvomsapi.so.1*
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/vomsdir
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/vomses.template
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/AUTHORS
%doc %{_pkgdocdir}/LICENSE
%doc %{_pkgdocdir}/README.md

%files devel
%defattr(-,root,root,-)
%{_libdir}/libvomsapi.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}-2.0.pc
%{_datadir}/aclocal/%{name}.m4
%{_mandir}/man3/*

%files doc
%defattr(-,root,root,-)
%doc %{_pkgdocdir}/VOMS_C_API
%doc %{_pkgdocdir}/VOMS_CC_API

%files clients
%defattr(-,root,root,-)
%{_bindir}/voms-proxy-destroy
%{_bindir}/voms-proxy-info
%{_bindir}/voms-proxy-init
%{_bindir}/voms-proxy-fake
%{_bindir}/voms-proxy-list
%{_mandir}/man1/voms-proxy-destroy.1*
%{_mandir}/man1/voms-proxy-info.1*
%{_mandir}/man1/voms-proxy-init.1*
%{_mandir}/man1/voms-proxy-fake.1*
%{_mandir}/man1/voms-proxy-list.1*

%files server
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/grid-security/%{name}
%attr(-,voms,voms) %dir %{_localstatedir}/log/%{name}
%{_datadir}/%{name}/mysql2oracle
%{_datadir}/%{name}/upgrade1to2
%{_datadir}/%{name}/voms.data
%{_datadir}/%{name}/voms_install_db
%{_datadir}/%{name}/voms-ping
%{_datadir}/%{name}/voms_replica_master_setup.sh
%{_datadir}/%{name}/voms_replica_slave_setup.sh
%{_mandir}/man8/voms.8*
%doc README.Fedora

%changelog
* Thu May 22 2014 Carl Edquist <edquist@cs.wisc.edu> - 2.0.11-2.3
- Handle DNS failures (SOFTWARE-1463)

* Mon May 12 2014 Brian Lin <blin@cs.wisc.edu> - 2.0.11-2.2
- Fix stack smashing when requesting an RFC-compliant, SHA2 proxy.

* Wed Dec 18 2013 Edgar Fajardo <efajardo@cern.ch> - 2.0.11-2.1
- Upgraded to version 2.0.11

* Wed Nov 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-2
- Specfile cleanup

* Wed Nov 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-1
- Update to version 2.0.11
- Drop patches voms-install-db2.patch and voms-doc-race.patch (accepted
  upstream)

* Thu Aug 08 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.10-3
- Activate hardened buildflags
- Use _pkgdocdir

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.9
- Do not rotate empty logfiles (SOFTWARE-1084). This avoids problems caused by 'copytruncate' on leftover bogus logs from before the 2.0.8-1.6 fix.

* Tue Jun 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.8
- Changed logrotate file so that rotation works for VOs with names ending in 'z' (SOFTWARE-1084)

* Mon Jun 17 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.6
- Updated logrotate file to rotate old logs into a separate directory (SOFTWARE-1084)

* Tue Feb 12 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.10-1
- Update to version 2.0.10

* Tue Nov 27 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.9-1
- Update to version 2.0.9
- Add Build Requires for texlive 2012 (Fedora 18+)

* Mon Aug 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.3
- Release bump for koji

* Mon Aug 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.8-1.1
- Add OSG patches and logrotate file

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.8-1
- Update to version 2.0.8 (EMI 2 version)

* Mon Apr 23 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.7-2
- Fix build of compat package with new globus headers

* Mon Apr 23 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.7-1
- Update to version 2.0.7
- No longer build the Java API - it is in a separate package now

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-5
- Rebuilt for c++ ABI breakage

* Fri Feb 10 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.6-4
- Rebuilt for gsoap 2.8.7 (Fedora 17+)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.6-3
- Rebuild for new gsoap

* Sat Oct 01 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.6-2
- Don't build java in parallel
- Remove the data.3 man page (too common name)

* Tue Aug 30 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.6-1
- Update to version 2.0.6

* Fri May 27 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.2-1
- Update to version 2.0.2
- Add compat package for older releases
- Drop Java AOT compilation for newer releases

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 26 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.19.2-2
- Make vomsjapi-javadoc arch depenent on EPEL

* Mon Nov 01 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.19.2-1
- Upstream 1.9.19.2 (CVS tag glite-security-voms_R_1_9_19_2)

* Sun Oct 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.18.1-3
- Add posttrans scriptlet to recover /etc/vomses

* Fri Oct 15 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.18.1-2
- Remove the empty /etc/vomses file - it will cause conflicts for users
  that have used the option to have /etc/vomses be a directory

* Mon Oct 04 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.18.1-1
- Upstream 1.9.18.1 (CVS tag glite-security-voms_R_1_9_18_1)

* Thu Jul 08 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.17.1-2
- Make -doc subpackage depend of main package for license reasons

* Sat Jun 05 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.17.1-1
- Upstream 1.9.17.1 (CVS tag glite-security-voms_R_1_9_17_1)
- Drop patches voms-db-method.patch and voms-thread.patch (accepted upstream)

* Sat Apr 03 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.16.1-2.1
- Enable java for x86 and x86_64

* Sun Mar 28 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.16.1-2
- Add mutex lock for accessing private data

* Fri Mar 19 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.16.1-1
- Upstream 1.9.16.1 (CVS tag glite-security-voms_R_1_9_16_1)
- Fix uninitialized variable in voms-proxy-init

* Mon Dec 28 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.14.3-1
- Upstream 1.9.14.3 (CVS tag glite-security-voms_R_1_9_14_3)
- Add missing dependencies for stricter binutils

* Tue Oct 20 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.14.2-1
- Upstream 1.9.14.2 (CVS tag glite-security-voms_R_1_9_14_2)

* Fri Sep 18 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.12.1-1
- Upstream 1.9.12.1 (CVS tag glite-security-voms_R_1_9_12_1)

* Mon Sep 07 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.11-4
- Fix building with openssl 1.0

* Thu Sep 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.11-3
- Add an empty /etc/vomses file to the main package to avoid error messages
- Let the voms user own only necessary directories
- Additional fixes for the server start-up script

* Tue Aug 25 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.11-2
- Add the /etc/voms directory to the server package
- Add setup instructions to the server package
- Run the server as non-root

* Fri Aug 14 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.11-1
- Upstream 1.9.11 (CVS tag glite-security-voms_R_1_9_11)
- Enable Java AOT bits

* Mon Jun 29 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.8.1-1
- Upstream 1.9.8.1 (CVS tag glite-security-voms_R_1_9_8_1)
- Build Java API

* Thu Feb 12 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.2-1
- Upstream 1.9.2 (CVS tag glite-security-voms_R_1_9_2)

* Fri Feb 06 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.9.1-1
- Upstream 1.9.1 (CVS tag glite-security-voms_R_1_9_1)

* Tue Jan 06 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.10-1
- Upstream 1.8.10 (CVS tag glite-security-voms_R_1_8_10)
- Rebuild against distribution Globus
- Add clear SSL error patch needed for openssl > 0.9.8b
- Add missing return value patch

* Sun Oct 26 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.8.9-1ng
- Upstream 1.8.9 (CVS tag glite-security-voms_R_1_8_9)
- Rebuild against Globus 4.0.8-0.11

* Thu May 15 2008 Anders Wäänänen <waananen@nbi.dk> - 1.7.24-4ng
- Add missing include patch

* Sat Apr 26 2008 Anders Wäänänen <waananen@nbi.dk> - 1.7.24-3ng
- Rebuild against Globus 4.0.7-0.10

* Sun Nov 25 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.24-2ng
- Fix GPT_LOCATION and GLOBUS_LOCATION detection in spec file

* Mon Oct 29 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.24-1ng
- Upstream 1.7.24 (CVS tag glite-security-voms_R_1_7_24_1)

* Mon Oct 15 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.23-1ng
- Upstream 1.7.23 (CVS tag glite-security-voms_R_1_7_23_1)

* Wed Sep 12 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.22-3ng
- Move /etc/voms/vomses back to /etc/vomses
- Added more openssl portability patches with input
  from Aake Sandgren <ake.sandgren@hpc2n.umu.se>

* Wed Sep 12 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.22-2ng
- Added more openssl portability patches with input
  from Aake Sandgren <ake.sandgren@hpc2n.umu.se>

* Mon Sep 10 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.22-1ng
- Try to link against system crypto library when Globus library is not
  available
- Make /etc/grid-security/vomsdir part of the voms sub-package
- Drop RPM prefix /etc
- Move the vomses.template to /etc/voms
- Use dashes instead of underscore in voms-install-replica.1 man page
- Do not try to link against system crypt library. Voms now
  does this internally.
- Upstream 1.7.22 (CVS tag glite-security-voms_R_1_7_22_1)

* Mon Jul 16 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.20-5ng
- Drop voms-struct_change.patch - problem is with libxml2

* Sat Jul 14 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.20-4ng
- Add missing openssl-devel dependency in voms-devel

* Thu Jul 12 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.20-3ng
- Add patch:
  - voms-struct_change.patch
    - Change API slightly - but now works with libxml2

* Sun Jul 08 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.20-2ng
- Make conditinal dependency on expat-devel (OpenSuSE 10.20 has only expat)

* Thu Jul 05 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.20-1ng
- Upstream 1.7.20 (CVS tag glite-security-voms_R_1_7_20_1) 

* Thu Jul 05 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.19-2ng
- Added patches:
  - voms-openssl_portability.patch
    - Support for newer OpenSSL-0.9.8
  - voms-isoc90_portability.patch
    - Support for older compilers
- Added openssl-devel build dependency

* Fri Jun 22 2007 Anders Wäänänen <waananen@nbi.dk> - 1.7.19-1ng
- Upstream 1.7.19 (CVS tag glite-security-voms_R_1_7_19_P2) 
- Remove patches (use shell substitutions instead)
- Disable Java API build

* Fri Jun 22 2007 Anders Wäänänen <waananen@nbi.dk> - 1.6.20-3ng
- Added Globus dependencies to voms-devel

* Mon Jul 24 2006 Anders Wäänänen <waananen@nbi.dk> - 1.6.20-2ng
- Fix dependency typo: Requires -> BuildRequires

* Sat May 06 2006 Anders Wäänänen <waananen@nbi.dk> - 1.6.20-1ng
- Many changes since upstream changed quite a lot.
- Added README.NorduGrid with packaging information
- Patches:
  - voms_openssl-0.9.8.patch
    - Support for OpenSSL 0.9.8
  - voms_noglobusopenssl-1.6.20.patch
    - Use system openssl rather than the one from Globus
    - Patch reworked for voms 1.6.20
  - Dont use project based (gLite) include paths
- Pseudo patches (fixes made at runtime and not from static patch files)
  - Fix broken --libexecdir support for configure
    (some systems do not have libexecdir = <prefix>/libexec)
  - Drop all documents except man pages which are pre-generated
    (section 3 man pages are skipped as well)
  - Do not use edg- prefix
    (can be turned on/off through macro)
  - Install flavored libraries in addition to non-flavored
    (can be turned on/off through macro)
  - Put start-up script in /etc/init.d
  - Move configuration files from <prefix>/etc to /etc

* Mon Dec 19 2005 Anders Wäänänen <waananen@nbi.dk> - 1.6.9-2
- Add patch voms_doc.patch to disable html and ps documentation
  and add man-mages and pdf files to distribution (make dist)
- Use rpm switch: --define "_autotools_bootstrap 1" to rebuild
  documentation and create "make dist" target
- Add patch voms_nohardcodelibexecdir.patch which use the libexecdir
  from configure rather than the hardcoded prefix/libexec

* Sun Nov 27 2005 Anders Wäänänen <waananen@nbi.dk> - 1.6.9-1
- Add patch voms_ssl_include.patch to add external openssl includes.
  Would be better to query globus_openssl about this

* Tue Oct 18 2005 Anders Wäänänen <waananen@nbi.dk> - 1.6.7-1
- Modfiy voms_noglobusopenssl.patch to match upstream
- Add patch voms_nops.patch to disable postscript versions of
  reference manual

* Fri Jun 17 2005 Anders Wäänänen <waananen@nbi.dk> - 1.5.4-1
- Remove the following patches:
  - voms_namespace.patch - Fixed in upstream
  - voms_external_mysql++-1.4.1.patch - Obsolete since mysql++ is no
    longer needed
  - voms-no_libs.path - Fixed in upstream
- Add Globus dependencies

* Wed Jun 01 2005 Anders Wäänänen <waananen@nbi.dk> - 1.4.1-3
- Do not hardcode Globus flavor but try to guess
- Remove explicit globus rpm Requirement
- Use external openssl - not globus_openssl

* Mon May 02 2005 Anders Wäänänen <waananen@nbi.dk> - 1.4.1-2
- Remove automake cache
- Add explicit dependency on mysql++-devel

* Sat Apr 30 2005 Anders Wäänänen <waananen@nbi.dk> - 1.4.1-1
- New upstream
- autogen.sh -> autobuild.sh

* Mon Apr 18 2005 Anders Wäänänen <waananen@nbi.dk> - 1.3.2-1
- Initial build.
