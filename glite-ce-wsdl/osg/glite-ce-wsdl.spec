Summary: WS definitions for the CREAM service
Name: glite-ce-wsdl
Version: 1.15.1
Release: 1.1%{?dist}
License: Apache Software License
URL: http://glite.cern.ch/
Group: Development/Libraries
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}.tar.gz


%description
WS definitions for the CREAM service

%prep
 
%setup -c -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/wsdl/cream-ce/es/
cp interface/CREAM/*.wsdl interface/CREAM/*.xsd %{buildroot}/usr/share/wsdl/cream-ce
cp interface/ES/*.wsdl interface/ES/*.xsd %{buildroot}/usr/share/wsdl/cream-ce/es


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /usr/share/wsdl/
%dir /usr/share/wsdl/cream-ce/
%dir /usr/share/wsdl/cream-ce/es
/usr/share/wsdl/cream-ce/*.wsdl
/usr/share/wsdl/cream-ce/*.xsd
/usr/share/wsdl/cream-ce/es/*.wsdl
/usr/share/wsdl/cream-ce/es/*.xsd




%changelog
* Mon Jul 11 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.15.1-1.1.osg
- Add dist tag

* Fri Aug 31 2012 CREAM group <cream-support@lists.infn.it> - 1.15.1-1.sl6
- New major release

