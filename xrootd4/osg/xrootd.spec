#-------------------------------------------------------------------------------
# Package definitions
#-------------------------------------------------------------------------------
Name:      xrootd4
Epoch:     1
Version:   4.0.4
Release:   1.2%{?dist}%{?_with_cpp11:.cpp11}%{?_with_clang:.clang}
Summary:   Extended ROOT file server
Group:     System Environment/Daemons
License:   LGPLv3+
URL:       http://xrootd.org/

	
Requires:	  %{name}-libs        = %{epoch}:%{version}-%{release}
Requires:	  %{name}-client-libs = %{epoch}:%{version}-%{release}
Requires:	  %{name}-server-libs = %{epoch}:%{version}-%{release}
#Conflicts:  xrootd
#Added the conflicts statements to prevent old plugins from using xroot4 rpms
#Obsoletes: xrootd < 1:4.0.0
Provides: xrootd4 = %{epoch}:%{version}-%{release}
Provides: xrootd4-server = %{epoch}:%{version}-%{release}

Requires: xrootd >= %{epoch}:4.1.1-1




%description
An empty shim package to provide a clean upgrade path to >=xrootd-4.1.1


#-------------------------------------------------------------------------------
# libs
#-------------------------------------------------------------------------------
%package libs
Summary:	Requires xrootd-libs>=4.1.1 and provides xrootd4-libs
Group:		System Environment/Libraries
#Conflicts: xrootd-libs
#Obsoletes: xrootd-libs < 1:4.0.0
Provides: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: xrootd-libs >= %{epoch}:4.1.1-1

%description libs
This shim package requries xrootd-libs>= 4.1.1 and provides xrootd4-libs


#-------------------------------------------------------------------------------
# devel
#------------------------------------------------------------------------------
%package devel
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		Development/Libraries
#Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Conflicts: xrootd-devel
#Obsoletes: xrootd-devel < 1:4.0.0
Provides: %{name}-devel = %{epoch}:%{version}-%{release}
Requires: xrootd-devel >=  %{epoch}:4.1.1-1
%description devel
This shim package requries xrootd-libs>= 4.1.1 and provides xrootd4-libs


#-------------------------------------------------------------------------------
# client-libs
#-------------------------------------------------------------------------------
%package client-libs
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Conflicts: xrootd-client-libs
#Obsoletes: xrootd-client-libs < 1:4.0.0
Provides: %{name}-client-libs = %{epoch}:%{version}-%{release}
Requires: xrootd-client-libs >= %{epoch}:4.1.1-1
%description client-libs
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# client-devel
#-------------------------------------------------------------------------------
%package client-devel
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		Development/Libraries
#Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
#Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Conflicts: xrootd-client-devel
#Obsoletes: xrootd-client-devel < 1:4.0.0
Provides: %{name}-client-devel = %{epoch}:%{version}-%{release}
Requires: xrootd-client-libs >= %{epoch}:4.1.1-1
%description client-devel
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# server-libs
#-------------------------------------------------------------------------------
%package server-libs
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		System Environment/Libraries
#Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Conflicts: xrootd-server-libs
#Obsoletes: xrootd-server-libs < 1:4.0.0
Provides: %{name}-server-libs = %{epoch}:%{version}-%{release}
Requires: xrootd-server-libs  >= %{epoch}:4.1.1-1
%description server-libs
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# server-devel
#-------------------------------------------------------------------------------
%package server-devel
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Conflicts: xrootd-server-devel
#Obsoletes: xrootd-server-devel < 1:4.0.0
Provides: %{name}-server-devel = %{epoch}:%{version}-%{release}
Requires: xrootd-server-devel >= %{epoch}:4.1.1-1
%description server-devel
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# private devel
#-------------------------------------------------------------------------------
%package private-devel
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		Development/Libraries
#Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
#%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
###BuildArch:	noarch
#%endif
#Conflicts: xrootd-private-devel
#Obsoletes: xrootd-private-devel < 1:4.0.0
Provides: %{name}-private-devel = %{epoch}:%{version}-%{release}
Requires: xrootd-private-devel >= %{epoch}:4.1.1-1

%description private-devel
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# client
#-------------------------------------------------------------------------------
%package client
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		Applications/Internet
#Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Obsoletes: xrootd-client < 1:4.0.0
Provides: %{name}-client = %{epoch}:%{version}-%{release}
Requires: xrootd-client >= %{epoch}:4.1.1-1

%description client
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# fuse
#-------------------------------------------------------------------------------
%package fuse
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		Applications/Internet
#Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
#Requires:	fuse
#Conflicts: xrootd-fuse
#Obsoletes: xrootd-fuse < 1:4.0.0
Provides: %{name}-fuse = %{epoch}:%{version}-%{release}
Requires: xrootd-fuse >= %{epoch}:4.1.1-1

