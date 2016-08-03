%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-gram-job-manager-fork
%global _name %(tr - _ <<< %{name})
Version:	2.4
Release:	1.1%{?dist}
Summary:	Globus Toolkit - Fork Job Manager Support

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt6/packages/%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GRAM5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#		A requirement on globus-gram-job-manager would make sense.
#		However, that would create a circular build dependency when
#		building the globus-gram-job-manager package, since the test
#		suite for that package requires globus-gram-job-manager-fork
#		to run.
# Requires:	globus-gram-job-manager >= 13
Requires:	globus-gram-job-manager-scripts >= 4
Requires:	globus-gass-cache-program >= 5
Requires:	globus-common-progs >= 14
Requires:	globus-gatekeeper >= 9
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	%{name}-setup = %{version}-%{release}
Provides:	globus-gram-job-manager-setup-fork = 4.3
Obsoletes:	globus-gram-job-manager-setup-fork < 4.3
Obsoletes:	globus-gram-job-manager-setup-fork-doc < 4.3
BuildRequires:	globus-common-devel >= 15
BuildRequires:	globus-xio-devel >= 3
BuildRequires:	globus-scheduler-event-generator-devel >= 4
BuildRequires:	globus-gram-protocol-devel >= 11

%package setup-poll
Summary:	Globus Toolkit - Fork Job Manager Support using polling
Group:		Applications/Internet
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Provides:	%{name}-setup = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

Requires(preun):	globus-gram-job-manager-scripts >= 4

%package setup-seg
Summary:	Globus Toolkit - Fork Job Manager Support using SEG
Group:		Applications/Internet
Provides:	%{name}-setup = %{version}-%{release}
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
Fork Job Manager Support

%description setup-poll
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-poll package contains:
Fork Job Manager Support using polling to monitor job state

%description setup-seg
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-setup-seg package contains:
Fork Job Manager Support using the scheduler event generator to monitor job
state

%prep
%setup -q -n %{_name}-%{version}

%build
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

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

# Remove jobmanager-fork from install dir - leave it for admin configuration
rm %{buildroot}/etc/grid-services/jobmanager-fork

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

%clean
rm -rf %{buildroot}

%post setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-fork-poll -n jobmanager-fork > /dev/null 2>&1 || :
    if [ ! -f /etc/grid-services/jobmanager ]; then
        globus-gatekeeper-admin -e jobmanager-fork-poll -n jobmanager
    fi
fi

%preun setup-poll
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-fork-poll > /dev/null 2>&1 || :
fi

%postun setup-poll
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-fork-poll -n jobmanager-fork > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%post setup-seg
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-fork-seg -n jobmanager-fork > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e fork > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator condrestart fork
fi

%preun setup-seg
if [ $1 -eq 0 ]; then
    globus-gatekeeper-admin -d jobmanager-fork-seg > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator stop fork > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -d fork > /dev/null 2>&1 || :
fi


%postun setup-seg
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    globus-gatekeeper-admin -e jobmanager-fork-seg > /dev/null 2>&1 || :
    globus-scheduler-event-generator-admin -e fork > /dev/null 2>&1 || :
    /sbin/service globus-scheduler-event-generator condrestart fork > /dev/null 2>&1 || :
elif [ $1 -eq 0 -a ! -f /etc/grid-services/jobmanager ]; then
    globus-gatekeeper-admin -E > /dev/null 2>&1 || :
fi

%files
%dir %{perl_vendorlib}/Globus
%dir %{perl_vendorlib}/Globus/GRAM
%dir %{perl_vendorlib}/Globus/GRAM/JobManager
%{perl_vendorlib}/Globus/GRAM/JobManager/fork.pm
%dir %{_sysconfdir}/globus
%config(noreplace) %{_sysconfdir}/globus/globus-fork.conf
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/GLOBUS_LICENSE
%doc %{_pkgdocdir}/README

%files setup-poll
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-fork-poll

%files setup-seg
%{_libdir}/libglobus_seg_fork.so
%{_sbindir}/globus-fork-starter
%doc %{_mandir}/man8/globus-fork-starter.8*
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-fork-seg
%config(noreplace) %{_sysconfdir}/globus/scheduler-event-generator/available/fork

%changelog
* Fri Feb 6 2015 Matyas Selmeci <matyas@cs.wisc.edu> 2.4-1.1.osg
- Merge OSG changes

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.4-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.5-12
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Brent Baude <baude@us.ibm.com> - 1.5-9
- Replace ppc64 arch with power64 macro

* Thu Jan 09 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-8
- Fix logfile location

* Fri Dec 20 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1.5-1.1.osg
- Use globus-gatekeeper-admin to set up "jobmanager-fork" aliases for "jobmanager-fork-seg" and "jobmanager-fork-poll"

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-6
- Implement updated packaging guidelines

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.5-5
- Perl 5.18 rebuild

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-4
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-2
- Specfile clean-up

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gram-jobmanager-fork-desc.patch (fixed upstream)

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.0-2
- Fix broken links in README file

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.0-1
- Autogenerated
