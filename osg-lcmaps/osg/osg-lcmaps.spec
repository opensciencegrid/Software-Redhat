Name:      osg-lcmaps
Summary:   OSG LCMAPS metapackage
Version:   3.1.15
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# versions are the latest at the time this was last updated
Requires: lcmaps >= 1.5.7-1.3
Requires: lcmaps-plugins-basic >= 1.5.1-2.1
Requires: lcmaps-plugins-verify-proxy >= 1.5.4-1.1
Requires: lcmaps-plugins-gums-client >= 0.0.2-4
Requires: lcmaps-plugins-saz-client >= 0.3.4-1.2

%description
%{summary}


%install
mkdir -p ${RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
# none

%changelog
* Thu Feb 5 2013 Dave Dykstra <dwd@fnal.gov> - 3.1.15-1
- Create metapackage requiring current versions of lcmaps and its plugins
