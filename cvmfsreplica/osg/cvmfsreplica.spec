%define name cvmfsreplica
%define version 0.9.3
%define unmangled_version 0.9.3
%define release 2

Summary: cvmfsreplica package
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
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


%if 0%{?rhel} >= 7 || 0%{?centos} == 7
%define systemd 1
Requires(post): systemd
Requires(preun): systemd
%else
%define systemd 0
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%endif

# _unitdir, _tmpfilesdir not defined on el6 build hosts
%{!?_unitdir: %global _unitdir %{_prefix}/lib/systemd/system}
%{!?_tmpfilesdir: %global _tmpfilesdir %{_prefix}/lib/tmpfiles.d}


%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

sed -i '/\/etc\/cvmfsreplica\/.*\.conf/ s/^/%config(noreplace) /'  INSTALLED_FILES
sed -i '/\/etc\/logrotate\.d\/cvmfsreplica/ s/^/%config(noreplace) /'  INSTALLED_FILES
sed -i '/\/etc\/sysconfig\/cvmfsreplica/ s/^/%config(noreplace) /'  INSTALLED_FILES

###################################################################
# to deal with the init scripts depending on the platform
#
# for this to work, the setup.py file can not include them
# in rpm_data_files
#
# NOTE: this may be a temporary solution
#
###################################################################
#%if 0%{?redhat} == 7 || 0%{?centos} == 7
#install -m 0644 etc/cvmfsreplica.service /usr/lib/systemd/system/
#ln -s /usr/lib/systemd/system/cvmfsreplica.service /etc/systemd/system/multi-user.target.wants/cvmfsreplica.service
#install -m 0755 etc/cvmfsreplica.start /usr/bin/cvmfsreplica.start
#install -m 0755 etc/cvmfsreplica.stop /usr/bin/cvmfsreplica.stop
#%else
#install -m 0644 etc/cvmfsreplica /etc/init.d/
#%endif


%if %systemd
# Copy systemd files into place
install -d $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 etc/cvmfsreplica.service $RPM_BUILD_ROOT%{_unitdir}/
install -m 0755 etc/cvmfsreplica.start $RPM_BUILD_ROOT%{_bindir}/cvmfsreplica.start
install -m 0755 etc/cvmfsreplica.stop $RPM_BUILD_ROOT%{_bindir}/cvmfsreplica.stop
%else
# Copy init script into place
install -d $RPM_BUILD_ROOT%{_initrddir}
install -m 0755 etc/cvmfsreplica $RPM_BUILD_ROOT%{_initrddir}/cvmfsreplica
%endif

###################################################################





mkdir -pm0755 $RPM_BUILD_ROOT%{_var}/log/cvmfsreplica


%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%if %systemd
%{_unitdir}/cvmfsreplica.service
%else
%{_initrddir}/cvmfsreplica
%endif
%{_bindir}/cvmfsreplica.start
%{_bindir}/cvmfsreplica.stop



%post
%if %systemd
systemctl enable cvmfsreplica
%else
/sbin/chkconfig --add cvmfsreplica
%endif

