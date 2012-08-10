Summary: GLite Security Delegation Interface
Name: emi-delegation-interface
Version: 2.0.3
Release: 1.1%{?dist}
License: Apache License
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
This package contains the  gridsite delegation inteface, along with its documentation.

%prep
 

%setup  

%build
 
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 make install prefix=$RPM_BUILD_ROOT
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /var/lib/delegation-interface/
%dir /var/lib/delegation-interface/doc/
/var/lib/delegation-interface/doc/RELEASE-NOTES
/var/lib/delegation-interface/doc/DelegationInterface.html
/var/lib/delegation-interface/doc/LICENSE
/var/lib/delegation-interface/doc/DelegationInterface.css
%dir /var/lib/delegation-interface/schema/
%dir /var/lib/delegation-interface/schema/mysql/
/var/lib/delegation-interface/schema/mysql/mysql-get-version.sql
/var/lib/delegation-interface/schema/mysql/mysql-drop.sql
/var/lib/delegation-interface/schema/mysql/mysql-schema.sql
%dir /var/lib/delegation-interface/schema/oracle/
/var/lib/delegation-interface/schema/oracle/oracle-get-version.sql
/var/lib/delegation-interface/schema/oracle/oracle-schema.sql
/var/lib/delegation-interface/schema/oracle/oracle-drop.sql
%dir /var/lib/delegation-interface/interface/
/var/lib/delegation-interface/interface/www.gridsite.org-delegation-1.0.0.wsdl
/var/lib/delegation-interface/interface/www.gridsite.org-delegation-2.0.0.wsdl
/var/lib/delegation-interface/interface/www.gridsite.org-delegation-1.1.0.wsdl

%changelog
 
* Fri Jun 01 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.3-1.1
- Add dist tag

