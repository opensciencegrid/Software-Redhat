Name:      osg-tested-internal
Summary:   All OSG packages we test (internal use only)
Version:   1
Release:   3%{?dist}
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
Requires: osg-voms
Requires: yum-utils
%endif

################################################################################
#
# RHEL 6
#
################################################################################
%if 0%{?rhel} == 6
Requires: glexec
Requires: globus-gridftp-server-progs
Requires: osg-wn-client
Requires: yum-utils
%endif


%description
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Fri Apr 06 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-3
- Removed lfc-python from list; has depsolver issues
- Added yum-utils

* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-2
- Removed multilib testing of lfc-python* from RHEL 5
- Fixed syntax for multilib testing of lfc-python for RHEL 6

* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-1
- Created

