%global _hardened_build 1

%if %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%{!?_unitdir: %global _unitdir /usr/lib/systemd/system}
%else
%global use_systemd 0
%endif

%global _rc rc2

Name:		voms
Version:	2.1.0
Release:	0.14.%{_rc}.7%{?dist}
Summary:	Virtual Organization Membership Service

License:	ASL 2.0
URL:		https://wiki.italiangrid.it/VOMS
Source0:	https://github.com/italiangrid/%{name}/archive/v%{version}-%{_rc}/%{name}-%{version}-%{_rc}.tar.gz
#		Post-install setup instructions:
Source1:	%{name}.INSTALL
#		systemd unit file:
Source2:	%{name}@.service

#		Fix for GCC 7
#		https://github.com/italiangrid/voms/pull/56
Patch1:		%{name}-gcc7.patch
#		Create RFC proxies as default
#		https://github.com/italiangrid/voms/pull/57
Patch2:		%{name}-default-proxyver.patch
#		Don't use macros in AC_CHECK_LIB
#		https://github.com/italiangrid/voms/pull/58
Patch3:		%{name}-lib-check-no-macro.patch
#		Change default proxy cert key length to 2048 bits
#		https://github.com/italiangrid/voms/pull/75
Patch6:		%{name}-change-default-proxy-cert-key-length-to-2048-bits.patch

Patch7:          mariadb-innodb.patch
Patch10:         sw3123-voms-proxy-direct.patch
Patch11:         4882-voms_install_db-cert-parsing.patch
Patch12:         Set-default-key-size-to-2048-bits-in-voms-proxy-dire.patch
Patch13:         116-better-ac-signature-error-message.patch

BuildRequires:	gcc-c++
BuildRequires:	openssl-devel
BuildRequires:	expat-devel
BuildRequires:	gsoap-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	libxslt
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
%if %{use_systemd}
BuildRequires:	systemd
%endif
  
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
BuildArch:	noarch

%description doc
Documentation for the Virtual Organization Membership Service.

%package clients-cpp
Summary:	Virtual Organization Membership Service Clients
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
Requires:	%{name}%{?_isa} = %{version}-%{release}

Requires(pre):		shadow-utils
%if %{use_systemd}
%{?systemd_requires}
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif

%description server
The Virtual Organization Membership Service (VOMS) is an attribute authority
which serves as central repository for VO user authorization information,
providing support for sorting users into group hierarchies, keeping track of
their roles and other attributes in order to issue trusted attribute
certificates and SAML assertions used in the Grid environment for
authorization purposes.

This package provides the VOMS service.

%prep
%setup -q -n %{name}-%{version}-%{_rc}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch6 -p1

%if %{?rhel}%{!?rhel:0} >= 7
%patch7 -p1
%endif

%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

install -m 644 -p %{SOURCE1} README.Fedora

%build
./autogen.sh

%configure --disable-static --enable-docs --disable-parser-gen

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*.la

%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -m 644 -p %SOURCE2 %{buildroot}%{_unitdir}
rm %{buildroot}%{_initrddir}/%{name}
%else
# Turn off default enabling of the service
sed -e 's/\(chkconfig: \)\w*/\1-/' \
    -e '/Default-Start/d' \
    -e 's/\(Default-Stop:\s*\).*/\10 1 2 3 4 5 6/' \
    -i %{buildroot}%{_initrddir}/%{name}
%endif

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

%ldconfig_scriptlets

%posttrans
# Recover /etc/vomses...
if [ -r %{_sysconfdir}/vomses.rpmsave -a ! -r %{_sysconfdir}/vomses ] ; then
   mv %{_sysconfdir}/vomses.rpmsave %{_sysconfdir}/vomses
fi

%pre server
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} \
    -d %{_sysconfdir}/%{name} -s /sbin/nologin -c "VOMS Server Account" %{name}

%if %{use_systemd}
# Remove old init config when systemd is used
/sbin/service voms stop >/dev/null 2>&1 || :
/sbin/chkconfig --del voms >/dev/null 2>&1 || :
%endif

%if %{use_systemd}

%post server
if [ $1 -eq 1 ] ; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun server
if [ $1 -eq 0 ] ; then
    for INSTANCE in `systemctl | grep %{name}@ | awk '{print $1;}'`; do
	systemctl --no-reload disable $INSTANCE > /dev/null 2>&1 || :
	systemctl stop $INSTANCE > /dev/null 2>&1 || :
    done
fi

%postun server
if [ $1 -ge 1 ] ; then
    systemctl daemon-reload >/dev/null 2>&1 || :
    for INSTANCE in `systemctl | grep %{name}@ | awk '{print $1;}'`; do
	systemctl try-restart $INSTANCE >/dev/null 2>&1 || :
    done
fi

%else

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

