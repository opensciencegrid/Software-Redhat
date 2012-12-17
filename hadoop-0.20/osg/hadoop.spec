#
# Hadoop RPM spec file
#
%define hadoop_name hadoop
%define etc_hadoop /etc/%{name}
%define config_hadoop %{etc_hadoop}/conf
%define lib_hadoop_dirname /usr/lib
%define lib_hadoop %{lib_hadoop_dirname}/%{name}
%define log_hadoop_dirname /var/log
%define log_hadoop %{log_hadoop_dirname}/%{name}
%define bin_hadoop /usr/bin
%define man_hadoop /usr/share/man
%define doc_hadoop /usr/share/doc/%{name}
%define src_hadoop /usr/src/%{name}
%define hadoop_username mapred
%define hadoop_services namenode secondarynamenode datanode jobtracker tasktracker
# Hadoop outputs built binaries into %{hadoop_build}
%define hadoop_src_path $RPM_BUILD_DIR/hadoop-0.20.2
%define hadoop_build_path build/hadoop-%{version}
%define static_images_dir src/webapps/static/images
%define cloudera_version 0.20.2+737
%define apache_branch 0.20

%ifarch i386
%global hadoop_arch Linux-i386-32
%endif
%ifarch amd64 x86_64
%global hadoop_arch Linux-amd64-64
%endif
%ifarch noarch
%global hadoop_arch ""
%endif

# brp-repack-jars uses unzip to expand jar files
# Unfortunately aspectjtools-1.6.5.jar pulled by ivy contains some files and directories without any read permission
# and make whole process to fail.
# So for now brp-repack-jars is being deactivated until this is fixed.
# See CDH-2151
%define __os_install_post \
    /usr/lib/rpm/redhat/brp-compress ; \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} ; \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
%{nil}



# Even though we split the RPM into arch and noarch, it still will build and install
# the entirety of hadoop. Defining this tells RPM not to fail the build
# when it notices that we didn't package most of the installed files.
%define _unpackaged_files_terminate_build 0

# RPM searches perl files for dependancies and this breaks for non packaged perl lib
# like thrift so disable this
%define _use_internal_dependency_generator 0

Name: %{hadoop_name}-%{apache_branch}
Version: %{cloudera_version}
Release: 28%{?dist}
Summary: Hadoop is a software platform for processing vast amounts of data
License: Apache License v2.0
URL: http://hadoop.apache.org/core/
Group: Development/Libraries
Source0: hadoop-%{cloudera_version}.tar.gz
Source1: hadoop-init.tmpl
Source2: hadoop-init-nn.tmpl
Source3: hadoop-0.20.default
Source4: apache-forrest-0.8.tar.gz
Source5: hadoop-fuse.te
Patch0:  hadoop_20_forrest.patch
Patch1:  https://issues.apache.org/jira/secure/attachment/12473651/hdfs-780-4.patch
Patch2:  fuse_dfs_020_memleaks_v8.patch
# HADOOP-6813 is missing from latest HADOOP
# https://issues.apache.org/jira/secure/attachment/12446533/h-6813.patch
Patch3:  h-6813.patch
Patch4:  hadoop_fuse_dfs_classpath.patch
Patch5:  hadoop_fuse_dfs_libjvm.patch

Patch6:  hdfs-799-backport.patch
Patch7:  HDFS-2452.patch
Patch8:  hadoop-7154.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ant >= 1.7, ant-nodeps, ant-trax, jdk >= 1.6, lzo-devel, python >= 2.4, /usr/bin/git, subversion, fuse-libs, fuse-devel, fuse, automake, autoconf, libtool, redhat-rpm-config, openssl-devel

Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service, jdk >= 1.6
Provides: hadoop
Obsoletes: hadoop <= 0.20.0
Obsoletes: hadoop-fuse <= 0.20.0

%description
Hadoop is a software platform that lets one easily write and
run applications that process vast amounts of data.

Here's what makes Hadoop especially useful:
* Scalable: Hadoop can reliably store and process petabytes.
* Economical: It distributes the data and processing across clusters
              of commonly available computers. These clusters can number
              into the thousands of nodes.
* Efficient: By distributing the data, Hadoop can process it in parallel
             on the nodes where the data is located. This makes it
             extremely rapid.
