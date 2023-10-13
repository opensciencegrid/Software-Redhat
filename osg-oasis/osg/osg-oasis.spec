Summary: OSG metapackage for OASIS and CVMFS
Name: osg-oasis
Version: 20
Release: 3%{?dist}
License: ASL 2.0
BuildArch: noarch
# Note: cannot require an exact release number (after a dash) unless 
#   including the dist as well, e.g. -2%{?dist}
Requires: cvmfs = 2.11.1
Requires: cvmfs-config-osg = 2.5
Requires: scitokens-cpp >= 0.6.2
Requires: cvmfs-x509-helper >= 2.3

%description
%{summary}

%prep
exit 0

%build
exit 0

%install
exit 0

%files

%changelog
* Fri Oct 13 2023 Dave Dykstra <dwd@fnal.gov> 20-3
- Update to cvmfs-2.11.1

* Fri Sep 8 2023 Matt Westphall <westphall@wisc.edu> 200
- Update to cvmfs-x509-helper 2.3

* Fri Aug 18 2023 Dave Dykstra <dwd@fnal.gov> 20-1
- Update to cvmfs-2.11.0

* Mon Feb 27 2023 Carl Vuosalo <covuosalo@wisc.edu> 19-3
- Update to cvmfs-2.10.1

* Thu Feb 16 2023 Carl Edquist <edquist@cs.wisc.edu> - 19-2
- Bump to rebuild for RPM GPG key (SOFTWARE-5457)

* Tue Oct 11 2022 Dave Dykstra <dwd@fnal.gov> 19-1
- Update to cvmfs-2.10.0

* Fri Jun 10 2022 Dave Dykstra <dwd@fnal.gov> 18-3
- Update to cvmfs-2.9.3

* Mon Mar 23 2022 Dave Dykstra <dwd@fnal.gov> 18-2
- Update to cvmfs-2.9.2

* Mon Nov 15 2021 Dave Dykstra <dwd@fnal.gov> 18-1
- Update to cvmfs-2.9.0

* Mon Sep 13 2021 Dave Dykstra <dwd@fnal.gov> 17-5
- Update to cvmfs-2.8.2

* Mon Aug 23 2021 Dave Dykstra <dwd@fnal.gov> 17-4
- Add requirement for scitokens-cpp >= 0.6.2

* Mon Aug 23 2021 Dave Dykstra <dwd@fnal.gov> 17-3
- Update to cvmfs-x509-helper-2.2

* Tue Mar 30 2021 Dave Dykstra <dwd@fnal.gov> 17-2
- Update to cvmfs-2.8.1

* Tue Jan 19 2021 Dave Dykstra <dwd@fnal.gov> 17-1
- Update to cvmfs-2.8.0

* Wed Oct 14 2020 Dave Dykstra <dwd@fnal.gov> 16-7
- Update to cvmfs-2.7.5 and cvmfs-config-osg-2.5

* Wed Sep 09 2020 Dave Dykstra <dwd@fnal.gov> 16-6
- Update to cvmfs-2.7.4

* Wed Jun 24 2020 Dave Dykstra <dwd@fnal.gov> 16-5
- Update to cvmfs-2.7.3
- Update to cvmfs-config-osg-2.4-4

* Wed Apr 22 2020 Dave Dykstra <dwd@fnal.gov> 16-3
- Update to cvmfs-2.7.2

* Tue Feb 17 2020 Dave Dykstra <dwd@fnal.gov> 16-2
- Update to cvmfs-2.7.1

* Tue Nov 03 2019 Dave Dykstra <dwd@fnal.gov> 16-1
- Update to cvmfs-2.7.0

* Thu Sep 19 2019 Dave Dykstra <dwd@fnal.gov> 15-4
- Update to cvmfs-x509-helper-2.1

* Mon Sep 09 2019 Dave Dykstra <dwd@fnal.gov> 15-3
- Update to cvmfs-2.6.3

* Tue Aug 13 2019 Dave Dykstra <dwd@fnal.gov> 15-2
- Update to cvmfs-2.6.2

* Wed Aug 07 2019 Dave Dykstra <dwd@fnal.gov> 15-1
- Update to cvmfs-2.6.1 and cvmfs-config-osg-2.4

* Fri Aug 02 2019 Carl Edquist <edquist@cs.wisc.edu> - 14-4
- Update cvmfs-config-osg version requirement to 2.4 (SOFTWARE-3761)

* Tue Jul 30 2019 Edgar Fajardo <emfajard@ucsd.edu> 14-3
- Changing version requirement on cvmfs-x509-helper to more or equal
  (SOFTWARE-3384)

* Tue Jul 30 2019 Edgar Fajardo <emfajard@ucsd.edu> 14-1
- Removing version requirements for other packages (SOFTWARE-3384)

* Thu Jun 20 2019 Diego Davila <didavila@ucsd.edu> 13-1
- Update to require cvmfs-x509-helper-2.0 (SOFTWARE-3736)

* Tue Mar 12 2019 Dave Dykstra <dwd@fnal.gov> 12-1
- Update to require cvmfs-2.6.0

* Tue Nov 27 2018 Dave Dykstra <dwd@fnal.gov> 11-1
- Update to require cvmfs-2.5.2

* Thu Aug 09 2018 Carl Edquist <edquist@cs.wisc.edu> - 9-3
- Update cvmfs-x509-helper version requirement (SOFTWARE-3376)

* Thu May 03 2018 Dave Dykstra <dwd@fnal.gov> 9-2
- Fix accidental changes to the other version numbers

* Thu May 03 2018 Dave Dykstra <dwd@fnal.gov> 9-1
- Update to cvmfs-2.4.5

* Tue Dec 19 2017 Dave Dykstra <dwd@fnal.gov> 8-5
- Update to cvmfs-2.4.4 and make the cvmfs-config-osg version not
  include the release part.

* Tue Dec 19 2017 Dave Dykstra <dwd@fnal.gov> 8-4
- Update to cvmfs-x509-helper to version 1.0.  (This version also for
  testing.)

* Tue Dec 19 2017 Dave Dykstra <dwd@fnal.gov> 8-3
- Switch to using '=' versions instead of >= versions.  (This version
  is for experimenting, not expected to be released).

* Fri Oct 20 2017 Dave Dykstra <dwd@fnal.gov> 8-2
- Update to cvmfs-2.4.2

* Wed Sep  9 2017 Dave Dykstra <dwd@fnal.gov> 8-1
- Update to cvmfs-2.4.1

* Thu Mar 23 2017 Brian Lin <blin@fnal.gov> 7-9
- Update to cvmfs-2.3.5

* Wed Mar 22 2017 Dave Dykstra <dwd@fnal.gov> 7-8
- Update to cvmfs-2.3.4

* Wed Feb 15 2017 Dave Dykstra <dwd@fnal.gov> 7-7
- Update to cvmfs-config-osg-2.0-1

* Sat Feb 11 2017 Dave Dykstra <dwd@fnal.gov> 7-6
- Update to cvmfs-2.3.3 and config-osg-1.3-1

* Tue Sep 20 2016 Dave Dykstra <dwd@fnal.gov> 7-5
- Update to cvmfs-2.3.2

* Tue Sep 13 2016 Dave Dykstra <dwd@fnal.gov> 7-4
- Update to cvmfs-2.3.1

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

