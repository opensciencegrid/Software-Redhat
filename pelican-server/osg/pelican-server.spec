Summary: Service files for Pelican
Name: pelican-server
Version: 7.4.0
Release: 4%{?dist}
License: ASL 2.0
Url: https://github.com/PelicanPlatform/pelican
BuildArch: noarch
Source0: pelican.tar.gz

%define requires_xrootd() %{expand:
Requires: xrootd-server >= 1:5.6.3
Requires: xrootd-scitokens
Requires: xrootd-voms
}

%define subpackage_common() %{expand:
Summary: Service file for %1
Requires: pelican >= 7.4.0

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
}

%description
Service files for Pelican


%prep
%setup -n pelican


%build
exit 0


%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
mkdir -p $RPM_BUILD_ROOT/etc/pelican/
install -m 0644 systemd/*.service $RPM_BUILD_ROOT/usr/lib/systemd/system/
install -m 0644 systemd/*.yaml $RPM_BUILD_ROOT/etc/pelican/


%package -n pelican-registry
%subpackage_common pelican-registry

%package -n pelican-director
%subpackage_common pelican-director

%package -n pelican-origin
%requires_xrootd
%subpackage_common pelican-origin

%package -n pelican-cache
%requires_xrootd
%subpackage_common pelican-cache

%package -n osdf-registry
Requires: pelican-osdf-compat
%subpackage_common osdf-registry

%package -n osdf-director
Requires: pelican-osdf-compat
%subpackage_common osdf-director

%package -n osdf-origin
%requires_xrootd
Requires: pelican-osdf-compat
%subpackage_common osdf-origin

%package -n osdf-cache
%requires_xrootd
Requires: pelican-osdf-compat
%subpackage_common osdf-cache




%changelog
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