* Reliable: Hadoop automatically maintains multiple copies of data and
            automatically redeploys computing tasks based on failures.

Hadoop implements MapReduce, using the Hadoop Distributed File System (HDFS).
MapReduce divides applications into many small blocks of work. HDFS creates
multiple replicas of data blocks for reliability, placing them on compute
nodes around the cluster. MapReduce can then process the data where it is
located.

%ifarch noarch

%package namenode
Summary: The Hadoop namenode manages the block locations of HDFS files
Group: System/Daemons
Requires: %{name} == %{version}

%description namenode
The Hadoop Distributed Filesystem (HDFS) requires one unique server, the
namenode, which manages the block locations of files on the filesystem.


%package secondarynamenode
Summary: Hadoop Secondary namenode
Group: System/Daemons
Requires: %{name} == %{version}

%description secondarynamenode
The Secondary Name Node periodically compacts the Name Node EditLog
into a checkpoint.  This compaction ensures that Name Node restarts
do not incur unnecessary downtime.


%package jobtracker
Summary: Hadoop Job Tracker
Group: System/Daemons
Requires: %{name} == %{version}

%description jobtracker
The jobtracker is a central service which is responsible for managing
the tasktracker services running on all nodes in a Hadoop Cluster.
The jobtracker allocates work to the tasktracker nearest to the data
with an available work slot.


%package datanode
Summary: Hadoop Data Node
Group: System/Daemons
Requires: %{name} == %{version}

%description datanode
The Data Nodes in the Hadoop Cluster are responsible for serving up
blocks of data over the network to Hadoop Distributed Filesystem
(HDFS) clients.


%package tasktracker
Summary: Hadoop Task Tracker
Group: System/Daemons
Requires: %{name} == %{version}

%description tasktracker
The tasktracker has a fixed number of work slots.  The jobtracker
assigns MapReduce work to the tasktracker that is nearest the data
with an available work slot.


%package conf-pseudo
Summary: Hadoop installation in pseudo-distributed mode
Group: System/Daemons
Requires: %{name} == %{version}, %{name}-namenode == %{version}, %{name}-datanode == %{version}, %{name}-secondarynamenode == %{version}, %{name}-tasktracker == %{version}, %{name}-jobtracker == %{version}

%description conf-pseudo
Installation of this RPM will setup your machine to run in pseudo-distributed mode
where each Hadoop daemon runs in a separate Java process.

%package docs
Summary: Hadoop Documentation
Group: Documentation

%description docs
Documentation for Hadoop

%package source
Summary: Source code for Hadoop
Group: System/Daemons

%description source
The Java source code for Hadoop and its contributed packages. This is handy when
trying to debug programs that depend on Hadoop.

# All architecture specific packages should follow here inside this else block
%else

%package fuse
Summary: Mountable HDFS
Group: Development/Libraries
Requires: %{name} == %{version}-%{release}, fuse-libs, fuse
Provides: hadoop-fuse

%description fuse
These projects (enumerated below) allow HDFS to be mounted (on most flavors of Unix) as a standard file system using the mount command. Once mounted, the user can operate on an instance of hdfs using standard Unix utilities such as 'ls', 'cd', 'cp', 'mkdir', 'find', 'grep', or use standard Posix libraries like open, write, read, close from C, C++, Python, Ruby, Perl, Java, bash, etc.


%define selinux_variants mls strict targeted
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)

%package fuse-selinux
Summary: SELinux policy files for fuse mount
Group:          System Environment/Daemons
BuildRequires:  checkpolicy selinux-policy-devel hardlink selinux-policy-targeted
Requires: %{name} = %{version}-%{release}
Requires:       selinux-policy >= %{selinux_policyver}
Requires(post):         /usr/sbin/semodule /usr/sbin/semanage /sbin/fixfiles
Requires(preun):        /sbin/service /usr/sbin/semodule /usr/sbin/semanage /sbin/fixfiles
Requires(postun):       /usr/sbin/semodule
%description fuse-selinux
selinux policy files for the Hadoop fuse hdfs mounts


%package native
Summary: Native libraries for Hadoop Compression
Group: Development/Libraries
Requires: %{name} == %{version}

%description native
Native libraries for Hadoop compression

