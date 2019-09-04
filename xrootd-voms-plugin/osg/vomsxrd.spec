#-------------------------------------------------------------------------------
# Package definitions
#-------------------------------------------------------------------------------
Name:      vomsxrd
Epoch:     1
Version:   0.6.0
Release:   3%{?dist}
Summary:   VOMS attribute extractor plug-in for XRootD
License:   BSD
URL:       http://gganis.github.io/vomsxrd/
Prefix:    /usr

# git clone git://github.com/gganis/voms.git vomsxrd
# cd vomsxrd
# ./packaging/maketar.sh --prefix vomsxrd --output ~/rpmbuild/SOURCES/vomsxrd.tar.gz
Source0:   vomsxrd-%{version}.tar.gz

BuildRequires: cmake >= 2.6
BuildRequires: voms >= 2.0.6
BuildRequires: voms-devel >= 2.0.6
BuildRequires: xrootd-libs >= 1:4.9.1
BuildRequires: xrootd-devel >= 1:4.9.1


Requires: voms >= 2.0.6
Requires: xrootd-libs >= 1:4.9.1


Provides: xrootd-voms-plugin = %{version}-%{release}
Obsoletes: xrootd-voms-plugin < 1:0.6.0-3

%description
The VOMS attribute extractor plug-in for XRootD

#-------------------------------------------------------------------------------
# devel
#-------------------------------------------------------------------------------
%package devel
Summary: Headers for using the VOMS attribute extractor plug-in
Requires: %{name} = %{epoch}:%{version}-%{release}
%description devel
Headers for using the VOMS attribute extractor plug-in

#-------------------------------------------------------------------------------
# Build instructions
#-------------------------------------------------------------------------------
%prep
%setup -c -n vomsxrd-%{version}

%build
cd vomsxrd-%{version}
mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo ../

make VERBOSE=1 %{?_smp_mflags}

#-------------------------------------------------------------------------------
# Installation
#-------------------------------------------------------------------------------
%install
cd vomsxrd-%{version}
cd build
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

#-------------------------------------------------------------------------------
# Post actions
#-------------------------------------------------------------------------------

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

#-------------------------------------------------------------------------------
# Files
#-------------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
%{_libdir}/libXrdSecgsiVOMS-4.so*
%doc %{_mandir}/man1/libXrdSecgsiVOMS.1.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/vomsxrd

#-------------------------------------------------------------------------------
# Changelog
#-------------------------------------------------------------------------------
%changelog
* Thu Aug 1 2019 Edgar Fajardo <emfajard@ucsd.edu> - 1:0.6.0-3
- Change the name to vomsxrd (SOFTWARE-3702)

* Wed May 15 2019 Carl Edquist <edquist@cs.wisc.edu> - 1:0.6.0-2
- Add Provides/Obsoletes for vomsxrd (SOFTWARE-3679)

* Tue Apr 30 2019 Carl Edquist <edquist@cs.wisc.edu> - 1:0.6.0-1
- Update to v0.6.0 (SOFTWARE-3679)

* Wed Apr 10 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1:0.4.0-3
- Rebuild against xrootd 4.9.1 (SOFTWARE-3485)

* Wed Feb 27 2019 Carl Edquist <edquist@cs.wisc.edu> - 1:0.4.0-2
- Rebuild against xrootd 4.9.0 (SOFTWARE-3485)

* Mon Jun 20 2016 Edgar Fajardo <emfajard@ucsd.edu> -1:0.4.0-1
- Updated to v0.4.0 SOFTWARE-2363

* Wed Feb 25 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1:0.2.0-1.6.osg
- Patch to not require xrootd-compat-libs

* Mon Feb 23 2015 Edgar Fajardo <emfajard@ucsd.edu> - 1:0.2.0-1.4
- Added the xrootd-compat-libs requirement for smooth transitioning to xrootd 4.1.1

* Thu Dec 4 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:0.2.0-1.4
- Explicetly require the xrootd4 libraries

* Thu Dec 4 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:0.2.0-1.3
- Added testing instructions to the README
- Changed the name of the spec file back to vomsxrd.spec

* Tue Dec 2 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:0.2.0-1.2
- Rebuild with xroot4 libraries

* Mon Apr 22 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1:0.2.0-1.1
- Rebuild for OSG
- Fix epoch and version on xrootd dependencies
- Rename to xrootd-voms-plugin

* Wed Mar 21 2013 G. Ganis <gerardo.ganis@cern.ch>
- Created
