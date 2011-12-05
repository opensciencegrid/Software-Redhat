
%define modname lcmaps_saz_client.mod

Name:           lcmaps-plugins-saz-client
Version:        0.2.22
Release:        8%{?dist}
Summary:        SAZ support for lcmaps

Group:          System Environment/Tools
License:        Apache 2.0

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  lcmaps-plugins-scas-client = %{version}-%{release}
Obsoletes:	lcmaps-plugins-saz
Requires:	saml2-xacml2-c-lib
# The following isn't technically necessary, but it helps us insure that
#   this package is updated whenever scas-client changes
Requires:	lcmaps-plugins-scas-client = %{version}-%{release}

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
* Mon Dec 05 2011 Dave Dykstra <dwd@fnal.gov> 0.2.22-8.osg
- Rebuild to match rebuilt lcmaps-plugins-scas-client.  Also added a 
  Requires statement to the same version of lcmaps-plugins-scas-client.
  This isn't needed technically, since this package contains a copy of the
  other, but it is included to ensure that this package is upgraded
  whever the other is upgraded.

* Mon Sep 19 2011 Dave Dykstra <dwd@fnal.gov> 0.2.22-7.osg
- Instead of a Conflicts: prima, have a Requires: saml2-xacml2-c-lib
  which is the correct provider of libxacml.so.0.

* Fri Sep 16 2011 Dave Dykstra <dwd@fnal.gov> 0.2.22-6.osg
- Add a Conflicts: prima.  Even though it was already in scas-client,
  scas-client is not required at install time by saz-client (only build
  time) so it isn't necessarily processed, plus even if it is the
  ordering can make a difference when yum calculates dependencies. 
  I am hoping this will prevent a fatal error when trying to install
  this package while a hadoop.repo is in /etc/yum.repos.d (although 
  that's better than silently installing wrong packages).

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

