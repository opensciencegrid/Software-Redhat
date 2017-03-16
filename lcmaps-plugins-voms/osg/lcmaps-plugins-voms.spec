Summary: VOMS plugins for the LCMAPS authorization framework
Name: lcmaps-plugins-voms
Version: 1.7.1
Release: 1.2%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
Patch0: sw2635-voms-validation.patch
BuildRequires: lcmaps-devel
Requires: lcmaps%{?_isa} >= 1.5.0-1
# BuildRoot is still required for EPEL5
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
The Local Centre MAPping Service (LCMAPS) is a security middleware
component that processes the users Grid credentials (typically X.509
proxy certificates and VOMS attributes) and maps the user to a local
account based on the site local policy.

This package contains the VOMS plugins.

%prep
%setup -q
%patch0 -p1

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
cp $RPM_BUILD_ROOT/%{_libdir}/lcmaps/lcmaps_voms_localaccount.mod \
   $RPM_BUILD_ROOT/%{_libdir}/lcmaps/lcmaps_voms_localaccount2.mod

# clean up installed documentation files
rm -rf ${RPM_BUILD_ROOT}%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS LICENSE NEWS BUGS
%{_libdir}/lcmaps/lcmaps_voms.mod
%{_libdir}/lcmaps/lcmaps_ban_fqan.mod
%{_libdir}/lcmaps/lcmaps_voms_localaccount.mod
%{_libdir}/lcmaps/lcmaps_voms_localaccount2.mod
%{_libdir}/lcmaps/lcmaps_voms_localgroup.mod
%{_libdir}/lcmaps/lcmaps_voms_poolaccount.mod
%{_libdir}/lcmaps/lcmaps_voms_poolgroup.mod
%{_libdir}/lcmaps/liblcmaps_voms.so
%{_libdir}/lcmaps/liblcmaps_ban_fqan.so
%{_libdir}/lcmaps/liblcmaps_voms_localaccount.so
%{_libdir}/lcmaps/liblcmaps_voms_localgroup.so
%{_libdir}/lcmaps/liblcmaps_voms_poolaccount.so
%{_libdir}/lcmaps/liblcmaps_voms_poolgroup.so
%{_mandir}/man8/lcmaps_voms.mod.8*
%{_mandir}/man8/lcmaps_ban_fqan.mod.8*
%{_mandir}/man8/lcmaps_voms_localaccount.mod.8*
%{_mandir}/man8/lcmaps_voms_localgroup.mod.8*
%{_mandir}/man8/lcmaps_voms_poolaccount.mod.8*
%{_mandir}/man8/lcmaps_voms_poolgroup.mod.8*

%changelog
* Thu Mar 16 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.7.1-1.2
- Add patch to fail plugin if VOMS validation is disabled (SOFTWARE-2635)

* Wed Feb 15 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 1.7.1-1.1
- Add hack to let us use two copies of lcmaps_voms_localaccount in the
  lcmaps.db (SOFTWARE-2563)

* Mon Jul 20 2015 Mischa Salle <msalle@nikhef.nl> 1.7.1-1
- updated version

* Mon Feb  9 2015 Mischa Salle <msalle@nikhef.nl> 1.7.0-1
- updated version
- update build-time dependencies

* Mon Sep 29 2014 Mischa Salle <msalle@nikhef.nl> 1.6.5-1
- updated version
- update globus build-time dependencies

* Fri Feb 28 2014 Mischa Salle <msalle@nikhef.nl> 1.6.4-1
- updated version

* Thu Feb 13 2014 Mischa Salle <msalle@nikhef.nl> 1.6.3-1
- prevent unnecessary linking
- updated version

* Tue Nov 12 2013 Mischa Salle <msalle@nikhef.nl> 1.6.2-1
- update buildroot
- change lcmaps build dependency into fedora-compliant lcmaps-devel
- update globus build requires
- update runtime requires
- updated version

* Wed Feb 27 2013 Mischa Salle <msalle@nikhef.nl> 1.6.1-1
- updated version

* Tue Feb 26 2013 Mischa Salle <msalle@nikhef.nl> 1.6.0-1
- install BUGS as doc
- updated version

* Wed Oct 31 2012 Mischa Salle <msalle@nikhef.nl> 1.5.5-1
- install NEWS as doc
- add protection against RPATHS
- remove docs created in make install, rpm does it
- updated version

* Tue Oct 23 2012 Mischa Salle <msalle@nikhef.nl> 1.5.4-1
- Added plugin lcmaps_ban_fqan including manpage. 
- Update URL.
- Add architecture to run-time requirements.
- Add minimum version for lcmaps run-time requirement
- updated version

* Tue Mar 20 2012 Mischa Salle <msalle@nikhef.nl> 1.5.3-1
- updated version
- adding manpages

* Wed Feb 29 2012 Mischa Salle <msalle@nikhef.nl> 1.5.2-1
- updated version

* Mon Jan 30 2012 Mischa Salle <msalle@nikhef.nl> 1.5.1-1
- updated version

* Thu Dec 15 2011 Mischa Salle <msalle@nikhef.nl> 1.5.0-1
- updated version

* Fri Jul 15 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.4-1
- removed vendor tag
- disabled versioning

* Wed Apr  6 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.3-1
- bumped version

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.2-1
- Updated dependencies

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 1.4.1-2
- fixed license string
- disabled static libraries
- dropped devel package

* Mon Feb 21 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


