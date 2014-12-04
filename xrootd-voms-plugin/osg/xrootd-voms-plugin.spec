#-------------------------------------------------------------------------------
# Package definitions
#-------------------------------------------------------------------------------
Name:      xrootd-voms-plugin
Epoch:     1
Version:   0.2.0
Release:   1.3%{?dist}
Summary:   VOMS attribute extractor plug-in for XRootD
Group:     System Environment/Libraries
License:   BSD
URL:       http://gganis.github.io/vomsxrd/
Prefix:    /usr

# git clone git://github.com/gganis/voms.git vomsxrd
# cd vomsxrd
# ./packaging/maketar.sh --prefix vomsxrd --output ~/rpmbuild/SOURCES/vomsxrd.tar.gz
Source0:   vomsxrd.tar.gz
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: cmake >= 2.6
BuildRequires: voms >= 2.0.6
BuildRequires: voms-devel >= 2.0.6
#BuildRequires: xrootd4-libs 
#BuildRequires: xrootd4-devel
BuildRequires: xrootd-libs >= 4.0.1
BuildRequires: xrootd-devel >= 4.0.1


Requires: voms >= 2.0.6
Requires: xrootd-libs >= 4.0.1
Conflicts: xrootd < 3.0.3-1

%description
The VOMS attribute extractor plug-in for XRootD

#-------------------------------------------------------------------------------
# devel
#-------------------------------------------------------------------------------
%package devel
Summary: Headers for using the VOMS attribute extractor plug-in
Group:   System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
%description devel
Headers for using the VOMS attribute extractor plug-in

#-------------------------------------------------------------------------------
# Build instructions
#-------------------------------------------------------------------------------
%prep
%setup -c -n vomsxrd

%build
cd vomsxrd
mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=RelWithDebInfo ../

make VERBOSE=1 %{?_smp_mflags}

#-------------------------------------------------------------------------------
# Installation
#-------------------------------------------------------------------------------
%install
cd vomsxrd
cd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_libdir}/libXrdSecgsiVOMS.so*
%doc %{_mandir}/man1/libXrdSecgsiVOMS.1.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/vomsxrd

#-------------------------------------------------------------------------------
# Changelog
#-------------------------------------------------------------------------------
%changelog
* Thur Dec 4 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:0.2.0-1.3
- Chaanged the name of the spec file
- Added testing instructions to the README

* Tue Dec 2 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 1:0.2.0-1.2
- Rebuild with xroot4 libraries

* Mon Apr 22 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1:0.2.0-1.1
- Rebuild for OSG
- Fix epoch and version on xrootd dependencies
- Rename to xrootd-voms-plugin

* Wed Mar 21 2013 G. Ganis <gerardo.ganis@cern.ch>
- Created
