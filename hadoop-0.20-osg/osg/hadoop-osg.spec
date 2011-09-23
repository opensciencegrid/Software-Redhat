%define hadoop_name hadoop
%define cloudera_version 0.20.2+737
%define apache_branch 0.20
%define etc_hadoop %{_sysconfdir}/%{hadoop_name}-%{apache_branch}
%define config_hadoop %{etc_hadoop}/conf.osg

Name:		%{hadoop_name}-%{apache_branch}-osg
Version:	%{cloudera_version}
Release:	8
Summary:	OSG configurations and scripts for Hadoop

Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://twiki.grid.iu.edu/bin/view/Storage/Hadoop

Source0:	hadoop.init
Source1:	hadoop.sysconfig

Source2:	getPoolSize.sh
Source3:	hdfs-site.xml.in
Source4:	hadoop-firstboot.init
Source5:	hadoop-env.sh
Source6:	core-site.xml.in
Source7:	configuration.xsl
Source8:	hadoop-metrics.properties
Source9:	log4j.properties
Source10:	mapred-site.xml
Source11:	ssl-client.xml.example
Source12:	ssl-server.xml.example

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#Conflicts: hadoop-fuse <= 0.19

Requires: hadoop-0.20 >= %{version}
Requires: hadoop-0.20-fuse >= %{version}
Requires(post): /sbin/chkconfig
Requires(postun): /sbin/chkconfig
Requires(postun): /sbin/service

%description
OSG configurations and firstboot scripts for HDFS.

%prep

%install
# Install init scripts
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -p -m 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_initrddir}/%{hadoop_name}
install -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_initrddir}/%{hadoop_name}-firstboot

# Install the sysconfig template
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/hadoop

# Install pool size script
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/getPoolSize

# Create logging and run directories
mkdir -p $RPM_BUILD_ROOT%{_var}/run/hadoop
mkdir -p $RPM_BUILD_ROOT%{_var}/log/hadoop

# Install the various configuration files
mkdir -p $RPM_BUILD_ROOT%{config_hadoop}
install -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{config_hadoop}/hdfs-site.xml.in
install -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{config_hadoop}/core-site.xml.in
install -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{config_hadoop}/hadoop-env.sh
install -p -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{config_hadoop}/configuration.xsl
install -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{config_hadoop}/hadoop-metrics.properties
install -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{config_hadoop}/log4j.properties
install -p -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{config_hadoop}/mapred-site.xml.in
install -p -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{config_hadoop}/ssl-client.xml.example
install -p -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{config_hadoop}/ssl-server.xml.example
ln -sf /usr/bin/hadoop-fuse-dfs $RPM_BUILD_ROOT%{_bindir}/hdfs
touch $RPM_BUILD_ROOT%{config_hadoop}/hosts_exclude

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group hadoop >/dev/null || groupadd -r hadoop
getent passwd hadoop >/dev/null || \
       useradd -r -g hadoop -c "HDFS runtime user" \
       -s /bin/bash hadoop
exit 0

%post
alternatives --install %{etc_hadoop}/conf %{hadoop_name}-%{apache_branch}-conf %{config_hadoop} 40
/sbin/chkconfig --add hadoop
/sbin/chkconfig --add hadoop-firstboot

%preun
if [ "$1" = "0" ]; then
    alternatives --remove %{hadoop_name}-%{apache_branch}-conf %{config_hadoop}
    /sbin/service hadoop stop > /dev/null 2>&1
    /sbin/chkconfig --del hadoop
    /sbin/chkconfig --del hadoop-firstboot
fi

%files
%defattr(-,root,root,-)
%{_bindir}/getPoolSize
%{_bindir}/hdfs
%{_initrddir}/%{hadoop_name}
%{_initrddir}/%{hadoop_name}-firstboot
%config(noreplace) %{config_hadoop}
#%{config_hadoop}/hdfs-site.xml.in
#%{config_hadoop}/core-site.xml.in
%config(noreplace) %{config_hadoop}/hadoop-env.sh
%config(noreplace) %{_sysconfdir}/sysconfig/%{hadoop_name}
%attr(0755,hadoop,hadoop) %{_var}/run/hadoop
%attr(0755,hadoop,hadoop) %{_var}/log/hadoop

%changelog
* Mon Jul 11 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-8
- Fix firstboot script typos when setting hadoop-metrics.properties.
- Only uncomment correct ganglia context in hadoop-metrics.properties.
- Fix status command in init script.

* Thu Apr 21 2011 Jeff Dost <jdost@ucsd.edu> 0.20.2+737-7
- Fix umask format.
- Move the following properties to hdfs-site.xml:
  dfs.block.size
  dfs.replication
  dfs.permissions.supergroup 

* Fri Apr 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-6
- Fix the default environment values for memory.
- Fix the default umask.

* Sat Feb 26 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-5
- Set dfs.permissions.supergroup to root.

