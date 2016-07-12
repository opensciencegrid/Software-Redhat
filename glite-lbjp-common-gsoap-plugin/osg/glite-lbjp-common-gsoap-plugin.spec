Name:           glite-lbjp-common-gsoap-plugin
Version:        3.2.12
Release:        1.1%{?dist}
Summary:        Plugin for gSoap to use glite-security-gss as the communication layer

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://glite.cern.ch
Vendor:         EMI
Source:         http://scientific.zcu.cz/emi/emi.lbjp-common.gsoap-plugin/%{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  c-ares-devel
BuildRequires:  cppunit-devel
BuildRequires:  chrpath
# gssapi is needed explicitly for gsoap-plugin, but the proper package is
# known only in glite-lbjp-common-gss-devel:
#  - gssapi from Globus (globus-gssapi-gsi-devel)
#  - gssapi from MIT Kerberos (krb5-devel)
#  - gssapi from Heimdal Kerberos
#BuildRequires: globus-gssapi-gsi-devel
BuildRequires:  gsoap-devel
BuildRequires:  glite-lbjp-common-gss-devel >= 3.2.16
BuildRequires:  libtool
BuildRequires:  perl
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(POSIX)
BuildRequires:  pkgconfig
Obsoletes:      glite-security-gsoap-plugin%{?_isa} < 2.0.1-1
Patch0: gsplugin.patch

%description
glite-security-gsoap-plugin is plugin for gSoap providing secured communication
via GSS, as well as strict timing control of all operations via
glite-security-gss.


%package        devel
Summary:        Development files for gLite gsoap-plugin
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glite-lbjp-common-gss-devel%{?_isa} >= 3.2.16
Provides:       glite-security-gsoap-plugin%{?_isa} = %{version}-%{release}
Obsoletes:      glite-security-gsoap-plugin%{?_isa} < 2.0.1-1

%description    devel
This package contains development libraries and header files for gLite
gsoap-plugin.


%prep
%setup -q
%patch0 -p1


%build
perl ./configure --root=/ --prefix=%{_prefix} --libdir=%{_lib} --project=emi
CFLAGS="%{?optflags}" LDFLAGS="%{?__global_ldflags}" make %{?_smp_mflags}


%check
CFLAGS="%{?optflags}" LDFLAGS="%{?__global_ldflags}" make check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
find %{buildroot} -name '*' -print | xargs -I {} -i bash -c "chrpath -d {} > /dev/null 2>&1" || echo 'Stripped RPATH'


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc ChangeLog LICENSE
%{_libdir}/libglite_security_gsoap_plugin_*.so.9
%{_libdir}/libglite_security_gsoap_plugin_*.so.9.*

%files devel
%defattr(-,root,root)
%doc examples
%{_includedir}/glite/security/glite_gscompat.h
%{_includedir}/glite/security/glite_gsplugin.h
%{_includedir}/glite/security/glite_gsplugin-int.h
%{_libdir}/libglite_security_gsoap_plugin_*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Jul 12 2016 Matyas Selmeci <matyas@cs.wisc.edu> - 3.2.12-1.1.osg
- Merge OSG changes
- Add version dependencies on glite-lbjp-common-gss-devel

* Wed Jun 25 2014 CESNET Product Teams <emi-lb@metacentrum.cz> - 3.2.12-1
- automatically generated package

* Fri Jul 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.2-2.1.osg
- Patch to add some more checking to avoid segfaults
