%if %{?fedora}%{!?fedora:0} >= 14 || %{?rhel}%{!?rhel:0} >= 6
%global pbs_log_path /var/log/torque/server_logs 
%else
%global pbs_log_path /var/torque/server_logs
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gram-job-manager-pbs
%global _name %(tr - _ <<< %{name})
Version:	2.4
Release:	2.1%{?dist}
Summary:	Globus Toolkit - PBS Job Manager Support

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt6/packages/%{_name}-%{version}.tar.gz
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
Requires:	globus-gatekeeper >= 9
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	%{name}-setup = %{version}-%{release}
Provides:	globus-gram-job-manager-setup-pbs = 4.5
Obsoletes:	globus-gram-job-manager-setup-pbs < 4.5
Obsoletes:	globus-gram-job-manager-setup-pbs-doc < 4.5
BuildRequires:	globus-common-devel >= 15
BuildRequires:	globus-scheduler-event-generator-devel >= 4

%package setup-poll
Summary:	Globus Toolkit - PBS Job Manager Support using polling
Group:		Applications/Internet
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Provides:	%{name}-setup = %{version}-%{release}
Provides:       globus-gram-job-manager-setup = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

Requires(preun):	globus-gram-job-manager-scripts >= 4

%package setup-seg
Summary:	Globus Toolkit - PBS Job Manager Support using SEG
Group:		Applications/Internet
Provides:	%{name}-setup = %{version}-%{release}
Provides:       globus-gram-job-manager-setup = %{version}-%{release}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-scheduler-event-generator-progs >= 4

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
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

export MPIEXEC=no
export MPIRUN=no
export QDEL=%{_bindir}/qdel-torque
export QSTAT=%{_bindir}/qstat-torque
export QSUB=%{_bindir}/qsub-torque
%configure --disable-static \
	   --includedir='${prefix}/include/globus' \
	   --libexecdir='${datadir}/globus' \
	   --docdir=%{_pkgdocdir} \
	   --with-perlmoduledir=%{perl_vendorlib} \
	   --with-globus-state-dir=%{_localstatedir}/log/globus \
	   --with-log-path=%{pbs_log_path}

# Reduce overlinking
sed 's!CC \(.*-shared\) !CC \\\${wl}--as-needed \1 !' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Install the caching_qstat
install -d %{buildroot}%{_bindir}
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

# Remove jobmanager-pbs from install dir - leave it for admin configuration
rm %{buildroot}/etc/grid-services/jobmanager-pbs

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Install the RVF file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/globus/gram/pbs.rvf

# Remove license file from pkgdocdir if licensedir is used
%{?_licensedir: rm %{buildroot}%{_pkgdocdir}/GLOBUS_LICENSE}


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
    /sbin/service globus-scheduler-event-generator condrestart pbs > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%files
%{_bindir}/caching_qstat
%{_datadir}/globus/globus_gram_job_manager/pbs.rvf
%dir %{perl_vendorlib}/Globus
%dir %{perl_vendorlib}/Globus/GRAM
%dir %{perl_vendorlib}/Globus/GRAM/JobManager
%{perl_vendorlib}/Globus/GRAM/JobManager/pbs.pm
%config(noreplace) %{_sysconfdir}/globus/globus-pbs.conf
%config(noreplace) %{_sysconfdir}/globus/gram/pbs.rvf 
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%files setup-poll
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-pbs-poll

%files setup-seg
# This is a loadable module (plugin)
%{_libdir}/libglobus_seg_pbs.so
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-pbs-seg
%config(noreplace) %{_sysconfdir}/globus/scheduler-event-generator/available/pbs

%changelog
* Wed Feb 11 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 2.4-2.1.osg
- Merge OSG changes

* Fri Jan 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.4-2
- Implement updated license packaging guidelines

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.4-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata
- Drop patch globus-gram-job-manager-pbs-enosr.patch (fixed upstream)

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.6-11
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6-1.10.osg
- Fix error in SOFTWARE-1162 patch if jobid started with 0

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 1.6-8
- Changing ppc64 arch to power64 macro

* Thu Jan 09 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6-7
- Fix logfile location

* Wed Jan 08 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.6-1.7.osg
- Re-add some 'devel' libraries and files to the setup-seg subpackage

* Mon Aug 26 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6-1.5.osg
- Patch to catch bad SLURM submits (SOFTWARE-1162)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6-5
- Implement updated packaging guidelines

* Thu Jul 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6-1.4.osg
- Patch to work with SLURM's PBS emulation layer (SOFTWARE-1105)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.6-4
- Perl 5.18 rebuild

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.6-3
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

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
