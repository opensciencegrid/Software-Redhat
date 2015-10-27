Summary: SCAS client plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-scas-client
Version: 0.5.4
Release: 1.1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRequires: openssl-devel
# xacml 1.3.0 is probably ok, but prefer newer one
BuildRequires: lcmaps-devel, xacml-devel >= 1.4.0
Requires: lcmaps%{?_isa} >= 1.5.0
Requires: xacml%{?_isa} >= 1.3.0

# BuildRoot is still required for EPEL5
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the SCAS client plug-in. This LCMAPS plugin
functions as the PEP (client side) implementation to an Site Central
Authorization Service (SCAS) or GUMS (new style) service.


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

# clean up installed documentation files
rm -rf ${RPM_BUILD_ROOT}%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS LICENSE BUGS NEWS
%{_libdir}/lcmaps/lcmaps_scas_client.mod
%{_libdir}/lcmaps/liblcmaps_scas_client.so
%{_mandir}/man8/lcmaps_plugins_scas_client.8*


%changelog
* Tue Jul 15 2014 Mischa Salle <msalle@nikhef.nl> 0.5.4-1
- updated version

* Thu Mar 27 2014 Mischa Salle <msalle@nikhef.nl> 0.5.3-1
- updated version

* Fri Mar 21 2014 Mischa Salle <msalle@nikhef.nl> 0.5.2-1
- updated version

* Mon Mar  3 2014 Mischa Salle <msalle@nikhef.nl> 0.5.1-1
- install NEWS file
- updated version

* Fri Feb 14 2014 Mischa Salle <msalle@nikhef.nl> 0.5.0-2
- clean up installed documentation files (breaks Fedora20)
- correct bogus dates in changelog (breaks Fedora20)

* Thu Feb 13 2014 Mischa Salle <msalle@nikhef.nl> 0.5.0-1
- update builddep on lcmaps-devel instead of -interface
- prevent unnecessary linking
- specify BuildRoot (and clean section) for EPEL5
- remove defattr
- updated version

* Fri Oct  4 2013 Mischa Salle <msalle@nikhef.nl> 0.4.0-1
- update build requirement on xacml-devel plus minimal version
- add requirement on xacml plus minimal version
- bumped version

* Thu Oct  3 2013 Mischa Salle <msalle@nikhef.nl> 0.3.5-1
- installed BUGS as documentation
- add requirement on LCMAPS plus minimal version
- use mandir for installing man pages
- bumped version

* Tue Mar  6 2012 Mischa Salle <msalle@nikhef.nl> 0.3.4-1
- bumped version

* Tue Feb 28 2012 Mischa Salle <msalle@nikhef.nl> 0.3.3-1
- bumped version

* Mon Feb 20 2012 Mischa Salle <msalle@nikhef.nl> 0.3.2-1
- bumped version

* Fri Dec 16 2011 Mischa Salle <msalle@nikhef.nl> 0.3.0-1
- bumped version
- updated installation dir plugins and removed .so.0* files

* Wed Apr  6 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.22-1
- bumped version

* Wed Mar 23 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.21-2
- removed explicit requires

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.21-1
- added openssl dependency

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.2.20-2
- fixed license string
- dropped devel package
- disable static libraries

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


