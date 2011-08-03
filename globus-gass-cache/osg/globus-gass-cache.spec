%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64pthr
%else
%global flavor gcc32pthr
%endif

Name:		globus-gass-cache
%global _name %(tr - _ <<< %{name})
Version:	5.4
Release:	5%{?dist}
Summary:	Globus Toolkit - Globus Gass Cache

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.0/installers/src/gt5.0.0-all-source-installer.tar.bz2
#		tar -jxf gt5.0.0-all-source-installer.tar.bz2
#		mv gt5.0.0-all-source-installer/source-trees/gass/cache/source globus_gass_cache-5.4
#		cp -p gt5.0.0-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gass_cache-5.4
#		tar -zcf globus_gass_cache-5.4.tar.gz globus_gass_cache-5.4
Source:		%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GRIDFTP
#		PATH_MAX should not be defined in installed headers:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6827
Patch0:		%{name}.patch
Patch1:         sprintf_n.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-openssl%{?_isa} >= 1
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-common-devel%{?_isa} >= 3
BuildRequires:	globus-openssl-devel%{?_isa} >= 1
BuildRequires:	globus-core%{?_isa} >= 4

%package devel
Summary:	Globus Toolkit - Globus Gass Cache Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-common-devel%{?_isa} >= 3
Requires:	globus-openssl-devel%{?_isa} >= 1
Requires:	globus-core%{?_isa} >= 4

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus Gass Cache

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Globus Gass Cache Development Files

%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1
%patch1 -p0

%build
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

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor}

make %{?_smp_mflags}

%install
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

%changelog
* Mon Aug 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 5.4-5
- Avoid invalid sprintf writes in x86.

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.4-4
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.4-2
- Update to Globus Toolkit 5.0.0

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.4-1
- Autogenerated
