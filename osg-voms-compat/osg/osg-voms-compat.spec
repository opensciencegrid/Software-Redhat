Name:           osg-voms-compat
Version:        1.0
Release:        3%{?dist}
Summary:        OSG VOMS Compatibility package

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://www.opensciencegrid.org/
Source0:        osg-voms-compat.sh
Source1:        osg-voms-compat.csh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       voms-clients

%description
%{summary}

%prep

%build


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
install -m 755 %{SOURCE0} %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/osg-voms-compat.sh
%{_sysconfdir}/profile.d/osg-voms-compat.csh



%changelog
* Wed Nov 23 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-3
- Reorganized source files

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-2
- Fixed the shell scripts to have =true

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 1.0-1
- Initial packaging


