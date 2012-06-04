Name: gratia-reporting
Summary: Reporting Gratia OSG accounting system
Group: Applications/System
Version: 1.12
Release: 5.pre%{?dist}
License: GPL
Group: Applications/System
URL: http://sourceforge.net/projects/gratia/

Source0: gratia-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: gratia-probe-common
Requires: libxml2-devel
Requires: mutt
Requires: perl-libxml-perl
Requires: perl-Date-Calc
Requires: perl-XML-LibXML 
#Requires: perl-IPC-Run --enablerepo dag
#Requires:perl-Text-Table --enablerepo dag


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
install -m 0644 reporting/summary/gradedefficiency      $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/gratiaSum.py          $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/gratiaSum.cron.sh     $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/longjobs              $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/newUsers              $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/osg-users             $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/range                 $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/range_mutt_nightly.sh $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0644 reporting/summary/range_mutt.sh         $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/reporting             $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/transfer              $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/usersitereport        $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
install -m 0755 reporting/summary/usersreport            $RPM_BUILD_ROOT%{_datadir}/gratia-reporting
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

%changelog
* Mon Jun 04 2012 Tanya Levshina <tlevshin@fnal.gov> - 1.12.5pre
add mysql and other dependencies , changed script permision

* Sun Jun 03 2012 Hyunwoo Kim <hyunwoo@fnal.gov> 
initial implementation of gratia.spec 

