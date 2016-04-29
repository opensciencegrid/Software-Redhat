%{?suse_version:%define dist .suse%suse_version}

Summary: CernVM File System X509 Authz Helper
Name: cvmfs-x509-helper
Version: 0.9
Release: 0.1.20160429103817.dwd.f2547a0ad01ae49bedbdbcd6c31ff93d864bfa2egit%{?dist}
Source0: https://ecsft.cern.ch/dist/cvmfs/%{name}-%{version}.tar.gz
Group: Applications/System
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?el5}
BuildRequires: buildsys-macros
%endif
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: globus-common-devel
BuildRequires: globus-gsi-callback-devel
BuildRequires: globus-gsi-cert-utils-devel
BuildRequires: globus-gsi-credential-devel
BuildRequires: globus-gsi-sysconfig-devel
%if 0%{?el5} || 0%{?el4}
BuildRequires: e2fsprogs-devel
%else
BuildRequires: libuuid-devel
%endif
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: voms-devel

Requires: cvmfs

%description
Authorization helper to verify X.509 proxy certificates and VOMS membership for
the CernVM-FS client.
See http://cernvm.cern.ch
Copyright (c) CERN

%prep
%setup -q

%build
%ifarch i386 i686
export CXXFLAGS="`echo %{optflags}|sed 's/march=i386/march=i686/'`"
export CFLAGS="`echo %{optflags}|sed 's/march=i386/march=i686/'`"
%endif

%if 0%{?suse_version}
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr .
%else
%cmake .
%endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
/usr/libexec/cvmfs/authz/cvmfs_x509_helper
%doc COPYING AUTHORS README ChangeLog

%changelog
* Fri Apr 29 2016 Dave Dykstra <dwd@fnal.gov> - 0.9-0.1.20160429103817.dwd.f2547a0ad01ae49bedbdbcd6c31ff93d864bfa2egit
- Build pre-release for OSG

* Fri Apr 22 2016 Jakob Blomer <jblomer@cern.ch> - 0.9-1
- Initial packaging
