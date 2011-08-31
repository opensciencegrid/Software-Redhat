Summary: SCAS client plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-scas-client
Version: 0.2.22
Release: 3%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
Patch0: memory_corruption.patch
Patch1: ca_only.patch
Patch2: timeout.patch
BuildRequires: openssl-devel
BuildRequires: lcmaps-interface, saml2-xacml2-c-lib-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the SCAS client plug-in. This LCMAPS plugin
functions as the PEP (client side) implementation to an Site Central
Authorization Service (SCAS) or GUMS (new style) service.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0

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
%{_libdir}/modules/lcmaps_scas_client.mod
%{_libdir}/modules/liblcmaps_scas_client.so.0
%{_libdir}/modules/liblcmaps_scas_client.so.0.0.0
%{_datadir}/man/man8/lcmaps_plugins_scas_client.8.gz
%exclude %{_libdir}/modules/liblcmaps_scas_client.so


%changelog
* Wed Aug 31 2011 Dave Dykstra <dwd@fnal.gov> - 0.2.22-3
- Increase socket connect timeout from 170 ms to 30 seconds and
  increase total retry timeout from 1 second to 30*4+5 seconds.
  This is necessary to survive the extremely heavy loads seen
  at a Fermilab stress test.

* Sun Jul 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.2.22-2
- Fix memory corruption issue on an error condition.
- Fix SEGV when no user certificate is present.

* Wed Apr  6 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.22-1
- bumped version

* Wed Mar 23 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.21-2
- removed explicit requires

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.21-1
- added openssl dependency

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.20-2
- fixed license string
- dropped devel package
- disable static libraries

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


