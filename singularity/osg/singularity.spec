# 
# Copyright (c) 2017-2018, SyLabs, Inc. All rights reserved.
# Copyright (c) 2017, SingularityWare, LLC. All rights reserved.
#
# Copyright (c) 2015-2017, Gregory M. Kurtzer. All rights reserved.
# 
# Copyright (c) 2016, The Regents of the University of California, through
# Lawrence Berkeley National Laboratory (subject to receipt of any required
# approvals from the U.S. Dept. of Energy).  All rights reserved.
# 
# This software is licensed under a customized 3-clause BSD license.  Please
# consult LICENSE file distributed with the sources of this project regarding
# your rights to use or distribute this software.
# 
# NOTICE.  This Software was developed under funding from the U.S. Department of
# Energy and the U.S. Government consequently retains certain rights. As such,
# the U.S. Government has been granted for itself and others acting on its
# behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software
# to reproduce, distribute copies to the public, prepare derivative works, and
# perform publicly and display publicly, and to permit other to do so. 
# 
# 


%{!?_rel:%{expand:%%global _rel 1}}

Summary: Application and environment virtualization
Name: singularity
Version: 2.5.1.999
Release: %{_rel}%{?dist}
# https://spdx.org/licenses/BSD-3-Clause-LBNL.html
License: BSD-3-Clause-LBNL
Group: System Environment/Base
URL: http://singularity.lbl.gov/
Source: %{name}-%{version}.tar.gz
ExclusiveOS: linux
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{name}-%{version}-%{release}-root
BuildRequires: python
BuildRequires: libarchive-devel
%if "%{_target_vendor}" == "suse"
Requires: squashfs
%else
Requires: squashfs-tools
%endif

Requires: %{name}-runtime = %{version}-%{release}

%description
Singularity provides functionality to make portable
containers that can be used across host environments.

%package devel
Summary: Development libraries for Singularity
Group: System Environment/Development

%description devel
Development files for Singularity

%package runtime
Summary: Support for running Singularity containers
Group: System Environment/Base

%description runtime
This package contains support for running containers created
by the %{name} package.

%prep
%setup


%build
if [ ! -f configure ]; then
  ./autogen.sh
fi

%configure
%{__make} %{?mflags}


%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
rm -f $RPM_BUILD_ROOT/%{_libdir}/singularity/lib*.la

