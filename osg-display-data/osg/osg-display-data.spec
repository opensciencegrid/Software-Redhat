Name: osg-display-data
Version: 1.0.9
Release: 1%{?dist}
Summary: Scripts and tools to generate the OSG Display's data.
Source: %{name}-%{version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Vendor: Brian Bockelman <bbockelm@cse.unl.edu>
Requires: MySQL-python
Requires: python-imaging
Requires: python-matplotlib >= 0.99
Requires: msttcorefonts
Requires: numpy >= 1.2
Provides: OSG_Display_Data = %{version}-%{release}
Obsoletes: OSG_Display_Data < 1.0.4-1

%description
UNKNOWN

%prep
%setup

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/var/log/osg_display
mkdir -p $RPM_BUILD_ROOT/var/www/html/osg_display

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%attr(-, apache, apache) /var/log/osg_display
%attr(-, apache, apache) /var/www/html/osg_display
%config(noreplace) %attr(600, apache, apache) /etc/osg_display/osg_display.conf
%config(noreplace) /etc/osg_display/osg_display.condor.cron

%changelog
* Tue Feb 18 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.9-1
- Don't discard most recent complete month (SOFTWARE-1400)

* Fri Jan 10 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.8-2
- Mark %%config files with noreplace

* Thu Jan 09 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.8-1
- Stop using deprecated sets module (SOFTWARE-1351)
- Increase default timeout and add --notimeout option (SOFTWARE-1352)
- Don't show stacktrace for --help output

* Tue Jan 07 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.7-1
- Address "-1 hours ago" issue (DISPLAY-16)

* Mon Jan 06 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.0.6-1
- Use months=12 instead of 13, etc, in config file (SOFTWARE-1326)
- Mark %%config files
- Add back osg_display dirs required for runtime
- Require python-imaging, used by display_graph.py (DISPLAY-8)

* Fri Dec 13 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0.5-2
- Add dist tag

* Fri Dec 13 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0.5-1
- Apply Brian Bockelman's fix to handle VOName 'Unknown' (SOFTWARE-1326)

* Mon Oct 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.0.4-1
- Package rename
- Update version

* Fri Apr 06 2012 Ashu Guru <aguru2@unl.edu> - 1.0.3-2
- Added the ignore index for index16 to force optimize query
- (https://jira.opensciencegrid.org/browse/DISPLAY-7)

* Mon Oct 11 2010 Brian Bockelman <bbockelm@cse.unl.edu> - 1.0.1-1
- Force-convert data to floats

* Mon Oct 11 2010 Brian Bockelman <bbockelm@cse.unl.edu> - 1.0.0-5
- Rebuild to decrease frequency of updates.
- Increase timeout value.

