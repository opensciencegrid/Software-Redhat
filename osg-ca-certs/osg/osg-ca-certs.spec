Name:           osg-ca-certs
Version:        3
Release:        1
Summary:        Metapackage to bring in the appropriate CA certs

Group:          System Environment/Base
License:        GPL
URL:            http://vdt.cs.wisc.edu/releases/2.0.0/certificate_authorities.html
#Source0:        osg-ca-certs.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  
Requires:       vdt-ca-certs

%description
%{summary}

%prep


%build


%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc



%changelog
* Fri Jul 08 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 3-1
- Initial creation of RPM to pull in vdt-ca-certs.



