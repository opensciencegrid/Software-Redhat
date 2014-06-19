Summary: SCAS client plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-scas-client
Version: 0.4.0
Release: 1.3%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
Patch0: ca_only.patch
# Patch1 is from http://ndpfsvn.nikhef.nl/viewvc/mwsec/trunk/lcmaps-plugins-scas-client/src/saml2-xacml2/io_handler/ssl/ssl-common.c?r1=17274&r2=17291&view=patch
#  but is adjusted for the 0.4.0 code base
Patch1: error-ssl-more-info.patch
Patch2: restore-euid-on-error.patch
BuildRequires: openssl-devel
BuildRequires: lcmaps-interface, xacml-devel >= 1.3.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: lcmaps%{?_isa} >= 1.5.0
Requires: xacml%{?_isa} >= 1.3.0

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the SCAS client plug-in. This LCMAPS plugin
functions as the PEP (client side) implementation to an Site Central
Authorization Service (SCAS) or GUMS (new style) service.

%package -n lcmaps-plugins-saz-client
Group: System Environment/Libraries
Obsoletes: lcmaps-plugins-saz
Summary: SAZ support for lcmaps

%description -n lcmaps-plugins-saz-client
%{summary}

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# the module must be a copy, not a symlink, because the gums-client
#  is a symlink and lcmaps can't use the same module file twice
cp $RPM_BUILD_ROOT%{_libdir}/lcmaps/liblcmaps_scas_client.so $RPM_BUILD_ROOT%{_libdir}/lcmaps/liblcmaps_saz_client.so
ln -s liblcmaps_saz_client.so $RPM_BUILD_ROOT%{_libdir}/lcmaps/lcmaps_saz_client.mod
cp $RPM_BUILD_ROOT%{_mandir}/man8/lcmaps_plugins_scas_client.8 $RPM_BUILD_ROOT%{_mandir}/man8/lcmaps_plugins_saz_client.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS  LICENSE  BUGS
%{_libdir}/lcmaps/lcmaps_scas_client.mod
%{_libdir}/lcmaps/liblcmaps_scas_client.so
%{_mandir}/man8/lcmaps_plugins_scas_client.8*

%files -n lcmaps-plugins-saz-client
%{_libdir}/lcmaps/lcmaps_saz_client.mod
%{_libdir}/lcmaps/liblcmaps_saz_client.so
%{_mandir}/man8/lcmaps_plugins_saz_client.8*

%changelog
* Thu Jun 19 2014 Dave Dykstra <dwd@fnal.gov> 0.4.0-1.3.osg
- Add patch to restore effective user id after errors reading certs
  or keys

* Thu Jan 23 2014 Dave Dykstra <dwd@fnal.gov> 0.4.0-1.2.osg
- Add patch from upstream to show SSL error queue when there is an
  openssl error

* Wed Oct  9 2013 Dave Dykstra <dwd@fnal.gov> 0.4.0-1.1.osg
- Reimported into OSG
- Removed log_xacml_errors.patch

* Tue Oct  4 2013 Mischa Salle <msalle@nikhef.nl> 0.4.0-1
- update build requirement on xacml-devel plus minimal version
- add requirement on xacml plus minimal version
- bumped version

* Tue Oct  3 2013 Mischa Salle <msalle@nikhef.nl> 0.3.5-1
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

* Tue Mar  8 2012 Mischa Salle <msalle@nikhef.nl> 0.3.4-1
- bumped version

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 0.3.3-1.3.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Wed Feb 29 2012 Dave Dykstra <dwd@fnal.gov> 0.3.3-1.2.osg
- Add enablekeepalive patch to turn on the --enable-keepalive option by
  default.  This is temporary until upstream enables it by default.

* Tue Feb 28 2012 Dave Dykstra <dwd@fnal.gov> 0.3.3-1.1.osg
- Upgraded upstream package, which adds certificate valid date messages
  to the authorization server for use by SAZ

* Mon Feb 28 2012 Mischa Salle <msalle@nikhef.nl> 0.3.3-1
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


