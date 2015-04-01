%define lib_hadoop_dirname /usr/lib
%define lib_hadoop %{lib_hadoop_dirname}/hadoop
%define lib_hdfs %{lib_hadoop_dirname}/hadoop-hdfs

#%if 0%{?el5}
#%define debug_package %{nil}
#%endif 

Name:           hdfs-xrootd-fallback-proj
Version:        1.0.1
Release:        2%{?dist}
Summary:        Tools to enable relaxed local Hadoop replication
Group:          System Environment/Daemons
License:        BSD
URL:            http://www.gled.org/cgi-bin/twiki/view/Main/HdfsXrootd
Source0:        %{name}-%{version}.tar.gz
Patch0:         parallel_make.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java7-devel
BuildRequires: pcre-devel
BuildRequires: xrootd-client-devel >= 4.0.4
BuildRequires: hadoop-hdfs >= 2.0.0+545-1.cdh4.1.1.p0.19.osg

%description
The HDFS XRootD Fallback system enables relaxed local Hadoop replication by
utilizing global redundancy provided by the XRootD Federation. This system
provides exception handling at the block level, a cache to locally store
repaired blocks retrieved from the Federation, and the ability to re-inject the
repaired blocks back into Hadoop.

%package -n hdfs-xrootd-fallback
Summary:        Hadoop extension to interface with XRootD for block-level read error prevention
Group:          System Environment/Daemons
Requires: pcre
Requires: xrootd-client-libs >= 4.0.4
Requires: hadoop-hdfs >= 2.0.0+545-1.cdh4.1.1.p0.19.osg
Requires: hadoop-hdfs-fuse >= 2.0.0+545-1.cdh4.1.1.p0.19.osg

%description -n hdfs-xrootd-fallback
The HDFS XRootD Fallback package is installed on every datanode in the Hadoop
cluster and accesses blocks on demand via XRootD Cache on failed read exceptions

%package -n hdfs-xrootd-healer
Summary:        Daemon that periodically re-injects cached blocks back into hadoop
Group:          System Environment/Daemons
%if 0%{!?el5:1}
BuildArch:      noarch
%endif
Requires: hadoop-hdfs-fuse >= 2.0.0+545-1.cdh4.1.1.p0.19.osg
Requires: python

%description -n hdfs-xrootd-healer
The HDFS XRootD Healer is installed on the XRootD Cache node and periodically
compares corrupt blocks in Hadoop with blocks stored in the cache. It re-injects
the repaired blocks once they are fully cached.

%package -n hdfs-xrootd-fbmon
Summary:        Fallback monitoring daemon
Group:          System Environment/Daemons
%if 0%{!?el5:1}
BuildArch:      noarch
%endif
Requires: perl
Requires: perl-Proc-Daemon

%description -n hdfs-xrootd-fbmon
The HDFS XRootD Fallback Monitor is a UDP listener that logs incomming messages
sent from the datanodes whenever a fallback is triggered.

%prep
%setup -q
%patch0 -p1

%build

export JAVA_HOME=%{java_home}

%configure \
HADOOP_HOME=%{lib_hadoop} \
HADOOP_HDFS_HOME=%{lib_hdfs} \
CPPFLAGS=-I/usr/include/xrootd

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# rhel specific dirs
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/cron.d
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d

# rhel specific healer stuff
mkdir -p %{buildroot}/%{_sysconfdir}/hdfs-xrootd-healer
install -p -m 644 %{buildroot}/%{_datadir}/hdfs-xrootd-healer/hdfs-xrootd-healer.cfg \
  %{buildroot}/%{_sysconfdir}/hdfs-xrootd-healer
install -p %{buildroot}/%{_datadir}/hdfs-xrootd-healer/hdfs-xrootd-healer.init \
  %{buildroot}/%{_initrddir}/hdfs-xrootd-healer
install -p -m 644 %{buildroot}/%{_datadir}/hdfs-xrootd-healer/hdfs-xrootd-healer.cron \
  %{buildroot}/%{_sysconfdir}/cron.d/hdfs-xrootd-healer
install -p -m 644 %{buildroot}/%{_datadir}/hdfs-xrootd-healer/hdfs-xrootd-healer.logrotate \
  %{buildroot}/%{_sysconfdir}/logrotate.d/hdfs-xrootd-healer
mkdir -p %{buildroot}/%{_localstatedir}/lock/hdfs-xrootd-healer

#rhel specific fbmon stuff
install -p -m 644 %{buildroot}/%{_datadir}/hdfs-xrootd-fbmon/hdfs-xrootd-fbmon.sysconfig \
  %{buildroot}/%{_sysconfdir}/sysconfig/hdfs-xrootd-fbmon
