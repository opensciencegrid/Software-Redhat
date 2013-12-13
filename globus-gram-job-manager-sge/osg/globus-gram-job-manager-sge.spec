%ifarch aarch64 alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gram-job-manager-sge
%global _name %(tr - _ <<< %{name})
Version:	1.7
Release:	1.1%{?dist}
Summary:	Globus Toolkit - Grid Engine Job Manager Support

Group:		Applications/Internet
License:	ASL 2.0 and LGPLv2
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.5/packages/src/%{_name}-%{version}.tar.gz
Source1:        sge.rvf
#		README file
Source8:	GLOBUS-GRAM5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-gram-job-manager >= 13
Requires:	globus-gram-job-manager-scripts >= 4
Requires:	globus-gass-cache-program >= 5
Requires:	globus-common-progs >= 14
Requires:	globus-gatekeeper >= 9
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	%{name}-setup
%if "%{?rhel}" == "6"
#		gridengine is not available for EPEL 6 ppc64
%ifnarch ppc64
Requires:	gridengine
%endif
%else
Requires:	gridengine
%endif
Provides:	globus-gram-job-manager-setup-sge = 2.6
Obsoletes:	globus-gram-job-manager-setup-sge < 2.6
Obsoletes:	globus-gram-job-manager-setup-sge-doc < 2.6
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core >= 8
BuildRequires:	globus-scheduler-event-generator-devel >= 4
BuildRequires:	globus-common-devel >= 14

%package setup-poll
Summary:	Globus Toolkit - Grid Engine Job Manager Support using polling
Group:		Applications/Internet
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Provides:	%{name}-setup
Provides:       globus-gram-job-manager-setup
Requires:	%{name} = %{version}-%{release}

Requires(post):         globus-gram-job-manager-scripts >= 4
Requires(preun):	globus-gram-job-manager-scripts >= 4

%package setup-seg
Summary:	Globus Toolkit - Grid Engine Job Manager Support using SEG
Group:		Applications/Internet
Provides:	%{name}-setup
Provides:       globus-gram-job-manager-setup
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-scheduler-event-generator%{?_isa} >= 4
Requires:	globus-common%{?_isa} >= 14

Requires(post):         globus-gram-job-manager-scripts >= 4
Requires(preun):	globus-gram-job-manager-scripts >= 4
Requires(preun):	globus-scheduler-event-generator-progs >= 4
Requires(preun):	initscripts
Requires(postun):	globus-scheduler-event-generator-progs >= 4
Requires(postun):	initscripts

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Grid Engine Job Manager Support

%description setup-poll
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-poll package contains:
Grid Engine Job Manager Support using polling to monitor job state

%description setup-seg
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-seg package contains:
Grid Engine Job Manager Support using the scheduler event generator to monitor
job state

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

%if %{?fedora}%{!?fedora:0} >= 9 || %{?rhel}%{!?rhel:0} >= 6
export QSUB=/usr/bin/qsub-ge
export QSTAT=/usr/bin/qstat-ge
export QDEL=/usr/bin/qdel-ge
%else
export QSUB=/usr/bin/qsub
export QSTAT=/usr/bin/qstat
export QDEL=/usr/bin/qdel
%endif
export QCONF=/usr/bin/qconf
export MPIRUN=no
export SUN_MPRUN=no
%configure --disable-static --with-flavor=%{flavor} \
	   --with-docdir=%{_pkgdocdir} \
	   --with-globus-state-dir=%{_localstatedir}/lib/globus \
	   --with-sge-config=/etc/sysconfig/gridengine \
	   --with-sge-root=undefined \
	   --with-sge-cell=undefined \
	   --without-queue-validation \
	   --without-pe-validation

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

GLOBUSPACKAGEDIR=%{buildroot}%{_datadir}/globus/packages

# This library is opened using lt_dlopenext, so the libtool archive
# (.la file) can not be removed - fix the libdir and clear dependency_libs
# ... and move it to the main package
for lib in `find %{buildroot}%{_libdir} -name 'lib*.la'` ; do
  sed -e "s!^libdir=.*!libdir=\'%{_libdir}\'!" \
      -e "s!^dependency_libs=.*!dependency_libs=\'\'!" -i $lib
done
grep 'lib.*\.la$' $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Remove jobmanager-sge from install dir - leave it for admin configuration
rm %{buildroot}/etc/grid-services/jobmanager-sge

# Install the RVF file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram/sge.rvf

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Devel package is redundant
rm %{buildroot}%{_libdir}/libglobus_seg_sge.so
rm %{buildroot}%{_libdir}/pkgconfig/globus-gram-job-manager-sge.pc
rm $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist
rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_%{flavor}_dev.gpt

# List config files in each package - drop the file list
rm $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist
rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_noflavor_data.gpt

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
  | sed -e s!^!%{_prefix}! -e 's!/man/.*!&*!' \
	-e /sge.pm/d > package-seg.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed 's!^!%doc %{_prefix}!' > package.filelist

%clean
rm -rf %{buildroot}

%post setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-sge-poll -n jobmanager-sge > /dev/null 2>&1 || :
    if [ ! -f /etc/grid-services/jobmanager ]; then
        globus-gatekeeper-admin -e jobmanager-sge-poll -n jobmanager
    fi
fi

%preun setup-poll
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-sge-poll > /dev/null 2>&1 || :
fi

%postun setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-sge-poll -n jobmanager-sge > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%post setup-seg
ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-sge-seg -n jobmanager-sge > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e sge > /dev/null 2>&1 || :
    service globus-scheduler-event-generator condrestart sge
fi

%preun setup-seg
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-sge-seg > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator stop sge > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -d sge > /dev/null 2>&1 || :
fi

%postun setup-seg
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-sge-seg > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e sge > /dev/null 2>&1 || :
    service globus-scheduler-event-generator condrestart sge > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%files -f package.filelist
%{_datadir}/globus/globus_gram_job_manager/sge.rvf
%{perl_vendorlib}/Globus
%config(noreplace) %{_sysconfdir}/globus/globus-sge.conf
%config(noreplace) %{_sysconfdir}/globus/gram/sge.rvf
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README

%files setup-poll
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-sge-poll

%files -f package-seg.filelist setup-seg
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-sge-seg
%config(noreplace) %{_sysconfdir}/globus/scheduler-event-generator/available/sge

%changelog
* Thu Dec 12 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.7-1.1.osg
- Merge OSG changes
- Drop seg_sge_module patch (fixed upstream)

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.7-1
- Update to Globus Toolkit 5.2.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-6
- Implement updated packaging guidelines

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.5-5
- Perl 5.18 rebuild

* Tue May 28 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-7.2.osg
- Add seg_sge_module patch from Jeff Porter to fix extra 'acct' records at midnight

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-4
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-2
- Specfile clean-up

* Fri Nov 02 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-7.1.osg
- Add placeholder file for user-editable sge.rvf

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gram-job-manager-sge-desc.patch (fixed upstream)

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.0-2
- Fix broken links in README file

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.0-1
- Autogenerated
