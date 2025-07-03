Summary: Service files for Pelican-based OSDF daemons
Name: osdf-server
Version: 7.17.1
Release: 2%{?dist}
License: ASL 2.0
Url: https://github.com/PelicanPlatform/pelican
BuildArch: noarch
#BuildRequires: pelican >= %%{version}
# ^^ does not work: the pelican RPM is missing the SIGMD5 header and cannot be used
#    in a BuildRequires - at least in Koji
Source0: 10-osdf-defaults.yaml
Source1: 15-osdf.yaml
Source2: 20-cache.yaml
Source3: 50-webui.yaml

Requires: pelican-server >= 7.17
Requires: xrootd-multiuser
%if 0%{?rhel} >= 9
Requires: xrootd-s3-http >= 0.4.1
%endif
## The following are already brought in by 'pelican-server':
# Requires: xrootd-server >= 1:5.8.2
# Requires: xrootd-scitokens
# Requires: xrootd-voms
Obsoletes: osdf-cache < 7.17
Obsoletes: osdf-director < 7.17
Obsoletes: osdf-origin < 7.17
Obsoletes: osdf-registry < 7.17
Provides: osdf-cache = %{version}
Provides: osdf-director = %{version}
Provides: osdf-origin = %{version}
Provides: osdf-registry = %{version}


%description
Service files for Pelican-based OSDF daemons


%prep
exit 0


%build
exit 0


%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
mkdir -p $RPM_BUILD_ROOT/usr/share/pelican/config.d/
mkdir -p $RPM_BUILD_ROOT/etc/pelican/config.d/
# ghost files (placeholders that we create in scriptlets)
# We do it that way because we need the old service file to exist so we can
# stop and disable it.
touch  $RPM_BUILD_ROOT/usr/lib/systemd/system/osdf-cache.service
touch  $RPM_BUILD_ROOT/usr/lib/systemd/system/osdf-director.service
touch  $RPM_BUILD_ROOT/usr/lib/systemd/system/osdf-origin.service
touch  $RPM_BUILD_ROOT/usr/lib/systemd/system/osdf-registry.service
# Compat symlinks. The targets come from the pelican-service RPM.
ln -s           pelican-cache.yaml        $RPM_BUILD_ROOT/etc/pelican/osdf-cache.yaml
ln -s           pelican-director.yaml     $RPM_BUILD_ROOT/etc/pelican/osdf-director.yaml
ln -s           pelican-origin.yaml       $RPM_BUILD_ROOT/etc/pelican/osdf-origin.yaml
ln -s           pelican-registry.yaml     $RPM_BUILD_ROOT/etc/pelican/osdf-registry.yaml
install -m 0644 %{SOURCE0}                $RPM_BUILD_ROOT/usr/share/pelican/config.d/
install -m 0644 %{SOURCE1}                $RPM_BUILD_ROOT/etc/pelican/config.d/
install -m 0644 %{SOURCE2}                $RPM_BUILD_ROOT/etc/pelican/config.d/
install -m 0644 %{SOURCE3}                $RPM_BUILD_ROOT/etc/pelican/config.d/


%files
%ghost /usr/lib/systemd/system/osdf-*.service
%config /etc/pelican/osdf-*.yaml
/usr/share/pelican/config.d/10-osdf-defaults.yaml
%config(noreplace) /etc/pelican/config.d/15-osdf.yaml
%config(noreplace) /etc/pelican/config.d/20-cache.yaml
%config(noreplace) /etc/pelican/config.d/50-webui.yaml


%postun
systemctl daemon-reload


%post
systemctl daemon-reload


%triggerin %name -- xrootd-server
for svc in cache origin
do
    [ ! -d /run/systemd/system ] || systemctl condrestart pelican-${svc}.service
done


%triggerin %name -- pelican-server
for svc in cache director origin registry
do
    [ ! -d /run/systemd/system ] || systemctl condrestart pelican-${svc}.service
done


%define warning_stamp %{_localstatedir}/lib/rpm-state/%{name}-warning-given

# migrate: A helper macro to get rid of some of the code duplication. This
# expands to the various sections needed for each pelican services. Add the -x
# flag for services that use XRootD (the cache and the origin).

# Other macros will be expanded when subpackage is defined, unless
# escaped (by doubling up the '%').

