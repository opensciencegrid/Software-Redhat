Name: installed-capacity-report
Version: 1.1
Release: 2%{?dist}
Summary: Installed Capacity Report
Requires: python-json
Provides: InstalledCapacityReport = %{version}-%{release}
Obsoletes: InstalledCapacityReport < 1.1-2
Source: %{name}-%{version}.tar.gz
Group: Development/System
License: GPL
URL: http://osgbdiifilter.svn.sourceforge.net/viewvc/osgbdiifilter/pledgedCapacity/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
BuildArch: noarch

# The GOC installs all their software under /usr/local
%define basedir %{_usr}/local/%{name}

%description
WLCG OIM Installed Capacity Report RPMs

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{basedir}/bin/
install -d $RPM_BUILD_ROOT%{basedir}/etc/
install -d $RPM_BUILD_ROOT%{basedir}/log/
install -m 0755 bin/report.py    $RPM_BUILD_ROOT%{basedir}/bin/
install -m 0755 bin/sendEmail.py $RPM_BUILD_ROOT%{basedir}/bin/
install -m 0755 bin/wlcg.sh      $RPM_BUILD_ROOT%{basedir}/bin/
install -m 0644 etc/config.ini   $RPM_BUILD_ROOT%{basedir}/etc/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{basedir}/bin/report.py*
%{basedir}/bin/sendEmail.py*
%{basedir}/bin/wlcg.sh
%config %{basedir}/etc/config.ini
%dir %{basedir}/log

%post
echo "--------------------------------------------------------"
echo "   %{name} Installed Capacity Report Installed in %{basedir}"
echo "   %{name} Please do the following:"
echo "   1) Configure email in %{basedir}/etc/config.ini"
echo "   2) make cron entry to run the report as %{basedir}/bin/report.py --email"
echo "--------------------------------------------------------"

%changelog
* Thu Oct 17 2013 Brian Lin <blin@cs.wisc.edu> - 1.1-2
- Package rename

* Fri Jul 19 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.1-1
- Spec cleanup, and use new tarball

* Thu Jan 31 2013  Ashu Guru <aguru2@unl.edu> 1.0-13
- Added UFlorida-HPC https://ticket.grid.iu.edu/goc/13345

* Mon Aug 20 2012  Ashu Guru <aguru2@unl.edu> 1.0-12
- Added exception handler for missing site

* Wed Aug 08 2012  Ashu Guru <aguru2@unl.edu> 1.0-11
- Added python-json as dependency

* Tue Jul 31 2012  Ashu Guru <aguru2@unl.edu> 1.0-10
- Added USCMS_Tier2

* Thu Dec 1 2011  Ashu Guru <aguru2@unl.edu> 1.0-8
- Edit for US-FNAL-CMS look at https://ticket.grid.iu.edu/goc/11033 for details

* Tue Oct 11 2011  Ashu Guru <aguru2@unl.edu> 1.0-7
- Changed the static map tobe read from http://gstat-wlcg.cern.ch/apps/topology/ instead

* Mon Jul 18 2011  Ashu Guru <aguru2@unl.edu> 1.0-4
- Modified the config file so it does not get overwritten

* Mon Jul 18 2011  Ashu Guru <aguru2@unl.edu> 1.0-2
- Removed logging and printed errors on console

* Thu Jul 7 2011  Ashu Guru <aguru2@unl.edu> 1.0-1
- Initial version of the package

