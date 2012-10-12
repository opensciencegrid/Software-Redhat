Name:		blahp
Version:	1.18.0.4
Release:	8%{?dist}
Summary:	gLite BLAHP daemon

Group:		System/Libraries
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.ce.blahp
# Retrieved on May 28 2012
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.ce.blahp.tar.gz?view=tar&pathrev=glite-ce-blahp_R_1_18_0_4
Source0:        org.glite.ce.blahp.tar.gz
# Retrieved on May 31 2012
# https://github.com/bbockelm/condor-ce/blob/master/src/pbs_status.py
Source1:        pbs_status.py
Patch0:         blahp_fedora.patch
# Config file patches from Condor.
#Patch1:         blahp.dl.patch
Patch2:         blahp.mtrace.patch
Patch3:         blahp.add-sge.patch
Patch4:         blahp.config-paths.patch
Patch5:         blahp.pbs-completion.patch
Patch6:         blahp.registry.patch
Patch7:         blahp.shared-fs.patch
Patch8:         blahp_chkconfig.patch
# Fix path to blparser_master and related binaries in init scripts
Patch9:         blahp_init_script_paths.patch
# Add values for using Condor as a jobmanager to the blah.config
Patch10:        blahp_condor_config.patch
# Allow blahp to handle relative proxy paths.  See Condor GT #3027
Patch11:		blahp-relative-proxypath.patch
# Blahp fails to escape some character sequences Condor jobs may use.
Patch12:        blahp.escape.args.patch
# Blahp uses a function which has been removed from newer versions of Condor ClassAds.
Patch13:        blahp.iclassad.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  glite-build-common-cpp
BuildRequires:  condor-classads-devel
BuildRequires:  globus-gss-assist-devel
BuildRequires:  globus-gsi-credential-devel
BuildRequires:  globus-gsi-proxy-core-devel
BuildRequires:  globus-gsi-cert-utils-devel
BuildRequires:  docbook-style-xsl, libxslt

#Requires(post):         chkconfig
#Requires(preun):        chkconfig
#Requires(preun):        initscripts
#Requires(postun):       initscripts

%description
%{summary}

%prep
%setup -n org.glite.ce.blahp

%patch0 -p0
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p0
%patch12 -p0
%patch13 -p0

cp %{SOURCE0} src/scripts/pbs_status.sh

%build
./bootstrap
export CPPFLAGS="-I/usr/include/classad"
export LDFLAGS="-lclassad"
%configure --with-classads-prefix=/usr --with-globus-prefix=/usr --with-glite-location=/usr
unset CPPFLAGS
unset LDFLAGS
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# Move all the blahp scripts into /usr/libexec/blahp
mkdir blahp
mv $RPM_BUILD_ROOT%{_libexecdir}/* blahp
install -m 0755 -d -p $RPM_BUILD_ROOT%{_libexecdir}/blahp/
mv blahp/* $RPM_BUILD_ROOT%{_libexecdir}/blahp/

# Correct the config file location
install -m 0755 -d -p $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{_sysconfdir}/blah.config.template $RPM_BUILD_ROOT%{_sysconfdir}/blah.config
mv $RPM_BUILD_ROOT%{_sysconfdir}/blparser.conf.template $RPM_BUILD_ROOT%{_sysconfdir}/blparser.conf
echo "blah_libexec_directory=/usr/libexec/blahp" >> $RPM_BUILD_ROOT%{_sysconfdir}/blah.config

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ $1 -eq 1 ] ; then
    /sbin/chkconfig --add glite-ce-blah-parser
fi

%preun

if [ $1 -eq 0 ] ; then
    /sbin/service glite-ce-blah-parser stop >/dev/null 2>&1
    /sbin/chkconfig --del glite-ce-blah-parser
fi

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/blahp
%{_docdir}/glite*
%config(noreplace) %{_sysconfdir}/blparser.conf
%config(noreplace) %{_sysconfdir}/blah.config
%{_mandir}/man1/*
%{_initrddir}/glite-ce-*

%changelog
* Fri Oct 12 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.18.0.4-8.osg
- Pull in all remaining patches from the OSG-CE work.
- Fix non-standard qstat locations.
- Fix arg escaping in Condor.
- Fix submissions with a relative proxy path.
- Release bumped a few extra versions to stay in line with the Caltech Koji.

* Thu Aug 29 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.18.0.4-5.osg
- Fixed paths in init script
- Added default options for condor

* Wed Jul 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.18.0.4-4.osg
- Disable autostart of blah parser

* Thu May 31 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.18.0.4-3
- Add caching for PBS script.

* Mon May 28 2012 Brian Bockelman <bbockelm@cse.unl.edu> -1.18.0.4-2
- Import patches from Condor team.

* Mon May 28 2012 Brian Bockelman <bbockelm@cse.unl.edu> -1.18.0.4-1
- Update to latest upstream.

* Fri Sep 16 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.16.1-3
- Rev bump for GT 5.2 recompile.

* Wed Jan 05 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.16.1-1
- Initial RPM packaging

