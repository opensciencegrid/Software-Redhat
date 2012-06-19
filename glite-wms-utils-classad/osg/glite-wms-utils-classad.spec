Summary: C/C++ libraries for ClassAd handling
Name: glite-wms-utils-classad
Version: 3.3.0
%global upstream_release 2
Release: %{upstream_release}.1%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildArch: %{_arch}
BuildRequires: chrpath, libtool, condor-classads-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source: %{name}-%{version}-%{upstream_release}.sl%{rhel}.tar.gz

%global debug_package %{nil}

%description
C/C++ libraries for ClassAd handling

%prep

%setup -c -q

%build
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  ./configure --prefix=%{buildroot}/usr --disable-static PVER=%{version}
  make
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
sed 's|^prefix=.*|prefix=/usr|g' %{buildroot}%{_libdir}/pkgconfig/classad-utils.pc > %{buildroot}%{_libdir}/pkgconfig/classad-utils.pc.new
mv %{buildroot}%{_libdir}/pkgconfig/classad-utils.pc.new %{buildroot}%{_libdir}/pkgconfig/classad-utils.pc
rm %{buildroot}%{_libdir}/*.la
chrpath --delete %{buildroot}%{_libdir}/libglite_wmsutils_classads.so.0.0.0

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig 

%files
%defattr(-,root,root)
%dir /usr/share/doc/glite-wms-utils-classad-%{version}/
%doc /usr/share/doc/glite-wms-utils-classad-%{version}/LICENSE
%{_libdir}/libglite_wmsutils_classads.so.0.0.0
%{_libdir}/libglite_wmsutils_classads.so.0



%package devel
Summary: C/C++ libraries for ClassAd handling (development files)
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: condor-classads-devel

%description devel
C/C++ libraries for ClassAd handling (development files)

%files devel
%defattr(-,root,root)
%dir /usr/include/glite/
%dir /usr/include/glite/wmsutils/
%dir /usr/include/glite/wmsutils/classads/
/usr/include/glite/wmsutils/classads/classad_utils.h
%{_libdir}/libglite_wmsutils_classads.so
%{_libdir}/pkgconfig/classad-utils.pc


%changelog
* Mon Jun 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.3.0-2.1.osg
- Rebuild for osg
- classads-devel requirement changed to condor-classads-devel
- Add el6 tarball; determine which one to include based on %%rhel macro

* Wed May 16 2012 WMS group <wms-support@lists.infn.it> - 3.3.0-2.sl5
- Major bugs fixed