install -p %{buildroot}/%{_datadir}/hdfs-xrootd-fbmon/hdfs-xrootd-fbmon.init \
  %{buildroot}/%{_initrddir}/hdfs-xrootd-fbmon
install -p -m 644 %{buildroot}/%{_datadir}/hdfs-xrootd-fbmon/hdfs-xrootd-fbmon.logrotate \
  %{buildroot}/%{_sysconfdir}/logrotate.d/hdfs-xrootd-fbmon

%clean
rm -rf %{buildroot}

%post -n hdfs-xrootd-fallback -p /sbin/ldconfig
%postun -n hdfs-xrootd-fallback -p /sbin/ldconfig

%post -n hdfs-xrootd-healer
if [ $1 = 1 ];then
  /sbin/chkconfig --add hdfs-xrootd-healer
fi

%preun -n hdfs-xrootd-healer
if [ $1 = 0 ];then
  /sbin/service hdfs-xrootd-healer stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del hdfs-xrootd-healer
fi

%pre -n hdfs-xrootd-fbmon
getent group hdfsfbmon >/dev/null || groupadd -r hdfsfbmon
getent passwd hdfsfbmon >/dev/null || \
  useradd -r -g hdfsfbmon -d %{_datadir}/hdfs-xrootd-fbmon -s /sbin/noligin \
  -c "HDFS XRootD Fallback Monitor User" hdfsfbmon
exit 0

%post -n hdfs-xrootd-fbmon
if [ $1 = 1 ];then
  /sbin/chkconfig --add hdfs-xrootd-fbmon
fi

%preun -n hdfs-xrootd-fbmon
if [ $1 = 0 ];then
  /sbin/service hdfs-xrootd-fbmon stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del hdfs-xrootd-fbmon
fi

%files -n hdfs-xrootd-fallback
%defattr(-,root,root,-)
%doc README LICENSE NEWS
%{lib_hadoop}/client/hdfs-xrootd-fallback-%{version}.jar
%{_libdir}/libXrdBlockFetcher.so*
%{_sysconfdir}/hadoop/conf.osg/xfbfs-site.xml

%files -n hdfs-xrootd-healer
%defattr(-,root,root,-)
%doc README LICENSE NEWS
%{_sbindir}/hdfs-xrootd-healer
%{_datadir}/hdfs-xrootd-healer
%dir %{_sysconfdir}/hdfs-xrootd-healer
%config(noreplace) %{_sysconfdir}/hdfs-xrootd-healer/hdfs-xrootd-healer.cfg
%{_initrddir}/hdfs-xrootd-healer
%{_sysconfdir}/cron.d/hdfs-xrootd-healer
%config(noreplace) %{_sysconfdir}/logrotate.d/hdfs-xrootd-healer
%dir %{_localstatedir}/lock/hdfs-xrootd-healer
%dir %{_localstatedir}/log/hdfs-xrootd-healer

%files -n hdfs-xrootd-fbmon
%defattr(-,root,root,-)
%doc README LICENSE NEWS
%{_libexecdir}/hdfs-xrootd-fbmon
%{_datadir}/hdfs-xrootd-fbmon
%config(noreplace) %{_sysconfdir}/sysconfig/hdfs-xrootd-fbmon
%{_initrddir}/hdfs-xrootd-fbmon
%config(noreplace) %{_sysconfdir}/logrotate.d/hdfs-xrootd-fbmon
%attr(-,hdfsfbmon,hdfsfbmon) %dir %{_localstatedir}/log/hdfs-xrootd-fbmon
%attr(-,hdfsfbmon,hdfsfbmon) %dir %{_localstatedir}/run/hdfs-xrootd-fbmon

%changelog
* Tue Mar 31 2015 Jeff Dost <jdost@ucsd.edu> - 1.0.1-2
- Add some fixes to spec and parallel make patch to build in OSG Koji

* Thu Mar 9 2015 Jeff Dost <jdost@ucsd.edu> - 1.0.1-1
- Release v1.0.1

* Thu Mar 2 2015 Jeff Dost <jdost@ucsd.edu> - 1.0.0-5
- Add fbmon rpm

* Thu Dec 24 2014 Jeff Dost <jdost@ucsd.edu> - 1.0.0-4
- Add healer rpm

* Thu Dec 4 2014 Jeff Dost <jdost@ucsd.edu> - 1.0.0-3
- Rebuild against xrootd4

* Thu Apr 3 2014 Jeff Dost <jdost@ucsd.edu> - 1.0.0-2
- Bug fix in libXrdBlockFetcher.so  

* Fri Feb 14 2014 Jeff Dost <jdost@ucsd.edu> - 1.0.0-1
- Initial release
