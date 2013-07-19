Name: InstalledCapacityReport          
Version: 1.0        
Release: 13
Summary: Installed Capacity Report        
Requires: python-json
Source: InstalledCapacityReport.tar      
Group: Development/System          
License: GPL        
URL: http://osgbdiifilter.svn.sourceforge.net/viewvc/osgbdiifilter/pledgedCapacity/ 

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
BuildArch: noarch

%description
WLCG OIM Installed Capacity Report RPMs

%install
rm -rf $RPM_BUILD_ROOT
tar -xvf $RPM_SOURCE_DIR/InstalledCapacityReport.tar
mkdir -p $RPM_BUILD_ROOT/%{_usr}/local/
cp -rf InstalledCapacityReport $RPM_BUILD_ROOT%{_usr}/local/
mkdir -p $RPM_BUILD_ROOT%{_usr}/local/InstalledCapacityReport/log

%clean
rm -rf InstalledCapacityReport

%files
%defattr(-,root,root,-)
%{_usr}/local/InstalledCapacityReport/bin/*
%dir %{_usr}/local/InstalledCapacityReport/log
%doc

%config %{_usr}/local/InstalledCapacityReport/etc/config.ini



%post
echo "--------------------------------------------------------"
echo "   %{name} Installed Capacity Report Installed in %{_usr}/local/InstalledCapacityReport"
echo "   %{name} Please do the following:"
echo "   1) Configure email in %{_usr}/local/InstalledCapacityReport/etc/config.ini"    
echo "   2) make cron entry to run the report as %{_usr}/local/InstalledCapacityReport/bin/report.py --email"    
echo "--------------------------------------------------------"

%changelog
* Thu Jan 31 2013  Ashu Guru <aguru2@unl.edu> 1.13
- Added UFlorida-HPC https://ticket.grid.iu.edu/goc/13345
* Mon Aug 20 2012  Ashu Guru <aguru2@unl.edu> 1.12
- Added exception handler for missing site
* Wed Aug 08 2012  Ashu Guru <aguru2@unl.edu> 1.11
- Added python-json as dependency
* Tue Jul 31 2012  Ashu Guru <aguru2@unl.edu> 1.10
- Added USCMS_Tier2
* Thu Dec 1 2011  Ashu Guru <aguru2@unl.edu> 1.08
- Edit for US-FNAL-CMS look at https://ticket.grid.iu.edu/goc/11033 for details
* Tue Oct 11 2011  Ashu Guru <aguru2@unl.edu> 1.07
- Changed the static map tobe read from http://gstat-wlcg.cern.ch/apps/topology/ instead
* Mon Jul 18 2011  Ashu Guru <aguru2@unl.edu> 1.04
- Modified the config file so it does not get overwritten
* Mon Jul 18 2011  Ashu Guru <aguru2@unl.edu> 1.02
- Removed logging and printed errors on console
* Thu Jul 7 2011  Ashu Guru <aguru2@unl.edu> 1.01
- Initial version of the package

