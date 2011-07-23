%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

Name:		globus-gram-job-manager-setup-pbs
%global _name %(tr - _ <<< %{name})
Version:	4.4
Release:	1%{?dist}
Summary:	Globus Toolkit - PBS Job Manager Setup

Group:		Applications/Internet
BuildArch:	noarch
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.4/installers/src/gt5.0.4-all-source-installer.tar.bz2
#		tar -jxf gt5.0.4-all-source-installer.tar.bz2
#		mv gt5.0.4-all-source-installer/source-trees/gram/jobmanager/setup/pbs globus_gram_job_manager_setup_pbs-4.4
#		cp -p gt5.0.4-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gram_job_manager_setup_pbs-4.4
#		tar -zcf globus_gram_job_manager_setup_pbs-4.4.tar.gz globus_gram_job_manager_setup_pbs-4.4
Source:		%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GRAM5
Patch1000: teragrid-pbs.patch
#Patch1001: osg-grid-location.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-gram-job-manager-scripts
Requires:	globus-gass-cache-program >= 2
Requires:	globus-common-setup >= 2
Requires:	globus-gram-job-manager >= 10.59
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-core
BuildRequires:	doxygen
BuildRequires:	graphviz
%if "%{?rhel}" == "5"
BuildRequires:	graphviz-gd
%endif
BuildRequires:	ghostscript
%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:	tex(latex)
%else
BuildRequires:	tetex-latex
%endif

%package doc
Summary:	Globus Toolkit - PBS Job Manager Setup Documentation Files
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
PBS Job Manager Setup

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
PBS Job Manager Setup Documentation Files

%prep
%setup -q -n %{_name}-%{version}
%patch1000 -p1
#%patch1001 -p1

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

%{_datadir}/globus/globus-bootstrap.sh

%configure --without-flavor --enable-doxygen

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Register setup
perl -MGrid::GPT::Setup <<EOF
my \$metadata = new Grid::GPT::Setup(package_name => "%{_name}",
				     globusdir => "$RPM_BUILD_ROOT%{_prefix}");
\$metadata->finish();
EOF

# Create perl module
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager
sed -e "s!'@MPIRUN@'!(defined(\$ENV{MPIRUN}) ? \$ENV{MPIRUN} : \"mpirun\")!" \
    -e "s!'@MPIEXEC@'!(defined(\$ENV{MPIEXEC}) ? \$ENV{MPIEXEC} : \"mpiexec\")!" \
    -e "s!'@QSUB@'!(defined(\$ENV{QSUB}) ? \$ENV{QSUB} : \"qsub\")!" \
    -e "s!'@QSTAT@'!(defined(\$ENV{QSTAT}) ? \$ENV{QSTAT} : \"qstat\")!" \
    -e "s!'@QDEL@'!(defined(\$ENV{QDEL}) ? \$ENV{QDEL} : \"qdel\")!" \
    -e "s!@CLUSTER@!(defined(\$ENV{CLUSTER}) ? \$ENV{CLUSTER} : 1)!" \
    -e "s!@CPU_PER_NODE@!(defined(\$ENV{CPU_PER_NODE}) ? \$ENV{CPU_PER_NODE} : 1)!" \
    -e "s!'@REMOTE_SHELL@'!(defined(\$ENV{REMOTE_SHELL}) ? \$ENV{REMOTE_SHELL} : \"ssh\")!" \
    -e "s!'@SOFTENV_DIR@'!(defined(\$ENV{SOFTENV_DIR}) ? \$ENV{SOFTENV_DIR} : \"\")!" \
  $RPM_BUILD_ROOT%{_datadir}/globus/setup/pbs.in > \
  $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/pbs.pm

# Extract validation file
sed -n '/print VALIDATION_FILE <<EOF/,/^EOF$/p' \
  $RPM_BUILD_ROOT%{_datadir}/globus/setup/setup-globus-job-manager-pbs.pl \
  | sed -e '1d' -e '$d' > $RPM_BUILD_ROOT%{_datadir}/globus/pbs.rvf

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Remove some intermediate files
rm -rf $RPM_BUILD_ROOT%{_datadir}/globus/setup
sed '/globus\/setup/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_pgm.filelist

# Move documentation to default RPM location
mv $RPM_BUILD_ROOT%{_docdir}/%{_name} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
sed s!doc/%{_name}!doc/%{name}-%{version}! \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Install license file
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 -p GLOBUS_LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Install README file
install -m 644 -p %{SOURCE8} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_pgm.filelist \
  | sed s!^!%{_prefix}! > package.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed 's!^!%doc %{_prefix}!' > package-doc.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%{_datadir}/globus/packages/setup/globus_gram_job_manager_service_setup/%{_name}.gpt
%{_datadir}/globus/pbs.rvf
%{perl_vendorlib}/Globus
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/GLOBUS_LICENSE
%doc %{_docdir}/%{name}-%{version}/README

%files doc -f package-doc.filelist
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/html

%changelog
* Sun Jun 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.4-1
- Update to Globus Toolkit 5.0.4

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.3-2
- Add README file

* Fri Feb 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.3-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.1-1
- Update to Globus Toolkit 5.0.2

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.0-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.8-1
- Autogenerated
