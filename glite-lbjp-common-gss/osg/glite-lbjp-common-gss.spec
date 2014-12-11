Summary: Wrapper of Globus GSS/SSL implementation used by gLite LB and JP
Name: glite-lbjp-common-gss
Version: 3.1.3
Release: 2.2%{?dist}
Url: http://glite.cern.ch
License: ASL 2.0
Vendor: EMI
Group: System Environment/Libraries
BuildRequires: c-ares-devel
BuildRequires: c-ares
BuildRequires: chrpath
BuildRequires: cppunit-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: libtool
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Obsoletes: glite-security-gss%{?_isa} < 2.1.5-1
AutoReqProv: yes
Source: http://eticssoft.web.cern.ch/eticssoft/repository/emi/emi.lbjp-common.gss/%{version}/src/%{name}-3.1.3-2.src.tar.gz
Patch0: proxy_file.patch
# patch from https://tomtools.its.cern.ch/jira/browse/GTSL-40 
Patch1: glite-lbjp-common-gss-resolverFix.patch


%description
glite-security-gss wraps GSS functions (and several non-GSS Globus calls) to a
secure network communication library with strict timing control (via timeout
arguments) of all remote
operations.


%package devel
Summary: Development files for gLite GSS library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: globus-gssapi-gsi-devel, pkgconfig
Provides: glite-security-gss%{?_isa} = %{version}-%{release}
Obsoletes: glite-security-gss%{?_isa} < 2.1.5-1


%description devel
This package contains development libraries and header files for gLite GSS
library.


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
/usr/bin/perl ./configure --thrflavour= --nothrflavour= --root=/ --prefix=/usr --libdir=%{_lib} --project=emi --module lbjp-common.gss
make


%check
make check


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
find $RPM_BUILD_ROOT -name '*.a' -exec rm -rf {} \;
find $RPM_BUILD_ROOT -name '*' -print | xargs -I {} -i bash -c "chrpath -d {} > /dev/null 2>&1" || echo 'Stripped RPATH'

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%dir /usr/share/doc/gss-%{version}
%doc /usr/share/doc/gss-%{version}/LICENSE
/usr/%{_lib}/libglite_security_gss.so.9.1.3
/usr/%{_lib}/libglite_security_gss.so.9


%files devel
%defattr(-,root,root)
%dir /usr/include/glite
%dir /usr/include/glite/security
/usr/include/glite/security/glite_gss.h
/usr/%{_lib}/libglite_security_gss.so


%changelog
* Thu Dec 11 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.1.3-2.2.osg
- Add patch to fix "Resolver internal error" issue at SDSC (SOFTWARE-1722)

* Thu Jul 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.3-2.1.osg
- Fix proxy file filename getting truncated

* Wed May 16 2012 CESNET Product Teams <emi-lb@metacentrum.cz> - 3.1.3-2
- automatically generated package
