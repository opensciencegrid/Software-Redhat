Summary: Plugin for gSoap to use glite-security-gss as the communication layer
Name: glite-lbjp-common-gsoap-plugin
Version: 3.1.2
Release: 2.2%{?dist}
Url: http://glite.cern.ch
License: ASL 2.0
Vendor: EMI
Group: System Environment/Libraries
BuildRequires: c-ares-devel
BuildRequires: cppunit-devel
BuildRequires: chrpath
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: gsoap
BuildRequires: gsoap-devel
BuildRequires: glite-lbjp-common-gss-devel
BuildRequires: libtool
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Obsoletes: glite-security-gsoap-plugin%{?_isa} < 2.0.1-1
AutoReqProv: yes
Source: http://eticssoft.web.cern.ch/eticssoft/repository/emi/emi.lbjp-common.gsoap-plugin/%{version}/src/%{name}-3.1.2-2.src.tar.gz
Patch0: gsplugin.patch


%description
glite-security-gsoap-plugin is plugin for gSoap providing secured communication
via GSS, as well as strict timing control of all operations via
glite-security-gss.


%package devel
Summary: Development files for gLite gsoap-plugin
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glite-lbjp-common-gss-devel
Provides: glite-security-gsoap-plugin%{?_isa} = %{version}-%{release}
Obsoletes: glite-security-gsoap-plugin%{?_isa} < 2.0.1-1


%description devel
This package contains development libraries and header files for gLite
gsoap-plugin.


%prep
%setup -q
%patch0 -p1


%build
/usr/bin/perl ./configure --thrflavour= --nothrflavour= --root=/ --prefix=/usr --libdir=%{_lib} --project=emi --module lbjp-common.gsoap-plugin
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
%dir /usr/share/doc/gsoap-plugin-%{version}
%doc /usr/share/doc/gsoap-plugin-%{version}/LICENSE
/usr/%{_lib}/libglite_security_gsoap_plugin_*.so.9.1.2
/usr/%{_lib}/libglite_security_gsoap_plugin_*.so.9


%files devel
%defattr(-,root,root)
%dir /usr/include/glite
%dir /usr/include/glite/security
/usr/include/glite/security/glite_gscompat.h
/usr/include/glite/security/glite_gsplugin.h
/usr/include/glite/security/glite_gsplugin-int.h
/usr/%{_lib}/libglite_security_gsoap_plugin_*.so
/usr/%{_lib}/pkgconfig/*.pc


%changelog
* Mon Jul 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.2-2.2.osg
- Bump to rebuild

* Fri Jul 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.2-2.1.osg
- Patch to add some more checking to avoid segfaults

* Wed May 16 2012 CESNET Product Teams <emi-lb@metacentrum.cz> - 3.1.2-2%{?dist}
- automatically generated package