%package libhdfs
Summary: Hadoop Filesystem Library
Group: Development/Libraries
Requires: %{name} == %{version}-%{release}, jdk >= 1.6
# TODO: reconcile libjvm
AutoReq: no
Provides: hadoop-libhdfs

%description libhdfs
Hadoop Filesystem Library

%package pipes
Summary: Hadoop Pipes Library
Group: Development/Libraries
Requires: %{name} == %{version}

%description pipes
Hadoop Pipes Library

%package sbin
Summary: Binaries for secured Hadoop clusters
Group: System/Daemons
Requires: %{name} == %{version}

%description sbin
This package contains a setuid program, 'task-controller', which is used for
launching MapReduce tasks in a secured MapReduce cluster. This program allows
the tasks to run as the Unix user who submitted the job, rather than the
Unix user running the MapReduce daemons.
This package also contains 'jsvc', a daemon wrapper necessary to allow
DataNodes to bind to a low (privileged) port and then drop root privileges
before continuing operation.

%endif

%prep
%setup -n hadoop-%{cloudera_version} -a 4
#%setup -T -a 4
%patch0
%patch1
%patch2 -p1
%patch3
%patch4
%patch5
%patch6
%patch7
%patch8

%build
# This assumes that you installed Java JDK 6 via RPM

export FORREST_HOME=$PWD/apache-forrest-0.8
%ifarch noarch
JAVA_HOME="/usr/java/default" ant -propertyfile cloudera/build.properties bin-package
%else
JAVA_HOME="/usr/java/default" ant -propertyfile cloudera/build.properties -Dcompile.native=true -Dlibhdfs=1 -Dfusedfs=1 -Dcompile.c++=true -Djava5.home=${JAVA5_HOME} -Dforrest.home=${FORREST_HOME}  task-controller package

# Build the selinux policy file
mkdir SELinux
cp %{SOURCE5} SELinux/%{name}.te
pushd SELinux
for variant in %{selinux_variants}
do
    make NAME=${variant} -f %{_datadir}/selinux/devel/Makefile
    mv %{name}.pp %{name}.pp.${variant}
    make NAME=${variant} -f %{_datadir}/selinux/devel/Makefile clean
done
popd

%endif


#########################
#### INSTALL SECTION ####
#########################
%install
%__rm -rf $RPM_BUILD_ROOT

%__install -d -m 0755 $RPM_BUILD_ROOT/%{lib_hadoop}


bash cloudera/install_hadoop.sh \
  --cloudera-source-dir=cloudera/files \
  --build-dir=%{hadoop_build_path} \
  --src-dir=$RPM_BUILD_ROOT%{src_hadoop} \
  --lib-dir=$RPM_BUILD_ROOT%{lib_hadoop} \
  --system-lib-dir=%{_libdir} \
  --etc-dir=$RPM_BUILD_ROOT%{etc_hadoop} \
  --prefix=$RPM_BUILD_ROOT \
  --doc-dir=$RPM_BUILD_ROOT%{doc_hadoop} \
  --example-dir=$RPM_BUILD_ROOT%{doc_hadoop}/examples \
  --native-build-string=%{hadoop_arch} \
  --installed-lib-dir=%{lib_hadoop} \
  --man-dir=$RPM_BUILD_ROOT%{man_hadoop} \
  --apache-branch=%{apache_branch}

%ifarch noarch
%else

# Install selinux policies
pushd SELinux
for variant in %{selinux_variants}
do
    install -d $RPM_BUILD_ROOT%{_datadir}/selinux/${variant}
    install -p -m 644 %{name}.pp.${variant} \
           $RPM_BUILD_ROOT%{_datadir}/selinux/${variant}/%{name}.pp
done
popd
# Hardlink identical policy module packages together
/usr/sbin/hardlink -cv $RPM_BUILD_ROOT%{_datadir}/selinux

rm $RPM_BUILD_ROOT%{_libdir}/libhdfs.la
rm $RPM_BUILD_ROOT%{lib_hadoop}/lib/native/%{hadoop_arch}/libhadoop.{a,la}
%endif


%ifarch noarch

# Init.d scripts
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/rc.d/init.d/

