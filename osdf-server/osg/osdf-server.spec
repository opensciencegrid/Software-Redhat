Summary: Service files for Pelican-based OSDF daemons
Name: osdf-server
Version: 7.5.99
Release: 0.1%{?dist}
License: ASL 2.0
Url: https://github.com/PelicanPlatform/pelican
BuildArch: noarch
Source0: pelican.tar.gz


# subpackage: A helper macro to get rid of some of the code duplication. This
# expands to the various sections needed for each osdf subpackage. Add the -x
# flag for services that use XRootD (the cache and the origin).

%define subpackage(x) %{expand:
%%package -n %1
Summary: Service file and configuration for %1
Requires: pelican >= 7.5.0
Requires: /usr/bin/osdf
%{-x:Requires: xrootd-server >= 1:5.6.6}
%{-x:Requires: xrootd-scitokens}
%{-x:Requires: xrootd-voms}
%{-x:Requires: xrdcl-pelican}

%%description -n %1
Service file for %1

%%preun -n %1
%%systemd_preun %1.service

%%postun -n %1
systemctl daemon-reload

%%post -n %1
%%systemd_post %1.service
systemctl daemon-reload

%%files -n %1
/usr/lib/systemd/system/%{1}*.service
%%config(noreplace) /etc/pelican/%{1}*.yaml
%{-x:%%attr(-,xrootd,xrootd) /var/spool/osdf}
%%dir %%attr(0700,root,root) /var/log/pelican
%%config(noreplace) /etc/logrotate.d/pelican
}
# end of subpackage helper macro

%description
Service files for Pelican


%prep
%setup -n pelican


%build
exit 0


%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
mkdir -p $RPM_BUILD_ROOT/etc/pelican/
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d/
mkdir -p $RPM_BUILD_ROOT/var/spool/osdf
mkdir -p $RPM_BUILD_ROOT/var/log/pelican
install -m 0644 systemd/osdf-*.service $RPM_BUILD_ROOT/usr/lib/systemd/system/
install -m 0644 systemd/osdf-*.yaml $RPM_BUILD_ROOT/etc/pelican/
install -m 0644 systemd/pelican.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/pelican


%subpackage osdf-registry

%subpackage osdf-director

%subpackage -x osdf-origin

%subpackage -x osdf-cache




%changelog
* Mon Feb 19 2024 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.5.99-0.1
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
