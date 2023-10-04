# The name of your package
Name: cvmfs-gateway

# A short summary of your package
Summary: CernVM-FS Repository Gateway

# The version of your package
Version: 1.2.0

# The release number of your package
Release: 1.2%{?dist}

# Any license you wish to list
License: BSD-3-Clause

# What group this RPM would typically reside in
Group: Applications/System

# Who packaged this RPM
Packager: Radu Popescu <radu.popescu@cern.ch>

# The build architecture of this RPM (noarch/x86_64/i386/etc)
Buildarch: x86_64

# You generally should not need to mess with this setting
Buildroot: %{_tmppath}/%{name}

# Change this extension to change the compression level in your RPM
#  tar / tar.gz / tar.bz2
Source0: %{name}.tar

# If you are having trouble building a package and need to disable
#  automatic dependency/provides checking, uncomment this:
# AutoReqProv: no

# If this package has prerequisites, uncomment this line and
#  list them here - examples are already listed
Requires: cvmfs-server >= 2.5.2

# cvmfs-gateway >= 1.1.0 includes the notification system server,
# obsoleting the cvmfs-notify package
Obsoletes: cvmfs-notify

BuildRequires: rsync

# A more verbose description of your package
%description
CernVM-FS Repository Gateway

# You probably do not need to change this
%define debug_package %{nil}


%prep
%setup -q -c

%build

%install
rsync -a . %{buildroot}/

%clean
rm -rf %{buildroot}

%pre

if [ x"$(pidof systemd >/dev/null && echo yes || echo no)" = "xyes" ]; then
    if [ "x$(systemctl list-unit-files | grep cvmfs-gateway)" != "x" ]; then
        if $(systemctl is-active --quiet cvmfs-gateway); then
            systemctl stop cvmfs-gateway
        fi
        if $(systemctl is-active --quiet cvmfs-gateway@*); then
            systemctl stop cvmfs-gateway@*
        fi
    fi
else
    if [ -x /usr/libexec/cvmfs-gateway/run_cvmfs_gateway.sh ]; then
        /usr/libexec/cvmfs-gateway/run_cvmfs_gateway.sh stop || true
    fi
fi

%post

if [ x"$(pidof systemd >/dev/null && echo yes || echo no)" = "xyes" ]; then
    systemctl daemon-reload
fi

%preun

if [ x"$(pidof systemd >/dev/null && echo yes || echo no)" = "xyes" ]; then
    if [ "x$(systemctl list-unit-files | grep cvmfs-gateway)" != "x" ]; then
        if $(systemctl is-active --quiet cvmfs-gateway); then
            systemctl stop cvmfs-gateway
        fi
        if $(systemctl is-active --quiet cvmfs-gateway@*); then
            systemctl stop cvmfs-gateway@*
        fi
    fi
else
    if [ -x /usr/libexec/cvmfs-gateway/run_cvmfs_gateway.sh ]; then
        /usr/libexec/cvmfs-gateway/run_cvmfs_gateway.sh stop || true
    fi
fi

%postun

if [ x"$(pidof systemd >/dev/null && echo yes || echo no)" = "xyes" ]; then
    systemctl daemon-reload
fi

#%trigger

#%triggerin

#%triggerun

%changelog
* Wed Oct 04 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2.0-1.2
- Bump to rebuild

* Mon Dec 12 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.2.0-1.1
- Bump to rebuild (SOFTWARE-5384)

* Tue Feb 09 2021 Anonymous <None>
- Initial version.

%files
%attr(0755, root, root) %dir "/etc/cvmfs/gateway"
%attr(0644, root, root) %config(noreplace) "/etc/cvmfs/gateway/repo.json"
%attr(0644, root, root) %config(noreplace) "/etc/cvmfs/gateway/user.json"
%attr(0644, root, root) %config(noreplace) "/etc/systemd/system/cvmfs-gateway.service"
%attr(0644, root, root) %config(noreplace) "/etc/systemd/system/cvmfs-gateway@.service"
%attr(0755, root, root) "/usr/bin/cvmfs_gateway"
%attr(0755, root, root) %dir "/usr/libexec/cvmfs-gateway"
%attr(0755, root, root) %dir "/usr/libexec/cvmfs-gateway/scripts"
%attr(0755, root, root) "/usr/libexec/cvmfs-gateway/scripts/run_cvmfs_gateway.sh"
%attr(0755, root, root) %dir "/var/lib/cvmfs-gateway"

