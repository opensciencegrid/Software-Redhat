# Create a macro to conditionalize based on systemd
%if %{?fedora}%{!?fedora:0} >= 17 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

%define zookeeper_version 3.4.5+cdh5.14.2+142
%define zookeeper_patched_version 3.4.5-cdh5.14.2
%define zookeeper_base_version 3.4.5 
%define zookeeper_release 1.cdh5.14.2.p0.11.1%{?dist}
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
%define etc_zookeeper /etc/%{name}
%define bin_zookeeper %{_bindir}
%define lib_zookeeper /usr/lib/%{name}
%define log_zookeeper /var/log/%{name}

%if %{?use_systemd}
%define run_zookeeper /run/%{name}
%else
%define run_zookeeper /var/run/%{name}
%endif

%define vlb_zookeeper /var/lib/%{name}
%define svc_zookeeper %{name}-server
%define man_dir %{_mandir}

# Disabling the following scripts from running:
# symbol stripping - not relevant here.
# jar repacking - to save time.
# byte-compiling python code - not relevant here.
# brp-compress - not relevant here.
#              - This compresses man and info pages under
#                 ./usr/man/man* ./usr/man/*/man* ./usr/info \
#                 ./usr/share/man/man* ./usr/share/man/*/man* ./usr/share/info \
#                 ./usr/kerberos/man ./usr/X11R6/man/man* ./usr/lib/perl5/man/man* \
#                 ./usr/share/doc/*/man/man* ./usr/lib/*/man/man*
%define __os_install_post %{nil}

%if  %{?suse_version:1}0

%define doc_zookeeper %{_docdir}/%{name}
%define alternatives_cmd update-alternatives
%define alternatives_dep update-alternatives
%define chkconfig_dep    aaa_base
%define service_dep      aaa_base
%global initd_dir %{_sysconfdir}/rc.d

%else

%define doc_zookeeper %{_docdir}/%{name}-%{zookeeper_version}
%define alternatives_cmd alternatives
%define alternatives_dep chkconfig 
%define chkconfig_dep    chkconfig
%define service_dep      initscripts
%global initd_dir %{_sysconfdir}/rc.d/init.d

%endif



Name: zookeeper
Version: %{zookeeper_version}
Release: %{zookeeper_release}
Summary: A high-performance coordination service for distributed applications.
URL: http://zookeeper.apache.org/
Group: Development/Libraries
Buildroot: %{_topdir}/INSTALL/%{name}-%{version}
License: ASL 2.0
Source0: %{name}-%{zookeeper_patched_version}.tar.gz
Source1: do-component-build
Source2: install_zookeeper.sh
Source3: zookeeper-server.sh
Source4: zookeeper-server.sh.suse
Source5: zookeeper.1
Source6: zoo.cfg
Source7: zookeeper.default
Source8: packaging_functions.sh
Patch0: packaging_functions.patch

# EL 7: tmpfiles.d configuration for the /run directory
Source9: %{name}-tmpfiles.conf

BuildRequires: ant, autoconf, automake, cppunit-devel
%if %{?suse_version:1}0
Requires(pre): coreutils, pwdutils, /usr/sbin/groupadd, /usr/sbin/useradd
%else
Requires(pre): coreutils, shadow-utils, /usr/sbin/groupadd, /usr/sbin/useradd
%endif
Requires(post): %{alternatives_dep}
Requires(preun): %{alternatives_dep}
Requires: bigtop-utils >= 0.7
Requires: java >= 1:1.7.0
Requires: jpackage-utils
Conflicts: hadoop-zookeeper

#ADDED BY OSG
%if 0%{?rhel} > 6
BuildRequires: maven >= 3
%else
BuildRequires: maven3
%endif
BuildRequires: java-devel = 1:1.7.0
BuildRequires: jpackage-utils
BuildRequires: /usr/lib/java-1.7.0
BuildRequires: /bin/hostname
BuildRequires: libtool

%description 
ZooKeeper is a centralized service for maintaining configuration information, 
naming, providing distributed synchronization, and providing group services. 
All of these kinds of services are used in some form or another by distributed 
applications. Each time they are implemented there is a lot of work that goes 
into fixing the bugs and race conditions that are inevitable. Because of the 
difficulty of implementing these kinds of services, applications initially 
usually skimp on them ,which make them brittle in the presence of change and 
difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.  

%package server
Summary: The Hadoop Zookeeper server
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires(post): %{chkconfig_dep}
Requires(preun): %{service_dep}, %{chkconfig_dep}

%if  %{?suse_version:1}0
# Required for init scripts
Requires: insserv
%endif

%if  0%{?mgaversion}
# Required for init scripts
Requires: initscripts
%endif

# CentOS 5 does not have any dist macro
# So I will suppose anything that is not Mageia or a SUSE will be a RHEL/CentOS/Fedora
%if %{!?suse_version:1}0 && %{!?mgaversion:1}0
# Required for init scripts
Requires: /lib/lsb/init-functions
%endif


%description server
This package starts the zookeeper server on startup

%package native
Summary: C bindings for ZooKeeper clients
Group: Development/Libraries

%description native
Provides native libraries and development headers for C / C++ ZooKeeper clients. Consists of both single-threaded and multi-threaded implementations.

%prep
%setup -n %{name}-%{zookeeper_patched_version}
patch %{SOURCE8} %{PATCH0}

