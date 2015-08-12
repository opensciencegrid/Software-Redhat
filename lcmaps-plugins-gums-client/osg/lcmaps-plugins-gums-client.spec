Name:           lcmaps-plugins-gums-client
Version:        0.0.2
Release:        4%{?dist}
Summary:        GUMS support for lcmaps

Group:          System Environment/Tools
License:        Apache 2.0

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:       lcmaps-plugins-scas-client
# Only Obsolete specific OSG version because NIKHEF has another package
#   by the same name
Obsoletes:	lcmaps-plugins-gums = 0.0.1-1

%description
%{summary}

%prep

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/man/man8
cd $RPM_BUILD_ROOT%{_datadir}/man/man8
ln -s lcmaps_plugins_scas_client.8.gz lcmaps_plugins_gums_client.8.gz

mkdir -p $RPM_BUILD_ROOT%{_libdir}/lcmaps
ln -s lcmaps_scas_client.mod $RPM_BUILD_ROOT%{_libdir}/lcmaps/lcmaps_gums_client.mod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/man/man8/lcmaps_plugins_gums_client.8.gz
%{_libdir}/lcmaps/lcmaps_gums_client.mod

%changelog
* Wed Dec 26 2012 Dave Dykstra <dwd@fnal.gov> 0.0.2-4.osg
- Remove support for modules symlink and %ghost file

* Fri Dec 30 2011 Dave Dykstra <dwd@fnal.gov> 0.0.2-3.osg
- Added symlink to man page
- Moved plugin symlink to libdir/lcmaps directory and added %ghost for it
  in the modules directory, since modules is currently a symlink to lcmaps

* Fri Sep 01 2011 Dave Dykstra <dwd@fnal.gov> 0.0.2-2.osg
- Just add the %{?dist} to the release to be like the others

* Mon Aug 22 2011 Dave Dykstra <dwd@fnal.gov> 0.0.2-1
- Change name from lcmaps-plugins-gums to lcmaps-plugins-gums-client

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-1
- Initial packaging.

