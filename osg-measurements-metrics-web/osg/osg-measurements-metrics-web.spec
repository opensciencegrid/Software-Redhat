%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           osg-measurements-metrics-web
Version:        1.2
Release:        0%{?dist}
Summary:        OSG Measurements and Metrics web and database

Group:          Applications/System
License:        Apache 2.0
URL:            http://t2.unl.edu/documentation/gratia_graphs
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-setuptools
Requires:       graphtool >= 0.6.4 
Requires:	MySQL-python 
Requires:	python-sqlite 
Requires:	python-cheetah 
Requires:	/usr/bin/ldapsearch 
Requires:	python-cherrypy >= 3.1.2 
Requires:	python-ZSI 
Requires: 	python-setuptools 
Requires: 	osg-measurements-metrics-db 
%if 0%{?el5}
Requires:	python-json 
%endif
Requires:	gratia-probe-common   
Requires:	gratia-probe-services




%description


%prep
%setup -q


%build
cp setup/setup_Web.py ./setup.py
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build



%install
rm -rf $RPM_BUILD_ROOT


%{__python} setup.py install --skip-build --root %{buildroot}

install -d %{buildroot}/%{_initrddir}
mv %{buildroot}/etc/init.d/GratiaWeb %{buildroot}/%{_initrddir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/GratiaWeb/*
%config %{_sysconfdir}/wlcg_email.conf.rpmnew
%config %{_sysconfdir}/access.db
%config %{_sysconfdir}/osg_graphs.conf
%{_sysconfdir}/cron.d/*
%{_sysconfdir}/logrotate.d/*
%{_initrddir}/*


%{python_sitelib}/*




%changelog
* Mon Feb 18 2013 Ashu Guru <aguru2@unl.edu>
- Added the Under Construction and BatchPilot 
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-28)

* Thu Jan 10 2013 Derek Weitzel <dwetizel@cse.unl.edu> - 1.1-4
- Fixing initrd dir

* Thu Jan 10 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 1.1-3
- Fixing sysconfdir in the spec file

* Thu Jan 10 2013 Derek Weitzel <dwetizel@cse.unl.edu> - 1.1-2
- Updating datarootdir to multi-platform version datadir

* Thu Jan 10 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 1.1-1
- Update to 1.1

* Mon Jun 28 2012 Ashu Guru <aguru2@unl.edu>
- Updated for gratia_data.cron emitting error email on gratiaweb-itb.grid.iu.edu
- (https://jira.opensciencegrid.org/browse/SOFTWARE-684)

* Mon Jun 28 2012 Ashu Guru <aguru2@unl.edu>
- Updated for fixing number of days in pie chart
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-17)

* Mon May 31 2012 Ashu Guru <aguru2@unl.edu>
- Updated for fixing the number of bins and days of bar chart report issue
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-17)

* Thu Apr 5 2012 Ashu Guru <aguru2@unl.edu>
- Top Pull Downs on the Gratia Web Interface 
- (http://jira.opensciencegrid.org/browse/GRATIAWEB-14)

* Wed Apr 4 2012 Ashu Guru <aguru2@unl.edu>
- Gratia/WLCG interface/reporting of Tier1/2 sites changes required due to new APEL SSM interface 
- (https://jira.opensciencegrid.org/browse/METRICS-10)

