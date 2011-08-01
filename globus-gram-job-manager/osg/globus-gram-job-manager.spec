%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64pthr
%else
%global flavor gcc32pthr
%endif

Name:		globus-gram-job-manager
%global _name %(tr - _ <<< %{name})
Version:	10.70
%global setupversion 4.3
Release:	5%{?dist}
Summary:	Globus Toolkit - GRAM Jobmanager

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.4/installers/src/gt5.0.4-all-source-installer.tar.bz2
#		tar -jxf gt5.0.4-all-source-installer.tar.bz2
#		mv gt5.0.4-all-source-installer/source-trees/gram/jobmanager/source globus_gram_job_manager-10.70
#		cp -p gt5.0.4-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gram_job_manager-10.70
#		tar -zcf globus_gram_job_manager-10.70.tar.gz globus_gram_job_manager-10.70
Source:		%{_name}-%{version}.tar.gz
#		Source1 is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.4/installers/src/gt5.0.4-all-source-installer.tar.bz2
#		tar -jxf gt5.0.4-all-source-installer.tar.bz2
#		mv gt5.0.4-all-source-installer/source-trees/gram/jobmanager/setup/program globus_gram_job_manager_setup-4.3
#		cp -p gt5.0.4-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gram_job_manager_setup-4.3
#		tar -zcf globus_gram_job_manager_setup-4.3.tar.gz globus_gram_job_manager_setup-4.3
Source1:	%{_name}_setup-%{setupversion}.tar.gz
#		README file
Source8:	GLOBUS-GRAM5
#		Fixes for FHS installation:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6823
Patch0:		%{name}.patch
#		Fixes for FHS installation:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6824
Patch1:		%{name}-setup.patch
#		Undefined make variable:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6855
Patch2:		%{name}-undefined.patch
#		Using PATH_MAX is not portable:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6997
Patch3:		%{name}-pathmax.patch
#		Fix doxygen markup
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=7185
Patch4:		%{name}-doxygen.patch

Patch5:         logging_null.patch
Patch6:         double_lock.patch
Patch7:         close_deadlock.patch
Patch8:         job_status.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	%{name}-setup = %{setupversion}
Requires:	globus-common >= 11.6
Requires:	globus-xio-popen-driver%{?_isa} >= 0.7
Requires:	globus-libxml2%{?_isa}
Requires:	globus-gram-protocol >= 9
Requires:	globus-gram-job-manager-scripts
Requires:	globus-gass-copy-progs >= 2
Requires:	globus-proxy-utils
Requires:	globus-gass-cache-program >= 2
Requires:	globus-common-setup >= 2
Requires:	globus-gatekeeper-setup >= 2
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-scheduler-event-generator-devel%{?_isa} >= 1
BuildRequires:	globus-xio-popen-driver-devel%{?_isa} >= 0.7
BuildRequires:	globus-xio-devel%{?_isa} >= 2
BuildRequires:	globus-gss-assist-devel%{?_isa} >= 3
BuildRequires:	globus-core%{?_isa} >= 4
BuildRequires:	globus-gsi-sysconfig-devel%{?_isa} >= 1
BuildRequires:	globus-rsl-assist-devel%{?_isa} >= 2
BuildRequires:	globus-callout-devel%{?_isa}
BuildRequires:	globus-gram-job-manager-callout-error-devel%{?_isa}
BuildRequires:	globus-gram-protocol-devel%{?_isa} >= 9
BuildRequires:	globus-common-devel%{?_isa} >= 11.6
BuildRequires:	globus-usage-devel%{?_isa} >= 1
BuildRequires:	globus-rsl-devel%{?_isa} >= 3
BuildRequires:	globus-gass-cache-devel%{?_isa} >= 5
BuildRequires:	globus-libxml2-devel%{?_isa}
BuildRequires:	globus-gass-transfer-devel%{?_isa} >= 4
BuildRequires:	globus-gram-protocol-doc >= 9
BuildRequires:	globus-common-doc
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

