%ifarch aarch64 alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gram-client
%global _name %(tr - _ <<< %{name})
Version:	12.5
Release:	1%{?dist}
Summary:	Globus Toolkit - GRAM Client Library

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.5/updates/src/%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GRAM5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-gram-protocol%{?_isa} >= 11
Requires:	globus-common%{?_isa} >= 14
Requires:	globus-gss-assist%{?_isa} >= 8
Requires:	globus-rsl%{?_isa} >= 9
Requires:	globus-io%{?_isa} >= 9
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8
BuildRequires:	globus-gram-protocol-devel >= 11
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-gss-assist-devel >= 8
BuildRequires:	globus-rsl-devel >= 9
BuildRequires:	globus-io-devel >= 9
BuildRequires:	globus-gram-protocol-doc >= 11
BuildRequires:	globus-common-doc >= 14
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	ghostscript
BuildRequires:	tex(latex)
%if %{?fedora}%{!?fedora:0} >= 18 || %{?rhel}%{!?rhel:0} >= 7
BuildRequires:	tex(fullpage.sty)
BuildRequires:	tex(multirow.sty)
BuildRequires:	tex(sectsty.sty)
BuildRequires:	tex(tocloft.sty)
BuildRequires:	tex(xtab.sty)
BuildRequires:	tex-ec
BuildRequires:	tex-courier
BuildRequires:	tex-helvetic
BuildRequires:	tex-times
BuildRequires:	tex-symbol
BuildRequires:	tex-rsfs
%endif

%package devel
Summary:	Globus Toolkit - GRAM Client Library Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-gram-protocol-devel%{?_isa} >= 11
Requires:	globus-common-devel%{?_isa} >= 14
Requires:	globus-gss-assist-devel%{?_isa} >= 8
Requires:	globus-rsl-devel%{?_isa} >= 9
Requires:	globus-io-devel%{?_isa} >= 9
Requires:	globus-core%{?_isa} >= 8

%package doc
Summary:	Globus Toolkit - GRAM Client Library Documentation Files
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Requires:	%{name} = %{version}-%{release}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
GRAM Client Library

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
GRAM Client Library Development Files

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
GRAM Client Library Documentation Files

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
	   --enable-doxygen --with-docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

GLOBUSPACKAGEDIR=%{buildroot}%{_datadir}/globus/packages

# Remove libtool archives (.la files)
find %{buildroot}%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Move license file to main package
grep GLOBUS_LICENSE $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist
sed /GLOBUS_LICENSE/d -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f package.filelist
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README

%files -f package-devel.filelist devel

%files -f package-doc.filelist doc
%dir %{_pkgdocdir}/html

%changelog
* Fri Dec 12 2014 Carl Edquist <edquist@cs.wisc.edu> - 12.5-1
- Update to 12.5 (SOFTWARE-1724)
  - GT-567: Remove requirement that GRAM5 use SSLv3
  - Fix latex dependencies for newer fedora/rhel

* Sat Oct 26 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.4-8
- Remove obsolete workaround for broken RHEL 5 epstopdf

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.4-6
- Implement updated packaging guidelines

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.4-5
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.4-3
- Add build requires for TexLive 2012

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.4-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gram-client-deps.patch (fixed upstream)

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.3-2
- Fix broken links in README file

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 12.3-1
- Update to Globus Toolkit 5.2.0
- Drop patch globus-gram-client-doxygen.patch (fixed upstream)

* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.4-4
- Fix doxygen markup

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.4-3
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.4-1
- Update to Globus Toolkit 5.0.2

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.3-1
- Update to Globus Toolkit 5.0.1
- Drop patch globus-gram-client-typo.patch (fixed upstream)

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 9.1-1
- Update to Globus Toolkit 5.0.0

* Tue Jul 28 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.2-1
- Autogenerated
