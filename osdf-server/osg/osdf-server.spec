Summary: Service files for Pelican-based OSDF daemons
Name: osdf-server
Version: 25
Release: 1%{?dist}
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

Requires: pelican-server >= 7.19
Requires: xrootd-multiuser
%if 0%{?rhel} >= 9
Requires: xrootd-s3-http >= 0.4.1
%endif
Obsoletes: osdf-cache < 24
Obsoletes: osdf-director < 24
Obsoletes: osdf-origin < 24
Obsoletes: osdf-registry < 24
Provides: osdf-registry = %{version}
Provides: osdf-cache = %{version}
Provides: osdf-director = %{version}
Provides: osdf-origin = %{version}


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
## Compat symlinks. The targets come from the pelican-service RPM.
#ln -s           pelican-cache.yaml        $RPM_BUILD_ROOT/etc/pelican/osdf-cache.yaml
#ln -s           pelican-director.yaml     $RPM_BUILD_ROOT/etc/pelican/osdf-director.yaml
#ln -s           pelican-origin.yaml       $RPM_BUILD_ROOT/etc/pelican/osdf-origin.yaml
#ln -s           pelican-registry.yaml     $RPM_BUILD_ROOT/etc/pelican/osdf-registry.yaml
install -m 0644 %{SOURCE0}                $RPM_BUILD_ROOT/usr/share/pelican/config.d/
install -m 0644 %{SOURCE1}                $RPM_BUILD_ROOT/etc/pelican/config.d/
install -m 0644 %{SOURCE2}                $RPM_BUILD_ROOT/etc/pelican/config.d/
install -m 0644 %{SOURCE3}                $RPM_BUILD_ROOT/etc/pelican/config.d/


%files
%ghost /usr/lib/systemd/system/osdf-*.service
#%config /etc/pelican/osdf-*.yaml
/usr/share/pelican/config.d/10-osdf-defaults.yaml
%config(noreplace) /etc/pelican/config.d/15-osdf.yaml
%config(noreplace) /etc/pelican/config.d/20-cache.yaml
%config(noreplace) /etc/pelican/config.d/50-webui.yaml


%postun
systemctl daemon-reload


%post
systemctl daemon-reload


%triggerin -n %name -- xrootd-server
for svc in cache origin
do
    [ ! -d /run/systemd/system ] || systemctl condrestart pelican-${svc}.service
done


%triggerin -n %name -- pelican-server
for svc in cache director origin registry
do
    [ ! -d /run/systemd/system ] || systemctl condrestart pelican-${svc}.service
done


%define warning_file %{_localstatedir}/lib/rpm-state/%{name}-warning-file

# migrate: A helper macro to get rid of some of the code duplication. This
# expands to the various sections needed for each pelican services.

# Other macros will be expanded when subpackage is defined, unless
# escaped (by doubling up the '%').

%define migrate() %{expand:
%%define old_name %1
%%define new_name %%{lua:print((string.gsub("%1", "osdf", "pelican")))}

# This happens after %%post of this package but before the %%preun of the old
# package and the removal of its files.
%%triggerun -n %%name -- %%old_name < 25

# Do nothing if this is an uninstall, not an upgrade
[ "$1" = 1 ] || exit 0

# Do nothing if the system was not booted with systemd
[ -d /run/systemd/system ] || exit 0


old_config=/etc/pelican/%%{old_name}.yaml
old_log=/var/log/%%{old_name}.log
old_override_dir=/etc/systemd/system/%%{old_name}.service.d
old_service=%%{old_name}.service
old_sysconfig=/etc/sysconfig/%%{old_name}

new_config=/etc/pelican/%%{new_name}.yaml
new_log=/var/log/%%{new_name}.log
new_override_dir=/etc/systemd/system/%%{new_name}.service.d
new_service=%%{new_name}.service
new_sysconfig=/etc/sysconfig/%%{new_name}

# Only display this once:
if [ ! -e %{warning_file} ]
then
    cat > %{warning_file} <<__END__

****** WARNING ******

The packages 'osdf-cache', 'osdf-director', 'osdf-origin', and 'osdf-registry'
have been combined into 'osdf-server'.
In addition, the paths and service file names have been changed.

The following migration steps were performed -- if you are using
configuration management, you may need to update your configuration
to make sure the changes remain applied.

__END__
fi

addwarn () {
    echo -e "$*" >> %{warning_file}
}

maybe_move () {
    if [ -e "${1}" ]
    then
        if [ -e "${2}" ]
        then
            if mv -f "${2}" "${2}.rpmsave"
            then
                mv -f "${1}" "${2}"
                addwarn "*   '${1}' has been moved to '${2}'. '${2}' was backed up as '${2}.rpmsave'"
                addwarn "    You may need to merge changes from '${2}.rpmsave' into '${2}'"
            else
                addwarn "*   '${2}' could not be moved out of the way."
                addwarn "    You may need to merge changes from '${1}' into '${2}'"
            fi
        else
            addwarn "*   '${1}' has been moved to '${2}'."
        fi
    fi
}

maybe_move "${old_sysconfig}" "${new_sysconfig}"
maybe_move "${old_override_dir}" "${new_override_dir}"

was_active=$(systemctl is-active ${old_service})
was_enabled=$(systemctl is-enabled ${old_service})

if [ "${was_active}" = "active" ]
then
    if systemctl stop "${old_service}"
    then
        if systemctl start "${new_service}"
        then
            addwarn "*   '${old_service}' was stopped and '${new_service}' was started instead."
        else
            addwarn "*   '${old_service}' was stopped but '${new_service}' could not be started."
        fi
    else
        addwarn "*   '${old_service}' could not be stopped. You must replace it with '${new_service}'."
    fi
fi
if [ "${was_enabled}" = "enabled" ]
then
    if systemctl disable "${old_service}"
    then
        if systemctl enable "${new_service}"
        then
            addwarn "*   '${old_service}' was disabled and '${new_service}' was enabled instead."
        else
            addwarn "*   '${old_service}' was disabled but '${new_service}' could not be enabled."
        fi
    else
        addwarn "*   '${old_service}' could not be disabled. You must replace it with '${new_service}'."
    fi
fi
addwarn "*   '${old_service}' has been replaced by '${new_service}'"
addwarn "    Run 'systemctl status ${new_service}' to check that the service is in"
addwarn "    the desired state."
addwarn "*   The default log location has been moved from '${old_log}' to '${new_log}'"
addwarn ""
}
# end of migrate helper macro

%posttrans
if [ -e "%{warning_file}" ]
then
    cat >&2 "%{warning_file}"
    rm -f "%{warning_file}"
fi

%migrate osdf-cache
%migrate osdf-director
%migrate osdf-origin
%migrate osdf-registry


%changelog
* Tue Oct 07 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 25-1
- Replace with metapackage containing configuration for using the pelican-*.service files.
  Includes migration instructions.

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
