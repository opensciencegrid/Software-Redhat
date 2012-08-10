Summary: GLite Security Delegation Java Implementation
Name: emi-delegation-java
Version: 2.2.0
%global upstream_release 2
Release: %{upstream_release}.1%{?dist}
License: Apache License
Vendor: EMI
Group: System Environment/Libraries
Packager: ETICS
BuildArch: noarch
BuildRequires: emi-trustmanager
BuildRequires: bouncycastle
BuildRequires: emi-delegation-interface
BuildRequires: emi-trustmanager-axis
BuildRequires: ant
BuildRequires: vomsjapi
BuildRequires: log4j
BuildRequires: java-devel
Requires: emi-trustmanager
Requires: bouncycastle
Requires: java
Requires: emi-trustmanager-axis
Requires: log4j
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv: yes
Source: %{name}-%{version}.tar.gz

%description
The java library that implements the delegation routines.

%prep
 

%setup  

%build
 
  
  
 echo skip

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 ant -Dmodule.version=%{name}-%{upstream_release} -Dprefix=$RPM_BUILD_ROOT -Dstage=/ install
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/delegation-java.jar
%dir /usr/share/doc/delegation-java/
/usr/share/doc/delegation-java/RELEASE-NOTES
/usr/share/doc/delegation-java/VERSION
%dir /usr/share/doc/delegation-java/html/
/usr/share/doc/delegation-java/html/serialized-form.html
/usr/share/doc/delegation-java/html/stylesheet.css
/usr/share/doc/delegation-java/html/package-list
/usr/share/doc/delegation-java/html/constant-values.html
%dir /usr/share/doc/delegation-java/html/resources/
/usr/share/doc/delegation-java/html/resources/inherit.gif
/usr/share/doc/delegation-java/html/help-doc.html
/usr/share/doc/delegation-java/html/allclasses-noframe.html
/usr/share/doc/delegation-java/html/index-all.html
/usr/share/doc/delegation-java/html/allclasses-frame.html
%dir /usr/share/doc/delegation-java/html/org/
%dir /usr/share/doc/delegation-java/html/org/glite/
%dir /usr/share/doc/delegation-java/html/org/glite/security/
%dir /usr/share/doc/delegation-java/html/org/glite/security/delegation/
/usr/share/doc/delegation-java/html/org/glite/security/delegation/GrDPX509Util.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/GrDProxyDlgorOptions.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/GrDPConstants.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/package-summary.html
%dir /usr/share/doc/delegation-java/html/org/glite/security/delegation/impl/
/usr/share/doc/delegation-java/html/org/glite/security/delegation/impl/GliteDelegation.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/impl/package-summary.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/impl/package-frame.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/impl/package-tree.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/GrDProxyGenerator.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/NewProxyReq.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/package-frame.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/DelegationHandler.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/DelegationException.html
%dir /usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageCacheElement.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageDatabase.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageFilesystemFactory.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageDatabaseFactory.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/package-summary.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/package-frame.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageFilesystem.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageFactory.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageElement.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorage.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/package-tree.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/storage/GrDPStorageException.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/GrDProxyDlgeeOptions.html
/usr/share/doc/delegation-java/html/org/glite/security/delegation/package-tree.html
/usr/share/doc/delegation-java/html/overview-frame.html
/usr/share/doc/delegation-java/html/overview-summary.html
/usr/share/doc/delegation-java/html/index.html
/usr/share/doc/delegation-java/html/deprecated-list.html
/usr/share/doc/delegation-java/html/overview-tree.html
/usr/share/doc/delegation-java/LICENSE
%dir /var/lib/delegation-java/
/var/lib/delegation-java/log4j.properties
/var/lib/delegation-java/dlgor.properties
/var/lib/delegation-java/dlgee.properties
/var/lib/delegation-java/dlgor-policy.dat

%changelog
 
* Fri Jun 01 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 2.2.0-2.1
- Imported; added dist tag
- Require changed from voms-api-java to vomsjapi

