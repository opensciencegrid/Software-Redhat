Summary: Grid (X.509) and VOMS credentials to local account mapping service
Name: lcmaps
Version: 1.4.28
Release: 21%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: System Environment/Libraries
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/lcmaps/%{name}-%{version}.tar.gz
Source1: lcmaps.db
Patch0: makefile_r15293.patch
Patch1: fill_x509.patch
#source of patch2: wget --no-check-certificate -Ogeneric_attributes_vomsdata.patch "https://sikkel.nikhef.nl/cgi-bin/viewvc.cgi/mwsec/trunk/lcmaps/src/grid_credential_handling/gsi_handling/lcmaps_voms_attributes.c?view=patch&r1=11815&r2=15240&pathrev=15240"
Patch2: generic_attributes_vomsdata.patch
#Patch 3 comes from the diff of all real source files in 1.4.31 compared to
# 1.4.33
Patch3: relative_path.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: globus-core%{?_isa}
BuildRequires: globus-common-devel%{?_isa}
BuildRequires: globus-gssapi-gsi-devel%{?_isa}
BuildRequires: globus-gss-assist-devel%{?_isa}
BuildRequires: globus-gsi-credential-devel%{?_isa}
BuildRequires: voms-devel%{?_isa}
BuildRequires: flex, bison
BuildRequires: automake, autoconf, libtool

Requires: globus-common
Requires: globus-gssapi-gsi
Requires: globus-gss-assist
Requires: globus-gsi-credential

Requires: lcmaps-plugins-gums-client
Requires: lcmaps-plugins-saz-client
%ifarch %{ix86}
Requires: liblcmaps_posix_enf.so.0
Requires: liblcmaps_scas_client.so.0
Requires: liblcmaps_verify_proxy.so.0
%else
Requires: liblcmaps_posix_enf.so.0()(64bit)
Requires: liblcmaps_scas_client.so.0()(64bit)
Requires: liblcmaps_verify_proxy.so.0()(64bit)
%endif

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

%package interface
Group: Development/Libraries
Summary: LCMAPS plug-in API header files
Requires: openssl-devel
Requires: globus-gssapi-gsi-devel
Requires: pkgconfig

%description interface
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

It is a highly configurable pluggable interface, and many plugins are
available to tailor almost every need. Since this is middleware, it
does not interact with the user directly; to use it in a program please
see the lcmaps-interface package.

This package contains the header files necessary to build LCMAPS plug-ins.

%package devel
Group: Development/Libraries
Summary: LCMAPS development libraries
Requires: lcmaps-interface
Requires: %{name} = %{version}-%{release}

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
%patch1 -p0
%patch2 -p2
%patch3 -p1

%build
./bootstrap
%configure --disable-static --disable-rpath --enable-osg
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
mv $RPM_BUILD_ROOT/%{_libdir}/modules $RPM_BUILD_ROOT/%{_libdir}/lcmaps
#Note: this file is %ghosted in the %files list, so it is not installed,
#  but rpmbuild requires something to be there.  There's also %ghost on
#  the example module files so this symlink takes care of them appearing
#  to be available too.
ln -s lcmaps $RPM_BUILD_ROOT/%{_libdir}/modules

