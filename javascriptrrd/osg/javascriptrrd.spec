
Name: javascriptrrd
Version: 1.1.1
Release: 1.2%{?dist}
Summary: A package to render RRD databases in javascript using Flot

License: MIT
# To make source tar ball (Be sure to get version with flot):
# mv javascriptrrd-1.1.0-with-flot-0.7.7-tooltip-0.4.4.tgz javascriptrrd-1.1.0.tar.gz
Source0: %{name}-%{version}.tgz
BuildArch: noarch

%description
javascriptRRD is a javascript library for reading Round Robin Database (RRD) archives (produced by rrdtool) using AJAX-like techniques. The library also provides graphing classes leveraging the Flot library.



%prep
%setup -q

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/%{_datadir}/javascriptrrd/js
install -m 644 src/lib/*.js $RPM_BUILD_ROOT/%{_datadir}/javascriptrrd/js
install -m 755 -d $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd
install -m 755 -d $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/rrds
install -m 644 data/example_rrds/*.rrd $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/rrds/
install -m 644 doc/*.txt $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/
install -m 755 -d $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/html
install -m 644 doc/lib/*.html $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/html
install -m 755 -d $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/example_site
install -m 644 src/examples/*.html $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/example_site

# Include flot as well
install -m 755 -d $RPM_BUILD_ROOT/%{_datadir}/javascriptrrd/flot
install -m 644 flot/*.js $RPM_BUILD_ROOT/%{_datadir}/javascriptrrd/flot
install -m 755 -d $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/flot
install -m 644 flot/*.txt $RPM_BUILD_ROOT/%{_defaultdocdir}/javascriptrrd/flot


%files
%defattr(-,nobody,nobody,-)
%{_defaultdocdir}/javascriptrrd/*
%{_datadir}/javascriptrrd/js/*.js
%{_datadir}/javascriptrrd/flot/*.js
%{_defaultdocdir}/javascriptrrd/flot

%changelog
* Thu Jan 26 2023 Carl Edquist <edquist@cs.wisc.edu> - 1.1.1-1.2
- Bump to rebuild (SOFTWARE-5457)

* Mon Dec 12 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.1.1-1.1
- Bump to rebuild (SOFTWARE-5384)

* Tue Apr 29 2014 Edgar Fajardo <efajardo@phsics.ucsd.edu> 1.1.1-1
Updated to the 1.1.1 release.

* Wed Nov 27 2013 Edgar Fajardo <efajardo@cern.ch> 1.1.0-1
Updated to the 1.1.0 release. It could not be a pass through build since the dist was missing in the Release entry in the spec file

* Fri Nov 8 2013 Igor Sfiligoi <isfiligoi@ucsd.edu> 1.1.0-1
Updated to the 1.1.0 release. Not using Flot 0.8 yet, since it is not backward compatible.

* Sun Apr 7 2013 Igor Sfiligoi <isfiligoi@ucsd.edu> 0.6.4-1
Updated to th 0.6.4 release.

* Wed Aug 24 2011 Igor Sfiligoi <isfiligoi@ucsd.edu> 0.6.1-1
Updated to th 0.6.1 release.

* Thu Jun 8 2011 Derek Weitzel <dweitzel@cse.unl.edu> 0.6.0-1
Updated to the 0.6.0 release.

* Thu Jun 3 2010 Derek Weitzel <dweitzel@cse.unl.edu> 0.5.0-2
Added flot to the install as well


