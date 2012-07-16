Summary: C/C++ libraries handling Job Description Language
Name: glite-jdl-api-cpp
Version: 3.3.0
%global upstream_release 3
Release: %{upstream_release}.2%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildRequires: %{!?extbuilddir:glite-build-common-cpp, } chrpath, libtool
BuildRequires: %{!?extbuilddir:glite-wms-utils-exception-devel, } boost-devel
BuildRequires: %{!?extbuilddir:glite-wms-utils-classad-devel, } classads-devel
BuildRequires: %{!?extbuilddir:glite-jobid-api-c-devel, } doxygen
BuildRequires: %{!?extbuilddir:glite-jobid-api-cpp-devel, } pkgconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source5: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Source6: %{name}-%{version}-%{upstream_release}.sl6.tar.gz

%global debug_package %{nil}

%description
C/C++ libraries and utilities for dealing with the Job Description Language

%prep
 

%setup -c -q -T -b %{rhel}

%build
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  export CLASSAD_CFLAGS=-I/usr/include/classad
  export CLASSAD_LIBS=-lclassad
  export GLITE_JOBID_CFLAGS=-I/usr/include/glite/jobid
  export GLITE_JOBID_LIBS=-lglite_jobid
  ./configure --prefix=%{buildroot}/usr --disable-static PVER=%{version}
  make
  make doxygen-doc
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  make install
  mkdir -p %{buildroot}/%{_docdir}/%{name}
  cp -R doc/html %{buildroot}/%{_docdir}/%{name}
else
  cp -R %{extbuilddir}/* %{buildroot}
fi
sed 's|^prefix=.*|prefix=/usr|g' %{buildroot}%{_libdir}/pkgconfig/jdl-api-cpp.pc > %{buildroot}%{_libdir}/pkgconfig/jdl-api-cpp.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/jdl-api-cpp.pc.new %{buildroot}%{_libdir}/pkgconfig/jdl-api-cpp.pc
rm %{buildroot}%{_libdir}/*.la
chrpath --delete %{buildroot}%{_libdir}/libglite_jdl_api_cpp.so.0.0.0

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
 

%files
%defattr(-,root,root)
%dir /usr/share/doc/%{name}-%{version}/
/usr/share/doc/%{name}-%{version}/LICENSE
%{_libdir}/libglite_jdl_api_cpp.so.0
%{_libdir}/libglite_jdl_api_cpp.so.0.0.0


%package devel
Summary: C/C++ libraries handling Job Description Language (development files)
Group: System Environment/Libraries
Requires: glite-jobid-api-c-devel, glite-jobid-api-cpp-devel
Requires: glite-wms-utils-classad-devel, glite-wms-utils-exception-devel
Requires: boost-devel, classads-devel, glite-build-common-cpp
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for dealing with the Job Description Language

%files devel
%defattr(-,root,root)
%dir /usr/include/glite/
%dir /usr/include/glite/jdl/
/usr/include/glite/jdl/*.h
%{_libdir}/pkgconfig/jdl-api-cpp.pc
%{_libdir}/libglite_jdl_api_cpp.so

%package doc
Summary: Documentation files for Job Description Language C/C++ library
Group: Documentation

%description doc
Documentation files for C/C++ implementation of Job Description Language

%files doc
%defattr(-,root,root)
%dir %{_docdir}/%{name}/html
%doc %{_docdir}/%{name}/html/*.html
%doc %{_docdir}/%{name}/html/*.css
%doc %{_docdir}/%{name}/html/*.png
%doc %{_docdir}/%{name}/html/*.gif


%changelog
* Mon Jul 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.3.0-3.2.osg
- Include both el5 and el6 tarballs in srpm

* Mon Jun 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.3.0-3.1.osg
- Rebuild for OSG
- Use sl6 tarball for sl6 build (based on %%rhel macro)
- Added cflags and ldflags for classads and jobid-api

* Wed May 16 2012 WMS group <wms-support@lists.infn.it> - 3.3.0-3.sl5
- Major bugs fixed