# Generate the init.d scripts
for service in %{hadoop_services}
do
       init_file=$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-${service}
       if [ $service = "namenode" ]
       then
         %__cp $RPM_SOURCE_DIR/hadoop-init-nn.tmpl $init_file
       else
         %__cp $RPM_SOURCE_DIR/hadoop-init.tmpl $init_file
       fi
       %__sed -i -e 's|@HADOOP_COMMON_ROOT@|%{lib_hadoop}|' $init_file
       %__sed -i -e "s|@HADOOP_DAEMON@|${service}|" $init_file
       %__sed -i -e 's|@HADOOP_CONF_DIR@|%{config_hadoop}|' $init_file
       chmod 755 $init_file
done
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/default
%__cp $RPM_SOURCE_DIR/hadoop-0.20.default $RPM_BUILD_ROOT/etc/default/hadoop-0.20


# /var/lib/hadoop/cache
%__install -d -m 1777 $RPM_BUILD_ROOT/var/lib/%{name}/cache
# /var/log/hadoop
%__install -d -m 0755 $RPM_BUILD_ROOT/var/log
%__install -d -m 0775 $RPM_BUILD_ROOT/var/run/%{name}
%__install -d -m 0775 $RPM_BUILD_ROOT/%{log_hadoop}


%pre
getent group hadoop 2>/dev/null >/dev/null || /usr/sbin/groupadd -r hadoop

/usr/sbin/useradd --comment "Hadoop MapReduce" --shell /bin/bash -M -r --groups hadoop --home %{lib_hadoop} mapred 2> /dev/null || :

# Upgrade

# If we have a hadoop user but not an hdfs user, rename hadoop -> hdfs
if getent passwd hadoop 2>/dev/null >/dev/null && \
   ! getent passwd hdfs 2>/dev/null >/dev/null ; then
  /usr/sbin/usermod --comment "Hadoop HDFS" --login hdfs hadoop
else
  # Create a hdfs user
  /usr/sbin/useradd --comment "Hadoop HDFS" --shell /bin/bash -M -r --groups hadoop --home %{lib_hadoop} hdfs 2> /dev/null || :
fi


%post

# Move away the previous OSG Hadoop configuration directories.
if [ -d /etc/hadoop ] && [ ! -h /etc/hadoop ]; then
  echo "Moving previous Hadoop conf directory to /etc/hadoop-0.19"
  mv /etc/hadoop /etc/hadoop-0.19
fi
if [ -d /var/log/hadoop ] && [ ! -h /var/log/hadoop ]; then
  echo "Moving previous Hadoop logfiles into /var/log/hadoop-0.19"
  echo "Please review and delete"
  mv /var/log/hadoop /var/log/hadoop-0.19
fi

alternatives --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.empty 10
alternatives --install %{bin_hadoop}/%{hadoop_name} %{hadoop_name}-default %{bin_hadoop}/%{name} 20 \
  --slave %{log_hadoop_dirname}/%{hadoop_name} %{hadoop_name}-log %{log_hadoop} \
  --slave %{lib_hadoop_dirname}/%{hadoop_name} %{hadoop_name}-lib %{lib_hadoop} \
  --slave /etc/%{hadoop_name} %{hadoop_name}-etc %{etc_hadoop} \
  --slave %{man_hadoop}/man1/%{hadoop_name}.1.gz %{hadoop_name}-man %{man_hadoop}/man1/%{name}.1.gz \
  --slave %{bin_hadoop}/hadoop-daemon %{hadoop_name}-daemon %{lib_hadoop}/bin/hadoop-daemon.sh \
  --slave %{bin_hadoop}/hadoop-config.sh %{hadoop_name}-config %{lib_hadoop}/bin/hadoop-config.sh

# Upgrade
if [ "$1" = 2 ]; then
  chgrp -R hadoop %{log_hadoop}
  chmod g+w /var/run/hadoop-0.20 /var/log/hadoop-0.20

  # Change the ownership of old logs so that we don't fail rotation on next startup
  find /var/log/hadoop-0.20/ | egrep 'jobtracker|tasktracker|userlogs|history' | xargs --no-run-if-empty chown mapred
  find /var/log/hadoop-0.20/ | egrep 'namenode|datanode' | xargs --no-run-if-empty chown hdfs

  # We don't want to do this recursively since we may be reinstalling, in which case
  # users have their own cache/<username> directories which shouldn't be stolen
  chown root:hadoop /var/lib/hadoop-0.20/ /var/lib/hadoop-0.20/cache/ /var/lib/hadoop-0.20/cache/hadoop/ 2>/dev/null || :
