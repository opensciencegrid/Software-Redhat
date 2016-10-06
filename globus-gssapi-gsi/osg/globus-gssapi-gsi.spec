%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gssapi-gsi
%global _name %(tr - _ <<< %{name})
Version:	12.1
Release:	1.1%{?dist}
Summary:	Globus Toolkit - GSSAPI library

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://toolkit.globus.org/
Source:		http://toolkit.globus.org/ftppub/gt6/packages/%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GSIC
Patch1:         disable-sslv3.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	globus-common-devel >= 15
BuildRequires:	globus-openssl-module-devel >= 3
BuildRequires:	globus-gsi-openssl-error-devel >= 2
BuildRequires:	globus-gsi-cert-utils-devel >= 8
BuildRequires:	globus-gsi-credential-devel >= 5
BuildRequires:	globus-gsi-callback-devel >= 4
BuildRequires:	globus-gsi-proxy-core-devel >= 6
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	openssl-devel
BuildRequires:	libtool-ltdl-devel
BuildRequires:	doxygen
#		Additional requirements for make check
BuildRequires:	openssl

%package devel
Summary:	Globus Toolkit - GSSAPI library Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-common-devel%{?_isa} >= 15
Requires:	globus-openssl-module-devel%{?_isa} >= 3
Requires:	globus-gsi-openssl-error-devel%{?_isa} >= 2
Requires:	globus-gsi-cert-utils-devel%{?_isa} >= 8
Requires:	globus-gsi-credential-devel%{?_isa} >= 5
Requires:	globus-gsi-callback-devel%{?_isa} >= 4
Requires:	globus-gsi-proxy-core-devel%{?_isa} >= 6
Requires:	globus-gsi-sysconfig-devel%{?_isa} >= 5
Requires:	openssl-devel%{?_isa}

%package doc
Summary:	Globus Toolkit - GSSAPI library Documentation Files
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
GSSAPI library

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
GSSAPI library Development Files

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
GSSAPI library Documentation Files

%prep
%setup -q -n %{_name}-%{version}
%patch1 -p1

%build
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

%configure --disable-static \
	   --includedir='${prefix}/include/globus' \
	   --libexecdir='${datadir}/globus' \
	   --docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC \(.*-shared\) !CC \\\${wl}--as-needed \1 !' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Remove license file from pkgdocdir if licensedir is used
%{?_licensedir: rm %{buildroot}%{_pkgdocdir}/GLOBUS_LICENSE}

%check
make %{?_smp_mflags} check VERBOSE=1

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libglobus_gssapi_gsi.so.*
%dir %{_sysconfdir}/grid-security
%config(noreplace) %{_sysconfdir}/grid-security/gsi.conf
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%files devel
%{_includedir}/globus/*
%{_libdir}/libglobus_gssapi_gsi.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%changelog
* Thu Oct 06 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 12.1-1.1
- Add patch to disable SSLv3 by default (SOFTWARE-2471)

* Fri May 06 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.1-1
- GT6 update: Change default host verification mode to strict

* Mon May 02 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.29-1
- GT6 update: Add support for certificates without a CN

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 11.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.26-1
- GT6 update
- Fix FORCE_TLS setting to allow TLSv1.1 and TLS1.2, not just TLSv1.0

* Wed Jan 13 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.25-1
- GT6 update: support loading mutiple extra CA certs

* Thu Dec 10 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.24-1
- GT6 update: Don't call SSLv3_method unless it is available

* Wed Sep 09 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.22-1
- GT6 update: GT-627: gss_import_cred crash
- Enable checks on EPEL6 ppc64 - no longer fails with above fix

* Wed Jul 29 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.20-1
- GT6 update
- GT-614: GLOBUS_GSS_C_NT_HOST_IP doesn't allow host-only imports and
  comparisons

* Sat Jun 20 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.19-1
- GT6 update (export config file values into environment if not set already)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.18-1
- GT6 update (Change the name compatibility mode in gsi.conf to HYBRID to
  match the behavior in 11.14 and earlier. Also some test fixes.)

* Fri May 29 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.16-1
- GT6-update (SSL cipher configuration)

* Fri Jan 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.14-2
- Implement updated license packaging guidelines

* Thu Nov 13 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.14-1
- GT6 update
- Drop patch globus-gssapi-gsi-doxygen.patch (fixed upstream)

* Mon Oct 27 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.13-1
- GT6 update
- Update patch globus-gssapi-gsi-doxygen.patch

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 11.12-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata
- Enable checks
- Disable checks on EPEL6 ppc64

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Brent Baude <baude@us.ibm.com> - 10.10-3
- Replace arch def of ppc64 with power64 macro for ppc64le enablement

* Thu Dec 05 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.10-2
- Remove directory man page

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.10-1
- Update to Globus Toolkit 5.2.5
- Drop patch globus-gssapi-gsi-doxygen.patch (fixed upstream)
- Remove obsolete workaround for broken RHEL 5 epstopdf

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.7-5
- Implement updated packaging guidelines

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.7-4
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.7-2
- Add build requires for TexLive 2012

* Sun Jul 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.7-1
- Update to Globus Toolkit 5.2.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.6-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gssapi-gsi-deps.patch, globus-gssapi-gsi-format.patch
  and globus-gssapi-gsi-doxygen.patch (fixed upstream)

* Mon Jan 23 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-2
- Fix broken links in README file

* Wed Dec 14 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.2-1
- Update to Globus Toolkit 5.2.0

* Fri Jun 03 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.8-1
- Update to Globus Toolkit 5.0.4

* Sun Apr 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.6-2
- Add README file

* Fri Feb 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.6-1
- Update to Globus Toolkit 5.0.3

* Fri Feb 11 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.5-1
- Update to Globus Toolkit 5.0.1
- Drop patch globus-gssapi-gsi-openssl.patch (fixed upstream)

* Mon Feb 08 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.0-2
- Update openssl 1.0.0 patch based on RIC-29 branch in upstream CVS

* Fri Jan 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.0-1
- Update to Globus Toolkit 5.0.0

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.9-5
- rebuilt with new openssl

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-4
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Wed Jun 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-3
- Update to official Fedora Globus packaging guidelines

* Tue May 12 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-2
- Change the License tag to take the library/ssl_locl.h file into account

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-0.3
- Adapt to updated GPT package

* Wed Oct 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-0.1
- Autogenerated
