Summary: SAML 2.0 profile of XACML v2.0
Name: saml2-xacml2-c-lib
Version: 1.0.1
Release: 7%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/saml2-xacml2-c-lib/xacml-%{version}.tar.gz
Source1: http://software.nikhef.nl/security/saml2-xacml2-c-lib/gsoap-2.7.17.tar.gz

Patch0: xacml_namespaces.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libtool automake autoconf
BuildRequires: openssl-devel, zlib-devel, bison, flex
Obsoletes: prima

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

%description devel

This API provides a basic implementation of the SAML 2.0 profile of
XACML v2.0, including support for obligations in XACML response
messages. It aids in writing XACML clients and servers.

This package contains the development libraries and header files.

%prep
%setup -q -n xacml-%{version} -a1

%patch0 -p1

%build

# Re-bootstrap due to patching Automake.am
#aclocal -I project
aclocal
libtoolize --force --copy
autoheader
automake --add-missing --copy
autoconf

CXXFLAGS=-fPIC
export CXXFLAGS
CPPFLAG="-DXACML_ADDING_THREADING"
export CPPFLAG

cd gsoap-2.7
./configure --prefix=/usr --disable-static
make
make DESTDIR=`pwd`/../stage install
cd ..

%configure --with-gsoap=`pwd`/stage/usr --disable-static

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

# remove the files we don't want


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libxacml.so.0
%{_libdir}/libxacml.so.0.0.0
%exclude %{_bindir}/xacml-client
%exclude %{_bindir}/xacml-server

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
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.1-7
- rebuilt

* Mon Sep 19 2011 Dave Dykstra <dwd@fnal.gov> - 1.0.1-6
- Add Obsoletes prima to avoid the old package from the hadoop repo

* Mon Aug 01 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.0.1-5
- Put all GSOAP functions in a separate namespace.

* Thu Mar 10 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.0.1-4
- Add CPPFLAG

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.0.1-3
- fixed license string
- disable static libraries

* Thu Feb 24 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


