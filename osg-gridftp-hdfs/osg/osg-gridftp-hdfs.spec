Name:      osg-gridftp-hdfs
Summary:   OSG GridFTP-HDFS meta package
Version:   3.0.0
Release:   5%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Source1: udt-%{name}.conf

Requires: osg-version
Requires: osg-system-profiler
Requires: gridftp-hdfs
Requires: vo-client
Requires: grid-certificates
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
Requires: gratia-probe-gridftp-transfer
Requires: gums-client

%if 0%{?rhel} >= 6
Requires: globus-xio-udt-driver
%endif

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
%if 0%{?rhel} >= 6
mkdir -p %{buildroot}%{_sysconfdir}/gridftp.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/gridftp.d/
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%if 0%{?rhel} >= 6
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/gridftp.d/udt-%{name}.conf
%endif

%changelog
* Thu Mar 13 2014 Carl Edquist <edquist@cs.wisc.edu> - 3.0.0-4
- Add globus-xio-udt-driver dependency for el6, and enable by default in
  /etc/gridftp.d/ (SOFTWARE-1412)

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 3.0.0-3
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.0-2
- Added dependencies on osg-version and osg-system-profiler

* Sat Sep 24 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 3.0.0-1
- Initial creation of meta-package for gridftp-hdfs.

