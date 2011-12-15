Name:      osg-gridftp-hdfs
Summary:   OSG GridFTP-HDFS meta package
Version:   3.0.0
Release:   2
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: osg-version
Requires: osg-system-profiler
Requires: gridftp-hdfs
Requires: vo-client
Requires: grid-certificates
Requires: fetch-crl
Requires: gratia-probe-gridftp-transfer
Requires: gums-client

%ifarch %{ix86}
Requires: liblcas_lcmaps_gt4_mapping.so.0
%else
Requires: liblcas_lcmaps_gt4_mapping.so.0()(64bit)
%endif

%description
This is a meta package for a standalone GridFTP server with 
HDFS and GUMS support.

%build

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files

%changelog
* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-2
- Added dependencies on osg-version and osg-system-profiler

* Sat Sep 24 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-1
- Initial creation of meta-package for gridftp-hdfs.