fi

%preun
if [ "$1" = 0 ]; then
  # Stop any services that might be running
  for service in %{hadoop_services}
  do
     service hadoop-$service stop 1>/dev/null 2>/dev/null || :
  done
  alternatives --remove %{name}-conf %{etc_hadoop}/conf.empty || true
  alternatives --remove %{hadoop_name}-default %{bin_hadoop}/%{name} || true
fi

%triggerpostun -- hadoop
if [ "$2" == 0 ]; then
  # restore symlinks that removing hadoop 0.19 may have deleted
  if [ ! -h %{bin_hadoop}/%{hadoop_name} ]; then
    ln -sf /etc/alternatives/%{hadoop_name}-default %{bin_hadoop}/%{hadoop_name}
  fi
  if [ ! -h %{log_hadoop_dirname}/%{hadoop_name} ]; then
    ln -sf /etc/alternatives/%{hadoop_name}-log %{log_hadoop_dirname}/%{hadoop_name}
  fi
  if [ ! -h /etc/%{hadoop_name} ]; then
    ln -sf /etc/alternatives/%{hadoop_name}-etc /etc/%{hadoop_name}
  fi
  if [ ! -h %{bin_hadoop}/hadoop-config.sh ]; then
    ln -sf /etc/alternatives/%{hadoop_name}-config %{bin_hadoop}/hadoop-config.sh
  fi
fi

%files
%defattr(-,root,root)
%dir %config %attr(-,root,root) %{etc_hadoop}/conf.empty
%config(noreplace) %attr(-,root,root) %{etc_hadoop}/conf.empty/*
/etc/default/hadoop-0.20
%{lib_hadoop}
%{bin_hadoop}/%{name}
%{man_hadoop}/man1/hadoop-%{apache_branch}.1.gz
%attr(0775,root,hadoop) /var/run/%{name}
%attr(0775,root,hadoop) %{log_hadoop}

%files docs
%defattr(-,root,root)
%doc %{doc_hadoop}

%files source
%defattr(-,root,root)
%{src_hadoop}



# Service file management RPMs
%define service_macro() \
%files %1 \
%defattr(-,root,root) \
%{_sysconfdir}/rc.d/init.d/%{name}-%1 \
%{lib_hadoop}/bin/hadoop-daemon.sh \
%post %1 \
chkconfig --add %{name}-%1 \
\
%preun %1 \
if [ "$1" = 0 ]; then \
  service %{name}-%1 stop > /dev/null \
  chkconfig --del %{name}-%1 \
fi
%service_macro namenode
%service_macro secondarynamenode
%service_macro datanode
%service_macro jobtracker
%service_macro tasktracker

# Pseudo-distributed Hadoop installation
%post conf-pseudo
alternatives --install %{config_hadoop} %{name}-conf %{etc_hadoop}/conf.pseudo 30

if [ ! -e %{etc_hadoop}/conf ]; then
  ln -s %{etc_hadoop}/conf.pseudo %{etc_hadoop}/conf
fi

nn_dfs_dir="/var/lib/%{name}/cache/hadoop/dfs"
if [ -z "$(ls -A $nn_dfs_dir 2>/dev/null)" ]; then
   HADOOP_NAMENODE_USER=hdfs hadoop-%{apache_branch} --config %{etc_hadoop}/conf.pseudo namenode -format 2>/dev/null 1>/dev/null || :
fi

%files conf-pseudo
%config %attr(755,root,root) %{etc_hadoop}/conf.pseudo
%dir %attr(0755,root,hadoop) /var/lib/%{name}
%dir %attr(1777,root,hadoop) /var/lib/%{name}/cache

%preun conf-pseudo
if [ "$1" = 0 ]; then
        alternatives --remove %{name}-conf %{etc_hadoop}/conf.pseudo
        rm -f %{etc_hadoop}/conf
fi

# non-noarch files (aka architectural specific files)
%else

%post fuse-selinux
# Install SELinux policy modules
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{name}.pp &> /dev/null || :
done
  
%preun fuse-selinux
if [ "$1" -lt "1" ] ; then
    for variant in %{selinux_variants} ; do
        /usr/sbin/semodule -s ${variant} -r %{name} &> /dev/null || :
    done
fi
%postun fuse-selinux
if [ "$1" -ge "1" ] ; then
    # Replace the module if it is already loaded. semodule -u also
    # checks the module version
    for variant in %{selinux_variants} ; do
        /usr/sbin/semodule -u %{_datadir}/selinux/${variant}/%{name}.pp || :
    done
fi

%files native
%defattr(-,root,root)
%{lib_hadoop}/lib/native/*

%files fuse
%defattr(-,root,root)
%attr(0755,root,root) %{lib_hadoop}/bin/fuse_dfs
%attr(0755,root,root) %{lib_hadoop}/bin/fuse_dfs_wrapper.sh
%attr(0755,root,root) %{bin_hadoop}/hadoop-fuse-dfs
%attr(0755,root,root) %{man_hadoop}/man1/hadoop-fuse-dfs.1.gz

%files fuse-selinux
%defattr(-,root,root,-)
%doc SELinux/*.??
%{_datadir}/selinux/*/%{name}.pp