%package doc
Summary:	Globus Toolkit - GRAM Jobmanager Documentation Files
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
GRAM Jobmanager
GRAM Job Manager Setup

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
GRAM Jobmanager Documentation Files

%prep
%setup -q -n %{_name}-%{version}
%setup -D -T -q -n %{_name}-%{version} -a 1
%patch0 -p1
cd %{_name}_setup-%{setupversion}
%patch1 -p1
cd -
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p1

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

sed 's!/share/globus_gram_job_manager/!/share/globus/!' \
  -i globus_gram_job_manager_validate.c

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} --enable-doxygen

make %{?_smp_mflags}

# setup package
cd %{_name}_setup-%{setupversion}

# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

%configure --without-flavor --enable-doxygen

make %{?_smp_mflags}

cd -

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# setup package
cd %{_name}_setup-%{setupversion}
make install DESTDIR=$RPM_BUILD_ROOT
cd -

# Register setup
perl -MGrid::GPT::Setup <<EOF
my \$metadata = new Grid::GPT::Setup(package_name => "%{_name}_setup",
				     globusdir => "$RPM_BUILD_ROOT%{_prefix}");
\$metadata->finish();
EOF

# These scripts are intended to be sourced, not executed
chmod 644 $RPM_BUILD_ROOT%{_datadir}/globus/globus-personal-gatekeeper-version.sh
chmod 644 $RPM_BUILD_ROOT%{_datadir}/globus/setup/setup-globus-gram-job-manager.pl

# Create the service setup directory
mkdir $RPM_BUILD_ROOT/%{_datadir}/globus/packages/setup/%{_name}_service_setup

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Move files into globus tree
mv $RPM_BUILD_ROOT%{_datadir}/%{_name}/* $RPM_BUILD_ROOT%{_datadir}/globus
rmdir $RPM_BUILD_ROOT%{_datadir}/%{_name}
sed s!share/%{_name}!share/globus! \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist

# Move client and server man pages to main package
grep '.[18]$' $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist
sed '/.[18]$/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Move documentation to default RPM location
mv $RPM_BUILD_ROOT%{_docdir}/%{_name} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
sed s!doc/%{_name}!doc/%{name}-%{version}! \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist
mv $RPM_BUILD_ROOT%{_docdir}/%{_name}_setup \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-setup-%{setupversion}
sed s!doc/%{_name}_setup!doc/%{name}-setup-%{setupversion}! \
  -i $GLOBUSPACKAGEDIR/%{_name}_setup/noflavor_doc.filelist

# Fix doxygen glitches
for f in globus_gram_job_manager_configuration.3 \
	 globus_gram_job_manager_job_execution_environment.3 \
	 globus_gram_job_manager_rsl_validation_file.3 \
	 globus_gram_job_manager_rsl.3 ; do
  sed 's/P\.RS/P\n.RS/' -i $RPM_BUILD_ROOT%{_mandir}/man3/$f
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
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
    $GLOBUSPACKAGEDIR/%{_name}_setup/noflavor_pgm.filelist \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}_setup/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/GLOBUS_LICENSE
%doc %{_docdir}/%{name}-%{version}/README
%dir %{_datadir}/globus/packages/%{_name}_setup
%{_datadir}/globus/packages/setup/%{_name}_setup
%dir %{_datadir}/globus/packages/setup/%{_name}_service_setup

%files doc -f package-doc.filelist
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/html
%dir %{_docdir}/%{name}-setup-%{setupversion}
%dir %{_docdir}/%{name}-setup-%{setupversion}/html

%changelog
* Mon Aug 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 10.70-5
- Fix deadlock upon child process exit.

* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.70-1
- Update to Globus Toolkit 5.0.4
- Fix doxygen markup

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.67-3
- Add README file

* Tue Apr 19 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.67-2
- Updated patch

* Thu Feb 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.67-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 18 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.59-2
- Move client and server man pages to main package

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.59-1
- Update to Globus Toolkit 5.0.2

* Sat Jun 05 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.42-2
- Additional portability fixes

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.42-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 10.17-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.15-1
- Autogenerated
