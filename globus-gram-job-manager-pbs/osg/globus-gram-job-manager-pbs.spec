%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

%if %{?fedora}%{!?fedora:0} >= 14 || %{?rhel}%{!?rhel:0} >= 6
%global pbs_log_path /var/log/torque/server_logs 
%else
%global pbs_log_path /var/torque/server_logs
%endif

Name:		globus-gram-job-manager-pbs
%global _name %(tr - _ <<< %{name})
Version:	1.6
Release:	1.10%{?dist}
Summary:	Globus Toolkit - PBS Job Manager Support

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.3/packages/src/%{_name}-%{version}.tar.gz
Source1:        pbs.rvf
Source2:        caching_qstat
#		README file
Source8:	GLOBUS-GRAM5
Patch1:         osg-teragrid-pbs.patch
Patch2:         slurm-support-pbs.pm.patch
Patch3:         bad-slurm-submits.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-gram-job-manager >= 13
Requires:	globus-gram-job-manager-scripts >= 4
Requires:	globus-gass-cache-program >= 5
Requires:	globus-common-progs >= 14
Requires:	globus-gatekeeper >= 9
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	torque-client
Requires:	%{name}-setup
Provides:	globus-gram-job-manager-setup-pbs = 4.5
Obsoletes:	globus-gram-job-manager-setup-pbs < 4.5
Obsoletes:	globus-gram-job-manager-setup-pbs-doc < 4.5
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core%{?_isa} >= 8
BuildRequires:	globus-scheduler-event-generator-devel%{?_isa} >= 4
BuildRequires:	globus-common-devel%{?_isa} >= 14

%package setup-poll
Summary:	Globus Toolkit - PBS Job Manager Support using polling
Group:		Applications/Internet
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Provides:	%{name}-setup
Provides:       globus-gram-job-manager-setup
Requires:	%{name} = %{version}-%{release}

Requires(preun):	globus-gram-job-manager-scripts >= 4

%package setup-seg
Summary:	Globus Toolkit - PBS Job Manager Support using SEG
Group:		Applications/Internet
Provides:	%{name}-setup
Provides:       globus-gram-job-manager-setup
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-scheduler-event-generator%{?_isa} >= 4
Requires:	globus-common%{?_isa} >= 14

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
PBS Job Manager Support
Patched with SLURM support

%description setup-poll
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-poll package contains:
PBS Job Manager Support using polling to monitor job state

%description setup-seg
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-seg package contains:
PBS Job Manager Support using the scheduler event generator to monitor job
state

%prep
%setup -q -n %{_name}-%{version}
%patch1 -p0
%patch2 -p0
%patch3 -p0

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

export MPIEXEC=no
export MPIRUN=no
export QDEL=/usr/bin/qdel-torque
export QSTAT=/usr/bin/qstat-torque
export QSUB=/usr/bin/qsub-torque
%configure --disable-static --with-flavor=%{flavor} \
	   --with-docdir=%{_docdir}/%{name}-%{version} \
	   --with-globus-state-dir=%{_localstatedir}/lib/globus \
	   --with-log-path=%{pbs_log_path}

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove jobmanager-pbs from install dir so that it can be
# added/removed by post scripts
rm %{buildroot}/etc/grid-services/jobmanager-pbs

# Install the caching_qstat
install -d %{buildroot}%{_bindir}
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}

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

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_docdir}/%{name}-%{version}/README

## Devel package is redundant
#rm %{buildroot}%{_libdir}/libglobus_seg_pbs.so
#rm %{buildroot}%{_libdir}/pkgconfig/globus-gram-job-manager-pbs.pc
#rm $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist
#rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_%{flavor}_dev.gpt

## List config files in each package - drop the file list
#rm $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist
#rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_noflavor_data.gpt

# Install the RVF file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram/pbs.rvf

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | sed -e s!^!%{_prefix}! -e 's!/man/.*!&*!' \
        -e s!^%{_prefix}/etc!/etc! \
	-e /pbs.pm/d > package-seg.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed 's!^!%doc %{_prefix}!' > package.filelist

%clean
rm -rf %{buildroot}

%post setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-pbs-poll -n jobmanager-pbs > /dev/null 2>&1 || :
    if [ ! -f /etc/grid-services/jobmanager ]; then
        globus-gatekeeper-admin -e jobmanager-pbs-poll -n jobmanager
    fi
fi

%preun setup-poll
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-pbs-poll > /dev/null 2>&1 || :
fi

%postun setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-pbs-poll -n jobmanager-pbs > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%post setup-seg
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-pbs-seg -n jobmanager-pbs > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e pbs > /dev/null 2>&1 || :
    service globus-scheduler-event-generator condrestart pbs
fi

%preun setup-seg
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-pbs-seg > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator stop pbs > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -d pbs > /dev/null 2>&1 || :
fi

%postun setup-seg
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-pbs-seg > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e pbs > /dev/null 2>&1 || :
    service globus-scheduler-event-generator condrestart pbs > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%files -f package.filelist
%defattr(-,root,root,-)
%{_bindir}/caching_qstat
%{_datadir}/globus/globus_gram_job_manager/pbs.rvf
%{perl_vendorlib}/Globus
%config(noreplace) %{_sysconfdir}/globus/globus-pbs.conf
%config(noreplace) %{_sysconfdir}/globus/gram/pbs.rvf 
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README

%files setup-poll
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-pbs-poll

%files -f package-seg.filelist setup-seg
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-pbs-seg
%config(noreplace) %{_sysconfdir}/globus/scheduler-event-generator/available/pbs

%changelog
* Wed May 28 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6-1.10.osg
- Fix error in SOFTWARE-1162 patch if jobid started with 0

* Thu Jan 31 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> 1.6-1.9.osg
- Reenable SOFTWARE-1162 patch

* Thu Jan 09 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.6-1.8.osg
- Disable SOFTWARE-1162 patch

* Wed Jan 08 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.6-1.7.osg
- Re-add some 'devel' libraries and files to the setup-seg subpackage

* Tue Jan 07 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.6-1.6.osg
- Bump release to rebuild

* Mon Aug 26 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6-1.5.osg
- Patch to catch bad SLURM submits (SOFTWARE-1162)

* Thu Jul 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6-1.4.osg
- Patch to work with SLURM's PBS emulation layer (SOFTWARE-1105)

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6-1
- Update to Globus Toolkit 5.2.3

* Fri Nov 02 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6-1.3.osg
- Update pbs.rvf with more info

* Fri Nov 02 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6-1.2.osg
- Add placeholder file for user-editable pbs.rvf

* Wed Sep 12 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6-1.1.osg
- Add OSG/TeraGrid patch

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gram-job-manager-pbs-desc.patch (fixed upstream)

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.1-2
- Fix broken links in README file

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.1-1
- Autogenerated