%build
%if 0%{?rhel} < 7
# use this mvn in do-component-build (Source1)
export PATH=/usr/share/apache-maven-3.0.4/bin:$PATH
%endif
export COMPONENT_HASH=8ba42f50f49cedf21dde09fccd232c5b2bae6a9b
env FULL_VERSION=%{zookeeper_patched_version} bash %{SOURCE1}

%install
cp $RPM_SOURCE_DIR/zookeeper.1 $RPM_SOURCE_DIR/zoo.cfg $RPM_SOURCE_DIR/zookeeper.default .
env FULL_VERSION=%{zookeeper_patched_version} bash %{SOURCE2} \
          --build-dir=build/%{name}-%{zookeeper_patched_version} \
          --doc-dir=%{doc_zookeeper} \
          --prefix=$RPM_BUILD_ROOT \
          --system-include-dir=%{_includedir} \
          --system-lib-dir=%{_libdir} \
          --source-dir=$RPM_SOURCE_DIR

%if  %{?suse_version:1}0
orig_init_file=%{SOURCE4}
%else
orig_init_file=%{SOURCE3}
%endif

%__install -d -m 0755 $RPM_BUILD_ROOT/%{initd_dir}/
init_file=$RPM_BUILD_ROOT/%{initd_dir}/%{svc_zookeeper}
%__cp $orig_init_file $init_file
chmod 755 $init_file

%if %{?use_systemd}
mkdir -p %{buildroot}%{_tmpfilesdir}
install -p -m 0644 %{SOURCE7} %{buildroot}%{_tmpfilesdir}/%{name}.conf
%endif

# Create the (/var)?/run/zookeeper directory in the package.  Note the %attr()
# directive below to set permissions, owner, and group.
mkdir -p %{buildroot}%{run_zookeeper}

%pre
getent group zookeeper >/dev/null || groupadd -r zookeeper
getent passwd zookeeper > /dev/null || useradd -c "ZooKeeper" -s /sbin/nologin -g zookeeper -r -d %{vlb_zookeeper} zookeeper 2> /dev/null || :

%__install -d -o zookeeper -g zookeeper -m 0755 %{log_zookeeper}
%__install -d -o zookeeper -g zookeeper -m 0755 %{vlb_zookeeper}

# Manage configuration symlink
%post
%{alternatives_cmd} --install %{etc_zookeeper}/conf %{name}-conf %{etc_zookeeper}/conf.dist 30

%preun
if [ "$1" = 0 ]; then
        %{alternatives_cmd} --remove %{name}-conf %{etc_zookeeper}/conf.dist || :
fi

%post server
	chkconfig --add %{svc_zookeeper}

%preun server
if [ $1 = 0 ] ; then
	service %{svc_zookeeper} stop > /dev/null 2>&1
	chkconfig --del %{svc_zookeeper}
fi

%postun server
if [ $1 -ge 1 ]; then
        service %{svc_zookeeper} condrestart > /dev/null 2>&1
fi

%files server
	%attr(0755,root,root) %{initd_dir}/%{svc_zookeeper}

#######################
#### FILES SECTION ####
#######################
%files
%config(noreplace) %{etc_zookeeper}/conf.dist
%config(noreplace) /etc/default/zookeeper
%{lib_zookeeper}
%{bin_zookeeper}/zookeeper-server
%{bin_zookeeper}/zookeeper-server-initialize
%{bin_zookeeper}/zookeeper-client
%{bin_zookeeper}/zookeeper-server-cleanup
%doc %{doc_zookeeper}
%{man_dir}/man1/zookeeper.1.*

%if %{?use_systemd}
%{_tmpfilesdir}/%{name}.conf
%endif

# The package should own the runtime directory.  Set the permissions, owner, and
# group here, because the owner/group do not exist until the pre scriptlet runs.
%dir %{run_zookeeper}
%attr(0755, %{name}, %{name}) %{run_zookeeper}

%files native
%defattr(-,root,root)
%{lib_zookeeper}-native
%{bin_zookeeper}/cli_*
%{bin_zookeeper}/load_gen*
%{_includedir}/zookeeper
%{_libdir}/*

%changelog
* Thu Jun 07 2018 Carl Edquist <edquist@cs.wisc.edu> - 3.4.5+cdh5.14.2+142-1.cdh5.14.2.p0.11.1
- Update to zookeeper 3.4.5 from CDH5 (SOFTWARE-3280)

* Thu Jan 25 2018 Carl Edquist <edquist@cs.wisc.edu> - 3.4.3+15-1.cdh4.0.1.p0.6
- Allow Java >= 1.7 (SOFTWARE-2993, SOFTWARE-2981)

* Thu Nov 02 2017 Carl Edquist <edquist@cs.wisc.edu> - 3.4.3+15-1.cdh4.0.1.p0.5
- Rename java7 dependencies (SOFTWARE-2991)

* Fri Dec 23 2016 Tim Cartwright <cat@cs.wisc.edu> 3.4.3+15-1.cdh4.0.1.p0.4
- EL 7: Add tmpfiles configuration to manage /run/zookeeper (SOFTWARE-2511)
- Own the (/var)?/run directory that the pre scriptlet makes (SOFTWARE-2511)
- Correct hostname build requirement to use /bin/hostname

* Tue Sep 16 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.4.3+15-1.cdh4.0.1.p0.3
- Use system maven on EL 7 (SOFTWARE-1541)

* Thu May 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.4.3+15-1.cdh4.0.1.p0.2
- Rebuild with java 7 / changed dependencies to java 7
