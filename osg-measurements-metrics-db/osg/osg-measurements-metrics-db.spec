%define name osg-measurements-metrics-db
%define version 1.1
%define unmangled_version 1.1
%define release 3

Summary: DB code - OSG Measurements and Metrics webpages.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Brian Bockelman <bbockelm@cse.unl.edu>
Requires: graphtool >= 0.6.4 MySQL-python python-sqlite python-cheetah /usr/bin/ldapsearch python-cherrypy python-ZSI python-setuptools
Obsoletes: OSG-Measurements-Metrics-Db
Url: http://t2.unl.edu/documentation/gratia_graphs

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%changelog
* Mon Jan 14 2013 Ashu Guru <aguru2@unl.edu>
- Renamed the package to lower name and fixed minor labeling errors
- (https://jira.opensciencegrid.org/browse/METRICS-15)

* Thu Jan 10 2013 Derek Weitzel <dweitzel@cse.unl.edu> - 1.1-1
- Update to 1.1

* Thu Jan 10 2013 Ashu Guru <aguru2@unl.edu>
- Added Pie chart for XSEDE Project Names and fixed exclude project
- (https://jira.opensciencegrid.org/browse/GRATIA-71)

* Wed Jan 01 2013 Ashu Guru <aguru2@unl.edu>
- Added new charts for XSEDE Project Names
- (https://jira.opensciencegrid.org/browse/GRATIA-71)

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
