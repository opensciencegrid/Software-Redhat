Summary: C/C++ libraries for the client of the CREAM service
Name: glite-ce-cream-client-api-c
Version: 1.15.4
Release: 2.1%{?dist}
License: Apache Software License
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildArch: %{_arch}
BuildRequires: cmake, chrpath
BuildRequires: glite-ce-wsdl >= 1.15.1
#BuildRequires: emi-pkgconfig-compat
BuildRequires: gsoap-devel
BuildRequires: gridsite-devel >= 2.2.5, libxml2-devel, boost-devel
BuildRequires: voms-devel, condor-classads-devel >= 8.0.4
BuildRequires: glite-lbjp-common-gsoap-plugin-devel >= 3.2.12, log4cpp-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}.tar.gz
Patch0: Fix-CMakeLists.txt-to-work-with-condor-classads.patch
Patch1: Fix-Wwrite-strings-warning.patch
Patch2: Fix-SOAP-defines.patch
Patch3: boost-filesystem-version-3-compatibility.patch

%global debug_package %{nil}

%description
The package contains C/C++ libraries for the client of the CREAM service

%prep
 

%setup -c -q
%patch0 -p1
%patch1 -p1
%if 0%{?rhel} >= 6
%patch2 -p1
%endif
%if 0%{?rhel} >= 7
%patch3 -p1
%endif

%build
%if 0%{?rhel} >= 7
export CXXFLAGS=-std=gnu++11${CXXFLAGS:+ $CXXFLAGS}
%endif
cmake -DCMAKE_INSTALL_PREFIX:string=%{buildroot} %{_builddir}/%{name}-%{version}
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make install
sed 's|%{buildroot}||g;s|lib\s*$|lib64|g' %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc > %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc.new %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc
sed 's|%{buildroot}||g;s|lib\s*$|lib64|g' %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc > %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc.new %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc


%clean
rm -rf %{buildroot}
 
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/libglite_ce_cream_client_*.so.0
%{_libdir}/libglite_ce_cream_client_*.so.0.0.0



%package -n glite-ce-cream-client-devel
Summary: Development files for the client of the CREAM service
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glite-jobid-api-cpp-devel, glite-jobid-api-c-devel,
Requires: glite-lbjp-common-gsoap-plugin-devel >= 3.2.12
Requires: boost-devel, condor-classads-devel >= 8.0.4, log4cpp-devel, gsoap-devel
Requires: voms-devel, gridsite-devel >= 2.2.5, libxml2-devel

%description -n glite-ce-cream-client-devel
The package contains development files for the client of the CREAM service

%files -n glite-ce-cream-client-devel
%defattr(-,root,root)
%dir /usr/include/glite/
%dir /usr/include/glite/ce/
%dir /usr/include/glite/ce/cream-client-api-c/
/usr/include/glite/ce/cream-client-api-c/*.h
/usr/include/glite/ce/cream-client-api-c/*.nsmap
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libglite_ce_cream_client_*.so


%changelog
* Mon Jul 11 2016 Matyas Selmeci <matyas@cs.wisc.edu> - 1.15.4-2.1
- Build for OSG; add versioned dependencies; use condor-classads library
- Patch to build for EL7
- Patch to fix warnings caused by implicit conversion of string literals into
  char*

* Fri Mar 21 2014 CREAM group <cream-support@lists.infn.it> - 1.15.4-2
- Fix for bug https://issues.infn.it/jira/browse/CREAM-137

* Mon Sep 30 2013 CREAM group <cream-support@lists.infn.it> - 1.15.3-3
- Fix for bug https://issues.infn.it/jira/browse/CREAM-123
- Fix for vulnerability

* Fri Aug 31 2012 CREAM group <cream-support@lists.infn.it> - 1.15.2-2
- New major release


