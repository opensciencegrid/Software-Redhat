Summary: OSG metapackage for OASIS and CVMFS
Name: osg-oasis
Version: 1
Release: 2%{?dist}
License: ASL 2.0
Group: Applications/Grid
BuildArch: noarch
Requires: cvmfs >= 2.1.13
Requires: oasis-config >= 3

%description
%{summary}

%prep
exit 0

%build
exit 0

%install
exit 0

%clean
exit 0

%files

%changelog
* Tue Aug 13 2013 Dave Dykstra <dwd@fnal.gov> 1-2
- Update to require cvmfs 2.1.13

* Wed Jul 24 2013 Dave Dykstra <dwd@fnal.gov> 1-1
- Initial version

# vim:ft=spec
