%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

%if "%{?rhel}" == "5"
%global docdiroption "with-docdir"
%else
%global docdiroption "docdir"
%endif

Name:		globus-gram-job-manager
%global _name %(tr - _ <<< %{name})
Version:	13.5
Release:	11%{?dist}
Summary:	Globus Toolkit - GRAM Jobmanager

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt5/5.1/5.1.2/packages/src/%{_name}-%{version}.tar.gz
Source1:       globus-gram-job-manager-logging
Source2:       globus-gram-job-manager-logrotate

# OSG-specific patches
Patch9:         unlock_init.patch
Patch11:        null_old_jm.patch
Patch13:        watchdog_timer.patch
Patch14:        recvmsg_eagain.patch
Patch16:        description_service_tag.patch
Patch19:        load_requests_before_activating_socket.patch
Patch20:        fix-job-home-dir.patch
Patch21:	condor-poll-GRAM-271.patch
Patch22:        fix-job-lock-location.patch
Patch23:        GRAM-273-ignore-logs.patch
Patch24:        GRAM-270-context-leak.patch
Patch25:        request-lock.patch
Patch26:        GRAM-275-logfile-names.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	globus-common >= 14
Requires:	globus-scheduler-event-generator%{?_isa} >= 4
Requires:	globus-xio-popen-driver%{?_isa} >= 2
Requires:	globus-xio%{?_isa} >= 3
Requires:	globus-gss-assist%{?_isa} >= 8
Requires:	libxml2%{?_isa}
Requires:	globus-gsi-sysconfig%{?_isa} >= 5
Requires:	globus-callout%{?_isa} >= 2
Requires:	globus-gram-job-manager-callout-error%{?_isa} >= 2
Requires:	globus-gram-protocol >= 11
Requires:	globus-usage%{?_isa} >= 3
Requires:	globus-rsl%{?_isa} >= 9
Requires:	globus-gass-cache%{?_isa} >= 8
Requires:	globus-gass-transfer%{?_isa} >= 7
Requires:	globus-gram-job-manager-scripts
Requires:	globus-gass-copy-progs >= 8
Requires:	globus-proxy-utils >= 5

Requires:	globus-gass-cache-program >= 2

BuildRequires:	grid-packaging-tools >= 3.4
BuildRequires:	globus-scheduler-event-generator-devel%{?_isa} >= 4
BuildRequires:	globus-xio-popen-driver-devel%{?_isa} >= 2
BuildRequires:	globus-xio-devel%{?_isa} >= 3
BuildRequires:	globus-gss-assist-devel%{?_isa} >= 8
BuildRequires:	globus-core%{?_isa} >= 8
BuildRequires:	globus-gsi-sysconfig-devel%{?_isa} >= 5
BuildRequires:	globus-callout-devel%{?_isa} >= 2
BuildRequires:	globus-gram-job-manager-callout-error-devel%{?_isa} >= 2
BuildRequires:	globus-gram-protocol-devel%{?_isa} >= 11
BuildRequires:	globus-common-devel%{?_isa} >= 14
BuildRequires:	globus-usage-devel%{?_isa} >= 3
BuildRequires:	globus-rsl-devel%{?_isa} >= 9
BuildRequires:	globus-gass-cache-devel%{?_isa} >= 8
BuildRequires:	libxml2-devel%{?_isa} >= 2.6.11
BuildRequires:	globus-gass-transfer-devel%{?_isa} >= 7
BuildRequires:	globus-gram-protocol-doc >= 11
BuildRequires:	globus-common-doc >= 14
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

%patch9 -p0
%patch11 -p0
%patch13 -p0
%patch14 -p0
%patch16 -p0
%patch19 -p0
%patch20 -p0
%patch21 -p0
%patch22 -p0
%patch23 -p0
%patch24 -p0
%patch25 -p0
%patch26 -p0

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache

aclocal_includes="-I ." %{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} --enable-doxygen \
           --%{docdiroption}=%{_docdir}/%{name}-%{version} \
           --disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages

# Move client and server man pages to main package
grep '.[18]$' $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  >> $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist
sed '/.[18]$/d' -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Move documentation to default RPM location

