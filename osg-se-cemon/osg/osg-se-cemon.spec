Name:           osg-se-cemon
Summary:        OSG CEMonitor and info provider tools for standalone SE
Version:        3.0.0
Release:        2%{?dist}
License:        GPL
Group:          System Environment/Daemons
URL:            https://twiki.grid.iu.edu/twiki/bin/view/Storage/WebHome

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: osg-version
Requires: osg-system-profiler
Requires: grid-certificates
Requires: glite-ce-monitor
Requires: gip
Requires: osg-configure-cemon
Requires: osg-configure-gip
Requires: osg-configure
Source0: gip.se_only.conf

%description
This is a meta-package for Compute Element Monitor (CEMon) and 
Generic Information Provider (GIP) for a stand-alone instance outside of 
a compute element.  This is intended for storage elements implementations.

%install
install -d $RPM_BUILD_ROOT/etc/gip
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/etc/gip/gip.se_only.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
/etc/gip/gip.se_only.conf

%changelog
* Tue Feb 7 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-2
- Added osg-configure to the list of dependencies

* Mon Feb 6 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-1
- Initial creation of meta-packages

