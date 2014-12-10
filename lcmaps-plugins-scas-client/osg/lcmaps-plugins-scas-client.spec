Summary: SCAS client plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-scas-client
Version: 0.5.4
Release: 1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
BuildRequires: openssl-devel
# xacml 1.3.0 is probably ok, but prefer newer one
BuildRequires: lcmaps-devel, xacml-devel >= 1.4.0
Requires: lcmaps%{?_isa} >= 1.5.0
Requires: xacml%{?_isa} >= 1.3.0
Obsoletes: lcmaps-plugins-saz-client

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
* Tue Dec  9 2014 Dave Dykstra <dwd@fnal.gov> 0.5.4-1.1.osg
- pull in upstream version, removing OSG-specific patches
- eliminate saz-client copy, and add Obsoletes line for it to make rpm
  delete it

* Tue Jul 15 2014 Mischa Salle <msalle@nikhef.nl> 0.5.4-1
- updated version

* Thu Jun 19 2014 Dave Dykstra <dwd@fnal.gov> 0.4.0-1.3.osg
- Add patch to restore effective user id after errors reading certs
  or keys

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

* Thu Jan 23 2014 Dave Dykstra <dwd@fnal.gov> 0.4.0-1.2.osg
- Add patch from upstream to show SSL error queue when there is an
  openssl error

* Wed Oct  9 2013 Dave Dykstra <dwd@fnal.gov> 0.4.0-1.1.osg
- Reimported into OSG
- Removed log_xacml_errors.patch

* Fri Oct  4 2013 Mischa Salle <msalle@nikhef.nl> 0.4.0-1
- update build requirement on xacml-devel plus minimal version
- add requirement on xacml plus minimal version
- bumped version

* Thu Oct  3 2013 Mischa Salle <msalle@nikhef.nl> 0.3.5-1
- installed BUGS as documentation
- add requirement on LCMAPS plus minimal version
- use mandir for installing man pages
- bumped version

* Mon Sep 16 2013 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.4-1.3.osg
- Log libxacml failures.

* Thu Dec 27 2012 Dave Dykstra <dwd@fnal.gov> 0.3.4-1.2.osg
- Remove %{_libdir}/modules symlink and %ghost files
- Include a .so in lcmaps-plugins-saz-client package like all the
  other plugins have, and a symlink at .mod

* Thu Mar 15 2012 Dave Dykstra <dwd@fnal.gov> 0.3.4-1.1.osg
- Reimported to OSG
- Removed keepalive patch

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 0.3.3-1.3.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Tue Mar  6 2012 Mischa Salle <msalle@nikhef.nl> 0.3.4-1
- bumped version

* Wed Feb 29 2012 Dave Dykstra <dwd@fnal.gov> 0.3.3-1.2.osg
- Add enablekeepalive patch to turn on the --enable-keepalive option by
  default.  This is temporary until upstream enables it by default.

* Tue Feb 28 2012 Dave Dykstra <dwd@fnal.gov> 0.3.3-1.1.osg
- Upgraded upstream package, which adds certificate valid date messages
  to the authorization server for use by SAZ

* Tue Feb 28 2012 Mischa Salle <msalle@nikhef.nl> 0.3.3-1
- bumped version

* Tue Feb 21 2012 Dave Dykstra <dwd@fnal.gov> 0.3.2-1.1.osg
- Upgraded upstream package
- Removed memory_corruption and fix_loglevels.patch

* Mon Feb 20 2012 Mischa Salle <msalle@nikhef.nl> 0.3.2-1
- bumped version

* Mon Jan 16 2012 Dave Dykstra <dwd@fnal.gov> 0.3.0-1.3.osg
- Rebuild to get package signed

* Fri Jan 13 2012 Dave Dykstra <dwd@fnal.gov> 0.3.0-1.2.osg
- Just a rebuild.  It turned out that I had forgotten to add the
    'Requires: saml2-xacml2-c-lib' which is just as well because
    I can't reproduce the problem with the hadoop repo anymore.
    This rebuild is mainly to document this fact.

* Fri Dec 30 2011 Dave Dykstra <dwd@fnal.gov> 0.3.0-1.1.osg
- Imported into OSG
- Added "Requires: saml2-xacml2-c-lib", instead of the implicit
    requirement of libxacml.so which sometimes instead picks up
    prima from hadoop repo
- Included ca_only.patch to fix a SEGV when no user certificate is present.
- Included memory_corrupt.patch to fix a memory corruption issue on an
    error condition.
- Added fix_loglevels.patch to complete conversion to new lcmaps_log levels
- Added subpackage lcmaps-plugins-saz-client
- Added %ghost for plugin files in modules directory so they won't
   get deleted in an upgrade (since modules is now a symlink).

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


