Name:      osg-tested-internal
Summary:   All OSG packages we test (internal use only)
Version:   1
Release:   2%{?dist}
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
Requires: lfc-python
Requires: lfc-python26
Requires: osg-ce-condor
Requires: osg-voms
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

# lfc-python*: want to test multilib so installing both arches if we are running on x86_64
%ifarch x86_64
Requires: lfc-python(x86-64)
%endif
Requires: lfc-python(x86-32)

%endif


%description
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-2
- Removed multilib testing of lfc-python* from RHEL 5
- Fixed syntax for multilib testing of lfc-python for RHEL 6

* Thu Apr 05 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-1
- Created

