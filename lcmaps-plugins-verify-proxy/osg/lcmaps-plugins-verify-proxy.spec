Summary: Proxy verification plugin for LCMAPS
Name: lcmaps-plugins-verify-proxy
Version: 1.5.9
Release: 1.1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRequires: lcmaps-devel, openssl-devel
Requires: lcmaps%{?_isa} >= 1.5.0-1
# BuildRoot is still required for EPEL5
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the Verify Proxy plugin and a command-line tool.

%prep
%setup -q

%build

%configure --disable-static

# The following two lines were suggested by
# https://fedoraproject.org/wiki/Packaging/Guidelines to prevent any
# RPATHs creeping in.
# https://fedoraproject.org/wiki/Common_Rpmlint_issues#unused-direct-shlib-dependency
# to prevent unnecessary linking
%define fixlibtool() sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool\
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool\
sed -i -e 's! -shared ! -Wl,--as-needed\\0!g' libtool

%fixlibtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Hack to let us use two copies of this plugin
cp $RPM_BUILD_ROOT%{_libdir}/lcmaps/lcmaps_verify_proxy.mod \
   $RPM_BUILD_ROOT%{_libdir}/lcmaps/lcmaps_verify_proxy2.mod

# clean up installed documentation files
rm -rf ${RPM_BUILD_ROOT}%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS LICENSE NEWS BUGS README
%{_bindir}/verify-proxy-tool
%{_libdir}/lcmaps/lcmaps_verify_proxy.mod
%{_libdir}/lcmaps/lcmaps_verify_proxy2.mod
%{_libdir}/lcmaps/liblcmaps_verify_proxy.so
%{_mandir}/man1/verify-proxy-tool.1*
%{_mandir}/man8/lcmaps_verify_proxy.mod.8*

%changelog
* Fri Feb 24 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.9-1.1
- Add hack to let us use two copies of lcmaps_verify_proxy in the
  lcmaps.db (SOFTWARE-2602)

* Mon May 30 2016 Mischa Salle <msalle@nikhef.nl> 1.5.9-1
- updated version

* Mon May  9 2016 Mischa Salle <msalle@nikhef.nl> 1.5.8-1
- updated version

* Thu Mar 12 2015 Mischa Salle <msalle@nikhef.nl> 1.5.7-1
- added verify-proxy-tool files
- updated version

* Tue Mar  4 2014 Mischa Salle <msalle@nikhef.nl> 1.5.6-2
- install BUGS file
- do not use macros in changelog

* Fri Feb 28 2014 Mischa Salle <msalle@nikhef.nl> 1.5.6-1
- updated version

* Thu Feb 13 2014 Mischa Salle <msalle@nikhef.nl> 1.5.5-1
- update builddep on lcmaps-devel instead of -interface
- prevent unnecessary linking
- specify BuildRoot (and clean section) for EPEL5
- remove defattr
- updated version

* Wed Oct 31 2012 Mischa Salle <msalle@nikhef.nl> 1.5.4-1
- add extra doc files README NEWS
- add protection against RPATHS
- update URL
- remove Vendor tag
- updated version

* Fri Jul  6 2012 Mischa Salle <msalle@nikhef.nl> 1.5.3-1
- added explicit requirement on lcmaps with minimal version
- updated version

* Mon Jan 30 2012 Mischa Salle <msalle@nikhef.nl> 1.5.2-1
- updated version

* Thu Dec 15 2011 Mischa Salle <msalle@nikhef.nl> 1.5.0-2
- updated version
- adding manpage

* Sun Aug  7 2011 Mischa Salle <msalle@nikhef.nl> 1.4.12-3
- Forgot to add changelog entry for 1.4.12-2

* Tue Aug  2 2011 Mischa Salle <msalle@nikhef.nl> 1.4.12-2
- Remove docs created in make install, rpm does it via doc macro
- Update files to reflect new layout: modules in lcmaps, no .so.0*

* Tue Aug  2 2011 Oscar Koeroo <okoeroo@nikhef.nl> 1.4.12-1
- New version 1.4.12

* Wed Mar 23 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.9-2
- removed explicit requires

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.9-1
- Updated dependencies on openssl

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.8-2
- disable static libraries
- fixed license string
- dropped devel package

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


