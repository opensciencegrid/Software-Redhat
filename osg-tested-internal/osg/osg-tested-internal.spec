Name:      osg-tested-internal
Summary:   All OSG packages we test (internal use only)
Version:   1
Release:   7%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


################################################################################
#
# RHEL 5
#
################################################################################
%if 0%{?rhel} < 6
Requires: edg-mkgridmap
Requires: glexec
Requires: osg-ce-condor
Requires: osg-se-bestman
Requires: osg-se-bestman-xrootd
Requires: osg-voms
Requires: rsv
Requires: yum-utils
Requires: osg-configure-tests
Requires: torque-server
Requires: torque-mom
Requires: torque-client
Requires: torque-scheduler
Requires: osg-ce-pbs
%endif

################################################################################
#
# RHEL 6
#
################################################################################
%if 0%{?rhel} == 6
Requires: edg-mkgridmap
Requires: glexec
Requires: osg-ce-condor
Requires: osg-se-bestman
Requires: osg-se-bestman-xrootd
Requires: osg-voms
Requires: rsv
Requires: yum-utils
Requires: osg-configure-tests
Requires: torque-server
Requires: torque-mom
Requires: torque-client
Requires: torque-scheduler
Requires: osg-ce-pbs
%endif


%description
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Thu May 17 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-7
- Add osg-configure-tests and pbs/torque rpms

* Tue Apr 24 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-6
- Add osg-se-bestman-xrootd, rsv

* Mon Apr 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-5
- bestman2-* packages replaced with osg-se-bestman

* Mon Apr 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-4
- Added all packages we test on RHEL 5 to RHEL 6, now that they're ready
- Added bestman2

* Fri Apr 06 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-3
- Removed lfc-python from list; has depsolver issues
- Added yum-utils

* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-2
- Removed multilib testing of lfc-python* from RHEL 5
- Fixed syntax for multilib testing of lfc-python for RHEL 6

* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-1
- Created

