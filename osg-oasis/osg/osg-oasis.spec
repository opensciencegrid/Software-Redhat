Summary: OSG metapackage for OASIS and CVMFS
Name: osg-oasis
Version: 4
Release: 2%{?dist}
License: ASL 2.0
Group: Applications/Grid
BuildArch: noarch
Requires: cvmfs >= 2.1.19
Requires: oasis-config >= 7

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
* Fri Jun 20 2014 Dave Dykstra <dwd@fnal.gov> 4-2
- Require oasis-config 7.  Also update cvmfs require to 2.1.19 although
  that's effectively no change because 2.1.18 was never released.

* Mon Apr 21 2014 Dave Dykstra <dwd@fnal.gov> 4-1
- Require cvmfs 2.1.18 and oasis-config 6

* Thu Mar 20 2014 Dave Dykstra <dwd@fnal.gov> 3-2
- Fix require of 2.1.17

* Thu Mar 20 2014 Dave Dykstra <dwd@fnal.gov> 3-1
- Update to require cvmfs 2.1.17 & oasis-config 5

* Thu Sep 26 2013 Dave Dykstra <dwd@fnal.gov> 2-2
- Update to require cvmfs 2.1.15

* Thu Aug 22 2013 Dave Dykstra <dwd@fnal.gov> 2-1
- Update to require oasis-config 4

* Tue Aug 13 2013 Dave Dykstra <dwd@fnal.gov> 1-3
- Update to require cvmfs 2.1.14

* Tue Aug 13 2013 Dave Dykstra <dwd@fnal.gov> 1-2
- Update to require cvmfs 2.1.13

* Wed Jul 24 2013 Dave Dykstra <dwd@fnal.gov> 1-1
- Initial version

# vim:ft=spec
