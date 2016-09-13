Summary: OSG metapackage for OASIS and CVMFS
Name: osg-oasis
Version: 7
Release: 3%{?dist}
License: ASL 2.0
Group: Applications/Grid
BuildArch: noarch
Requires: cvmfs >= 2.3.0
Requires: cvmfs-config-osg >= 1.2-5
Requires: cvmfs-x509-helper >= 0.9

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
* Wed Jun 29 2016 Dave Dykstra <dwd@fnal.gov> 7-3
- Update to cvmfs-config-osg-1.2-5

* Wed Jun 29 2016 Dave Dykstra <dwd@fnal.gov> 7-2
- Update to cvmfs-config-osg-1.2-4

# this version number is out of order because 7-1 was originally osg-upcoming only
#* Thu May 26 2016 Dave Dykstra <dwd@fnal.gov> 6-5
#- Update to cvmfs-2.2.3

* Fri Apr 29 2016 Dave Dykstra <dwd@fnal.gov> 7-1
- Update to cvmfs 2.3.0, and add cvmfs-x509-helper 0.9

* Fri Mar 25 2016 Dave Dykstra <dwd@fnal.gov> 6-4
- Update to cvmfs-config-osg-1.2-3

* Tue Feb  9 2016 Dave Dykstra <dwd@fnal.gov> 6-3
- Update to cvmfs-2.2.1

* Mon Feb  1 2016 Dave Dykstra <dwd@fnal.gov> 6-2
- Fix typo in cvmfs version number

* Mon Feb  1 2016 Dave Dykstra <dwd@fnal.gov> 6-1
- Require cvmfs-2.2.0 and cvmfs-config-osg-1.2-2

* Tue Oct 27 2015 Dave Dykstra <dwd@fnal.gov> 5-3
- Require cvmfs-config-osg-1.1-8

* Tue Jul 28 2015 Dave Dykstra <dwd@fnal.gov> 5-2
- Require cvmfs-config-osg-1.1-7

* Wed Mar 24 2015 Dave Dykstra <dwd@fnal.gov> 5-1
- Require cvmfs-2.1.20 and cvmfs-config-osg-1.1

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