# Fix doxygen glitches
for f in man3/globus_gram_job_manager_configuration.3 \
	 man3/globus_gram_job_manager_job_execution_environment.3 \
	 man3/globus_gram_job_manager_rsl_validation_file.3 \
	 man5/rsl.5 ; do
  sed 's/P\.RS/P\n.RS/' -i $RPM_BUILD_ROOT%{_mandir}/$f
done

# Remove unwanted documentation (needed for RHEL4)
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*_%{_name}-%{version}_*.3
sed -e '/_%{_name}-%{version}_.*\.3/d' \
  -i $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist

# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_dev.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_rtl.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' \
  | sed -e s!^%{_prefix}/etc!/etc!  > package.filelist

cat $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
  | sed -e 's!/man/.*!&*!' -e 's!^!%doc %{_prefix}!' > package-doc.filelist

# Add logging
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/globus
cat %{SOURCE1} >> $RPM_BUILD_ROOT%{_sysconfdir}/globus/globus-gram-job-manager.conf

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/globus
chmod 01777 $RPM_BUILD_ROOT%{_localstatedir}/log/globus 

# Add log rotation
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
cp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/globus-gram-job-manager

%clean
rm -rf $RPM_BUILD_ROOT

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}
%dir %{_localstatedir}/lib/globus/gram_job_state
%dir %{_localstatedir}/log/globus
%config(noreplace) %{_sysconfdir}/globus/globus-gram-job-manager.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/globus-gram-job-manager
%config(noreplace) %{_datadir}/globus/globus_gram_job_manager/globus-gram-job-manager.rvf

%files doc -f package-doc.filelist
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}/html

%changelog
* Tue Nov 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.5-11
- Added patch to fix logfiles with garbage names getting created (GRAM-275)

* Mon Nov 21 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.5-10
- Enabled logging by default.

* Mon Nov 21 2011 Alain Roy <roy@cs.wisc.edu> - 13.5-9
- Added patch to fix lock confusion (update to fix from -8)
- Added patch to fix security context memory leak. 
- Configure logging

* Sat Nov 19 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-8
- If holding the wrong lock file, make sure to close the fd.

* Sun Nov 13 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-7
- Reduce the polling frequency and load of the condor job manager.

* Fri Nov 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-6
- Make job home different from job lock dir.

* Wed Nov 09 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-5
- No longer reload Condor logfiles every 5 seconds.

* Wed Nov 09 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 13.5-4
- Fix the globus-job-dir option in the job manager.

* Thu Oct 27 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.5-3
- Merged upstream 13.5-2:

* Mon Oct 24 2011 Joseph Bester <bester@mcs.anl.gov> - 13.5-2
- set aclocal_includes="-I ." prior to bootsrap

* Thu Oct 20 2011 Joseph Bester <bester@mcs.anl.gov> - 13.5-1
- GRAM-227: Manager double-locked

* Tue Oct 18 2011 Joseph Bester <bester@mcs.anl.gov> - 13.4-1
- GRAM-262: job manager -extra-envvars implementation doesn't match description

* Tue Oct 11 2011 Joseph Bester <bester@mcs.anl.gov> - 13.3-2
- Add explicit dependencies on >= 5.2 libraries

* Tue Oct 04 2011 Alain Roy <roy@cs.wisc.edu> - 13.3-2
- Merged upstream 13.3-1 with our patches

* Tue Oct 04 2011 Joseph Bester <bester@mcs.anl.gov> - 13.3-1
- GRAM-240: globus_xio_open in script code can recurse

* Fri Sep 23 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.2-2
- Merged upstream 13.2-1:

* Thu Sep 22 2011  <bester@mcs.anl.gov> - 13.2-1
- GRAM-257: Set default values for GLOBUS_GATEKEEPER_*

* Thu Sep 22 2011 Joseph Bester <bester@mcs.anl.gov> - 13.1-1
- Fix: GRAM-250

* Tue Sep 06 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 13.0-3
- Merged upstream 13.0-2:
    * Thu Sep 01 2011 Joseph Bester <bester@mcs.anl.gov> - 13.0-2
    - Update for 5.1.2 release

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 12.10-2
- Forward-port OSG patches.

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
