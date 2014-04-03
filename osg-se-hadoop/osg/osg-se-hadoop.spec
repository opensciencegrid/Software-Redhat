Name:           osg-se-hadoop
Summary:        OSG Hadoop Storage Element package for RPM distribution
Version:        3.0.0
Release:        11%{?dist}
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: hdfs-site.xml
Source1: core-site.xml
Requires: %{name}-namenode = %{version}-%{release}
Requires: %{name}-datanode = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-gridftp = %{version}-%{release}
Requires: %{name}-srm = %{version}-%{release}

%description
This is a meta-package for Hadoop Storage Element. By default, it will
install all the packages needed for a Hadoop Storage Element.  For specific portions,
see the subpackages namenode, datanode, gridftp, etc.


%package namenode
Summary: Namenode meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-namenode
Requires: gratia-probe-hadoop-storage
Requires: osg-version
Requires: osg-system-profiler
%description namenode
This is the Hadoop namenode that stores directory and file system information
for a Hadoop Storage Element.


%package datanode
Summary: Datanode meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-datanode
Requires: osg-version
Requires: osg-system-profiler
%description datanode
This is the Hadoop datanode that stores file data for a Hadoop Storage Element.

%package client
Summary: Client meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-fuse
Requires: osg-version
Requires: osg-system-profiler
%description client
This is the Hadoop client that has client binaries and fuse mount.

%package gridftp
Summary: Gridftp meta-package for Hadoop
Group: System Environment/Libraries
Requires: %{name}-client = %{version}-%{release}
Requires: hadoop-hdfs-fuse
Requires: osg-version
Requires: osg-system-profiler
Requires: edg-mkgridmap
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
# 3.0.0-6 pulls in gridftp-hdfs that uses /etc/gridftp.d
Requires: osg-gridftp-hdfs >= 3.0.0-6
Requires: globus-gridftp-server-progs
Requires: gratia-probe-gridftp-transfer
Requires: gums-client
Requires: vo-client
%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif
%description gridftp
This is a Globus GridFTP frontend for a Hadoop Storage Element.



%package srm
Summary: Datanode meta-package for Hadoop
Group: System Environment/Libraries
Requires: grid-certificates
Requires: osg-version
Requires: osg-system-profiler
Requires: edg-mkgridmap
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
Requires: bestman2-server
Requires: bestman2-client
Requires: bestman2-tester
Requires: vo-client
Requires: hadoop-hdfs-fuse
%description srm
This is a BeStMan SRM frontend for a Hadoop cluster.



%install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/hadoop/conf.osg
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/hadoop/conf.osg/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/hadoop/conf.osg/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sysconfdir}/hadoop/conf.osg/

%files namenode
%{_sysconfdir}/hadoop/conf.osg/

%files datanode
%{_sysconfdir}/hadoop/conf.osg/

%files client
%{_sysconfdir}/hadoop/conf.osg/

%files gridftp
%{_sysconfdir}/hadoop/conf.osg/

%files srm
%{_sysconfdir}/hadoop/conf.osg/

%changelog
* Thu Apr 03 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-11
- Add version requirement for osg-gridftp-hdfs (SOFTWARE-1412)

* Thu Apr 04 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-10
- Remove java dependency.

* Mon Feb 25 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-9
- Update -srm subpackage so that rhel5 requires fetch-crl3 instead of fetch-crl

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-8
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Wed Aug 8 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-7
- Added fuse client to srm sub-package (mount is needed for permissions)
- Also added default OSG configs to srm package
- Added hadoop storage probe to namenode

* Tue Aug 7 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-4
- Reduced value for du.reserved 
-   Since it causes problems with smaller (<10GB) hard drives
- Added empty files section to cause packages to be made for gridftp/bestman

* Wed Aug 1 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-1
- Initial meta-package creation for Hadoop-2.0.0

