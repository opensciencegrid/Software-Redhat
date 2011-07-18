Name:           osg-voms-compat
Version:        1.0
Release:        1%{?dist}
Summary:        OSG VOMS Compatibility package

Group:          System Environment/Libraries
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/
Source0:        osg-voms-compat-1.0.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
%{summary}

%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
install -m 755 etc/profile.d/* $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/



%changelog
* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-1
- Initial packaging


