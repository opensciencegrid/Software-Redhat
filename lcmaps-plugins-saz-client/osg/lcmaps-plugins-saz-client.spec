
%define modname lcmaps_saz_client.mod

Name:           lcmaps-plugins-saz-client
Version:        0.2.22
Release:        5%{?dist}
Summary:        SAZ support for lcmaps

Group:          System Environment/Tools
License:        Apache 2.0

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  lcmaps-plugins-scas-client = %{version}-%{release}
Obsoletes:	lcmaps-plugins-saz

%description
%{summary}

%prep

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/modules
cp %{_libdir}/modules/lcmaps_scas_client.mod $RPM_BUILD_ROOT%{_libdir}/modules/%{modname}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/modules/%{modname}

%changelog
* Fri Sep 16 2011 Dave Dykstra <dwd@fnal.gov> 0.2.22-5.osg
- Update to match scas-client

* Fri Sep 16 2011 Dave Dykstra <dwd@fnal.gov> 0.2.22-4.osg
- Update to match scas-client

* Wed Aug 31 2011 Dave Dykstra <dwd@fnal.gov> 0.2.22-3.osg
- Also add the %{dist} to the release to completely match the scas-client.
  Make BuildRequires always require the exact same %{version}-%{release}

* Wed Aug 31 2011 Dave Dykstra <dwd@fnal.gov> 0.2.22-3
- Update for corresponding update in lcmaps-plugin-scas-client.  Updated
  the release number to match the scas client release number.

* Mon Aug 22 2011 Dave Dykstra <dwd@fnal.gov> 0.0.2-1
- Rename package to lcmaps-plugins-saz-client
- Turn .mod file into a copy instead of a symlink, because lcmaps 
    cannot load the same physical module twice

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.0.1-1
- Initial packaging.

