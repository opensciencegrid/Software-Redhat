Name:      xrootd-rucioN2N-for-Xcache
Version:   1.1
Release:   2%{?dist}
Summary:   Xrootd Name-to-Name plugin for Disk Caching Proxy (Xcache) to utilize RUCIO metalink
Group:     System Environment/Libraries
License:   BSD 
Vendor:    Stanford University/SLAC
URL:       https://github.com/wyang007/rucioN2N-for-Xcache


Source0:   rucioN2N-for-Xcache-%{version}.tar.gz
BuildArch: x86_64
BuildRequires: xrootd-devel xrootd-server-devel xrootd-client-devel libcurl-devel openssl-devel

Requires: xrootd >= 4.8.1 xrootd-client libcurl openssl

%description
rucioN2N-for-Xcache is a xrootd plugin module that will identify multiple copies of a distributed file based on ATLAS RUCIO data management system. Please refers to project's twiki in github (https://github.com/wyang007/rucioN2N-for-Xcache) for more info.

%prep
#%setup -q -c -D -T %{name} 
%setup -q -c %{name} 
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
* Wed Feb 27 2019 Carl Edquist <edquist@cs.wisc.edu> - v1.1-2
- Rebuild against xrootd 4.9.0 (SOFTWARE-3485)

* Fri Sep 21 2018 Edgar Fajardo <emfajard@ucsd.edu> v1.1-1
- Releasing for SOFTWARE-3383
- Removed some noise from the spec only needed for rhel5

* Tue Oct 3 2017 Wei Yang <yangw.slac.stanford.edu> v1.0, require xrootd 4.7, generate -4.so
- Tue Oct 3 2017 initial version
