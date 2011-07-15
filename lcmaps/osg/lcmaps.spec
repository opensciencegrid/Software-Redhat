Summary: Grid (X.509) and VOMS credentials to local account mapping service
Name: lcmaps
Version: 1.4.28
Release: 2%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/lcmaps/%{name}-%{version}.tar.gz
Source1: lcmaps.db
Patch0: makefile_r15293.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: globus-core
BuildRequires: globus-common-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: voms-devel
BuildRequires: flex, bison
BuildRequires: automake, autoconf, libtool

Requires: globus-common
Requires: globus-gssapi-gsi
Requires: globus-gss-assist
Requires: globus-gsi-credential

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

%package interface
Group: Development/Libraries
Summary: LCMAPS plug-in API header files
Requires: openssl-devel
Requires: globus-gssapi-gsi-devel
Requires: pkgconfig

%description interface
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

This package contains the header files necessary to build LCMAPS plug-ins.

%package devel
Group: Development/Libraries
Summary: LCMAPS development libraries
Requires: lcmaps-interface
Requires: %{name} = %{version}-%{release}

%description devel
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

This package contains the development libraries.


%prep
%setup -q
%patch0 -p0

%build
./bootstrap
%configure --disable-static --disable-rpath --enable-osg
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# clean up installed files
rm -rf ${RPM_BUILD_ROOT}/usr/share/doc

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}
%__sed -i -e 's|@LIBDIR@|%{_libdir}|' $RPM_BUILD_ROOT/%{_sysconfdir}/lcmaps.db

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/lcmaps.db
%{_libdir}/lcmaps.mod
%{_libdir}/lcmaps_gss_assist_gridmap.mod
%{_libdir}/lcmaps_return_poolindex.mod
%{_libdir}/liblcmaps.so
%{_libdir}/liblcmaps.so.0
%{_libdir}/liblcmaps.so.0.0.0
%{_libdir}/liblcmaps_gss_assist_gridmap.so.0
%{_libdir}/liblcmaps_gss_assist_gridmap.so.0.0.0
%{_libdir}/liblcmaps_return_account_from_pem.so.0
%{_libdir}/liblcmaps_return_account_from_pem.so.0.0.0
%{_libdir}/liblcmaps_return_poolindex.so.0
%{_libdir}/liblcmaps_return_poolindex.so.0.0.0
%{_libdir}/liblcmaps_verify_account_from_pem.so.0
%{_libdir}/liblcmaps_verify_account_from_pem.so.0.0.0
%{_libdir}/modules/lcmaps_plugin_example.mod
%{_libdir}/modules/liblcmaps_plugin_example.so.0
%{_libdir}/modules/liblcmaps_plugin_example.so.0.0.0
%{_libdir}/liblcmaps_return_account_from_pem.so

%doc AUTHORS INSTALL doc/INSTALL_WITH_WORKSPACE_SERVICE LICENSE
%doc README README.NO_LDAP
%doc etc/lcmaps.db etc/groupmapfile etc/vomapfile

%files interface
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/lcmaps/*.h

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblcmaps_gss_assist_gridmap.so
%{_libdir}/liblcmaps_return_poolindex.so
%{_libdir}/liblcmaps_verify_account_from_pem.so
%{_libdir}/modules/*.so

%changelog
* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.28-2
- Include OSG default lcmaps.db

* Wed Mar  9 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.28-1
- Made examples out of config files

* Tue Mar  8 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.27-2
- Disable rpath in configure

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.27-1
- Fixed globus dependencies
- added ldconfig %post(un)

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.26-3
- disabled static libraries
- added proper base package requirement for devel
- fixed license string

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