%endif

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
%{_bindir}/voms-proxy-direct
%{_bindir}/voms-proxy-list
%{_bindir}/voms-verify
%ghost %{_bindir}/voms-proxy-destroy
%ghost %{_bindir}/voms-proxy-info
%ghost %{_bindir}/voms-proxy-init
%{_mandir}/man1/voms-proxy-destroy2.1*
%{_mandir}/man1/voms-proxy-info2.1*
%{_mandir}/man1/voms-proxy-init2.1*
%{_mandir}/man1/voms-proxy-fake.1*
%{_mandir}/man1/voms-proxy-direct.1*
%{_mandir}/man1/voms-proxy-list.1*
%ghost %{_mandir}/man1/voms-proxy-destroy.1*
%ghost %{_mandir}/man1/voms-proxy-info.1*
%ghost %{_mandir}/man1/voms-proxy-init.1*

%files server
%{_sbindir}/%{name}
%if %{use_systemd}
%{_unitdir}/%{name}@.service
%else
%{_initrddir}/%{name}
%endif
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
* Thu Apr 27 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.1.0-0.14.rc2.6
- Add 116-better-ac-signature-error-message.patch (SOFTWARE-5560)

* Mon Nov 08 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.1.0-0.14.rc2.5
- Increase default key size to 2048 bits in voms-proxy-direct (SOFTWARE-4889)
  - Add Set-default-key-size-to-2048-bits-in-voms-proxy-dire.patch

* Mon Nov 01 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.1.0-0.14.rc2.4
- Fix voms_install_db cert parsing to deal with OpenSSL 1.1+ format and "Let's Encrypt" (SOFTWARE-4882)
  - Add 4882-voms_install_db-cert-parsing.patch

* Tue Jun 29 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.1.0-0.14.rc2.2
- Reinstate /etc/sysconfig/voms (SOFTWARE-4577)

* Tue Apr 20 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.1.0-0.14.rc2.1
- Update to 2.1.0-rc2

* Mon Apr 19 2021 Carl Edquist <edquist@cs.wisc.edu> - 2.1.0-0.14.rc1.1
- Merge out upstreamed OSG changes
- Bring voms-clients back into build (SOFTWARE-4577)

* Fri May 29 2020 Brian Lin <blin@cs.wisc.edu> - 2.1.0-0.14.rc0.1
- Merge in OSG changes

* Mon Dec 16 2019 Diego Davila <didavila@ucsd.edu> - 2.0.14-1.5
- Add patches to disable TLSv1 and TLSv1.1 connections and
- insecure ciphers (SOFTWARE-3879)

* Sat Aug 17 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.1.0-0.14.rc0
- Rebuild for gsoap 2.8.91 (Fedora 32)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.13.rc0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.12.rc0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 31 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.1.0-0.11.rc0
- Change default proxy cert key length to 2048 bits

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.10.rc0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 13 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0.14-1.4
- Add voms-proxy-direct (SOFTWARE-3123)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.9.rc0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.1.0-0.8.rc0
- Fix wsdl version detection

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.7.rc0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.1.0-0.6.rc0
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.5.rc0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Kalev Lember <klember@redhat.com> - 2.1.0-0.4.rc0
- Rebuilt for libgsoapssl++ soname bump

* Tue Jun 27 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.1.0-0.3.rc0
- Update the "check if NID is defined" patch
- Improve compatibility with the kerberos gssapi header file
- Rebuild for gsoap 2.8.48 (Fedora 27)

* Mon Feb 20 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0.14-1.3
- Add Validate-top-level-group-of-VOMS-attribute.patch (SOFTWARE-2593)

* Tue Feb 07 2017 Kalev Lember <klember@redhat.com> - 2.1.0-0.2.rc0
- Rebuilt for libgsoapssl++ soname bump

* Wed Feb 01 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.1.0-0.1.rc0
- Fix a few remaining OpenSSL 1.1 issues
- Fix a GCC 7 compiler error
- Create RFC proxies as default

* Wed Jan 25 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.1.0-0.rc0
- Update to version 2.1.0-rc0 (Port to OpenSSL 1.1)

* Thu Dec 22 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0.14-1.2
- Use upstream .service file

* Wed Dec 21 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0.14-1.1
- Merge OSG changes (SOFTWARE-2557)

* Mon Sep 19 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.0.14-2
- Rebuild for gsoap 2.8.35 (Fedora 26)

* Sun Sep 11 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.0.14-1
- Update to version 2.0.14

* Sun Aug 14 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 2.0.13-3
- Convert to systemd unit file (Fedora 25+)

* Tue Jul 05 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0.12-3.3
- Make RFC proxies by default (SOFTWARE-2381)

* Wed Jun 08 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0.12-3.2
- Replace init script with systemd service file on EL7 (SOFTWARE-2357)

* Tue Apr 19 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.13-2
- Rebuild for gsoap 2.8.30 (Fedora 25)

* Sat Feb 20 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.13-1
- Update to version 2.0.13
- Drop patches: voms-nossl3.patch, voms-tls1.patch, voms-gcc6.patch,
  voms-paren.patch, voms-comment-in-comment.patch and voms-doxygen.patch

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.12-7
- Disable SSLv3
- Fix compilation with gcc 6

* Fri Oct 16 2015 Carl Edquist <edquist@cs.wisc.edu> - 2.0.12-3.1
- Fix SQL syntax for mariadb in EL7 (SOFTWARE-1604)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.0.12-5
- Rebuild for gsoap 2.8.22 (Fedora 23)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.12-4
- Rebuilt for GCC 5 C++11 ABI change

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
