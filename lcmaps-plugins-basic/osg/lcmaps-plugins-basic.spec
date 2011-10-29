Summary: Basic plugins for the LCMAPS authorization framework
Name: lcmaps-plugins-basic
Version: 1.4.5
Release: 2%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRequires: lcmaps-interface
BuildRequires: openldap-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the basic plugins.

%package ldap
Summary: LDAP enforcement plug-in for LCMAPS
Group: System Environment/Libraries

%description ldap
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the LDAP enforcement plug-in.

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
%{_libdir}/modules/lcmaps_dummy_bad.mod
%{_libdir}/modules/lcmaps_dummy_good.mod
%{_libdir}/modules/lcmaps_localaccount.mod
%{_libdir}/modules/lcmaps_poolaccount.mod
%{_libdir}/modules/lcmaps_posix_enf.mod
%{_libdir}/modules/liblcmaps_dummy_bad.so.0
%{_libdir}/modules/liblcmaps_dummy_bad.so.0.0.0
%{_libdir}/modules/liblcmaps_dummy_good.so.0
%{_libdir}/modules/liblcmaps_dummy_good.so.0.0.0
%{_libdir}/modules/liblcmaps_localaccount.so.0
%{_libdir}/modules/liblcmaps_localaccount.so.0.0.0
%{_libdir}/modules/liblcmaps_poolaccount.so.0
%{_libdir}/modules/liblcmaps_poolaccount.so.0.0.0
%{_libdir}/modules/liblcmaps_posix_enf.so.0
%{_libdir}/modules/liblcmaps_posix_enf.so.0.0.0
/usr/share/man/man8/lcmaps_dummy_bad.mod.8.gz
%{_datadir}/man/man8/lcmaps_dummy_good.mod.8.gz
%{_datadir}/man/man8/lcmaps_localaccount.mod.8.gz
%{_datadir}/man/man8/lcmaps_poolaccount.mod.8.gz
%{_datadir}/man/man8/lcmaps_posix_enf.mod.8.gz
%exclude %{_libdir}/modules/*.so

%files ldap
%defattr(-,root,root,-)
%doc AUTHORS  LICENSE
%{_libdir}/modules/lcmaps_ldap_enf.mod
%{_libdir}/modules/liblcmaps_ldap_enf.so.0
%{_libdir}/modules/liblcmaps_ldap_enf.so.0.0.0
%{_datadir}/man/man8/lcmaps_ldap_enf.mod.8.gz


%changelog
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.5-2
- rebuilt

* Thu Jun 30 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.5-1
- Moved lcmaps_ldap_enf.mod to the -ldap package
- Updated to version 1.4.5

* Wed Apr  6 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.3-1
- bumped version

* Wed Mar 23 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.2-4
- removed explicit requires

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.2-3
- Split off the ldap enforcement plug-in

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.2-2
- drop the development package
- fixed the licence string

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


