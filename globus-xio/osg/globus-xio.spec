%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64pthr
%else
%global flavor gcc32pthr
%endif

Name:		globus-xio
%global _name %(tr - _ <<< %{name})
Version:	2.8
Release:	5%{?dist}
Summary:	Globus Toolkit - Globus XIO Framework

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.0/installers/src/gt5.0.0-all-source-installer.tar.bz2
#		tar -jxf gt5.0.0-all-source-installer.tar.bz2
#		mv gt5.0.0-all-source-installer/source-trees/xio/src globus_xio-2.8
#		cp -p gt5.0.0-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_xio-2.8
#		tar -zcf globus_xio-2.8.tar.gz globus_xio-2.8
Source:		%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-XIO
#		This is a workaround for the broken epstopdf script in RHEL5
#		See: https://bugzilla.redhat.com/show_bug.cgi?id=450388
Source9:	epstopdf-2.9.5gw
#		Remove some doxygen warnings:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6585
Patch0:		%{name}-doxygen.patch
#		Bad version information:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6584
Patch1:		%{name}-bad-age.patch
#		Dereferencing of type-punned pointers:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6605
Patch2:		%{name}-type-punned-pointer.patch
#		Fixes for mingw compilation:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6742
Patch3:		%{name}-mingw.patch
#		Fix format errors:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6757
Patch4:		%{name}-format.patch

Patch5:         timeout_close.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-common-devel%{?_isa} >= 4
BuildRequires:	globus-core%{?_isa} >= 4
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	ghostscript
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 5
BuildRequires:	tex(latex)
%else
BuildRequires:	tetex-latex
%endif

%package devel
Summary:	Globus Toolkit - Globus XIO Framework Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-common-devel%{?_isa} >= 4
Requires:	globus-core%{?_isa} >= 4

%package doc
Summary:	Globus Toolkit - Globus XIO Framework Documentation Files
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
Globus XIO Framework

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Globus XIO Framework Development Files

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
Globus XIO Framework Documentation Files

%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0

%if "%{rhel}" == "5"
mkdir bin
install %{SOURCE9} bin/epstopdf
%endif

%build
%if "%{rhel}" == "5"
export PATH=$PWD/bin:$PATH
%endif

# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

# Remove flavor tags
for f in `find . -name Makefile.am` ; do
  sed -e 's!^flavorinclude_HEADERS!include_HEADERS!' \
      -e 's!\(lib[a-zA-Z_]*\)_$(GLOBUS_FLAVOR_NAME)\.la!\1.la!g' \
      -e 's!^\(lib[a-zA-Z_]*\)___GLOBUS_FLAVOR_NAME__la_!\1_la_!' -i $f
done
sed -e "s!<With_Flavors!<With_Flavors ColocateLibraries=\"no\"!" \
  -i pkgdata/pkg_data_src.gpt.in
sed -e 's!\(lib[a-zA-Z_${}]*\)_${GLOBUS_FLAVOR_NAME}\.la!\1.la!g' \
  -i configure.in

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} --enable-doxygen

make %{?_smp_mflags}

%install
%if "%{rhel}" == "5"
export PATH=$PWD/bin:$PATH
%endif

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Remove libtool archives (.la files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist

# Remove static libraries (.a files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.a' -exec rm -v '{}' \;
sed '/lib.*\.a$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Generate pkg-config file from GPT metadata
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
%{_datadir}/globus/globus-gpt2pkg-config pkgdata/pkg_data_%{flavor}_dev.gpt > \
  $RPM_BUILD_ROOT%{_libdir}/pkgconfig/%{name}.pc

# Move documentation to default RPM location
mv $RPM_BUILD_ROOT%{_docdir}/%{_name} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
sed s!doc/%{_name}!doc/%{name}-%{version}! \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Fix doxygen glitches
for f in $RPM_BUILD_ROOT%{_mandir}/man3/globus_xio_driver.3 \
	 $RPM_BUILD_ROOT%{_mandir}/man3/GLOBUS_XIO_API_ASSIST.3 ; do
  sed 's/P\.RS/P\n.RS/' -i $f
done

# Remove unwanted documentation (needed for RHEL4)
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*_%{_name}-%{version}_*.3
sed -e '/_%{_name}-%{version}_.*\.3/d' \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Install license file
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 -p GLOBUS_LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Install README file
install -m 644 -p %{SOURCE8} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/GLOBUS_LICENSE
%doc %{_docdir}/%{name}-%{version}/README

%files -f package-devel.filelist devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc

%files -f package-doc.filelist doc
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/html

%changelog
* Mon Aug 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 2.8-5
- Automatically timeout the close operation in case if things get deadlocked there.

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.8-4
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.8-2
- Update to Globus Toolkit 5.0.0

* Wed Jul 29 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.8-1
- Update to upstream update release 2.8

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-5
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Wed Jun 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-4
- Update to official Fedora Globus packaging guidelines

* Mon Apr 27 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-3
- Rebuild with updated libtool

* Mon Apr 20 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-2
- Put GLOBUS_LICENSE file in extracted source tarball

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-0.3
- Adapt to updated GPT package

* Mon Oct 20 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.7-0.1
- Autogenerated
