%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

Name:		globus-gram-job-manager-setup-condor
%global _name %(tr - _ <<< %{name})
Version:	4.4
Release:	4%{?dist}
Summary:	Globus Toolkit - Condor Job Manager Setup

Group:		Applications/Internet
BuildArch:	noarch
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.2/installers/src/gt5.0.2-all-source-installer.tar.bz2
#		tar -jxf gt5.0.2-all-source-installer.tar.bz2
#		mv gt5.0.2-all-source-installer/source-trees/gram/jobmanager/setup/condor globus_gram_job_manager_setup_condor-4.4
#		cp -p gt5.0.2-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_gram_job_manager_setup_condor-4.4
#		tar -zcf globus_gram_job_manager_setup_condor-4.4.tar.gz globus_gram_job_manager_setup_condor-4.4
Source:		%{_name}-%{version}.tar.gz
#		Condor configuration generator script
#		The version of this script that is installed by the package
#		hardcodes the architecture at compilation time
#		This version detects the architecture at runtime, which is
#		appropriate for a noarch package
Source1:	globus-condor-print-config
#		README file
Source8:	GLOBUS-GRAM5

Source9:        condor_accounting_groups.pm

#		Remove hardcoded paths:
#		http://bugzilla.globus.org/bugzilla/show_bug.cgi?id=6826
Patch0:		%{name}.patch
Patch1000:  job_status.patch
Patch1001:  gratia.patch
Patch1002:  nfslite.patch
Patch1003:  groupacct.patch
Patch1004:  managedfork.patch
Patch1005:  conf_location.patch

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
Summary:	Globus Toolkit - Condor Job Manager Setup Documentation Files
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Condor Job Manager Setup

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
Condor Job Manager Setup Documentation Files

%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1
%patch1000 -p1
%patch1001 -p1
%patch1002 -p0
%patch1003 -p0
%patch1004 -p0
%patch1005 -p0

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
sed -e "s!'@CONDOR_SUBMIT@'!(defined(\$ENV{CONDOR_SUBMIT}) ? \$ENV{CONDOR_SUBMIT} : \"condor_submit\")!" \
    -e "s!'@CONDOR_RM@'!(defined(\$ENV{CONDOR_RM}) ? \$ENV{CONDOR_RM} : \"condor_rm\")!" \
    -e "s!'@CONDOR_CONFIG@'!(defined(\$ENV{CONDOR_CONFIG}) ? \$ENV{CONDOR_CONFIG} : \"\")!" \
  $RPM_BUILD_ROOT%{_datadir}/globus/setup/condor.in > \
  $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/condor.pm

# Extract validation file
sed -n '/print VALIDATION_FILE <<EOF/,/^EOF$/p' \
  $RPM_BUILD_ROOT%{_datadir}/globus/setup/setup-globus-job-manager-condor.pl \
  | sed -e '1d' -e '$d' > $RPM_BUILD_ROOT%{_datadir}/globus/condor.rvf

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Remove some intermediate files
rm -rf $RPM_BUILD_ROOT%{_datadir}/globus/setup
sed '/globus\/setup/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_pgm.filelist

# And install this one instead
mkdir -p $RPM_BUILD_ROOT%{_datadir}/globus/setup
install %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/globus/setup

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

# Install configuration file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/globus-condor/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/globus-condor/jobmanager.conf << EOF
#Set to 0 to disable NFS-lite mode.
isNFSLite=1
EOF

# Install the group accounting patch
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{perl_vendorlib}/Globus/GRAM/JobManager/
touch $RPM_BUILD_ROOT%{_sysconfdir}/globus-condor/uid_table.txt
touch $RPM_BUILD_ROOT%{_sysconfdir}/globus-condor/ea_table.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%{_datadir}/globus/packages/setup/globus_gram_job_manager_service_setup/%{_name}.gpt
%{_datadir}/globus/condor.rvf
%{_datadir}/globus/setup/globus-condor-print-config
%{perl_vendorlib}/Globus
%dir %{_sysconfdir}/globus-condor
%config(noreplace) %{_sysconfdir}/globus-condor/jobmanager.conf
%config(noreplace) %{_sysconfdir}/globus-condor/ea_table.txt
%config(noreplace) %{_sysconfdir}/globus-condor/uid_table.txt
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/GLOBUS_LICENSE
%doc %{_docdir}/%{name}-%{version}/README

%files doc -f package-doc.filelist
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/html

%changelog
* Mon Aug 08 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.4-4
- Add OSG's NFS-lite patch.
- Add OSG's group accounting patch.
- Created a dedicated configuration directory.
- Add Gratia patch

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.4-3
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.4-1
- Update to Globus Toolkit 5.0.2

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 30 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.1-1
- Autogenerated
