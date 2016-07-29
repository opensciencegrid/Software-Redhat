Summary: Mapping interface between Globus Toolkit and LCAS/LCMAPS
Name: lcas-lcmaps-gt4-interface
Version: 0.3.0
Release: 1.1%{?dist}
Vendor: Nikhef
License: ASL 2.0
Group: Applications/System
URL: http://wiki.nikhef.nl/grid/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
Source1: gsi-authz.conf.in
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: globus-core
BuildRequires: globus-common-devel
BuildRequires: globus-gridmap-callout-error-devel
BuildRequires: globus-gsi-callback-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: globus-gsi-proxy-core-devel
BuildRequires: globus-gssapi-error-devel
BuildRequires: globus-gssapi-gsi-devel
BuildRequires: globus-gss-assist-devel
BuildRequires: lcmaps-interface
BuildRequires: openssl-devel

# explicit require as this is dlopen'd
%ifarch %{ix86}
Requires: liblcmaps.so.0
%else
Requires: liblcmaps.so.0()(64bit)
%endif

# OSG doesn't use lcas anymore
Obsoletes: lcas
Obsoletes: lcas-plugins-basic

%description

This interface extends the basic map-file based mapping capabilities of the
Globus Toolkit to use the full LCMAPS pluggable framework, which includes
pool accounts and VOMS attribute based decisions and mappings.

%prep
%setup -q

%build

%configure --disable-static --enable-lcas=no
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Install the mapping by default
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security
sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/gsi-authz.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc doc/README AUTHORS LICENSE 
%{_libdir}/liblcas_lcmaps_gt4_mapping.so
%{_libdir}/liblcas_lcmaps_gt4_mapping.so.0
%{_libdir}/liblcas_lcmaps_gt4_mapping.so.0.0.0
%{_sbindir}/gt4-interface-install.sh
%{_datadir}/man/man8/lcas_lcmaps_gt_interface.8.gz
%{_datadir}/man/man8/lcas_lcmaps_gt4_interface.8.gz
%config(noreplace) %{_sysconfdir}/grid-security/gsi-authz.conf

%changelog
* Fri Dec 20 2013 Dave Dykstra <dwd@fnal.gov> 0.3.0-1.1.osg
- pulled in new upstream version

* Tue Feb 26 2013 Mischa Salle <msalle@nikhef.nl> 0.3.0-1
- add _isa to requirement
- updated version

* Wed Feb 20 2013 Dave Dykstra <dwd@fnal.gov> 0.2.6-1.1.osg
- import 0.2.6 to OSG

* Wed Feb  6 2013 Mischa Salle <msalle@nikhef.nl> 0.2.6-1
- updated version

* Wed Dec 26 2012 Dave Dykstra <dwd@fnal.gov> 0.2.5-1.1.osg
- import 0.2.5 to OSG

* Mon Oct 22 2012 Mischa Salle <msalle@nikhef.nl> 0.2.5-1
- removed LCAS runtime dependency
- updated version

* Tue Mar 20 2012 Dave Dykstra <dwd@fnal.gov> 0.2.4-1.3.osg
- Change gsi-authz.conf to have the callout commented out by default
  so globus will fall back to the grid-mapfile

* Thu Mar 08 2012 Dave Dykstra <dwd@fnal.gov> 0.2.4-1.2.osg
- Rebuild after merging from branches/lcmaps-upgrade into trunk

* Wed Feb 29 2012 Dave Dykstra <dwd@fnal.gov> 0.2.4-1.1.osg
- Reimported upstream version and remove compilation patch

* Mon Feb 29 2012 Mischa Salle <msalle@nikhef.nl> 0.2.4-1
- updated version

* Wed Feb 22 2012 Dave Dykstra <dwd@fnal.gov> 0.2.3-1.1.osg
- Reimported upstream version, removed two patches and added disablelcas
  patch because of a minor compilation error with --enable-lcas=no

* Mon Feb 16 2012 Mischa Salle <msalle@nikhef.nl> 0.2.3-1
- updated version

* Fri Jan 20 2012 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.8
- Undo the last change, it didn't force removal, just reported an error

* Fri Jan 20 2012 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.7
- Try using Conflicts rather than Obsoletes to remove lcas & lcas-basic-plugins

* Mon Jan 16 2012 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.6
- Another rebuild now that this repository is getting signed

* Fri Jan 13 2012 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.5
- Force rebuild because for some reason the existing package isn't signed

* Wed Jan 11 2012 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.4
- There was a bug in no_lcas_interface.patch

* Mon Jan  9 2012 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.3
- Add lcas-plugins-basic to Obsoletes to see if that will avoid trying
  to pull in the 32-bit version of that package on a 64-bit install

* Thu Jan  5 2012 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.2
- Apply patch to correctly parse and use $LCMAPS_POLICY_NAME
- Apply patch to allow building with --disable-lcas and no
  lcas-interface package installed

* Thu Dec 29 2011 Dave Dykstra <dwd@fnal.gov> 0.2.1-4.1
- Imported to OSG, including adding default gsi-authz.conf
- Changed default gsi-authz.conf to have the callout uncommented
- Disabled LCAS

* Fri Dec 16 2011 Mischa Salle <msalle@nikhef.nl> 0.2.1-4
- updated version
- adding manpages

* Wed Aug 17 2011 Mischa Salle <msalle@nikhef.nl> 0.2.0-1
- Build requirements for lcas/lcmaps are only their interfaces
- updated version

* Wed Jul 13 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.1.5-1
- updated version

* Thu Jun 30 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.1.4-1
- Updated to version 0.1.4

* Mon Mar  7 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.1.2-1
- Fixed globus dependencies
- Added openssl dependency

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.1.1-3
- added ldconfig post(un) script
- disable static libraries

* Fri Feb 25 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.