%post runtime -p /sbin/ldconfig
%postun runtime -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc examples CONTRIBUTORS.md CONTRIBUTING.md COPYRIGHT.md INSTALL.md LICENSE-LBNL.md LICENSE.md README.md
%attr(0755, root, root) %dir %{_sysconfdir}/singularity
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/singularity/*

%{_libexecdir}/singularity/cli/apps.*
%{_libexecdir}/singularity/cli/bootstrap.*
%{_libexecdir}/singularity/cli/build.*
%{_libexecdir}/singularity/cli/check.*
%{_libexecdir}/singularity/cli/create.*
%{_libexecdir}/singularity/cli/image.*
%{_libexecdir}/singularity/cli/inspect.*
%{_libexecdir}/singularity/cli/mount.*
%{_libexecdir}/singularity/cli/pull.*
%{_libexecdir}/singularity/cli/selftest.*
%{_libexecdir}/singularity/helpers
%{_libexecdir}/singularity/python

# Binaries
%{_libexecdir}/singularity/bin/builddef
%{_libexecdir}/singularity/bin/cleanupd
%{_libexecdir}/singularity/bin/get-section
%{_libexecdir}/singularity/bin/mount
%{_libexecdir}/singularity/bin/image-type
%{_libexecdir}/singularity/bin/prepheader
%{_libexecdir}/singularity/bin/docker-extract

# Directories
%{_libexecdir}/singularity/bootstrap-scripts

#SUID programs
%attr(4755, root, root) %{_libexecdir}/singularity/bin/mount-suid

%files runtime
%dir %{_libexecdir}/singularity
%dir %{_localstatedir}/singularity
%dir %{_localstatedir}/singularity/mnt
%dir %{_localstatedir}/singularity/mnt/session
%dir %{_localstatedir}/singularity/mnt/container
%dir %{_localstatedir}/singularity/mnt/overlay
%dir %{_localstatedir}/singularity/mnt/final
%{_bindir}/singularity
%{_bindir}/run-singularity
%{_libdir}/singularity/lib*.so.*
%{_libexecdir}/singularity/cli/action_argparser.*
%{_libexecdir}/singularity/cli/exec.*
%{_libexecdir}/singularity/cli/help.*
%{_libexecdir}/singularity/cli/instance.*
%{_libexecdir}/singularity/cli/run.*
%{_libexecdir}/singularity/cli/shell.*
%{_libexecdir}/singularity/cli/test.*
%{_libexecdir}/singularity/bin/action
%{_libexecdir}/singularity/bin/start
%{_libexecdir}/singularity/bin/docker-extract
%{_libexecdir}/singularity/functions
%{_libexecdir}/singularity/handlers
%{_libexecdir}/singularity/image-handler.sh
%dir %{_sysconfdir}/singularity
%config(noreplace) %{_sysconfdir}/singularity/*
%{_mandir}/man1/singularity.1*
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/singularity

#SUID programs
%attr(4755, root, root) %{_libexecdir}/singularity/bin/action-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/start-suid

%files devel
%defattr(-, root, root)
%{_libdir}/singularity/lib*.so
%{_libdir}/singularity/lib*.a
%{_includedir}/singularity/*.h


%changelog
* Fri Jun 29 2018 Dave Dykstra <dwd@fnal.gov> 2.5.1.999-1
- Test build of 2.5.2-rc2

* Tue Jun 26 2018 Dave Dykstra <dwd@fnal.gov> 2.5.1.99-1
- Test build of 2.5.2-rc1

* Thu Jun 14 2018 Dave Dykstra <dwd@fnal.gov> 2.5.1-3.underlay
- Scratch build with development-2.x branch and the underlay PR #1638

* Tue May 29 2018 Edgar Fajardo <emfajard@ucsd.edu> 2.5.1-2
- Add PR #1525 patch SOFTWARE-3230

* Thu May 03 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.1-1
- Package upstream release for OSG
- Remove PR #1491 patch

* Sat Apr 28 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.0-1.1
- Add PR #1491

* Fri Apr 27 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.0-1
- Package upstream release for OSG.  No changes beside this log entry.

* Sat Apr 07 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.6-1
- Package upstream release for OSG.  No changes beside this log entry.

* Wed Apr 04 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.5-1.3
- Rebuild with final PR #1436

* Tue Apr 03 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.5-1.2
- Apply patch from simpler PR #1436 instead

* Fri Mar 30 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.4.5-1.1
- Apply patch from PR #1424

* Tue Mar 20 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.5
- Package upstream release for OSG.  No changes beside this log entry.

* Wed Mar 07 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.4
- Package upstream release for OSG.  No changes beside adding the changelog.

* Tue Mar 06 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.3
- Package for OSG.  No changes other than this log entry.
- Restore log entries from previous releases

* Tue Dec 05 2017 Dave Dykstra <dwd@fnal.gov> - 2.4.2
- Package for OSG.  No changes other than this log entry.

* Wed Nov 22 2017 Dave Dykstra <dwd@fnal.gov> - 2.4.1
 - Package for OSG.  No changes other than this log entry.

* Thu Oct 12 2017 Dave Dykstra <dwd@fnal.gov> - 2.4
 - Package for OSG.  No changes other than this log entry.

* Tue Sep 5 2017 Edgar Fajardo <emfajard@ucsd.edu> 2.3.1-0.1.4
- Added pathc for singularity on el6.

* Wed Aug 2 2017 Edgar Fajardo <emfajard@ucsd.edu> 2.3.1-0.1.3
- Split the package bit into the runtime and main (SOFTWARE-2755)
- Update to upstream's singularity-2.3.1-0.1 singularity.spec

* Thu Jun  1 2017 Dave Dykstra <dwd@fnal.gov> - 2.3-0.1
- Update to upstream's singularity-2.3-0.1 singularity.spec

* Tue Feb 14 2017 Derek Weitzel <dweitzel@cse.unl.edu> - 2.2.1-1
- Packaging bug release version of Singularity 2.2.1

* Thu Nov 10 2016 Derek Weitzel <dweitzel@cse.unl.edu> - 2.2-1
- First packaging of Singularity 2.2 for OSG

