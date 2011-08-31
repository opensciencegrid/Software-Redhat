Summary: Authorization service for grid credentials
Name: lcas
Version: 1.3.13
Release: 7%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: globus-core
BuildRequires: globus-common-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-libtool-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: globus-openssl-module-devel

%ifarch %{ix86}
Requires: liblcas_userban.so
%else
Requires: liblcas_userban.so()(64bit)
%endif

%description

LCAS makes binary ('yes' or 'no') authorization decisions at the site
and resource level. In making this decision, it can use a variety of
inputs: the 'grid' name of the user (the Subject Distinguished Name),
any VO attributes the user has (like VOMS FQANs), the name of the
executable the user intends to execute. It supports basic black and
white list functionality, but also more complex VOMS-based
expressions, based on the GACL language.

%package interface
Group: Development/Libraries
Summary: LCAS plug-in API header files
Requires: globus-gssapi-gsi-devel
Requires: pkgconfig

%description interface
This package contains the interface, needed to build plug-ins for
LCAS.

%package devel
Group: Development/Libraries
Summary: LCAS development libraries
Requires: lcas-interface
Requires: %{name} = %{version}-%{release}
Requires: globus-gssapi-gsi-devel

%description devel
This package contains the development libraries for LCAS.

%prep
%setup -q

%build

%configure --disable-static --disable-rpath

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

rm -rf $RPM_BUILD_ROOT/usr/share/doc/lcas-1.3.12/*
rm $RPM_BUILD_ROOT/%{_libdir}/lcas.mod
rm $RPM_BUILD_ROOT/%{_libdir}/modules/lcas_plugin_example.mod
rm $RPM_BUILD_ROOT/%{_libdir}/modules/liblcas_plugin_example.*

# Move config files to their own subdir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mv $RPM_BUILD_ROOT%{_sysconfdir}/*.in $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/

cat > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/lcas.db << EOF
pluginname=%{_libdir}/lcas/lcas_userban.mod,pluginargs=/etc/lcas/ban_users.db
EOF

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ban_users.db

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc INSTALL LICENSE README
%{_sysconfdir}/lcas/allowed_users.db.in
%{_sysconfdir}/lcas/ban_users.db.in
%config(noreplace) %{_sysconfdir}/lcas/ban_users.db
%{_sysconfdir}/lcas/lcas.db.in
%config(noreplace) %{_sysconfdir}/lcas/lcas.db
%{_sysconfdir}/lcas/lcas_voms.gacl.in
%{_sysconfdir}/lcas/timeslots.db.in
%{_libdir}/liblcas.so
%{_libdir}/liblcas.so.0
%{_libdir}/liblcas.so.0.0.0

%files interface
%defattr(-,root,root,-)
%{_includedir}/lcas/*.h
%{_libdir}/pkgconfig/lcas-interface.pc
%{_libdir}/pkgconfig/lcas.pc

%files devel
%defattr(-,root,root,-)
%doc README

%changelog
* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.13-7
Another update to get Requires right for 32-bit modules

* Tue Aug 30 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.3.13-6
- Rebuilt against Globus 5.2

* Tue Aug 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.13-5
Explicitly require dlopened modules.

* Fri Aug 12 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.13-4
- Fix user_ban module location.

* Thu Aug 04 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.13-3
- Add usable defaults for LCAS.

* Wed Mar 23 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.3.13-2
- removed explicit requires

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.3.13-1
- bumped to version 1.3.13
- Added globus-gssapi-gsi-devel dependency on devel pkg
- Reduced globus dependencies to minimum

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.3.12-5
- Added post(un) ldconfig scripts
- disable static libraries
- fixed license string

* Thu Mar  3 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.3.12-4
- Fixed typo in summary

* Thu Feb 24 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


