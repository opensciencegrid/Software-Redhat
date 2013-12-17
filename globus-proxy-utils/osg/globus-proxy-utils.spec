%ifarch aarch64 alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-proxy-utils
%global _name %(tr - _ <<< %{name})
Version:	5.2
Release:	1.1%{?dist}
Summary:	Globus Toolkit - Globus GSI Proxy Utility Programs

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.5/packages/src/%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GSIC
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-gsi-credential%{?_isa} >= 5
Requires:	globus-gsi-callback%{?_isa} >= 4
Requires:	globus-openssl-module%{?_isa} >= 3
Requires:	globus-gss-assist%{?_isa} >= 8
Requires:	globus-gsi-openssl-error%{?_isa} >= 2
Requires:	globus-gsi-proxy-core%{?_isa} >= 6
Requires:	globus-common%{?_isa} >= 14
Requires:	globus-gsi-sysconfig%{?_isa} >= 5
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8
BuildRequires:	globus-gsi-proxy-ssl-devel >= 4
BuildRequires:	globus-gsi-credential-devel >= 5
BuildRequires:	globus-gsi-callback-devel >= 4
BuildRequires:	globus-openssl-module-devel >= 3
BuildRequires:	globus-gss-assist-devel >= 8
BuildRequires:	globus-gsi-openssl-error-devel >= 2
BuildRequires:	globus-gsi-proxy-core-devel >= 6
BuildRequires:	globus-gsi-cert-utils-devel >= 8
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	openssl-devel

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus GSI Proxy Utility Programs

%prep
%setup -q -n %{_name}-%{version}

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

unset GLOBUS_LOCATION
unset GPT_LOCATION
%{_datadir}/globus/globus-bootstrap.sh

%configure --disable-static --with-flavor=%{flavor} \
	   --with-docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

GLOBUSPACKAGEDIR=%{buildroot}%{_datadir}/globus/packages

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' >> package.filelist

%clean
rm -rf %{buildroot}

%files -f package.filelist
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README

%changelog
* Mon Dec 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 5.2-1.1
- Bump to rebuild with OpenSSL 1.0.0

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.2-1
- Update to Globus Toolkit 5.2.5
- Drop patch globus-proxy-utils-1024-bits.patch (fixed upstream)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-7
- Implement updated packaging guidelines

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-6
- Add aarch64 to the list of 64 bit platforms
- Use 1024 bits as default for generated proxies

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-4
- Specfile clean-up

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-2
- Fix broken links in README file

* Wed Dec 14 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-1
- Update to Globus Toolkit 5.2.0
- Drop patch globus-proxy-utils-mingw.patch (fixed upstream)

* Fri Jun 03 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.10-1
- Update to Globus Toolkit 5.0.4

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.9-3
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.9-1
- Update to Globus Toolkit 5.0.2
- Drop patch globus-proxy-utils-oid.patch (fixed upstream)

* Mon May 31 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.7-2
- Fix OID registration pollution

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.7-1
- Update to Globus Toolkit 5.0.1
- Drop patches globus-proxy-utils-ldflag-overwrt.patch and
  globus-proxy-utils-deps.patch (fixed upstream)

* Fri Jan 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.5-1
- Update to Globus Toolkit 5.0.0

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.5-4
- rebuilt with new openssl

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-3
- Add instruction set architecture (isa) tags

* Wed Jun 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.4
- Add s390x to the list of 64 bit platforms

* Tue Dec 30 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.3
- Adapt to updated GPT package

* Wed Oct 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.1-0.1
- Autogenerated
