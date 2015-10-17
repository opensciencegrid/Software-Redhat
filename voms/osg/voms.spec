%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global _hardened_build 1

Name:		voms
Version:	2.0.12
Release:	3%{?dist}
Summary:	Virtual Organization Membership Service

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		https://wiki.italiangrid.it/VOMS
Source0:	https://github.com/italiangrid/%{name}/archive/v%{version}.tar.gz
#		Post-install setup instructions:
Source1:	%{name}.INSTALL
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	openssl-devel
BuildRequires:	expat-devel
BuildRequires:	gsoap-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	libxslt
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen

%description
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

This package provides libraries that applications using the VOMS functionality
will bind to.

%package devel
Summary:	Virtual Organization Membership Service Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	openssl-devel%{?_isa}

%description devel
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

This package provides header files for programming with the VOMS libraries.

%package doc
Summary:	Virtual Organization Membership Service Documentation
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%description doc
Documentation for the Virtual Organization Membership Service.

%package clients-cpp
Summary:	Virtual Organization Membership Service Clients
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	voms-clients = %{version}-%{release}
Obsoletes:	voms-clients < 2.0.12-3

Requires(post):		%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description clients-cpp
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

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
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

This package provides the VOMS service.

%prep
%setup -q

./autogen.sh

install -m 644 %{SOURCE1} README.Fedora

%build
%configure --disable-static --enable-docs --disable-parser-gen

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*.la

