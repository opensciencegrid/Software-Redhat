%define name cvmfsreplica
%define version 0.9.2
%define unmangled_version 0.9.2
%define release 1

Summary: cvmfsreplica package
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Jose Caballero <jcaballero@bnl.gov>
Packager: Jose Caballero
Provides: cvmfsreplica
Url: https://github.com/jose-caballero/cvmfsreplica

%description
This package contains cvmfsreplica

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

sed -i '/\/etc\/cvmfsreplica\/.*\.conf/ s/^/%config(noreplace) /'  INSTALLED_FILES
sed -i '/\/etc\/logrotate\.d\/cvmfsreplica/ s/^/%config(noreplace) /'  INSTALLED_FILES
sed -i '/\/etc\/sysconfig\/cvmfsreplica/ s/^/%config(noreplace) /'  INSTALLED_FILES

mkdir -pm0755 $RPM_BUILD_ROOT%{_var}/log/cvmfsreplica


%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
