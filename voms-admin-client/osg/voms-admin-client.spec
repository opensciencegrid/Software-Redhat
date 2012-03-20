Summary: emi.voms.voms-admin-client
Name: voms-admin-client
Version: 2.0.16
Release: 2%{?dist}
License: Apache Software License
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildRequires: maven2
BuildRequires: java-devel-sun
%if 0%{?rhel} == 6
BuildRequires: maven-resources-plugin
%endif
Requires: python-ZSI
Requires: java-sun
Requires: PyXML
BuildRoot: %{_builddir}/%{name}-root
AutoReqProv: yes
Source: voms-admin-client-2.0.16-1.src.tar.gz
Patch0: directory-defaults.patch


%description
emi.voms.voms-admin-client

%prep
 

%setup  
%patch0 -p0

%build
 
 export JAVA_HOME=%{java_home}
 # added -Dmaven2.usejppjars to use the maven-resources-plugin we bring in as a BuildRequires. Safe to leave in for el5
 mvn -B -Dmaven2.usejppjars -e -Dmaven.repo.local=/tmp/m2-repository package
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT/usr/share/voms-admin/client; mkdir -p $RPM_BUILD_ROOT/usr/bin; cp target/stage/voms-admin.py $RPM_BUILD_ROOT/usr/bin/voms-admin; cp -r target/stage/VOMSAdmin $RPM_BUILD_ROOT/usr/share/voms-admin/client; chmod 755 $RPM_BUILD_ROOT/usr/bin/voms-admin
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /usr/share/voms-admin/
%dir /usr/share/voms-admin/client/
%dir /usr/share/voms-admin/client/VOMSAdmin/
/usr/share/voms-admin/client/VOMSAdmin/__init__.py
/usr/share/voms-admin/client/VOMSAdmin/__init__.pyc
/usr/share/voms-admin/client/VOMSAdmin/__init__.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService_services.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService_services.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService_services.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSCommands.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSCommands.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSCommands.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService_services_types.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService_services_types.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService_services_types.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSPermission.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSPermission.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSPermission.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService_services_types.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService_services_types.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService_services_types.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService.pyo
/usr/share/voms-admin/client/VOMSAdmin/AttributesFix.py
/usr/share/voms-admin/client/VOMSAdmin/AttributesFix.pyc
/usr/share/voms-admin/client/VOMSAdmin/AttributesFix.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService_services_types.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService_services_types.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService_services_types.pyo
/usr/share/voms-admin/client/VOMSAdmin/ListRoleFix.py
/usr/share/voms-admin/client/VOMSAdmin/ListRoleFix.pyc
/usr/share/voms-admin/client/VOMSAdmin/ListRoleFix.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificatesService_services.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificatesService_services.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificatesService_services.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificatesService_services_types.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificatesService_services_types.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificatesService_services_types.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSAttributesService.pyo
/usr/share/voms-admin/client/VOMSAdmin/CertificatesFix.py
/usr/share/voms-admin/client/VOMSAdmin/CertificatesFix.pyc
/usr/share/voms-admin/client/VOMSAdmin/CertificatesFix.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService_services.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService_services.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSAdminService_services.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSCommandsDef.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSCommandsDef.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSCommandsDef.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService_services.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService_services.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSACLService_services.pyo
/usr/share/voms-admin/client/VOMSAdmin/X509Helper.py
/usr/share/voms-admin/client/VOMSAdmin/X509Helper.pyc
/usr/share/voms-admin/client/VOMSAdmin/X509Helper.pyo
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificateService.py
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificateService.pyc
/usr/share/voms-admin/client/VOMSAdmin/VOMSCertificateService.pyo
/usr/bin/voms-admin

%changelog
* Mon Mar 19 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.16-2
Fix JAVA_HOME on el6
Use maven-resources-plugin from jpackage on el6

* Sat Jul 23 2011 Tanya Levshina <tlevshin@fnal.gov> - 2.0.16-1
Initial release, patched env. variable setting

 
