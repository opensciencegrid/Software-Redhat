Name:      xrootd-rucioN2N-for-Xcache
Version:   1.2
Release:   3.4%{?dist}
Summary:   Xrootd Name-to-Name plugin for Disk Caching Proxy (Xcache) to utilize RUCIO metalink
Group:     System Environment/Libraries
License:   BSD 
Vendor:    Stanford University/SLAC
URL:       https://github.com/wyang007/rucioN2N-for-Xcache


Source0:   rucioN2N-for-Xcache-%{version}.tar.gz
Patch0: dont_link.patch 

%define xrootd_current_major 5
%define xrootd_next_major 6

BuildRequires: xrootd-server-devel >= 1:%{xrootd_current_major}.0.0-1
BuildRequires: xrootd-server-devel <  1:%{xrootd_next_major}.0.0-1
BuildRequires: xrootd-client-devel >= 1:%{xrootd_current_major}.0.0-1
BuildRequires: xrootd-client-devel <  1:%{xrootd_next_major}.0.0-1
BuildRequires: xrootd-devel >= 1:%{xrootd_current_major}.0.0-1
BuildRequires: xrootd-devel <  1:%{xrootd_next_major}.0.0-1
BuildRequires: libcurl-devel openssl-devel

Requires: xrootd >= 1:%{xrootd_current_major}.0.0-1
Requires: xrootd <  1:%{xrootd_next_major}.0.0-1
Requires: xrootd-client >= 1:%{xrootd_current_major}.0.0-1
Requires: xrootd-client <  1:%{xrootd_next_major}.0.0-1
Requires: libcurl openssl

%description
rucioN2N-for-Xcache is a xrootd plugin module that will identify multiple copies of a distributed file based on ATLAS RUCIO data management system. Please refers to project's twiki in github (https://github.com/wyang007/rucioN2N-for-Xcache) for more info.

%prep
#%setup -q -c -D -T %{name} 
%setup -q -c %{name} 
%patch0 -p1

%build
pwd
ls
cd rucioN2N-for-Xcache-%{version}
# Caution !!!
# if you build along with the xrootd rpms, uncommand the folloing line and comment out the 2 lines after it
make
#make XRD_INC=/afs/slac/package/xrootd/xrootd-4.6.0/xrootd/src XRD_LIB=/afs/slac/package/xrootd/xrootd-4.6.0/@sys/src
#mv XrdName2NameDCP4RUCIO.so XrdName2NameDCP4RUCIO-4.so

%install
mkdir -p %{buildroot}/usr/lib64
cp rucioN2N-for-Xcache-%{version}/XrdName2NameDCP4RUCIO.so %{buildroot}/usr/lib64/XrdName2NameDCP4RUCIO.so


%files
/usr/lib64/XrdName2NameDCP4RUCIO.so

%post -p /sbin/ldconfig

%changelog 
* Fri Sep 19 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 1.2-3.4
- Build for aarch64

* Thu Jul 09 2020 Diego Davila <didavila@ucsd.edu> - v1.2-3.3
- building against xrootd-5.0.0-1 (SOFTWARE-3923)
- updating xrootd_current_major and xrootd_next_major to 5 and 6 respectively

* Fri Jul 2 2020 Diego Davila <didavila@ucsd.edu> - v1.2-3.2
- Building against XRootD-5.0.0-rc5 

* Fri Jul 2 2020 Diego Davila <didavila@ucsd.edu> - v1.2-3.2
- Building against XRootD-5.0.0-rc5 

* Fri Apr 10 2020 Diego Davila <didavila@ucsd.edu> - v1.2-3.1
- Removing patch: link_to_lXrdPfc5.patch 
- Adding patch: dont_link.patch that removes the linking against libXrdFileCache-4 

* Wed Apr 1 2020 Diego Davila <didavila@ucsd.edu> - v1.2-2.1
- Building against Xrootd 5.0.0-rc2 (SOFTWARE-3923)

* Sat Feb 1 2020 Diego Davila <didavila@ucsd.edu> - v1.2-1
- Building against Xrootd 5.0 (SOFTWARE-3923)
- Adding patch: link_to_lXrdPfc5.patch 
- Bumping version 1.2-1

* Mon Aug 5 2019 Edgar Fajardo <emfajard@ucsd.edu> - v1.2-0
- Bumping version 1.2 (SOFTWARE-3784)

* Thu Jul 18 2019 Carl Edquist <edquist@cs.wisc.edu> - v1.1-4
- Rebuild against xrootd 4.10.0 (SOFTWARE-3697)

* Wed Apr 24 2019 Carl Edquist <edquist@cs.wisc.edu> - v1.1-3
- Rebuild against xrootd 4.9.1 (SOFTWARE-3678)

* Wed Feb 27 2019 Carl Edquist <edquist@cs.wisc.edu> - v1.1-2
- Rebuild against xrootd 4.9.0 (SOFTWARE-3485)

* Fri Sep 21 2018 Edgar Fajardo <emfajard@ucsd.edu> v1.1-1
- Releasing for SOFTWARE-3383
- Removed some noise from the spec only needed for rhel5

* Tue Oct 3 2017 Wei Yang <yangw.slac.stanford.edu> v1.0, require xrootd 4.7, generate -4.so
- Tue Oct 3 2017 initial version
