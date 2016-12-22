Name:           osg-update-vos
Version:        1.0
Release:        1%{?dist}
Summary:        VO data updater for OSG

Group:          System Environment/Tools
License:        Apache 2.0

Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       yum-utils

%description
%{summary}


%prep
%setup -q

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%doc %{_defaultdocdir}/%{name}-%{version}/README*

%changelog
* Tue Dec 20 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0
- Created
