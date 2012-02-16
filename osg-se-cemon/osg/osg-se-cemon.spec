Name:           osg-se-cemon
Summary:        OSG CEMonitor and info provider tools for standalone SE
Version:        3.0.0
Release:        4%{?dist}
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
Requires: osg-configure-ce
Requires: osg-configure
Requires: gums-client

%description
This is a meta-package for Compute Element Monitor (CEMon) and 
Generic Information Provider (GIP) for a stand-alone instance outside of 
a compute element.  This is intended for storage elements implementations.

%install
install -d $RPM_BUILD_ROOT/etc/gip

%clean
rm -rf $RPM_BUILD_ROOT

%files
/etc/gip/gip.se_only.conf

%changelog
* Tue Feb 14 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-4
- Added configure-osg-ce to dependencies.
- As per Tony, this is needed by gip to function correctly.

* Tue Feb 14 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-3
- Added gums-client to the list of dependencies

* Tue Feb 7 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-2
- Added osg-configure to the list of dependencies

* Mon Feb 6 2012 Doug Strain <dstrain@fnal.gov> - 3.0.0-1
- Initial creation of meta-packages