%description fuse
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# doc
#-------------------------------------------------------------------------------
%package doc
Summary:	Requires xrootd>=4.1.1 and provides xrootd4
Group:		Documentation
#%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
###BuildArch:	noarch
#%endif
Provides: %{name}-doc = %{epoch}:%{version}-%{release}
Requires: xrootd-doc >= %{epoch}:4.1.1-1

%description doc
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# selinux
#-------------------------------------------------------------------------------
%package selinux
Summary:	 Requires xrootd>=4.1.1 and provides xrootd4
Group:		 System Environment/Base
#%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
###BuildArch: noarch
#%endif
#Requires:  policycoreutils
#Requires:  selinux-policy-targeted
Provides: %{name}-selinux = %{epoch}:%{version}-%{release}
Requires: xrootd-selinux >= %{epoch}:4.1.1-1
%description selinux
This shim package Requires xrootd>=4.1.1 and provides xrootd4.

#-------------------------------------------------------------------------------
# tests
#-------------------------------------------------------------------------------
#%if %{?_with_tests:1}%{!?_with_tests:0}
%package tests
Summary: Requires xrootd>=4.1.1 and provides xrootd4
Group:   Development/Tools
#Requires: %{name}-client = %{epoch}:%{version}-%{release}
Provides: %{name}-tests = %{epoch}:%{version}-%{release}
Requires: xrootd-tests >= %{epoch}:4.1.1-1
%description tests
This shim package Requires xrootd>=4.1.1 and provides xrootd4.
#%endif

#-------------------------------------------------------------------------------
# Build instructions
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Installation
#-------------------------------------------------------------------------------
%install

%clean
rm -rf $RPM_BUILD_ROOT

#-------------------------------------------------------------------------------
# Files
#-------------------------------------------------------------------------------
%files
%files libs
%files devel
%files client-libs
%files client-devel
%files server-libs
%files server-devel
%files private-devel
%files client
%files fuse
%files doc
%files tests
%files selinux


#-------------------------------------------------------------------------------
# Changelog
#-------------------------------------------------------------------------------
%changelog
* Fri Feb 20 2015 Edgar Fajardo <emfajard@ucsd.edu> - 4.0.4-1.2
- Turned into an empty shim package

* Wed Oct 22 2014 Jose Caballero <jcaballero@BNL.gov> - 4.0.4-1.1
- Bumped to 4.0.4-1 

* Tue Sep 09 2014 Jose Caballero <jcaballero@BNL.gov> - 4.0.3-1.2
  Updated release number to -1.2 

* Mon Aug 04 2014 Jose Caballero <jcaballero@BNL.gov> - 4.0.3-1.1
- Bumped to 4.0.3-1 

* Thu Jul 31 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-1.9
- Removed the conflicts statements in the subpackages and added a general one

* Wed Jul 30 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-1.6
- Added some conflicts statements.

* Mon Jul 28 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-1.5
- Added some provides statements to the subpackages.

* Fri Jul 11 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-1.4
- Added some obsoletes and provides statement from the hcc build

* Thu Jun 5 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-1.1
- First packaging of the official release 4.0.0

* Fri May 16 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:4.0.0-3.rc1
- First package on the osg repo of xrootd4. Release candidate 1.
- Added the conflict statements for the xrootd plugins version not yet build with xrootd4.

* Tue Apr 01 2014 Lukasz Janyst <ljanyst@cern.ch>
- correct the license field (LGPLv3+)
- rename to xrootd4
- add 'conflicts' statements
- remove 'provides' and 'obsoletes'

* Mon Mar 31 2014 Lukasz Janyst <ljanyst@cern.ch>
- Add selinux policy

* Fri Jan 24 2014 Lukasz Janyst <ljanyst@cern.ch>
- Import XrdHttp

* Fri Jun 7 2013 Lukasz Janyst <ljanyst@cern.ch>
- adopt the EPEL RPM layout by Mattias Ellert

* Tue Apr 2 2013 Lukasz Janyst <ljanyst@cern.ch>
- remove perl

* Thu Nov 1 2012 Justin Salmon <jsalmon@cern.ch>
- add tests package

* Fri Oct 21 2011 Lukasz Janyst <ljanyst@cern.ch> 3.1.0-1
- bump the version to 3.1.0

* Mon Apr 11 2011 Lukasz Janyst <ljanyst@cern.ch> 3.0.3-1
- the first RPM release - version 3.0.3
- the detailed release notes are available at:
  http://xrootd.org/download/ReleaseNotes.html
