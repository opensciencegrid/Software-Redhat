Summary: C libraries for accessing the service discovery system
Name: glite-service-discovery-api-c
Version: 2.2.3
Release: 2.sl5
License: Apache License 2.0
Vendor: EMI
Group: System Environment/Libraries
URL: http://glite.cern.ch/
BuildRequires: doxygen
BuildRequires: libtool
BuildRequires: glite-build-common-cpp
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Source: glite-service-discovery-api-c-2.2.3-1.src.tar.gz
Patch0: link_against_dl.patch

%description
C libraries for accessing the service discovery system

%prep
 

%setup  
%patch0

%build
mkdir -p build; cd build; ../configure --disable-static --prefix=$RPM_BUILD_ROOT/usr; cd ..
 cd build; make ; cd ..
  
%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 cd build; make install; cd ..
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir /usr/share/doc/glite-service-discovery-api-c-%{version}/
%doc /usr/share/doc/glite-service-discovery-api-c-%{version}/LICENSE
%{_libdir}/libglite-sd-c.so.2
%{_libdir}/libglite-sd-c.so.2.0.2

%changelog
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.2.3-2.sl5
- rebuilt

* Sun Jul  3 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.2.3-1
- Initial packaging, adopted from CVS and EMI.

%package devel
Summary: C libraries for accessing the service discovery system (development files)
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
C libraries for accessing the service discovery system (development files)

%files devel
%defattr(-,root,root)
/usr/include/ServiceDiscoveryI.h
/usr/include/ServiceDiscovery.h
%{_libdir}/pkgconfig/service-discovery-api-c.pc
%{_libdir}/libglite-sd-c.so

%package doc
Summary: Documentation files for the service discovery system API
Group: Documentation

%description doc
Documentation files for the service discovery system API

%files doc
%defattr(-,root,root)
%dir %{_docdir}/%{name}-%{version}/html
%doc %{_docdir}/%{name}-%{version}/html/*.html
%doc %{_docdir}/%{name}-%{version}/html/*.css
%doc %{_docdir}/%{name}-%{version}/html/*.png
%doc %{_docdir}/%{name}-%{version}/html/*.gif

