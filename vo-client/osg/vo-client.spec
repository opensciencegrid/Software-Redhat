Name:           vo-client
Version:        38
Release:        1%{?dist}
Summary:        Vomses file for use with user authentication

Group:          system environment/base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       osg-ca-certs

%description
%{summary}

%prep
%setup -q 


%build


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -m 644 voms/etc/vomses $RPM_BUILD_ROOT/%{_sysconfdir}/vomses

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/vomses


%changelog
* Fri Jul 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-1
- Initial build of vo-client


