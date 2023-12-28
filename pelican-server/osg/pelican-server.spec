Summary: Service files for Pelican
Name: pelican-server
Version: 7.2.0
Release: 4%{?dist}
License: ASL 2.0
Url: https://github.com/PelicanPlatform/pelican
BuildArch: noarch
Source0: make-services.sh

%define services pelican-registry pelican-director pelican-origin pelican-cache osdf-registry osdf-director osdf-origin osdf-cache

%define subpackage() %{expand:
%%package -n %1
Summary: Service file for %1
Requires: xrootd-server
Requires: xrootd-scitokens
Requires: xrootd-voms
Requires: pelican

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
/etc/pelican/%1.yaml
}

%description
Service files for Pelican



%build
bash %{SOURCE0} %services


%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/
mkdir -p $RPM_BUILD_ROOT/etc/pelican/
install -m 0644 *.service $RPM_BUILD_ROOT/usr/lib/systemd/system/
install -m 0644 *.yaml $RPM_BUILD_ROOT/etc/pelican/


%subpackage pelican-registry
%subpackage pelican-director
%subpackage pelican-origin
%subpackage pelican-cache
%subpackage osdf-registry
%subpackage osdf-director
%subpackage osdf-origin
%subpackage osdf-cache






%changelog
* Thu Dec 28 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.2.0-4
- Add missing xrootd-voms dependency

* Fri Dec 22 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 7.2.0-3
- Add missing xrootd-scitokens dependency
- Flesh out cache and origin configs

* Mon Dec 04 2023 Mátyás Selmeci <matyas@cs.wisc.edu>
- Created


# vim:ft=spec
