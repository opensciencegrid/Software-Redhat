# Notes:
# The *-interface packages are meant for developing client
# programs. The preferred model of development is to dlopen() the
# interface library at run-time, which means that a) the libraries are
# not required for development at all and b) client programs become
# independent of the run-time version of LCMAPS.
# This is why the interface packages only contain header files and do
# not depend on the base package. It is also the reason that the .so
# symlinks are in the run-time package and not in the devel package.

Summary: Grid (X.509) and VOMS credentials to local account mapping service
Name: lcmaps
Version: 1.5.4
Release: 1.5%{?dist}
#Release: 0.%(date +%%Y%%m%%d_%%H%%M)%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/lcmaps/lcmaps-%{version}.tar.gz
Source1: lcmaps.db
Patch0: defaultnovomscheck.patch
BuildRoot: %{_tmppath}/lcmaps-%{version}-%{release}-buildroot
BuildRequires: globus-core
BuildRequires: globus-common-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: voms-devel
BuildRequires: flex, bison
BuildRequires: automake, autoconf, libtool

Requires: lcmaps-plugins-gums-client
Requires: lcmaps-plugins-saz-client
Requires: lcmaps-plugins-basic
Requires: lcmaps-plugins-verify-proxy

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

%package globus-interface
Group: Development/Libraries
Summary: LCMAPS plug-in API header files
Requires: lcmaps-openssl-interface = %{version}-%{release}
Requires: globus-gssapi-gsi-devel
# the pkgconfig requirement is only necessary for EPEL5 and below;
# it's automatic for Fedora and EPEL6.
%if %{?rhel}%{!?rhel:0} <= 5
Requires: pkgconfig
%endif
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch: noarch
%endif
Provides: lcmaps-interface = %{version}-%{release}
Obsoletes: lcmaps-interface < 1.4.31-1

%package openssl-interface
Group: Development/Libraries
Summary: LCMAPS plug-in API header files
Requires: lcmaps-basic-interface = %{version}-%{release}
Requires: openssl-devel
%if %{?rhel}%{!?rhel:0} <= 5
Requires: pkgconfig
%endif
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch: noarch
%endif

%package basic-interface
Group: Development/Libraries
Summary: LCMAPS plug-in API header files
%if %{?rhel}%{!?rhel:0} <= 5
Requires: pkgconfig
%endif
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch: noarch
%endif

%description globus-interface
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the header files and interface definitions
that depend on Globus Toolkit data structures.

%description openssl-interface
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the header files and interface definitions
that depend on openssl data structures.

%description basic-interface
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the header files and interface definitions
for client applications.

%package devel
Group: Development/Libraries
Summary: LCMAPS development libraries
Requires: lcmaps-globus-interface = %{version}-%{release}
Requires: lcmaps = %{version}-%{release}

%description devel
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

This package contains the development libraries.

%prep
%setup -q
%patch0 -p0

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
#mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lcmaps

# clean up installed files
rm -rf ${RPM_BUILD_ROOT}%{_docdir}
rm ${RPM_BUILD_ROOT}%{_libdir}/lcmaps/lcmaps_plugin_example.mod
rm ${RPM_BUILD_ROOT}%{_libdir}/lcmaps/liblcmaps_plugin_example.so

#Note: this file is %ghosted in the %files list, so it is not installed,
#  but rpmbuild requires something to be there.
# Normally touch would be used, but the lcmaps-plugins-* rpms make a symlink
# instead, so we have to follow suit here to avoid conflicts.
ln -s lcmaps $RPM_BUILD_ROOT/%{_libdir}/modules

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ ! -L %{_libdir}/modules ]; then
    if [ -d %{_libdir}/modules ]; then
	# move anything left in modules to lcmaps directory unless 
	#  the corresponding file already exists
	(cd %{_libdir}/modules
	for F in *; do
	    if [ "$F" = "*" ]; then
		break
	    fi
	    if [ -e "../lcmaps/$F" ]; then
		rm -f "$F"
	    else
		mv "$F" ../lcmaps
	    fi
	done
	)
	rmdir %{_libdir}/modules
    fi
    # create the modules symlink for backward compatibility
    ln -s lcmaps %{_libdir}/modules
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
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
%ghost %{_libdir}/modules
%doc AUTHORS INSTALL doc/INSTALL_WITH_WORKSPACE_SERVICE LICENSE
%doc README README.NO_LDAP
%doc etc/lcmaps.db etc/groupmapfile etc/vomapfile

%files globus-interface
%defattr(-,root,root,-)
%{_includedir}/lcmaps/lcmaps_return_poolindex.h
%{_includedir}/lcmaps/_lcmaps_return_poolindex.h
%{_includedir}/lcmaps/lcmaps.h
%{_includedir}/lcmaps/lcmaps_globus.h
%{_datadir}/pkgconfig/lcmaps-globus-interface.pc
%{_datadir}/pkgconfig/lcmaps-interface.pc

%files openssl-interface
%defattr(-,root,root,-)
%{_includedir}/lcmaps/lcmaps_openssl.h
%{_datadir}/pkgconfig/lcmaps-openssl-interface.pc

%files basic-interface
%defattr(-,root,root,-)
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
%{_datadir}/pkgconfig/lcmaps-basic-interface.pc
%doc LICENSE

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/lcmaps-gss-assist-gridmap.pc
%{_libdir}/pkgconfig/lcmaps-return-account-from-pem.pc
%{_libdir}/pkgconfig/lcmaps-return-poolindex.pc
%{_libdir}/pkgconfig/lcmaps-verify-account-from-pem.pc
%{_libdir}/pkgconfig/lcmaps.pc

%changelog
* Thu Dec 06 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.5.osg
- Remove accidentally-added "{%_isa}" junk on Requires statements

* Thu Dec 06 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.4.osg
- Prevent printing an error "mv: cannot stat `*': No such file or directory"
  when %{_libdir}/modules is empty

* Fri Sep 14 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.3.osg
- Prevent the movement of files from the old %{_libdir}/modules directory
  to %{_libdir}/lcmaps from overwriting anything that was already there

* Fri Jun 15 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.2.osg
- Add authorize_only policy to default lcmaps.db, for Condor

* Mon Apr 23 2012 Dave Dykstra <dwd@fnal.gov> 1.5.4-1.1.osg
- Reimported from upstream, fixes bug with parsing that caused unmatched
  quotes in lcmaps.db to trigger an 'out of memory' error
  
* Mon Apr 23 2012 Mischa Salle <msalle@nikhef.nl> 1.5.4-1
- updated version

* Wed Apr 18 2012 Dave Dykstra <dwd@fnal.gov> 1.5.3-1.3.osg
- Add patch to change the default voms certificate check to be off,
  but still possible to be enabled at run time

* Wed Apr 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> 1.5.3-1.2.osg
- Added fix for %{_libdir}/modules conflict between lcmaps and the plugins

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

* Mon Jan 30 2012 Mischa Salle <msalle@nikhef.nl> 1.5.2-2
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
