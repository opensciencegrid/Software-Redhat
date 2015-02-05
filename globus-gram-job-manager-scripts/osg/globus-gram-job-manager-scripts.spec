%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gram-job-manager-scripts
%global _name %(tr - _ <<< %{name})
Version:	5.0
Release:	1.1%{?dist}
Summary:	Globus Toolkit - GRAM Job ManagerScripts

Group:		Applications/Internet
BuildArch:	noarch
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.5/packages/src/%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GRAM5

# OSG-specific patches
Patch0:         gratia.patch
Patch1:         osg-environment.patch
Patch2:         osg-path.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common-progs >= 14
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8

%package doc
Summary:	Globus Toolkit - GRAM Job ManagerScripts Documentation Files
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
GRAM Job ManagerScripts

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
GRAM Job ManagerScripts Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%patch0 -p0
%patch1 -p0
%patch2 -p0

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

%configure --disable-static --without-flavor \
	   --with-docdir=%{_pkgdocdir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

GLOBUSPACKAGEDIR=%{buildroot}%{_datadir}/globus/packages

# Move license file to main package
grep GLOBUS_LICENSE $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/noflavor_rtl.filelist
sed /GLOBUS_LICENSE/d -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Move client man pages to progs package 
grep '.[18]$' $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/noflavor_pgm.filelist
sed '/.[18]$/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_rtl.filelist \
  | sed -e 's!/man/.*!&*!' -e s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf %{buildroot}

%files -f package.filelist
%dir %{_datadir}/globus/packages/%{_name}
%dir %{perl_vendorlib}/Globus
%dir %{perl_vendorlib}/Globus/GRAM
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README

%files doc -f package-doc.filelist
%dir %{_pkgdocdir}/perl
%dir %{_pkgdocdir}/perl/Globus
%dir %{_pkgdocdir}/perl/Globus/GRAM

%changelog
* Thu Dec 12 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 5.0-1.1.osg
- Merge OSG changes

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0-1
- Update to Globus Toolkit 5.2.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-9
- Implement updated packaging guidelines

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.2-8
- Perl 5.18 rebuild

* Thu May 23 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-7
- Specfile clean-up

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-5
- Specfile clean-up

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 4.2-3
- Perl 5.16 rebuild

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-2
- Fix broken links in README file

* Mon Dec 19 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 4.1-3.1.osg
- Merge OSG changes
- Remove GRAM-278.diff, incorporated upstream

* Sat Dec 17 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-1
- Post-release update from upstream

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.1-1
- Update to Globus Toolkit 5.2.0

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 4.1-3
- Update for 5.2.0 release

* Mon Dec 05 2011 Joseph Bester <bester@mcs.anl.gov> - 4.1-2
- Last sync prior to 5.2.0

* Mon Nov 28 2011 Joseph Bester <bester@mcs.anl.gov> - 4.1-1
- GRAM-278: GASS cache location not set in the perl environment

* Tue Nov 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.0-7.osg
- Switch to fix for GRAM-278 from Globus.

* Mon Nov 14 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.0-6.osg
- Properly configure the GASS cache from the job manager.

* Mon Oct 24 2011 Alain Roy <roy@cs.wisc.edu> - 4.0-4.osg
- Updated pathnames in osg-environment.patch

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 4.0-3
- Add explicit dependencies on >= 5.2 libraries

* Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 4.0-2
- Update for 5.1.2 release

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.1-3.osg
- Small syntax error in the default path patch.

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.1-2.osg
- Porting OSG patches to GT5.2.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.12-3
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.12-2
- Perl 5.14 mass rebuild

* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.12-1
- Update to Globus Toolkit 5.0.4

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.11-3
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.11-1
- Update to Globus Toolkit 5.0.2

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.5-2
- Mass rebuild with perl-5.12.0

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.4-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.7-1
- Autogenerated