%files pipes
%defattr(-,root,root)
%{_libdir}/libhadooppipes*
%{_libdir}/libhadooputil*
%{_includedir}/hadoop/*

%files libhdfs
%defattr(-,root,root)
%{_libdir}/libhdfs*
%{_includedir}/hdfs.h

%files sbin
%attr(4754,root,mapred) %{lib_hadoop}/sbin/%{hadoop_arch}/task-controller
%attr(0755,root,root) %{lib_hadoop}/sbin/%{hadoop_arch}/jsvc

%endif

%changelog
* Mon Dec 17 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.20.2+737-28
- Fix VSZ explosion issue in datanode (HADOOP-7154, HDFS-2452).

* Fri Dec 07 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.20.2+737-27
- Backport patch for HDFS-799, which caused memory leaks in fuse_dfs.

* Thu Aug 9 2012 Doug Strain <dstrain@fnal.gov> - 0.20.2+737-26
- Added obsoletes for hadoop 2.0.0
- Made alternatives removal optional and not cause a failure

* Sat Feb 18 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.20.2+737-24
- Fix placement of ifarch statements.
- Tweak SELinux definition.

* Tue Feb 14 2012 Doug Strain <dstrain@fnal.gov> - 0.20.2+737-23
- Added SE linux module

* Wed Feb 08 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.20.2+737-19
- Rebuild with proper arch setting.

* Mon Nov 28 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-18
- Change to correctly run hadoop as user hdfs.

* Fri Oct 21 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-17
- Prevent chown on log files from hadoop user to hdfs if 0.20 already
  installed.

* Thu Oct 20 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-16
- Ensure 0.19 backups are created only if previous installation was 0.19.

* Thu Oct 06 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-15
- Patch hadoop-fuse-dfs to follow symlinks when finding libjvm.so.

* Fri Aug 23 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-14
- Release bump because of missing noarch rpms on previous build.

* Fri Jun 05 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-13
- Add hadoop-config.sh to alternatives to prevent hadoop-daemon from failing
- Add triggerpostun section to fix alternatives links that break when
  removing hadoop 0.19

* Fri Apr 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-12
- Fix mkdir.
- Fix race issues in connect.

* Sat Mar 19 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-10
- Slightly better FS stability in testing.

* Tue Mar 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-9
- Found another case where we improperly passed around a FS object.

* Mon Mar 14 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-8
- Update FUSE to keep a per-user FS object cache.  Should alleviate slowness
  with operating on large directories.

* Tue Mar 1  2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-6
- Require -fuse to be aligned with the exact release of the parent package.

* Sat Feb 26 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-5
- FUSE-DFS adds $HADOOP_CONF to the $CLASSPATH.

* Tue Feb 22 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-4
- Fix memory leaks in fuse-dfs.

* Thu Dec 23 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-2
- Moved away the directories causing alternatives to choke
- Fixed ownership in the conf.empty directory.
- Removed the Cloudera init scripts.
- Add an Obsoletes line in order to allow for a clean upgrade from OSG RPMs.

