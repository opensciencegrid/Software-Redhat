# Notes:
# The lcmaps-*-devel packages are meant for developing client
# programs. The preferred model of development is to dlopen() the
# interface library at run-time, which means that a) the libraries are
# not required for development at all and b) client programs become
# independent of the run-time version of LCMAPS.  This is why the
# devel packages only contain header files and the .so symlinks are in
# the run-time package.
#
# The LCMAPS interfaces are:
# -basic, which are very simple and do not require openssl,
# -openssl, which include 'basic' and require openssl for x509 structures,
# -globus, which include 'openssl' and require Globus Toolkit functions.
#
# The lcmaps-devel package is the most inclusive, so it's a safe choice
# to install in case of any development work.

Summary: Grid (X.509) and VOMS credentials to local account mapping service
Name: lcmaps
Version: 1.6.4
Release: 1.2%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/LCMAPS
Source0: http://software.nikhef.nl/security/lcmaps/lcmaps-%{version}.tar.gz
Source1: lcmaps.db
Patch0: defaultnovomscheck.patch
# BuildRoot is still required for EPEL5
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: globus-core
BuildRequires: globus-common-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: voms-devel
BuildRequires: flex, bison

# these should be in a metapackage instead of here
Requires: lcmaps-plugins-gums-client
Requires: lcmaps-plugins-basic
Requires: lcmaps-plugins-verify-proxy

# these two conflicts are because older versions of these packages depend
#  on lcmaps.db policy osg_default which has been removed
Conflicts: globus-gatekeeper < 9.6-1.9
Conflicts: globus-gridftp-server-progs < 6.14-3

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.


%package without-gsi
Group: System Environment/Libraries
Summary: Grid mapping service without GSI

%description without-gsi
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

This version is built without support for the GSI protocol.


%package devel
Group: Development/Libraries
Summary: LCMAPS plug-in API header files
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-common-devel%{?_isa} = %{version}-%{release}
Requires: globus-gssapi-gsi-devel%{?_isa}
Requires: openssl-devel%{?_isa}
Provides: %{name}-globus-interface = %{version}-%{release}
Obsoletes: %{name}-globus-interface < 1.6.1-4
Provides: %{name}-openssl-interface = %{version}-%{release}
Obsoletes: %{name}-openssl-interface < 1.6.1-4
Provides: %{name}-interface = %{version}-%{release}
Obsoletes: %{name}-interface < 1.4.31-1
# the pkgconfig requirement is only necessary for EPEL5 and below;
# it's automatic for Fedora and EPEL6.
%if %{?rhel}%{!?rhel:6} <= 5
Requires: pkgconfig
%endif

%description devel
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

This package contains the files necessary to compile and link
against the LCMAPS library.


%package common-devel
Group: Development/Libraries
Summary: LCMAPS plug-in API header files
Provides: %{name}-basic-interface = %{version}-%{release}
Obsoletes: %{name}-basic-interface < 1.6.1-4
# the pkgconfig requirement is only necessary for EPEL5 and below;
# it's automatic for Fedora and EPEL6.
%if %{?rhel}%{!?rhel:6} <= 5
Requires: pkgconfig
%endif

%description common-devel
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the header files and interface definitions
for client applications.


%package without-gsi-devel
Group: Development/Libraries
Summary: LCMAPS development libraries
Requires: %{name}-without-gsi%{?_isa} = %{version}-%{release}
Requires: %{name}-common-devel%{?_isa} = %{version}-%{release}
# the pkgconfig requirement is only necessary for EPEL5 and below;
# it's automatic for Fedora and EPEL6.
%if %{?rhel}%{!?rhel:6} <= 5
Requires: pkgconfig
%endif

%description without-gsi-devel
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

This package contains the development libraries to build
without the GSI protocol.


%prep
%setup -q
%patch0 -p0

%build

# First configure and build the without-gsi version
mkdir build-without-gsi && cd build-without-gsi && ln -s ../configure
%configure --disable-gsi-mode --disable-static

# The following lines were suggested by
# https://fedoraproject.org/wiki/Packaging/Guidelines to prevent any
# RPATHs creeping in, and by
# https://fedoraproject.org/wiki/Common_Rpmlint_issues#unused-direct-shlib-dependency
# to prevent unnecessary linking
%define fixlibtool() sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool\
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool\
sed -i -e 's! -shared ! -Wl,--as-needed\\0!g' libtool

%fixlibtool
make %{?_smp_mflags}
cd ..

# configure and build the full version
mkdir build && cd build && ln -s ../configure
%{configure} --disable-static
%fixlibtool
make %{?_smp_mflags}
cd ..

