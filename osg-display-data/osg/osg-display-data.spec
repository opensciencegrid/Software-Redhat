Name: osg-display-data
Version: 1.0.4
Release: 1
Summary: Scripts and tools to generate the OSG Display's data.
Source: %{name}-%{version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Vendor: Brian Bockelman <bbockelm@cse.unl.edu>
Requires: MySQL-python
Requires: python-matplotlib >= 0.99
Requires: msttcorefonts
Requires: numpy >= 1.2
Provides: OSG_Display_Data = %{version}-%{release}
Obsoletes: OSG_Display_Data < 1.0.4-1

%description
UNKNOWN

%prep
%setup -n %{name}-%{version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Mon Oct 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.0.4-1
- Package rename
- Update version

* Fri Apr 06 2012 Ashu Guru <aguru2@unl.edu> - 1.0.3-2
- Added the ignore index for index16 to force optimize query
- (https://jira.opensciencegrid.org/browse/DISPLAY-7)
