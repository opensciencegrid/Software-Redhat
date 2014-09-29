Name:		blahp
Version:	1.18.11.bosco
Release:	1%{?dist}
Summary:	gLite BLAHP daemon

Group:		System/Libraries
License:	Apache 2.0
URL:		https://github.com/osg-bosco/BLAH

# Tarball created with the following command:
# git archive v1_18_bosco | gzip -8 > ~/rpmbuild/SOURCES/blahp.tar.gz
Source0:        blahp.tar.gz

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
%setup -c -n %{name}-%{version}

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

install -m 0755 -d -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mv $RPM_BUILD_ROOT%{_libexecdir}/blahp/sge_local_submit_attributes.sh $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/sge_local_submit_attributes.sh
ln -s %{_sysconfdir}/%{name}/sge_local_submit_attributes.sh    $RPM_BUILD_ROOT%{_libexecdir}/blahp/sge_local_submit_attributes.sh


# Insert appropriate templates for LSF and HTCondor; admins will need to change these
for i in lsf condor; do
  ln -s %{_sysconfdir}/%{name}/${i}_local_submit_attributes.sh    $RPM_BUILD_ROOT%{_libexecdir}/blahp/${i}_local_submit_attributes.sh

cat > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/${i}_local_submit_attributes.sh << EOF
#/bin/sh

# This file is sourced by blahp before submitting the job to ${i}
# Anything printed to stdout is included in the submit file.
# For example, to set a default walltime of 24 hours in PBS, you
# could uncomment this line:

# echo "#PBS -l walltime=24:00:00"

# blahp allows arbitrary attributes to be passed to this script on a per-job
# basis.  If you add the following to your HTCondor-G submit file:

#+remote_cerequirements = NumJobs == 100 && foo = 5

# Then an environment variable, NumJobs, will be exported prior to calling this
# script and set to a value of 100.  The variable foo will be set to 5.

# You could allow users to set the walltime for the job with the following
# customization (PBS syntax given; adjust for the appropriate batch system):

#if [ -n "\$Walltime" ]; then
#  echo "#PBS -l walltime=\$Walltime"
#else
#  echo "#PBS -l walltime=24:00:00"
#fi

EOF
done

# A more appropriate template for PBS; actually does something
ln -s %{_sysconfdir}/%{name}/pbs_local_submit_attributes.sh    $RPM_BUILD_ROOT%{_libexecdir}/blahp/pbs_local_submit_attributes.sh

cat > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pbs_local_submit_attributes.sh << EOF
#/bin/sh

# This file is sourced by blahp before submitting the job to PBS
# Anything printed to stdout is included in the submit file.
# For example, to set a default walltime of 24 hours in PBS, you
# could uncomment this line:

# echo "#PBS -l walltime=24:00:00"

# blahp allows arbitrary attributes to be passed to this script on a per-job
# basis.  If you add the following to your HTCondor-G submit file:

#+remote_cerequirements = NumJobs == 100 && foo = 5

# Then an environment variable, NumJobs, will be exported prior to calling this
# script and set to a value of 100.  The variable foo will be set to 5.

# You could allow users to set the walltime for the job with the following
# customization (PBS syntax given; adjust for the appropriate batch system):

# Uncomment the else block to default to 24 hours of runtime; otherwise, the queue
# default is used.
if [ -n "\$Walltime" ]; then
  echo "#PBS -l walltime=\$Walltime"
#else
#  echo "#PBS -l walltime=24:00:00"
fi

EOF

mv $RPM_BUILD_ROOT%{_docdir}/glite-ce-blahp-@PVER@ $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/sge_local_submit_attributes.sh

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
%{_libexecdir}/%{name}
%{_docdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/blparser.conf
%config(noreplace) %{_sysconfdir}/blah.config
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.sh
%{_mandir}/man1/*
%{_initrddir}/glite-ce-*

%changelog
* Mon Sep 29 2014 Brian Lin <blin@cs.wisc.edu> - 1.18.11.bosco-1
- Fix bug in PBS status script

* Thu Sep 25 2014 Brian Lin <blin@cs.wisc.edu> - 1.18.10.bosco-1
- Fixes to LSF scripts pushed upstream (SOFTWARE-1589, creating a temp file in /tmp)
- Fix to PBS script that tracks job status (SOFTWARE-1594)

* Mon Aug 25 2014 Brian Lin <blin@cs.wisc.edu> - 1.18.9.bosco-2
- Fix for memory allocation failure when tracking LSF jobs (SOFTWARE-1589)

* Thu Jan 09 2014 Brian Bockelman <bbockelm@cse.unl.edu> - 1.18.9.bosco-1
- Fix proxy renewal in the case where no home directory exists.
- Improve packaging of local customization scripts and include defaults.
  These are now marked as config files and places in /etc.
- Change name of documentation directory to reflect RPM name.

* Tue Jan 07 2014 Brian Bockelman <bbockelm@cse.unl.edu> - 1.18.8.bosco-1
- Fixes from PBS testing.  Blahp now handles multiple arguments correctly
  and the wrapper script will remove the job proxy after it finishes.

* Wed Oct 30 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.18.7.bosco-2
- Bump to rebuild against condor-7.8.8-x (OSG-3.1) and condor-8.0.4-x (OSG 3.2)

* Fri Sep 20 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 1.18.7.bosco-1
- Do not close stderr fd from the blah.

* Tue May 14 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 1.18.5.bosco-1
- Alter the pbs_status.py locking algorithm to add random component to 
  sleeps between poll.

* Thu Jan 17 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 1.18.4.bosco-1
- Fixing pbs_status.py via upstream SOFTWARE-905

* Thu Dec 13 2012 Brian Bockelman <bbockelm@cse.unl.edu> 1.18.3.bosco-1.osg
- Merge BOSCO and OSG distribution of blahp.

* Fri Dec 05 2012 John Thiltges <jthiltges2@unl.edu> 1.18.0.4-9.osg
- Fix pbs_status.sh in spec file

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