# Turn off default enabling of the service
mkdir -p %{buildroot}%{_initrddir}
sed -e 's/\(chkconfig: \)\w*/\1-/' \
    -e '/Default-Start/d' \
    -e 's/\(Default-Stop:\s*\).*/\10 1 2 3 4 5 6/' \
    -i %{buildroot}%{_initrddir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
echo VOMS_USER=voms > %{buildroot}%{_sysconfdir}/sysconfig/%{name}

mkdir -p %{buildroot}%{_pkgdocdir}
install -m 644 -p AUTHORS README.md %{buildroot}%{_pkgdocdir}
%{!?_licensedir: install -m 644 -p LICENSE %{buildroot}%{_pkgdocdir}}

mkdir -p %{buildroot}%{_pkgdocdir}/VOMS_C_API
cp -pr doc/apidoc/api/VOMS_C_API/html %{buildroot}%{_pkgdocdir}/VOMS_C_API
rm -f %{buildroot}%{_pkgdocdir}/VOMS_C_API/html/installdox

mkdir -p %{buildroot}%{_pkgdocdir}/VOMS_CC_API
cp -pr doc/apidoc/api/VOMS_CC_API/html %{buildroot}%{_pkgdocdir}/VOMS_CC_API
rm -f %{buildroot}%{_pkgdocdir}/VOMS_CC_API/html/installdox

for b in voms-proxy-init voms-proxy-info voms-proxy-destroy; do
  ## Rename client binaries
  mv %{buildroot}%{_bindir}/${b} %{buildroot}%{_bindir}/${b}2
  touch %{buildroot}/%{_bindir}/${b}
  chmod 755 %{buildroot}/%{_bindir}/${b}
  ## and man pages
  mv %{buildroot}%{_mandir}/man1/${b}.1 %{buildroot}%{_mandir}/man1/${b}2.1
  touch %{buildroot}%{_mandir}/man1/${b}.1
done

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

%pre clients-cpp
if [ $1 -gt 1 ]; then
  for c in voms-proxy-init voms-proxy-info voms-proxy-destroy; do
    if [ -r %{_bindir}/$c -a ! -h %{_bindir}/$c ]; then
      rm -f %{_bindir}/$c
    fi
    if [ -r %{_mandir}/man1/$c.1.gz -a ! -h %{_mandir}/man1/$c.1.gz ]; then
      rm -f %{_mandir}/man1/$c.1.gz
    fi
  done
fi

%post clients-cpp
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-init \
    voms-proxy-init %{_bindir}/voms-proxy-init2 50 \
    --slave %{_mandir}/man1/voms-proxy-init.1.gz voms-proxy-init-man \
    %{_mandir}/man1/voms-proxy-init2.1.gz
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-info \
    voms-proxy-info %{_bindir}/voms-proxy-info2 50 \
    --slave %{_mandir}/man1/voms-proxy-info.1.gz voms-proxy-info-man \
    %{_mandir}/man1/voms-proxy-info2.1.gz
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-destroy \
    voms-proxy-destroy %{_bindir}/voms-proxy-destroy2 50 \
    --slave %{_mandir}/man1/voms-proxy-destroy.1.gz voms-proxy-destroy-man \
    %{_mandir}/man1/voms-proxy-destroy2.1.gz

%postun clients-cpp
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove voms-proxy-init \
    %{_bindir}/voms-proxy-init2
    %{_sbindir}/update-alternatives --remove voms-proxy-info \
    %{_bindir}/voms-proxy-info2
    %{_sbindir}/update-alternatives --remove voms-proxy-destroy \
    %{_bindir}/voms-proxy-destroy2
fi

%triggerpostun clients-cpp -- voms-clients
# Uninstalling the old voms-clients package will remove the alternatives
# for voms-clients-cpp - put them back in this triggerpostun script
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-init \
    voms-proxy-init %{_bindir}/voms-proxy-init2 50 \
    --slave %{_mandir}/man1/voms-proxy-init.1.gz voms-proxy-init-man \
    %{_mandir}/man1/voms-proxy-init2.1.gz
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-info \
    voms-proxy-info %{_bindir}/voms-proxy-info2 50 \
    --slave %{_mandir}/man1/voms-proxy-info.1.gz voms-proxy-info-man \
    %{_mandir}/man1/voms-proxy-info2.1.gz
%{_sbindir}/update-alternatives --install %{_bindir}/voms-proxy-destroy \
    voms-proxy-destroy %{_bindir}/voms-proxy-destroy2 50 \
    --slave %{_mandir}/man1/voms-proxy-destroy.1.gz voms-proxy-destroy-man \
    %{_mandir}/man1/voms-proxy-destroy2.1.gz

%files
%{_libdir}/libvomsapi.so.1*
%dir %{_sysconfdir}/grid-security
%dir %{_sysconfdir}/grid-security/vomsdir
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/vomses.template
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/AUTHORS
%doc %{_pkgdocdir}/README.md
%{!?_licensedir: %doc %{_pkgdocdir}/LICENSE}
%{?_licensedir: %license LICENSE}

%files devel
%{_libdir}/libvomsapi.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}-2.0.pc
%{_datadir}/aclocal/%{name}.m4
%{_mandir}/man3/*

%files doc
%doc %{_pkgdocdir}/AUTHORS
%doc %{_pkgdocdir}/VOMS_C_API
%doc %{_pkgdocdir}/VOMS_CC_API
%{!?_licensedir: %doc %{_pkgdocdir}/LICENSE}
%{?_licensedir: %license LICENSE}

%files clients-cpp
%{_bindir}/voms-proxy-destroy2
%{_bindir}/voms-proxy-info2
%{_bindir}/voms-proxy-init2
%{_bindir}/voms-proxy-fake
%{_bindir}/voms-proxy-list
%ghost %{_bindir}/voms-proxy-destroy
%ghost %{_bindir}/voms-proxy-info
%ghost %{_bindir}/voms-proxy-init
%{_mandir}/man1/voms-proxy-destroy2.1*
%{_mandir}/man1/voms-proxy-info2.1*
%{_mandir}/man1/voms-proxy-init2.1*
%{_mandir}/man1/voms-proxy-fake.1*
%{_mandir}/man1/voms-proxy-list.1*
%ghost %{_mandir}/man1/voms-proxy-destroy.1*
%ghost %{_mandir}/man1/voms-proxy-info.1*
%ghost %{_mandir}/man1/voms-proxy-init.1*

%files server
%{_sbindir}/%{name}
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(-,voms,voms) %dir %{_sysconfdir}/%{name}
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
* Wed Mar 18 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.12-3
- Rename client package and make voms-clients a virtual provides

* Wed Jan 21 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.12-2
- Rebuild for gsoap 2.8.21 (Fedora 22)
- Implement updated license packaging guidelines

* Mon Nov 17 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.12-1
- Update to version 2.0.12
- Drop patches voms-gsoap.patch, voms-sha2-proxy.patch and voms-strndup.patch
  (accepted upstream)
- Add alternatives to the client package to allow parallel installation of
  the java implementation of the client tools

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 13 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-9
- Rebuild properly

* Sun Jul 13 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-8
- Rebuild for gsoap 2.8.17 (Fedora 22)

* Wed Jul 02 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-7
- Update the gsoap patch

* Thu Jun 26 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-6
- Clean up SHA2 patch

* Thu Jun 26 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-5
- Fix compilation problems when strndup is already defined

* Thu Jun 26 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.11-4
- Patch that fixes a stack smash when SHA2 certificates are used

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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

* Tue Feb 12 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.10-1
- Update to version 2.0.10

* Tue Nov 27 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.9-1
- Update to version 2.0.9
- Add Build Requires for texlive 2012 (Fedora 18+)

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