* Tue Feb 22 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-4
- Fix issue with conflicting with hadoop-0.20-fuse RPM.
- Fix naming issue for the mapred-site.xml.in.

* Fri Feb 4 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-3
- Fix to init script to change username when starting and formatting the namenode.

* Tue Feb 1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+737-1
- Update to latest Cloudera RPMs; set to conflicts the old hadoop-fuse RPM.

* Thu Dec 23 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+320-4
- Fix configuration references and paths in the init script.
- Fix getPoolSize in hadoop-firstboot.  Added -P flag.
- Create the /usr/bin/hdfs symlink.

* Thu Dec 23 2010 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.2+320-3
- Fix the alternatives remove line

* Tue Dec 29 2009 Brian Bockelman <bbockelm@cse.unl.edu> 0.20.1+152
- Remove Hadoop build and code, leaving only the config files.

* Wed Sep 2 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-13
- Set defaults for namenode_port, replication_min, and replication_max
  in /etc/sysconfig/hadoop.
- Add fstab entry for fuse-dfs based on value of HADOOP_UPDATE_FSTAB
  in /etc/sysconfig/hadoop

* Mon Aug 24 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-12
- Increase ulimit -n in init script
- auto-detect ganglia 31 and update hadoop-metrics.properties if found.
- Rename a few patches for easier bookkeeping
- Add patches for JIRA 5479, 5465

* Mon Jul 27 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-11
- Add syslog entry to log4j and adjust default logging levels

* Tue Jun 9 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-10
- Remove JMX options from balancer

* Wed Apr 22 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-9
- UNRELEASED
- Add patch to fix jmx bean name
- Use a custom hadoop-env.sh instead of trying to patch it in %%prep.
- Add -duration patch for gratia reporting

* Mon Mar 30 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-8
- Allow multiple data directories on a data node
- Remove fuse components that have been moved to a separate arch-specific
  package.
- Package is now noarch

* Fri Mar 27 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-7
- Add hdfs patch for better error messages
- Add hdfs patch to avoid overwriting directories with files
- Add $HADOOP_CONF_DIR to CLASSPATH so that the fuse_dfs can find
  hadoop-site.xml
- Move hosts_exclude to /etc/hadoop/

* Wed Mar 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-6
- Re-enable the ganglia metrics for dfs and jvm

* Wed Mar 25 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-5
- Fix log directory ownership in hadoop.init

* Mon Mar 23 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-4
- Move configuration files to /etc
- Move hadoop cli applications to /usr/bin
- Move logs to /var/log/hadoop
- Split fuse interface files into -fuse subpackage
- Remove all settings from /etc/profile.d/hadoop except for
  HADOOP_CONF_DIR

* Mon Mar 23 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-3
- Extract version info from svn before creating the tarball.
- Remove .svn directories from tarball

* Mon Mar 23 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-2
- Add extra hack for .so dependencies with Sun's jdk

* Sun Mar 22 2009 Michael Thomas <thomas@hep.caltech.edu> 0.19.1-1
- Major reorganization of package to support building from source
- Include hadoop-firstboot init script
- Fix bad version number in spec file

* Fri Mar 20 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.1-2
- Fix bad Source filename

* Thu Mar 19 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.1-1
- Update to 0.19.1 with additional UNL patches

* Thu Mar 19 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-10
- Updated build with proper build rev

* Thu Mar 19 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-9
- Fix bad variable name in hadoop-site.xml.in

* Wed Mar 18 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-8
- Updated build with bug fix for fuse_dfs boundary error

* Mon Mar 16 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-7
- Split sources into subpackage
- Increase ulimit -n when mounting hdfs.
- Add checkpoint server (secondary namenode) settings to /etc/sysconfig/hadoop
- Set default ganglia reporting interval, namenode heap size, in
  /etc/sysconfig/hadoop.
- Document settings in /etc/sysconfig/hadoop
- Move datanode directory minimum size to /etc/sysconfig/hadoop
- Add Prefix: to make rpm relocatable (not recommended)
- Move pid file to /var/run/hadoop/ so that tmpwatch doesn't eat it.
- Move fuse_dfs to /usr/bin
- Move libhdfs libraries to %%{_libdir} so that we don't need to add hadoop's
  install dir to LD_LIBRARY_PATH

* Thu Mar 12 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-6
- Install a hadoop-site.xml.in template for end-user patching
- Change to the hadoop conf directory before running fuse_dfs

* Thu Mar 12 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-5
- Add more settings to /etc/sysconfig/hadoop

* Sun Mar 8 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-4
- Add getPoolSize.sh script from dcache-firstboot
- Fix typo in init script (dCache -> hadoop)

* Fri Mar 6 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-3
- Move fuse mount from hadoop init script to /etc/fstab
- Add utility to calculate rack number from hostname

* Thu Mar 5 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-2
- Added init script
- Run as the hadoop user

* Tue Mar 3 2009 Michael Thomas <thomas@hep.caltech.edu> 0.9.0-1
- Initial version

