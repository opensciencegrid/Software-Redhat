Summary: WS definitions for the CREAM service
Name: glite-ce-wsdl
Version: 1.13.1
Release: 3.1%{?dist}
License: Apache License 2.0
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: glite-ce-wsdl-1.13.1-3.src.tar.gz

%description
WS definitions for the CREAM service

%prep
 

%setup  

%build
 
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 ./project/install.sh $RPM_BUILD_ROOT/usr
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /usr/share/wsdl/
%dir /usr/share/wsdl/cream-ce/
/usr/share/wsdl/cream-ce/org.glite.ce-monitor_consumer_service.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-monitor_types.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-cream_service.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-monitor_service.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-cream_faults.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-cream2_service.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-monitor_faults.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-faults.xsd
/usr/share/wsdl/cream-ce/www.gridsite.org-delegation-2.0.0.wsdl
/usr/share/wsdl/cream-ce/org.glite.ce-cream_types.wsdl

%changelog
 