%install
rm -rf $RPM_BUILD_ROOT

# install the without-gsi version
cd build-without-gsi
make DESTDIR=$RPM_BUILD_ROOT install
cd ..

# install the full version
cd build
make DESTDIR=$RPM_BUILD_ROOT install
cd ..

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# install lcmaps.db
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}

# create empty plugin directory
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/lcmaps

# clean up installed files
rm -rf ${RPM_BUILD_ROOT}%{_docdir}

# Retain the clean section for EPEL5
%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post without-gsi -p /sbin/ldconfig

%postun without-gsi -p /sbin/ldconfig

%files
%config(noreplace) %{_sysconfdir}/lcmaps.db
# The libraries are meant to be dlopened by client applications,
# so the .so symlinks are here and not in devel.
%{_libdir}/liblcmaps.so
%{_libdir}/liblcmaps.so.0
%{_libdir}/liblcmaps.so.0.0.0
%{_libdir}/liblcmaps_gss_assist_gridmap.so
%{_libdir}/liblcmaps_gss_assist_gridmap.so.0
%{_libdir}/liblcmaps_gss_assist_gridmap.so.0.0.0
%{_libdir}/liblcmaps_return_account_from_pem.so
%{_libdir}/liblcmaps_return_account_from_pem.so.0
%{_libdir}/liblcmaps_return_account_from_pem.so.0.0.0
%{_libdir}/liblcmaps_return_poolindex.so
%{_libdir}/liblcmaps_return_poolindex.so.0
%{_libdir}/liblcmaps_return_poolindex.so.0.0.0
%{_libdir}/liblcmaps_verify_account_from_pem.so
%{_libdir}/liblcmaps_verify_account_from_pem.so.0
%{_libdir}/liblcmaps_verify_account_from_pem.so.0.0.0
%{_datadir}/man/man3/lcmaps.3*
%dir %{_libdir}/lcmaps
%doc BUGS AUTHORS doc/INSTALL_WITH_WORKSPACE_SERVICE LICENSE
%doc README README.NO_LDAP
%doc build/etc/lcmaps.db build/etc/groupmapfile build/etc/vomapfile

%files without-gsi
# These libraries are dlopened, so the .so symlinks cannot be in devel
%{_libdir}/liblcmaps_without_gsi.so
%{_libdir}/liblcmaps_without_gsi.so.0
%{_libdir}/liblcmaps_without_gsi.so.0.0.0
%{_libdir}/liblcmaps_return_poolindex_without_gsi.so
%{_libdir}/liblcmaps_return_poolindex_without_gsi.so.0
%{_libdir}/liblcmaps_return_poolindex_without_gsi.so.0.0.0
%{_libdir}/liblcmaps_gss_assist_gridmap_without_gsi.so
%{_libdir}/liblcmaps_gss_assist_gridmap_without_gsi.so.0
%{_libdir}/liblcmaps_gss_assist_gridmap_without_gsi.so.0.0.0
%{_datadir}/man/man3/lcmaps.3*
%dir %{_libdir}/lcmaps
%doc BUGS AUTHORS LICENSE
%doc README README.NO_LDAP
%doc build-without-gsi/etc/lcmaps.db
%doc build-without-gsi/etc/groupmapfile
%doc build-without-gsi/etc/vomapfile

%files devel
%{_includedir}/lcmaps/lcmaps_return_poolindex.h
%{_includedir}/lcmaps/_lcmaps_return_poolindex.h
%{_includedir}/lcmaps/lcmaps.h
%{_includedir}/lcmaps/lcmaps_globus.h
%{_includedir}/lcmaps/lcmaps_openssl.h
%{_datadir}/pkgconfig/lcmaps-openssl-interface.pc
%{_datadir}/pkgconfig/lcmaps-globus-interface.pc
%{_datadir}/pkgconfig/lcmaps-interface.pc
%{_libdir}/pkgconfig/lcmaps-gss-assist-gridmap.pc
%{_libdir}/pkgconfig/lcmaps-return-account-from-pem.pc
%{_libdir}/pkgconfig/lcmaps-return-poolindex.pc
%{_libdir}/pkgconfig/lcmaps-verify-account-from-pem.pc
%{_libdir}/pkgconfig/lcmaps.pc
%doc LICENSE

