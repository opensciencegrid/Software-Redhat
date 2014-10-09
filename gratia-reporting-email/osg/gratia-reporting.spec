Name: gratia-reporting-email
Summary: Email Reporting for Gratia OSG accounting system
Group: Applications/System
Version: 1.15.1
Release: 1%{?dist}
License: GPL
Group: Applications/System
URL: http://sourceforge.net/projects/gratia/

Obsoletes: gratia-reporting < 1.13.10-2
Provides: gratia-reporting = %{version}-%{release}
Source0: gratia-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: gratia-probe-common
Requires: mysql 
Requires: libxml2-devel
Requires: mutt
Requires: perl-libxml-perl
Requires: perl-Date-Calc
Requires: perl-XML-LibXML 
Requires: perl-DBD-MySQL
Requires: perl-IPC-Run
Requires: perl-Text-Table
#perl-IPC-Run and perl-Text-Table are in dag repo


%description
%{summary}

%prep
%setup -q -n gratia-%{version}

%build
#pushd build-scripts
#sed -i 's|@GRATIA_VERSION@|%{version}|' Makefile
#make
#popd

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -d $RPM_BUILD_ROOT%{_datadir}/gratia-reporting/GratiaReporting
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gratia/gratia-reporting

install -m 0644 reporting/summary/AccountingReports.py  $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/all-sites-oim         $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/all-vos-oim           $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/compareVOs.py         $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/configReport.py       $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/daily                 $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/daily_mutt.sh         $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/dailyStatus           $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/efficiency            $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/getConfigInfo.py      $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/gradedefficiency      $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/gratiaSum.py          $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/gratiaSum.cron.sh     $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/longjobs              $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/newUsers              $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/osg-users             $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/range                 $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/range_mutt_nightly.sh $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/range_mutt.sh         $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/reporting             $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/transfer              $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/transfertrvo          $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/usersitereport        $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/usersreport           $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/voefficiency          $RPM_BUILD_ROOT%{_datadir}/gratia-reporting

install -m 0644 reporting/summary/GratiaReporting/Data.pm          $RPM_BUILD_ROOT%{_datadir}/gratia-reporting/GratiaReporting/
install -m 0644 reporting/summary/GratiaReporting/JobInfoBranch.pm $RPM_BUILD_ROOT%{_datadir}/gratia-reporting/GratiaReporting/
install -m 0644 reporting/summary/GratiaReporting/JobInfo.pm       $RPM_BUILD_ROOT%{_datadir}/gratia-reporting/GratiaReporting/
install -m 0644 reporting/summary/GratiaReporting/Person.pm        $RPM_BUILD_ROOT%{_datadir}/gratia-reporting/GratiaReporting/
install -m 0644 reporting/summary/GratiaReporting/Reporter.pm      $RPM_BUILD_ROOT%{_datadir}/gratia-reporting/GratiaReporting/

install -m 0644 reporting/summary/all-vos.dat                 $RPM_BUILD_ROOT%{_sysconfdir}/gratia/gratia-reporting/
install -m 0644 reporting/summary/gratiareports.conf.template $RPM_BUILD_ROOT%{_sysconfdir}/gratia/gratia-reporting/gratiareports.conf
install -m 0644 reporting/summary/muttrc                      $RPM_BUILD_ROOT%{_sysconfdir}/gratia/gratia-reporting/
install -m 0644 reporting/summary/user-reports.dat            $RPM_BUILD_ROOT%{_sysconfdir}/gratia/gratia-reporting/

# Logs
mkdir -p $RPM_BUILD_ROOT%{_var}/log/gratia-reporting
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/gratia/tmp

%files
%defattr(-,root,root,-)
%{_datadir}/gratia-reporting/
%{_datadir}/gratia-reporting/GratiaReporting/
%{_sysconfdir}/gratia/gratia-reporting/
%dir %{_var}/log/gratia-reporting
%dir %{_var}/lib/gratia/tmp
%config(noreplace) %{_sysconfdir}/gratia/gratia-reporting/all-vos.dat
%config(noreplace) %{_sysconfdir}/gratia/gratia-reporting/user-reports.dat
%config(noreplace) %{_sysconfdir}/gratia/gratia-reporting/muttrc
%config(noreplace) %{_sysconfdir}/gratia/gratia-reporting/gratiareports.conf


%changelog
* Thu Oct 09 2014 Hyunwoo Kim <hyunwoo@fnal.gov> - 1.15.1 - 1
modified AccountingReport.py to deal with NULL in DB caused by zero WallDuration reported by some probes

* Tue Oct 22 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.13.10-2
- Renamed to gratia-reporting-email

* Fri Apr 26 2013 Hyunwoo Kim <hyunwoo@fnal.gov> - 1.13.10 - 1
modified AccountingReport.py and range_mutt_nightly.sh, and created transfertrvo, for a new report transfer vo decache

* Tue Mar 12 2013 Tanya Levshina <tlevshin@fnal.gov> - 1.13.9 - 4
fixes for AccountingReport.py and compareVOs.py

* Fri Sep 14 2012 Hyunwoo Kim <hyunwoo@fnal.gov>
modified such that all 4 files in /etc/gratia/gratia-reporting/ can be saved

* Thu Jul 05 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.13.4pre
all-sites-oim modification, gratia-reporting spec

* Thu Jul 05 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.11
production release 

* Tue Jul 03 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.10pre
fixed cron file 

* Mon Jun 25 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.8
production release

* Wed Jun 20 2012 Tanya Levshina <tlevshin@fnal.gob> - 1.12.7pre
gratia pre-production release (from gratia trunk)

* Fri Jun 15 2012 Tanya Levshina <tlevshin@fnal.gob> - 1.12.6pre
New version of reporting with several fixes, really added mysql depedency this time

* Tue Jun 12 2012 Hyunwoo Kim <hyunwoo@fnal.gov>
Tanya found out another dependency, perl-DBD-MySQL

* Mon Jun 04 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.5pre
add mysql and other dependencies , changed script permision

* Sun Jun 03 2012 Hyunwoo Kim <hyunwoo@fnal.gov> 
initial implementation of gratia.spec 
