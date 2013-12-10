%define name graphtool
%define version 0.6.6
%define release 17
%define _unpackaged_files_terminate_build 0

Summary: CMS Common Graphing Package.
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Brian Bockelman <bbockelm@math.unl.edu>
Requires: python >= 2.3 python-matplotlib >= 0.97.1 numpy >= 1.2.1 python-imaging >= 1.1.5

%description
UNKNOWN

%prep
%setup

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%changelog
* Tue Dec 10 2013 Carl Edquist <edquist@cs.wisc.edu> - 0.6.6-17
- Remove _tmppath define, which was breaking osg-build prebuild
- Add dist tag

* Wed Feb 20 2013 Ashu Guru <aguru2@unl.edu>
- Added space gaps for the query placeholders in connection_manager to avoid index clashes in find

* Fri Jan 11 2013 Ashu Guru <aguru2@unl.edu>
- Moving spec file to upstream

* Wed Jan 09 2013 Ashu Guru <aguru2@unl.edu>
- Fixing the problem of static sites

* Tue Oct 02 2012 Ashu Guru <aguru2@unl.edu>
- Fixing xsl for safari and Chrome

* Mon May 31 2012 Ashu Guru <aguru2@unl.edu>
- Updated for fixing the number of bins and days of bar chart report issue
- (https://jira.opensciencegrid.org/browse/GRATIAWEB-17)

* Mon Apr 9 2012 Ashu Guru <aguru2@unl.edu>
- Updated the javascript code for resolving the IE dropdown incompatability
- (http://jira.opensciencegrid.org/browse/GRATIAWEB-14)


