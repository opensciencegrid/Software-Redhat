Summary: SAML 2.0 profile of XACML v2.0 library
Name: xacml
Version: 1.3.0
Release: 1.1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source: http://software.nikhef.nl/security/xacml/xacml-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl-devel, zlib-devel, bison, flex, gsoap-devel, pkgconfig
Provides: saml2-xacml2-c-lib = %{version}-%{release}
# On 64-bit platform we also need to provide the arch dependent provide
%if "x%{__isa}" != "x"
Provides: saml2-xacml2-c-lib%{?_isa} = %{version}-%{release}
%endif
Obsoletes: saml2-xacml2-c-lib < 1.1.0

%description

This API provides a basic implementation of the SAML 2.0 profile of
XACML v2.0, including support for obligations in XACML response
messages. It aids in writing XACML clients and servers.

%package devel
Summary: SAML 2.0 profile of XACML v2.0 development files
Group: Development/Libraries
Requires: openssl-devel
Requires:  %{name} = %{version}-%{release}
Requires: pkgconfig
Provides: saml2-xacml2-c-lib-devel = %{version}-%{release}
# On 64-bit platform we also need to provide the arch dependent provide
%if "x%{__isa}" != "x"
Provides: saml2-xacml2-c-lib-devel%{?_isa} = %{version}-%{release}
%endif
Obsoletes: saml2-xacml2-c-lib-devel < 1.1.0

%description devel

This API provides a basic implementation of the SAML 2.0 profile of
XACML v2.0, including support for obligations in XACML response
messages. It aids in writing XACML clients and servers.

This package contains the development libraries and header files.

%prep
%setup -q

%build

CXXFLAGS=-fPIC
export CXXFLAGS
# We *must* match the build flags of gsoap.so
# or risk misalignment of the fields of struct soap
# see: https://bugzilla.redhat.com/show_bug.cgi?id=978872
# Note: from xacml-1.1.5 onwards, this is implemented in the code so no longer
# needed here.

%configure --disable-static

# The following two lines were suggested by
# https://fedoraproject.org/wiki/Packaging/Guidelines to prevent any
# RPATHs creeping in.
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libxacml.so.0
%{_libdir}/libxacml.so.0.0.0
%exclude %{_bindir}/xacml-client
%exclude %{_bindir}/xacml-server
%doc NEWS

%files devel
%defattr(-,root,root,-)
%{_includedir}/xacml.h
%{_includedir}/xacml_authz_interop_profile.h
%{_includedir}/xacml_client.h
%{_includedir}/xacml_datatypes.h
%{_includedir}/xacml_server.h
%{_libdir}/libxacml.so
%{_libdir}/pkgconfig/xacml.pc

%changelog
* Thu Oct  9 2013 Dave Dykstra <dwd@fnal.gov> 1.3.0-1.1.osg
- Reimported into osg
- Removed xacml_namespaces.patch

* Wed Oct  4 2013 Mischa Salle <msalle@nikhef.nl> 1.3.0-1
- updated version

* Mon Sep 16 2013 Brian Bockelman <bbockelm@cse.unl.edu > 1.1.2-5.1
- Rename global 'namespaces' to avoid conflicts with parent executable

* Wed Sep 11 2013 Mischa Salle <msalle@nikhef.nl> 1.2.0-1
- removed CPPFLAGS for THREADING
- updated version

* Fri Aug 30 2013 Mischa Salle <msalle@nikhef.nl> 1.1.5-1
- remove pkg-config line added in 1.1.2-5, it is now included in the source
- updated version

* Mon Jul 29 2013 Mischa Salle <msalle@nikhef.nl> 1.1.4-1
- updated version

* Mon Jul 29 2013 Mischa Salle <msalle@nikhef.nl> 1.1.3-1
- updated version

* Thu Jun 27 2013 Dennis van Dok <dennisvd@nikhef.nl> 1.1.2-5
- Use pkg-config to find the gsoap cflags.

* Fri Jun 14 2013 Dennis van Dok <dennisvd@nikhef.nl> 1.1.2-4
- Fix the typo in the CPPFLAGS variable

* Thu Jun 13 2013 Dennis van Dok <dennisvd@nikhef.nl> 1.1.2-3
- Add -DWITH_IPV6 -DWITH_DOM to CPPFLAGS, for compatibility with HTCondor

* Tue Oct 23 2012 Mischa Salle <msalle@nikhef.nl> 1.1.2-2
- Update URL.

* Fri Apr 20 2012 Mischa Salle <msalle@nikhef.nl> 1.1.2-1
- updated version

* Mon Mar 26 2012 Mischa Salle <msalle@nikhef.nl> 1.1.1-2
- provide architecture dependent and indepent %%Provides
- updated version

* Fri Dec 16 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.1.0-3
- Set provides/obsoletes on devel as well

* Thu Dec 15 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.1.0-2
- use gSOAP from system rather than our own.
- Added ldconfig call to postin and postun

* Thu Mar 10 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.0.1-4
- Add CPPFLAG

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.0.1-3
- fixed license string
- disable static libraries

* Thu Feb 24 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


