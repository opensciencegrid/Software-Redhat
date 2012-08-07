Name:           osg-se-hadoop
Summary:        OSG Hadoop Storage Element package for RPM distribution
Version:        3.0.0
Release:        4%{?dist}
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
Requires: osg-version
Requires: osg-system-profiler
Requires: java-1.6.0-sun-compat
%description namenode
This is the Hadoop namenode that stores directory and file system information
for a Hadoop Storage Element.


%package datanode
Summary: Datanode meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-datanode
Requires: osg-version
Requires: osg-system-profiler
Requires: java-1.6.0-sun-compat
%description datanode
This is the Hadoop datanode that stores file data for a Hadoop Storage Element.

%package client
Summary: Client meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-fuse
Requires: osg-version
Requires: osg-system-profiler
Requires: java-1.6.0-sun-compat
%description client
This is the Hadoop client that has client binaries and fuse mount.

%package gridftp
Summary: Gridftp meta-package for Hadoop
Group: System Environment/Libraries
Requires: %{name}-client = %{version}-%{release}
Requires: hadoop-hdfs-fuse
Requires: osg-version
Requires: osg-system-profiler
Requires: java-1.6.0-sun-compat
Requires: edg-mkgridmap
Requires: fetch-crl
Requires: osg-gridftp-hdfs
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
Requires: java-1.6.0-sun-compat
Requires: edg-mkgridmap
Requires: fetch-crl
Requires: bestman2-server
Requires: bestman2-client
Requires: bestman2-tester
Requires: vo-client
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

%changelog
* Tue Aug 7 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-4
- Reduced value for du.reserved 
-   Since it causes problems with smaller (<10GB) hard drives
- Added empty files section to cause packages to be made for gridftp/bestman

* Wed Aug 1 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-1
- Initial meta-package creation for Hadoop-2.0.0