# clean up installed files
rm -rf ${RPM_BUILD_ROOT}/usr/share/doc

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}
%__sed -i -e 's|@LIBDIR@|%{_libdir}|' $RPM_BUILD_ROOT/%{_sysconfdir}/lcmaps.db

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ ! -L %{_libdir}/modules ]; then
    if [ -d %{_libdir}/modules ]; then
	# move anything left in modules to lcmaps directory
	mv %{_libdir}/modules/* %{_libdir}/lcmaps >/dev/null 2>&1 || true
	rmdir %{_libdir}/modules
    fi
    # create the modules symlink for backward compatibility
    ln -s lcmaps %{_libdir}/modules
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/lcmaps.db
%{_libdir}/lcmaps.mod
%{_libdir}/lcmaps_gss_assist_gridmap.mod
%{_libdir}/lcmaps_return_poolindex.mod
%{_libdir}/liblcmaps.so
%{_libdir}/liblcmaps.so.0
%{_libdir}/liblcmaps.so.0.0.0
%{_libdir}/liblcmaps_gss_assist_gridmap.so.0
%{_libdir}/liblcmaps_gss_assist_gridmap.so.0.0.0
%{_libdir}/liblcmaps_return_account_from_pem.so.0
%{_libdir}/liblcmaps_return_account_from_pem.so.0.0.0
%{_libdir}/liblcmaps_return_poolindex.so.0
%{_libdir}/liblcmaps_return_poolindex.so.0.0.0
%{_libdir}/liblcmaps_verify_account_from_pem.so.0
%{_libdir}/liblcmaps_verify_account_from_pem.so.0.0.0
%{_libdir}/lcmaps/lcmaps_plugin_example.mod
%{_libdir}/lcmaps/liblcmaps_plugin_example.so.0
%{_libdir}/lcmaps/liblcmaps_plugin_example.so.0.0.0
%ghost %{_libdir}/modules
# in order to remove these eventually, can probably add a %preun that
#   removes the modules symlink first so the uninstall will not remove the
#   real files in the lcmaps directory.  Or maybe if the symlink is removed
#   at the same time it will just work if that goes first. 
%ghost %{_libdir}/modules/lcmaps_plugin_example.mod
%ghost %{_libdir}/modules/liblcmaps_plugin_example.so.0
%ghost %{_libdir}/modules/liblcmaps_plugin_example.so.0.0.0
# this should move into -devel package, and probably liblcmaps.so too
%{_libdir}/liblcmaps_return_account_from_pem.so

%doc AUTHORS INSTALL doc/INSTALL_WITH_WORKSPACE_SERVICE LICENSE
%doc README README.NO_LDAP
%doc etc/lcmaps.db etc/groupmapfile etc/vomapfile

%files interface
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/lcmaps/*.h

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblcmaps_gss_assist_gridmap.so
%{_libdir}/liblcmaps_return_poolindex.so
%{_libdir}/liblcmaps_verify_account_from_pem.so
%{_libdir}/lcmaps/*.so

%changelog
* Fri Dec 02 2011 Dave Dykstra <dwd@fnal.gov> - 1.4.28-21
- Add the example lcmaps plugin module files as %ghost so rpm won't think
    it has to delete them from a previous install.

* Thu Dec 01 2011 Dave Dykstra <dwd@fnal.gov> - 1.4.28-20
- Eliminate disturbing-looking log message:
    lcmaps_get_attributes Error: Could not allocate more memory
  which always appeared now with --enable-osg.  Changed it in
  the generic_attributes_vomsdata.patch, which actually probably
  isn't even needed anymore with --enable-osg.

* Wed Nov 16 2011 Dave Dykstra <dwd@fnal.gov> - 1.4.28-19
- Moved libdir/modules to libdir/lcmaps and create a symlink at
  libdir/modules for backward compatibility

* Wed Nov 16 2011 Dave Dykstra <dwd@fnal.gov> - 1.4.28-18
- Added relative_path.patch based on all the source differences between
  lcmaps-1.4.31 and lcmaps-1.4.33.  This patch allows the "path" directive
  in lcmaps.db to be a relative path, so we don't have to hardcode it to
  /usr/lib64 and break 32-bit builds.  Would have preferred just an
  upgrade but people were nervous about being too close to the
  official release, plus it seemed less time consuming at the moment
  because there are a lot of changes to lcmaps.spec in the newer 
  versions.  
  http://jira.opensciencegrid.org/browse/SOFTWARE-354
- Re-disabled VOMS verification by adding configure option --enable-osg.
  http://jira.opensciencegrid.org/browse/SOFTWARE-334

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.28-17
- rebuilt

* Mon Oct 24 2011 Dave Dykstra <dwd@drdykstra.us> - 1.4.28-16.osg
- Take patch directly from Nikhef's lcmaps-1.4.30 instead.

* Sun Oct 23 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-15
- Do not crash when a VOMS server uses generic attributes.

* Fri Sep 30 2011 Alain Roy <roy@cs.wisc.edu> - 1.4.28-14
- Fixed minor typo in spelling of sazclient.

* Mon Sep 23 2011 Dave Dykstra <dwd@fnal.gov> - 1.4.28-13
- Update lcmaps.db with gridmapfile option, glexec policies commented out
  by default (to prod admins to include glexectracking), and with better
  explanation about what needs to be editted especially for glexec.

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.28-12
- Rebuilt against updated Globus libraries

* Wed Aug 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-11
Another update to get Requires right for 32-bit modules

* Tue Aug 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-10
- Make dlopened requirements explicit.
- Default path to /usr/lib64 always until we have a better solution from upstream

* Mon Aug 29 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.28-9
- Rebuild against Globus 5.2

* Mon Aug 22 2011 Dave Dykstra <dwd@fnal.gov> - 1.4.28-8
- Change names of required lcmaps-plugins-{gums,saz}-client packages
- Remove lcmaps-plugins-glexec-tracking as a requirement at this level,
  instead it is required by osg-wn-client-glexec

* Sun Aug 07 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-7
- Let glexec-tracking find the procd in PATH, instead of specifying the directory.

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-6
- Fix dependencies so default config is usable out-of-the-box.

* Sun Jul 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-5
- Fill in appropriate x509 structs.

* Sun Jul 31 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-4
- Re-enable VOMS validation.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.28-3
A few config file tweaks discovered during testing of lcmaps.

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.28-2
- Include OSG default lcmaps.db

* Wed Mar  9 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.28-1
- Made examples out of config files

* Tue Mar  8 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.27-2
- Disable rpath in configure

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.27-1
- Fixed globus dependencies
- added ldconfig %post(un)

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.26-3
- disabled static libraries
- added proper base package requirement for devel
- fixed license string

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.
