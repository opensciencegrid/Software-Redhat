%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%{!?perl_vendorlib: %global perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)}

Name:		globus-gram-job-manager-fork
%global _name %(tr - _ <<< %{name})
Version:	1.5
Release:	1.1%{?dist}
Summary:	Globus Toolkit - Fork Job Manager Support

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.2/5.2.1/packages/src/%{_name}-%{version}.tar.gz
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
Provides:	globus-gram-job-manager-setup-fork = 4.3
Obsoletes:	globus-gram-job-manager-setup-fork < 4.3
Obsoletes:	globus-gram-job-manager-setup-fork-doc < 4.3
BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-core%{?_isa} >= 8
BuildRequires:	globus-gram-protocol-devel%{?_isa} >= 11
BuildRequires:	globus-scheduler-event-generator-devel%{?_isa} >= 4
BuildRequires:	globus-common-devel%{?_isa} >= 14
BuildRequires:	globus-xio-devel%{?_isa} >= 3

%package setup-poll
Summary:	Globus Toolkit - Fork Job Manager Support using polling
Group:		Applications/Internet
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif
Provides:	%{name}-setup
Requires:	%{name} = %{version}-%{release}

Requires(preun):	globus-gram-job-manager-scripts >= 4

%package setup-seg
Summary:	Globus Toolkit - Fork Job Manager Support using SEG
Group:		Applications/Internet
Provides:	%{name}-setup
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-gram-protocol%{?_isa} >= 11
Requires:	globus-scheduler-event-generator%{?_isa} >= 4
Requires:	globus-common%{?_isa} >= 14
Requires:	globus-xio%{?_isa} >= 3

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
%configure --disable-static --with-flavor=%{flavor} \
	   --with-docdir=%{_docdir}/%{name}-%{version} \
	   --with-globus-state-dir=%{_localstatedir}/lib/globus

# Reduce overlinking
sed 's!CC -shared !CC \${wl}--as-needed -shared !g' -i libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# This library is opened using lt_dlopenext, so the libtool archive
# (.la file) can not be removed - fix the libdir and clear dependency_libs
# ... and move it to the main package
for lib in `find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la'` ; do
  sed -e "s!^libdir=.*!libdir=\'%{_libdir}\'!" \
      -e "s!^dependency_libs=.*!dependency_libs=\'\'!" -i $lib
done
grep 'lib.*\.la$' $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist
sed '/lib.*\.la$/d' -i $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist

# Remove jobmanager-fork from install dir - leave it for admin configuration
rm $RPM_BUILD_ROOT/etc/grid-services/jobmanager-fork

# Move script man pages to progs package
grep '.[18]$' $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist
sed '/.[18]$/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Install README file
install -m 644 -p %{SOURCE8} \
  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README

# Devel package is redundant
rm $RPM_BUILD_ROOT%{_libdir}/libglobus_seg_fork.so
rm $RPM_BUILD_ROOT%{_libdir}/pkgconfig/globus-gram-job-manager-fork.pc
rm $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist
rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_%{flavor}_dev.gpt

# List config files in each package - drop the file list
rm $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist
rm $GLOBUSPACKAGEDIR/%{_name}/pkg_data_noflavor_data.gpt

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
  | sed -e s!^!%{_prefix}! -e 's!/man/.*!&*!' \
	-e /fork.pm/d > package-seg.filelist
cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed 's!^!%doc %{_prefix}!' > package.filelist

%clean
rm -rf $RPM_BUILD_ROOT

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


%files -f package.filelist
%defattr(-,root,root,-)
%{perl_vendorlib}/Globus
%config(noreplace) %{_sysconfdir}/globus/globus-fork.conf
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README

%files setup-poll
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-fork-poll

%files -f package-seg.filelist setup-seg
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/grid-services/available/jobmanager-fork-seg
%config(noreplace) %{_sysconfdir}/globus/scheduler-event-generator/available/fork

%changelog
* Fri Dec 20 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1.5-1.1.osg
- Use globus-gatekeeper-admin to set up "jobmanager-fork" aliases for "jobmanager-fork-seg" and "jobmanager-fork-poll"

* Sat Apr 28 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.5-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-gram-jobmanager-fork-desc.patch (fixed upstream)

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.0-2
- Fix broken links in README file

* Thu Dec 15 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.0-1
- Autogenerated
