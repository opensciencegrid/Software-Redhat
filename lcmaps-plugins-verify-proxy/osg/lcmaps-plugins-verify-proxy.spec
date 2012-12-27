Summary: Proxy verification plugin for LCMAPS
Name: lcmaps-plugins-verify-proxy
Version: 1.5.4
Release: 1.1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRequires: lcmaps-interface, openssl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: lcmaps%{?_isa} >= 1.5.0

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the Verify Proxy plugin.

%prep
%setup -q

%build

%configure --disable-static

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

# clean up installed documentation files
rm -rf ${RPM_BUILD_ROOT}%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README NEWS
%{_libdir}/lcmaps/lcmaps_verify_proxy.mod
%{_libdir}/lcmaps/liblcmaps_verify_proxy.so
%{_datadir}/man/man8/lcmaps_verify_proxy.mod.8*


%changelog
* Thu Dec 27 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.1.osg
- Update upstream version including new --disallow-limited-proxy feature
  and fixes for GT3 proxies
- Remove %{_libdir}/modules symlink and corresponding %ghost files

* Wed Oct 31 2012 Mischa Salle <msalle@nikhef.nl> 1.5.4-1
- add extra doc files README NEWS
- add protection against RPATHS
- update URL
- remove Vendor tag
- updated version

* Fri Jul 20 2012 Dave Dykstra <dwd@fnal.gov> 1.5.3-1.1.osg
- Updated upstream version to pick up fix for doubly-limited proxies
  that showed up with openssl version 0.9.8c

* Fri Jul  6 2012 Mischa Salle <msalle@nikhef.nl> 1.5.3-1
- added explicit requirement on lcmaps with minimal version
- updated version

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 1.5.2-1.2.osg
- Rebuild in trunk

* Fri Feb 17 2012 Dave Dykstra <dwd@fnal.gov> 1.5.2-1.1.osg
- Updated upstream version

* Mon Jan 30 2012 Mischa Salle <msalle@nikhef.nl> 1.5.2-1
- updated version

* Fri Dec 30 2011 Dave Dykstra <dwd@fnal.gov> 1.5.0-2.1.osg
- Imported into OSG
- Moved moduledir from libdir/lcmaps to libdir/lcmaps/plugins
- Added %ghost files for the files under libdir/modules since that is
  currently a symlink to the lcmaps directory

* Thu Dec 15 2011 Mischa Salle <msalle@nikhef.nl> 1.5.0-2
- updated version
- adding manpage

* Tue Aug  7 2011 Mischa Salle <msalle@nikhef.nl> 1.4.12-3
- Forgot to add changelog entry for 1.4.12-2

* Tue Aug  2 2011 Mischa Salle <msalle@nikhef.nl> 1.4.12-2
- Remove docs created in make install, rpm does it via %doc
- Update %files to reflect new layout: modules in lcmaps, no .so.0*

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