%files common-devel
%dir %{_includedir}/lcmaps
%{_includedir}/lcmaps/lcmaps_version.h
%{_includedir}/lcmaps/lcmaps_account.h
%{_includedir}/lcmaps/lcmaps_arguments.h
%{_includedir}/lcmaps/lcmaps_basic.h
%{_includedir}/lcmaps/lcmaps_cred_data.h
%{_includedir}/lcmaps/lcmaps_db_read.h
%{_includedir}/lcmaps/lcmaps_defines.h
%{_includedir}/lcmaps/_lcmaps_gss_assist_gridmap.h
%{_includedir}/lcmaps/lcmaps_gss_assist_gridmap.h
%{_includedir}/lcmaps/_lcmaps.h
%{_includedir}/lcmaps/lcmaps_if.h
%{_includedir}/lcmaps/lcmaps_log.h
%{_includedir}/lcmaps/lcmaps_modules.h
%{_includedir}/lcmaps/_lcmaps_return_account_from_pem.h
%{_includedir}/lcmaps/lcmaps_return_account_from_pem.h
%{_includedir}/lcmaps/lcmaps_types.h
%{_includedir}/lcmaps/lcmaps_utils.h
%{_includedir}/lcmaps/_lcmaps_verify_account_from_pem.h
%{_includedir}/lcmaps/lcmaps_verify_account_from_pem.h
%{_includedir}/lcmaps/lcmaps_vo_data.h
%{_includedir}/lcmaps/lcmaps_return_poolindex_without_gsi.h
%{_includedir}/lcmaps/lcmaps_plugin_typedefs.h
%{_includedir}/lcmaps/lcmaps_plugin_prototypes.h
%{_datadir}/pkgconfig/lcmaps-basic-interface.pc
%doc LICENSE

%files without-gsi-devel
%{_libdir}/pkgconfig/lcmaps-return-poolindex-without-gsi.pc
%{_libdir}/pkgconfig/lcmaps-gss-assist-gridmap-without-gsi.pc
%{_libdir}/pkgconfig/lcmaps-without-gsi.pc
%doc LICENSE


%changelog
* Tue Dec 09 2014 Dave Dykstra <dwd@fnal.gov> 1.6.4-1.2.osg
- Removed requirement of lcmaps-plugins-saz-client

* Tue Dec 09 2014 Dave Dykstra <dwd@fnal.gov> 1.6.4-1.1.osg
- Reimported upstream version into OSG

* Fri Feb 28 2014 Mischa Salle <msalle@nikhef.nl> 1.6.4-1
- updated version
- do not install very old doc/INSTALL_WITH_WORKSPACE_SERVICE

* Sun Feb 16 2014 Mischa Salle <msalle@nikhef.nl> 1.6.3-2
- fix macro expansion for pkgconfig to include only rhel not fedora

* Thu Feb 13 2014 Mischa Salle <msalle@nikhef.nl> 1.6.3-1
- updated version

* Fri Feb  7 2014 Mischa Salle <msalle@nikhef.nl> 1.6.2-1
- Add new interface files
- Remove unused patch
- Create empty plugin directory
- Do not remove lcmaps_plugin_example related files, as they are not installed
- updated version

* Tue Nov 12 2013 Dennis van Dok <dennisvd@nikhef.nl> 1.6.1-6
- Make requirements arch-specific for devel package

* Mon Nov 11 2013 Dennis van Dok <dennisvd@nikhef.nl> 1.6.1-5
- put BuildRoot and clean section back in for EPEL5
- Add requirement on pkgconfig for EPEL5
- Include Provides/Obsoletes to rename interface packages

* Wed Oct 30 2013 Dennis van Dok <dennisvd@nikhef.nl> 1.6.1-3
- Reduced the number of development packages

* Wed Oct 23 2013 Dennis van Dok <dennisvd@nikhef.nl> 1.6.1-2
- Renamed the -interface packages to -devel
- Dropped buildroot and defattr

* Wed Feb 27 2013 Mischa Salle <msalle@nikhef.nl> 1.6.1-1
- install BUGS as doc
- updated version

* Tue Feb 26 2013 Mischa Salle <msalle@nikhef.nl> 1.6.0-1
- updated version

* Thu Feb 21 2013 Dave Dykstra <dwd@fnal.gov> 1.5.7-1.4.osg
- Remove the osg_default policy from lcmaps.db since it is no longer 
  used by any application

* Thu Jan 10 2013 Dave Dykstra <dwd@fnal.gov> 1.5.7-1.3.osg
- Back out the changes of 1.5.7-1.2.osg for now

* Fri Jan 02 2013 Dave Dykstra <dwd@fnal.gov> 1.5.7-1.2.osg
- Move lcmaps.db and Requires of lcmaps plugins to new osg-lcmaps metapackage

