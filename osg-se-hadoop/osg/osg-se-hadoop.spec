Name:           osg-se-hadoop
Summary:        OSG Hadoop Storage Element package for RPM distribution
Version:        3.4
Release:        8%{?dist}
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome

Source0: hdfs-site.xml
Source1: core-site.xml
Requires: %{name}-namenode = %{version}-%{release}
Requires: %{name}-secondarynamenode = %{version}-%{release}
Requires: %{name}-datanode = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: %{name}-gridftp = %{version}-%{release}
%endif

%description
This is a meta-package for Hadoop Storage Element. By default, it will
install all the packages needed for a Hadoop Storage Element.  For specific portions,
see the subpackages namenode, datanode, gridftp, etc.


%package namenode
Summary: Namenode meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-namenode
Requires: gratia-probe-hadoop-storage
Requires: osg-system-profiler
%description namenode
This is the Hadoop namenode that stores directory and file system information
for a Hadoop Storage Element.

%package secondarynamenode
Summary: Secondary Namenode meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-secondarynamenode
Requires: gratia-probe-hadoop-storage
Requires: osg-system-profiler
%description secondarynamenode
This is the Hadoop secondary namenode that stores directory and file system
information for a Hadoop Storage Element.

%package datanode
Summary: Datanode meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-datanode
Requires: osg-system-profiler
%description datanode
This is the Hadoop datanode that stores file data for a Hadoop Storage Element.

%package client
Summary: Client meta-package for Hadoop
Group: System Environment/Libraries
Requires: hadoop-hdfs-fuse
Requires: osg-system-profiler
%description client
This is the Hadoop client that has client binaries and fuse mount.

%if 0%{?rhel} >= 7
%package gridftp
Summary: Gridftp meta-package for Hadoop
Group: System Environment/Libraries
Requires: %{name}-client = %{version}-%{release}
# 3.0.0-6 pulls in gridftp-hdfs that uses /etc/gridftp.d
Requires: osg-gridftp-hdfs >= 3.0.0-7
%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif
%description gridftp
This is a Globus GridFTP frontend for a Hadoop Storage Element.
%endif



%install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/hadoop/conf.osg
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/hadoop/conf.osg/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/hadoop/conf.osg/

%files
%{_sysconfdir}/hadoop/conf.osg/

%files namenode
%{_sysconfdir}/hadoop/conf.osg/

%files secondarynamenode
%{_sysconfdir}/hadoop/conf.osg/

%files datanode
%{_sysconfdir}/hadoop/conf.osg/

%files client
%{_sysconfdir}/hadoop/conf.osg/

%if 0%{?rhel} >= 7
%files gridftp
%{_sysconfdir}/hadoop/conf.osg/
%endif

%changelog
* Tue Apr 30 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4-8
- Drop gridftp sub-package for EL6 (SOFTWARE-3673)

* Thu Jun 21 2018 Carl Edquist <edquist@cs.wisc.edu> - 3.4-6
- Move lcmaps-voms & osg-configure deps to osg-gridftp-hdfs (SOFTWARE-3177)
- Drop redundant deps from osg-se-hadoop-gridftp (SOFTWARE-3177)

* Wed Mar 14 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.4-5
- Remove edg-mkgridmap requirement; add osg-configure-misc and
  vo-client-lcmaps-voms (SOFTWARE-3138)

* Tue Mar 6 2018 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.4-4
- Remove srm and gums references (SOFTWARE-3138)
- Remove osg-version requirement (SOFTWARE-3116)

* Wed Jan 17 2018 Carl Edquist <edquist@cs.wisc.edu> - 3.4-3
- Drop & obsolete srm metapackage - bestman2 is gone in OSG 3.4 (SOFTWARE-2985)

* Wed Nov 22 2017 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.4-1
- Update for OSG 3.4 release

* Tue Feb 09 2016 Carl Edquist <edquist@cs.wisc.edu> - 3.3-3
- Remove gums-client requirement for EL7 (SOFTWARE-2176)

* Wed Jul 01 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.3-2
- Require grid-certificates >= 7 (SOFTWARE-1883)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3-1
- Rebuild for OSG 3.3

* Tue May 27 2014 Brian Lin <blin@cs.wisc.edu> - 3.0.0-14
- Secondarynamenode metapackage didn't get created in the last build

* Fri May 23 2014 Brian Lin <blin@cs.wisc.edu> - 3.0.0-13
- Add secondarynamenode metapackage

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

