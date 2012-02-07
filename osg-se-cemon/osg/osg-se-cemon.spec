Name:           osg-se-cemon
Summary:        OSG CEMonitor and info provider tools for standalone SE
Version:        3.0.0
Release:        1%{?dist}
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

%description
This is a meta-package for Compute Element Monitor (CEMon) and 
Generic Information Provider (GIP) for a stand-alone instance outside of 
a compute element.  This is intended for storage elements implementations.


%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Mon Feb 6 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-1
- Initial creation of meta-packages