* Wed Jan 02 2013 Dave Dykstra <dwd@fnal.gov> 1.5.7-1.1.osg
- Import latest upstream version
- Remove references to %{_libdir}/modules and %ghost files

* Thu Dec 06 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.5.osg
- Remove accidentally-added "{%_isa}" junk on Requires statements

* Thu Dec 06 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.4.osg
- Prevent printing an error "mv: cannot stat `*': No such file or directory"
  when %{_libdir}/modules is empty

* Tue Oct 23 2012 Mischa Salle <msalle@nikhef.nl> 1.5.7-1
- Do not install INSTALL in doc.
- Update URL.
- updated version

* Fri Sep 14 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.3.osg
- Prevent the movement of files from the old %{_libdir}/modules directory
  to %{_libdir}/lcmaps from overwriting anything that was already there

* Fri Jul  6 2012 Mischa Salle <msalle@nikhef.nl> 1.5.6-1
- updated version

* Fri Jun 15 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.2.osg
- Add authorize_only policy to default lcmaps.db, for Condor

* Mon Apr 23 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.1.osg
- Reimported from upstream, fixes bug with parsing that caused unmatched
  quotes in lcmaps.db to trigger an 'out of memory' error

* Mon Apr 23 2012 Mischa Salle <msalle@nikhef.nl> 1.5.5-1
- build both with and without gsi packages in one spec file
- updated version

* Wed Apr 18 2012 Dave Dykstra <dwd@fnal.gov> 1.5.3-1.3.osg
- Add patch to change the default voms certificate check to be off,
  but still possible to be enabled at run time

* Wed Apr 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> 1.5.3-1.2.osg
- Added fix for %{_libdir}/modules conflict between lcmaps and the plugins

* Mon Mar 26 2012 Mischa Salle <msalle@nikhef.nl> 1.5.4-1
- updated version

* Mon Mar 19 2012 Dave Dykstra <dwd@fnal.gov> 1.5.3-1.1.osg
- Reimported into OSG, removed the temporary patch

* Fri Mar 16 2012 Mischa Salle <msalle@nikhef.nl> 1.5.3-1
- updated version

* Mon Mar 12 2012 Dave Dykstra <dwd@fnal.gov> 1.5.2-2.4.osg
- Add temporary patch to turn "error:storing gss_credential or its
  derivative credentials" into a warning when grid-proxy-init is
  used instead of voms-proxy-init.

* Fri Mar 09 2012 Dave Dykstra <dwd@fnal.gov> 1.5.2-2.3.osg
- Update the default lcmaps.db to give 3 policy options for the
  osg_default policy exactly like there was for glexec

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 1.5.2-2.2.osg
- Rebuild for trunk

* Fri Feb 17 2012 Dave Dykstra <dwd@fnal.gov> 1.5.2-2.1.osg
- Updated upstream version

* Mon Jan 30 2012 Mischa Salle <msalle@nikhef.nl> 1.5.2-3
- add manpage in main package
- updated version

* Fri Dec 30 2011 Dave Dykstra <dwd@fnal.gov> 1.5.0-1.1.osg
- Re-import to OSG, applying still-relevant OSG modifications
- Update default lcmaps.db with new glexectracking options and with
  combined osg_default rule for gridftp & gatekeeper

* Wed Dec 14 2011 Mischa Salle <msalle@nikhef.nl> 1.5.0-1

* Tue Sep 20 2011 Mischa Salle <msalle@nikhef.nl> 1.4.33-1
- updated version
- added obsoletes for lcmaps-interface

* Fri Sep 16 2011 Mischa Salle <msalle@nikhef.nl> 1.4.32-1
- updated version

* Tue Sep 13 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.31-5
- Repaired the unintended post macro in the changelog

* Wed Aug 10 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.31-4
- Split interface according to dependencies on globus and openssl

* Wed Jul 20 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.30-2
- Moved the .so files to the runtime package as these are dlopened

* Wed Jul 13 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.30-1
- updated version

* Mon Jul  4 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1.4.29-2
- Make interface package noarch
- Remove Vendor tag

* Mon Jul  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.29-1
- Updated version

* Wed Mar 23 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.28-2
- removed explicit requires

* Wed Mar  9 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.28-1
- Made examples out of config files

* Tue Mar  8 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.27-2
- Disable rpath in configure

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.27-1
- Fixed globus dependencies
- added ldconfig to post and postun section

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.26-3
- disabled static libraries
- added proper base package requirement for devel
- fixed license string

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl>
- Initial build.