%define migrate %{expand:
%%define old_name %1
%%define new_name %%{lua:print((string.gsub("%1", "osdf", "pelican")))}

# This happens after %%post of this package but before the %%preun of the old
# package and the removal of its files.
%%triggerun -n %name -- %old_name < 7.17.1-2

# Do nothing if the system was not booted with systemd
[ -d /run/systemd/system ] || exit 0


old_service=%{old_name}.service
new_service=%{new_name}.service
old_log=/var/log/%{old_name}.log
new_log=/var/log/%{new_name}.log
old_config=/etc/pelican/%{old_name}.yaml
new_config=/etc/pelican/%{new_name}.yaml
old_sysconfig=/etc/sysconfig/%{old_name}
new_sysconfig=/etc/sysconfig/%{new_name}
old_override_dir=/etc/systemd/system/${old_service}.d
new_override_dir=/etc/systemd/system/${new_service}.d

# Only display this once:
if [ ! -e %warning_stamp ]
then
    cat >&2 <<__END__
****** WARNING ******

The package osdf-service replaced osdf-cache, osdf-director, osdf-origin, and osdf-registry.
Some paths have changed and migration steps may be necessary, especially if
you are using configuration management.  See below for details.

__END__
    touch %warning_stamp
fi

maybe_move_and_link () {
    if [ -e "$1" ]
    then
        if [ ! -e "$2" ]
        then
            mv "$1" "$2" && ln -s "$(basename "$2")" "$1"
            echo >&2 "$1 has been moved to $2 and a compatibility symlink has been created."
        else
            echo >&2 "$2 already exists - you will need to merge changes from $1."
        fi
    fi
}

maybe_move_and_link "$old_sysconfig" "$new_sysconfig"
maybe_move_and_link "$old_override_dir" "$new_override_dir"

# We need to stop/disable the old service and start/enable the new service
# _before_ the old service files have been replaced by symlinks, otherwise
# systemd will follow the symlink and the user won't be able to shut the old
# service off.

was_active=$(systemctl is-active $old_service)
was_enabled=$(systemctl is-enabled $old_service)

if [ "$was_active" = "active" ]
then
    echo >&2 "$old_service is active. Stopping it and starting $new_service instead."
    systemctl stop $old_service
    systemctl start $new_service
fi
if [ "$was_enabled" = "enabled" ]
then
    echo >&2 "$old_service is enabled. Disabling it and enabling $new_service instead."
    systemctl disable $old_service
    systemctl enable $new_service
fi
mv -f "$old_service" "$old_service.rpmsave"
ln -s "$new_service" "$old_service"
systemctl daemon-reload || :
echo >&2
echo >&2 "$old_service has been replaced by $new_service"
echo >&2 "A compatibility symlink has been created."
echo >&2 "Run \"systemctl status $new_service\" to check that the service is in the expected status."
echo >&2 "Future logs will be written to $new_log"
echo >&2
}
# end of migrate helper macro

%posttrans
rm -f %warning_stamp || :

%migrate osdf-cache
%migrate osdf-director
%migrate osdf-origin
%migrate osdf-registry


%changelog
* Tue Jul 01 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 7.17.1-2
- Upgrade to Pelican 7.17.1
- Replace osdf-*.service files with symlinks to the corresponding pelican-*.service files;
  replace /etc/pelican/osdf-*.yaml files with symlinks to the corresponding pelican-*.yaml files

* Wed Jun 18 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 7.16.6-1
- Upgrade to Pelican 7.16.6 (SOFTWARE-6152)
- Require xrootd-s3-http where available
- Drop explicit dependency on xrootd since it is already implied by pelican-server
- Instruct user to specify Cache.StorageLocation in cache config

* Fri Jun 06 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 7.16.5-1
- Upgrade to Pelican 7.16.5 (SOFTWARE-6152)

* Tue May 13 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 7.16.1-1
- Upgrade to Pelican 7.16.1 (SOFTWARE-6152)
- Require "pelican-server" for the cache and origin (SOFTWARE-6152)

* Tue Mar 25 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 7.11.7-2
- Do not attempt to restart systemd services if we were not booted with systemd

* Thu Dec 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.11.7-1
- Upgrade to Pelican 7.11.7 (SOFTWARE-6028)

* Tue Nov 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.11.1-1
- Upgrade to Pelican 7.11.1 and switch to config.d layout (SOFTWARE-6028)

* Wed Oct 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.10.7-1
- Upgrade to Pelican 7.10.7 (SOFTWARE-6004)

* Fri Aug 16 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.9.9-1
- Upgrade to Pelican 7.9.9
- Require pelican version >= service version
- Restart service if pelican or (for xrootd-requiring services) xrootd-server is upgraded
- Require xrootd >= 5.7.0
- Require xrootd-multiuser

* Fri Jul 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.9.3-1
- Upgrade to Pelican 7.9.3 (SOFTWARE-5847)
- Require xrootd >= 5.6.9-1.6 for various backports from 5.7.0

* Wed May 22 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.8.3-1
- Upgrade to Pelican 7.8.3 (SOFTWARE-5847)

* Thu May 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.7.6-1
- Upgrade to Pelican 7.7.6 (SOFTWARE-5847)
- Add logrotate.conf

* Fri Feb 16 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.5.6-1
- Upgrade to Pelican 7.5.6
- Require xrootd >= 5.6.6 for pelican:// URL support
- Put log files in /var/log/pelican

* Fri Feb 02 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.99-2.1
- Require xrdcl-pelican

* Thu Feb 01 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.99-2
- Prerelease build for 7.5.0; remove pelican-* subpackages and only build osdf-* subpackages

* Mon Jan 29 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-5
- Add /var/spool/pelican and /var/spool/osdf directories for the xrootd-based daemons

* Mon Jan 22 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-4
- Mark config files as %config(noreplace)

* Mon Jan 22 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-3
- Updates to yaml and service files
- Remove redundant *-origin-multiuser services
- Add osdf-cache-public and osdf-origin-public

* Fri Jan 05 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-2
- Remove xrootd requirements from registry and director
- Add pelican-osdf-compat requirement to osdf subpackages

* Wed Jan 03 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.4.0-1
- Add minimum version requirements:
  - xrootd must be 5.6.3 to avoid chunked upload incompatibility
  - pelican must be 7.3.3 to avoid authfile/scitokens.conf parsing issues
- Make origin and origin-multiuser services conflict

* Thu Dec 28 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.2.0-5
- Add missing xrootd-voms dependency
- osdf config improvements

* Fri Dec 22 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.2.0-3
- Add missing xrootd-scitokens dependency
- Flesh out cache and origin configs

* Mon Dec 04 2023 Mátyás Selmeci <matyas@cs.wisc.edu>
- Created


# vim:ft=spec
