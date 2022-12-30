Summary: Manage cvmfs replicas
Name: cvmfs-manage-replicas
Version: 1.5
# The release_prefix macro is used in the OBS prjconf, don't change its name
%define release_prefix 1.1
Release: %{release_prefix}%{?dist}
BuildArch: noarch
Group: Applications/System
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: https://github.com/cvmfs-contrib/%{name}/archive/%{name}-%{version}.tar.gz

Requires: python-anyjson

%description
Automates the addition and deletion of cvmfs stratum 1 replicas.

%prep
%setup -q

%install
mkdir -p $RPM_BUILD_ROOT/etc/cvmfs
install -p -m 644 manage-replicas.conf $RPM_BUILD_ROOT/etc/cvmfs
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -p -m 555 manage-replicas manage-replicas-log $RPM_BUILD_ROOT%{_sbindir}

%files
%config(noreplace) /etc/cvmfs/*
%{_sbindir}/*

%changelog
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.5-1.1
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Wed Mar 10 2021 Dave Dykstra <dwd@fnal.gov> - 1.5-1
- Fix typo in downloaded .pub filename; remove ending blank

* Tue Mar  9 2021 Dave Dykstra <dwd@fnal.gov> - 1.4-1
- Fix typo in key storage that caused all key files to be called 'outfile'
  in current working directory
- Add manage-replicas -k/--only-download-keys option

* Fri Mar  5 2021 Dave Dykstra <dwd@fnal.gov> - 1.3-1
- Support following symlinks on github download

* Thu Mar  4 2021 Dave Dykstra <dwd@fnal.gov> - 1.2-1
- Add keysource option to download domain keys from github.

* Mon May 13 2019 Dave Dykstra <dwd@fnal.gov> - 1.1-1
- Apply addcmd and remcmd sequentially, so different values can be used
  by different repositories.

* Wed Jun 20 2018 Dave Dykstra <dwd@fnal.gov> - 1.0-1
- Initial packaging
