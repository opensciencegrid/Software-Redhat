%ifarch aarch64 alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?_initddir: %global _initddir %{_initrddir}}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-scheduler-event-generator
%global _name %(tr - _ <<< %{name})
Version:	4.7
Release:	6.1%{?dist}
Summary:	Globus Toolkit - Scheduler Event Generator

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.3/packages/src/%{_name}-%{version}.tar.gz
Source1:	%{name}
#		README file
Source8:	GLOBUS-GRAM5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common%{?_isa} >= 14
Requires:	globus-xio-gsi-driver%{?_isa} >= 2
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8
BuildRequires:	globus-gram-protocol-devel >= 11
BuildRequires:	globus-common-devel >= 14
BuildRequires:	globus-xio-gsi-driver-devel >= 2
BuildRequires:	globus-xio-devel >= 3
%if %{?fedora}%{!?fedora:0} >= 4 || %{?rhel}%{!?rhel:0} >= 5
BuildRequires:	libtool-ltdl-devel
%else
BuildRequires:	libtool
%endif
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

%package progs
Summary:	Globus Toolkit - Scheduler Event Generator Programs
Group:		Applications/Internet
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-common%{?_isa} >= 14
Requires:	globus-xio-gsi-driver%{?_isa} >= 2
Requires:	globus-xio%{?_isa} >= 3
Requires:	globus-common-progs >= 14
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%package devel
Summary:	Globus Toolkit - Scheduler Event Generator Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-gram-protocol-devel%{?_isa} >= 11
Requires:	globus-common-devel%{?_isa} >= 14
Requires:	globus-xio-gsi-driver-devel%{?_isa} >= 2
Requires:	globus-xio-devel%{?_isa} >= 3
Requires:	globus-core%{?_isa} >= 8

%package doc
Summary:	Globus Toolkit - Scheduler Event Generator Documentation Files
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
Scheduler Event Generator

%description progs
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-progs package contains:
Scheduler Event Generator Programs

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
Scheduler Event Generator Development Files

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
Scheduler Event Generator Documentation Files

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
	   --enable-doxygen --with-docdir=%{_pkgdocdir} \
	   --with-initscript-config-path=%{_sysconfdir}/sysconfig/%{name} \
	   --with-lockfile-path='${localstatedir}/lock/subsys/%{name}'

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

# Remove start-up scripts
rm -rf %{buildroot}%{_sysconfdir}/init.d
sed '/init\.d/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist

# Install start-up scripts
mkdir -p %{buildroot}%{_initddir}
install -p %{SOURCE1} %{buildroot}%{_initddir}

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | sed -e s!^!%{_prefix}! \
	-e 's!%{_prefix}%{_sysconfdir}!%config(noreplace) %{_sysconfdir}!' \
  > package-progs.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  | sed s!^!%{_prefix}! > package-devel.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post progs
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi

%preun progs
if [ $1 -eq 0 ]; then
    /sbin/chkconfig --del %{name}
    /sbin/service %{name} stop > /dev/null 2>&1 || :
fi

%postun progs
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%files -f package.filelist
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README

%files -f package-progs.filelist progs
%{_initddir}/%{name}

%files -f package-devel.filelist devel

%files -f package-doc.filelist doc
%dir %{_pkgdocdir}/html

%changelog
* Fri Jan 10 2014 Matyas Selmeci <matyas@cs.wisc.edu> 4.7-6.1.osg
- Fix init script chkconfig priorities to run after netfs and autofs (SOFTWARE-1250)

* Sat Oct 26 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.7-6
- Remove obsolete workaround for broken RHEL 5 epstopdf

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.7-4
- Implement updated packaging guidelines

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.7-3
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.7-1
- Update to Globus Toolkit 5.2.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.6-1
- Update to Globus Toolkit 5.2.1

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.4-2
- Fix broken links in README file

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.4-1
- Update to Globus Toolkit 5.2.0
- Drop patch globus-scheduler-event-generator.patch (fixed upstream)

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.1-4
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.1-2
- Update to Globus Toolkit 5.0.0

* Wed Jul 29 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.1-1
- Autogenerated
