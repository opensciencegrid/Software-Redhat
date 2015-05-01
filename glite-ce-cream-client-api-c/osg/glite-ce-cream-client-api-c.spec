Summary: C/C++ libraries for the client of the CREAM service
Name: glite-ce-cream-client-api-c
Version: 1.14.0
%global upstream_release 4
Release: %upstream_release.10%{?dist}
License: Apache Software License
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildRequires: chrpath, libtool
BuildRequires: %{!?extbuilddir: glite-ce-wsdl, glite-build-common-cpp, } gsoap-devel
BuildRequires: %{!?extbuilddir: gridsite-devel,} libxml2-devel, boost-devel
BuildRequires: %{!?extbuilddir: voms-devel} 
BuildRequires: %{!?extbuilddir: glite-lbjp-common-gsoap-plugin-devel,} log4cpp-devel
BuildRequires: condor-classads-devel >= 8.0.4
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source5: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Source6: %{name}-%{version}-%{upstream_release}.sl6.tar.gz

%description
The package contains C/C++ libraries for the client of the CREAM service

%prep
 

%setup -c -q -T -b %{rhel}

%build
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  # We don't have pkgconfig files for classads
  export CLASSAD_CFLAGS=-I/usr/include/classad
  export CLASSAD_LIBS=-lclassad
  # We don't have pkgconfig files for gridsite
  export GRIDSITE_OPENSSL_CFLAGS=-I/usr/include
  export GRIDSITE_OPENSSL_LIBS="-lgridsite"
  # libxml2 had trouble finding its own header files
  export CPPFLAGS="-I/usr/include/libxml2"
  ./configure --prefix=%{buildroot}/usr --disable-static PVER=%{version}
  # Parallel make fails; the process that autogenerates some header files
  # finishes later than the compilation which uses those header files
  make -j1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  make install
else
  cp -R %{extbuilddir}/* %{buildroot}
fi
sed 's|^prefix=.*|prefix=/usr|g' %{buildroot}%{_libdir}/pkgconfig/cream-client-api-c.pc > %{buildroot}%{_libdir}/pkgconfig/cream-client-api-c.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/cream-client-api-c.pc.new %{buildroot}%{_libdir}/pkgconfig/cream-client-api-c.pc
sed 's|^prefix=.*|prefix=/usr|g' %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc > %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc.new %{buildroot}%{_libdir}/pkgconfig/cream-client-api-soap.pc
sed 's|^prefix=.*|prefix=/usr|g' %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc > %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc.new %{buildroot}%{_libdir}/pkgconfig/cream-client-api-util.pc
sed 's|^prefix=.*|prefix=/usr|g' %{buildroot}%{_libdir}/pkgconfig/es-client-api-c.pc > %{buildroot}%{_libdir}/pkgconfig/es-client-api-c.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/es-client-api-c.pc.new %{buildroot}%{_libdir}/pkgconfig/es-client-api-c.pc
rm %{buildroot}%{_libdir}/*.la
chrpath --delete %{buildroot}%{_libdir}/libglite_ce_cream_client_util.so.0.0.0
chrpath --delete %{buildroot}%{_libdir}/libglite_ce_cream_client_soap.so.0.0.0

%clean
rm -rf %{buildroot}
 
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%dir /usr/share/doc/%{name}-%{version}/
%doc /usr/share/doc/%{name}-%{version}/LICENSE
%{_libdir}/libglite_ce_cream_client_*.so.0
%{_libdir}/libglite_ce_cream_client_*.so.0.0.0
%{_libdir}/libglite_ce_es_client.so.0
%{_libdir}/libglite_ce_es_client.so.0.0.0



%package -n glite-ce-cream-client-devel
Summary: Development files for the client of the CREAM service
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glite-jobid-api-cpp-devel, glite-jobid-api-c-devel,
Requires: glite-lbjp-common-gsoap-plugin-devel
Requires: boost-devel, log4cpp-devel, gsoap-devel
Requires: voms-devel, gridsite-devel, libxml2-devel, glite-build-common-cpp
Requires: condor-classads-devel >= 8.0.4

%description -n glite-ce-cream-client-devel
The package contains development files for the client of the CREAM service

%files -n glite-ce-cream-client-devel
%defattr(-,root,root)
%dir /usr/include/glite/
%dir /usr/include/glite/ce/
%dir /usr/include/glite/ce/cream-client-api-c/
/usr/include/glite/ce/cream-client-api-c/*.h
/usr/include/glite/ce/cream-client-api-c/*.nsmap
%dir /usr/include/glite/ce/es-client-api-c
/usr/include/glite/ce/es-client-api-c/*.h
/usr/include/glite/ce/es-client-api-c/*.nsmap
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libglite_ce_cream_client_*.so
%{_libdir}/libglite_ce_es_client.so




%changelog
* Fri Oct 31 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.14.0-4.10
- Rebuild against condor 8.2.3

* Thu Oct 24 2013 Brian Lin <blin@cs.wisc.edu> - 1.14.0-4.9.osg
- Fixed incorrect requires statement

* Thu Oct 24 2013 Brian Lin <blin@cs.wisc.edu> - 1.14.0-4.8.osg
- Build against condor-8.0.4-1

* Tue Sep 10 2013  <edquist@cs.wisc.edu> - 1.14.0-4.7.osg
- Rebuild against latest condor

* Tue May 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.14.0-4.6.osg
- Changed classads-devel to condor-classads-devel

* Tue May 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.14.0-4.5.osg
- Fixed build requires for classads-devel

* Tue May 21 2013 Brian Lin <blin@cs.wisc.edu> - 1.14.0-4.4.osg
- Build against Condor 7.9.6

* Mon Jul 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.3.osg
- Build debug package

* Mon Jul 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.2.osg
- Include both sl5 and sl6 tarballs in the srpm

* Wed Jun 20 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.1.osg
- Rebuild for OSG
- Use sl6 tarball for el6 builds, based on %%rhel macro
- Add environment variables for configure

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 1.14.0-4.sl5
- Major bugs fixed

