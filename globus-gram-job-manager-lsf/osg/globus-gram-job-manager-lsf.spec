%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gram-job-manager-lsf
%global _name %(tr - _ <<< %{name})
Version:	2.6
Release:	1.1%{?dist}
Summary:	Globus Toolkit - LSF Job Manager Support

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt6/packages/%{_name}-%{version}.tar.gz
Source1:        lsf.rvf
#		README file
Source8:	GLOBUS-GRAM5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-gram-job-manager >= 13
Requires:	globus-gram-job-manager-scripts >= 4
Requires:	globus-gass-cache-program >= 5
Requires:	globus-gatekeeper >= 9
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	%{name}-setup = %{version}-%{release}
Provides:	globus-gram-job-manager-setup-lsf = 2.6
Obsoletes:	globus-gram-job-manager-setup-lsf < 2.6
Obsoletes:	globus-gram-job-manager-setup-lsf-doc < 2.6
BuildRequires:	globus-common-devel >= 15
BuildRequires:	globus-scheduler-event-generator-devel >= 4

%package setup-poll
Summary:	Globus Toolkit - LSF Job Manager Support using polling
Group:		Applications/Internet
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Provides:	%{name}-setup = %{version}-%{release}
Provides:   globus-gram-job-manager-setup = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

Requires(post):   globus-gram-job-manager-scripts >= 4
Requires(preun):  globus-gram-job-manager-scripts >= 4

%package setup-seg
Summary:	Globus Toolkit - LSF Job Manager Support using SEG
Group:		Applications/Internet
Provides:	%{name}-setup = %{version}-%{release}
Provides:   globus-gram-job-manager-setup = %{version}-%{release}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-scheduler-event-generator-progs >= 4

Requires(post):     globus-gram-job-manager-scripts >= 4
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
LSF Job Manager Support

%description setup-poll
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-poll package contains:
LSF Job Manager Support using polling to monitor job state

%description setup-seg
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-seg package contains:
LSF Job Manager Support using the scheduler event generator to monitor job
state

%prep
%setup -q -n %{_name}-%{version}

%build
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

export BSUB=%{_bindir}/bsub
export BQUEUES=%{_bindir}/bqueues
export BJOBS=%{_bindir}/bjobs
export BKILL=%{_bindir}/bkill
export BHIST=%{_bindir}/bhist
export BACCT=%{_bindir}/bacct
export MPIEXEC=no
export MPIRUN=no
%configure --disable-static \
	   --includedir='${prefix}/include/globus' \
	   --libexecdir='${datadir}/globus' \
	   --docdir=%{_pkgdocdir} \
	   --with-perlmoduledir=%{perl_vendorlib} \
	   --with-globus-state-dir=%{_localstatedir}/log/globus

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

# Add RVF file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/globus/gram/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/globus/gram/lsf.rvf

# Remove jobmanager-lsf from install dir - leave it for admin configuration
rm %{buildroot}/etc/grid-services/jobmanager-lsf

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

%clean
rm -rf %{buildroot}

%post setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-lsf-poll -n jobmanager-lsf > /dev/null 2>&1 || :
    if [ ! -f /etc/grid-services/jobmanager ]; then
        globus-gatekeeper-admin -e jobmanager-lsf-poll -n jobmanager
    fi
fi

%preun setup-poll
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-lsf-poll > /dev/null 2>&1 || :
fi

%postun setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-lsf-poll -n jobmanager-lsf > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%post setup-seg
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-lsf-seg -n jobmanager-lsf > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e lsf > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator condrestart lsf
fi

%preun setup-seg
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-lsf-seg > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator stop lsf > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -d lsf > /dev/null 2>&1 || :
fi

%postun setup-seg
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-lsf-seg > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e lsf > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator condrestart lsf > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%files
%{_datadir}/globus/globus_gram_job_manager/lsf.rvf
%dir %{perl_vendorlib}/Globus
%dir %{perl_vendorlib}/Globus/GRAM
%dir %{perl_vendorlib}/Globus/GRAM/JobManager
%{perl_vendorlib}/Globus/GRAM/JobManager/lsf.pm
%config(noreplace) %{_sysconfdir}/globus/globus-lsf.conf
%config(noreplace) %{_sysconfdir}/globus/gram/lsf.rvf
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE
%doc %{_pkgdocdir}/README

%files setup-poll
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-lsf-poll

%files setup-seg
%{_libdir}/libglobus_seg_lsf.so
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-lsf-seg
%config(noreplace) %{_sysconfdir}/globus/scheduler-event-generator/available/lsf

%changelog
* Wed Feb 11 2015 Matyas Selmeci <matyas@cs.wisc.edu> - 2.6-1.1.osg
- Merge OSG changes

* Mon Oct 27 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.6-1
- GT6 update

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata
- Drop patch globus-gram-job-manager-lsf-statedir.patch (fixed upstream)

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.2-6
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 1.2-3
- Replacing ppc64 arch with power64 macro

* Thu Jan 09 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.2-2
- Fix logfile location

* Thu Dec 12 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2-1.1.osg
- Merge OSG changes
- Drop patch host-xcount.patch (fixed upstream)

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.2-1
- Update to Globus Toolkit 5.2.5
- Drop patch globus-gram-job-manager-desc.patch (fixed upstream)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.1-4
- Implement updated packaging guidelines

* Fri Jul 19 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.1-3
- Remove isa from BuildRequires :-(

* Sat May 25 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.1-2
- Add aarch64 to the list of 64 bit platforms

* Tue Mar 19 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1.5.osg
- Replaced xcount patch Suchandra Thapa's version (SOFTWARE-978)

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.1-1
- Autogenerated

* Fri Nov 02 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1.4.osg
- Update lsf.rvf with more info

* Fri Nov 02 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1.3.osg
- Add placeholder file for user-editable lsf.rvf

* Tue Oct 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1.2.osg
- Replaced xcount patch with Joe Bester's version

* Thu Oct 04 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-1.1.osg
- Added xcount patch which adds an attribute that lets the user specify the number of cores for a job.
- Changed PBS to LSF in the metadata

* Fri Aug 17 2012 Joseph Bester <bester@mcs.anl.gov> - 1.0-1
- Initial packaging
