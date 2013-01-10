Name:      osg-lcmaps
Summary:   OSG LCMAPS metapackage
Version:   3.2.0
Release:   2%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch
#Source0:   lcmaps.db

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# lcmaps-1.5.7-1.2 needed to avoid lcmaps.db conflict
Requires: lcmaps >= 1.5.7-1.2  
# plugins versions are the latest versions at the time this was last updated
Requires: lcmaps-plugins-basic >= 1.5.1-2.1
Requires: lcmaps-plugins-verify-proxy >= 1.5.4-1.1
Requires: lcmaps-plugins-gums-client >= 0.0.2-4
Requires: lcmaps-plugins-saz-client >= 0.3.4-1.2

%description
%{summary}


%install
#mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
#cp %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
#%config(noreplace) %{_sysconfdir}/lcmaps.db


%changelog
* Thu Jan 10 2013 Dave Dykstra <dwd@fnal.gov> - 3.2.0-2
- Move lcmaps.db back to the lcmaps package for now

* Fri Jan 04 2013 Dave Dykstra <dwd@fnal.gov> - 3.2.0-1
- Create metapackage using pieces that were in the OSG lcmaps package:
    Requires of the plugins, and lcmaps.db
