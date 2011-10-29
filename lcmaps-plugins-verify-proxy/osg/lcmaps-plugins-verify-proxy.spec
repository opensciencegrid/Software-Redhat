Summary: Proxy verification plugin for LCMAPS
Name: lcmaps-plugins-verify-proxy
Version: 1.4.9
Release: 3%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRequires: lcmaps-interface, openssl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the Verify Proxy plugin.

%prep
%setup -q

%build

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS  LICENSE
%{_libdir}/modules/lcmaps_verify_proxy.mod
%{_libdir}/modules/liblcmaps_verify_proxy.so.0
%{_libdir}/modules/liblcmaps_verify_proxy.so.0.0.0
%exclude %{_libdir}/modules/liblcmaps_verify_proxy.so


%changelog
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.9-3
- rebuilt

* Wed Mar 23 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.9-2
- removed explicit requires

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.9-1
- Updated dependencies on openssl

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.8-2
- disable static libraries
- fixed license string
- dropped devel package

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


