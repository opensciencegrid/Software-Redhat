# Create a macro to conditionalize based on systemd
%if %{?fedora}%{!?fedora:0} >= 17 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

%define zookeeper_version 3.4.3+15
%define zookeeper_patched_version 3.4.3-cdh4.0.1
%define zookeeper_base_version 3.4.3
%define zookeeper_release 1.cdh4.0.1.p0.4%{?dist}
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

%if  %{?suse_version:1}0

# Only tested on openSUSE 11.4. le'ts update it for previous release when confirmed
%if 0%{suse_version} > 1130
%define suse_check \# Define an empty suse_check for compatibility with older sles
%endif

# SLES is more strict anc check all symlinks point to valid path
# But we do point to a hadoop jar which is not there at build time
# (but would be at install time).
# Since our package build system does not handle dependencies,
# these symlink checks are deactivated
%define __os_install_post \
    %{suse_check} ; \
    /usr/lib/rpm/brp-compress ; \
    %{nil}


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
License: APL2
Source0: %{name}-%{zookeeper_patched_version}.tar.gz
Source1: do-component-build
Source2: install_zookeeper.sh
Source3: zookeeper-server.sh
Source4: zookeeper-server.sh.suse
Source5: zookeeper.1
Source6: zoo.cfg

# EL 7: tmpfiles.d configuration for the /run directory
Source7: %{name}-tmpfiles.conf

BuildArch: noarch
BuildRequires: ant, autoconf, automake

#ADDED BY OSG
%if 0%{?rhel} > 6
BuildRequires: maven >= 3
%else
BuildRequires: maven3
%endif
BuildRequires: java7-devel
BuildRequires: jpackage-utils
BuildRequires: /usr/lib/java-1.7.0
BuildRequires: /bin/hostname
Patch0: mvn304.patch

Requires(pre): coreutils, shadow-utils, /usr/sbin/groupadd, /usr/sbin/useradd
Requires(post): %{alternatives_dep}
Requires(preun): %{alternatives_dep}
Requires: bigtop-utils
Requires: java7
Requires: jpackage-utils
Requires: /usr/lib/java-1.7.0
Conflicts: hadoop-zookeeper

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
Provides: %{svc_zookeeper}
Requires: %{name} = %{version}-%{release}
Requires(post): %{chkconfig_dep}
Requires(preun): %{service_dep}, %{chkconfig_dep}
BuildArch: noarch

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
Requires: redhat-lsb
%endif


%description server
This package starts the zookeeper server on startup

%prep
%setup -n %{name}-%{zookeeper_patched_version}

#Changes needed to do-component-build
cp %{SOURCE1} .
%if 0%{?rhel} < 7
%patch0 -p0
%endif

%build
env FULL_VERSION=%{zookeeper_patched_version} bash do-component-build

%install
%__rm -rf $RPM_BUILD_ROOT
cp $RPM_SOURCE_DIR/zookeeper.1 $RPM_SOURCE_DIR/zoo.cfg .
sh %{SOURCE2} \
          --build-dir=build/%{name}-%{zookeeper_patched_version} \
          --doc-dir=%{doc_zookeeper} \
          --prefix=$RPM_BUILD_ROOT


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
getent passwd zookeeper > /dev/null || useradd -c "ZooKeeper" -s /sbin/nologin -g zookeeper -r -d %{run_zookeeper} zookeeper 2> /dev/null || :

%__install -d -o zookeeper -g zookeeper -m 0755 %{log_zookeeper}

# Manage configuration symlink
%post
%{alternatives_cmd} --install %{etc_zookeeper}/conf %{name}-conf %{etc_zookeeper}/conf.dist 30
%__install -d -o zookeeper -g zookeeper -m 0755 %{vlb_zookeeper}

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
%defattr(-,root,root)
%config(noreplace) %{etc_zookeeper}/conf.dist
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

%changelog
* Fri Dec 23 2016 Tim Cartwright <cat@cs.wisc.edu> 3.4.3+15-1.cdh4.0.1.p0.4
- EL 7: Add tmpfiles configuration to manage /run/zookeeper (SOFTWARE-2511)
- Own the (/var)?/run directory that the pre scriptlet makes (SOFTWARE-2511)
- Correct hostname build requirement to use /bin/hostname

* Tue Sep 16 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.4.3+15-1.cdh4.0.1.p0.3
- Use system maven on EL 7 (SOFTWARE-1541)

* Thu May 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.4.3+15-1.cdh4.0.1.p0.2
- Rebuild with java 7 / changed dependencies to java 7
