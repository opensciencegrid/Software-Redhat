# This is modified spec for the OSG packaging purposes and OASIS requirement
# URL:            https://github.com/OpenSC/libp11
# Source0:        https://github.com/OpenSC/libp11/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

Version:	0.4.6
Release: 1%{?dist}
%if 0%{?fedora}
%define enginesdir %{_libdir}/engines-1.1
%else
%define enginesdir %{_libdir}/openssl/engines
%endif

Name:           libp11
Summary:        Library for using PKCS#11 modules

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://github.com/OpenSC/libp11
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	autoconf automake libtool
BuildRequires:  doxygen graphviz
BuildRequires:  libtool-ltdl-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
%if 0%{?fedora}
BuildRequires:  autoconf automake libtool
# needed for testsuite
BuildRequires:  softhsm opensc
%else
%ifnarch ppc ppc64 ppc64le
BuildRequires:  softhsm opensc
%endif
%endif


%description
Libp11 is a library implementing a small layer on top of PKCS#11 API to
make using PKCS#11 implementations easier.

%package devel
Summary:        Files for developing with %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%if 0%{?fedora}
Conflicts: compat-openssl10-devel < 1:1.1.0
%endif

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n engine_pkcs11
Summary: A PKCS#11 engine for use with OpenSSL
Group: Development/Libraries
License: BSD

BuildRequires:  openssl-devel pkgconfig
BuildRequires:  pkgconfig(p11-kit-1)
%if 0%{?fedora}
BuildRequires:  softhsm opensc
Recommends:	p11-kit-trust
%else
%ifnarch ppc ppc64 ppc64le
BuildRequires:  softhsm opensc
Requires:	p11-kit-trust
%endif
%endif
Requires:       openssl > 0.9.6
Requires:	%{name} = %{version}-%{release}

%description -n engine_pkcs11
Engine_pkcs11 is an implementation of an engine for OpenSSL. It can be loaded
using code, config file or command line and will pass any function call by
openssl to a PKCS#11 module. Engine_pkcs11 is meant to be used with smart
cards and software for using smart cards in PKCS#11 format, such as OpenSC.

%prep
%setup -q

%build
%if 0%{?fedora}
autoreconf -fvi
%endif
%configure --disable-static --enable-api-doc --with-enginesdir=%{enginesdir}
make V=1 %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{enginesdir}
#make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
make install DESTDIR=$RPM_BUILD_ROOT

# Use %%doc to install documentation in a standard location
mkdir __docdir
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/api/ __docdir/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/

# Remove libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{enginesdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%check
%if 0%{?fedora}
make check %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS
%{_libdir}/libp11.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/ __docdir/api/
%{_libdir}/libp11.so
%{_libdir}/pkgconfig/libp11.pc
%{_includedir}/libp11.h

%files -n engine_pkcs11
%defattr(-,root,root,-)
%doc NEWS
%{enginesdir}/*.so

%changelog
* Tue Apr 24 2018 Marian Zvada <marian.zvada@cern.ch> - 0.4.6-1
- Recompile in osg-development repo
- OO-220

* Sun Apr 30 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.4.6-1
- Update to upstream 0.4.6 release

* Fri Oct 14 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.4.2-1
- Initial version of the package
