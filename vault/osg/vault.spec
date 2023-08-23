# Forked from vault.spec by John Boero - jboero@hashicorp.com

Name: vault
Version: 1.13.2
Release: 1%{?dist}
Summary: Vault is a tool for securely accessing secrets
License: MPL
Source0: https://github.com/opensciencegrid/%{name}-rpm/archive/v%{version}/%{name}-rpm-%{version}.tar.gz
# This is created by ./make-source-tarball
Source1: %{name}-src-%{version}.tar.gz

#BuildRequires: golang
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
URL: https://www.vaultproject.io/

# This is to avoid
#   *** ERROR: No build ID note found
%define debug_package %{nil}

%description
Vault secures, stores, and tightly controls access to tokens, passwords,
certificates, API keys, and other secrets in modern computing. Vault handles
leasing, key revocation, key rolling, and auditing. Through a unified API, users
can access an encrypted Key/Value store and network encryption-as-a-service, or
generate AWS IAM/STS credentials, SQL/NoSQL databases, X.509 certificates, SSH
credentials, and more.

%prep
%setup -q -n %{name}-rpm-%{version}
RPMDIR=`pwd`
%setup -q -T -b 1 -n %{name}-src-%{version}

%build
# starts out in %{name}-src-%{version} directory
export GOPATH="`pwd`/gopath"
export PATH=$PWD/go/bin:$GOPATH/bin:$PATH
export GOPROXY=file://$(go env GOMODCACHE)/cache/download
cd %{name}-%{version}
# this prevents it from complaining that ui assets are too old
touch http/web_ui/index.html
# this prevents the build from trying to use git to figure out the version
#  which fails because there's no git info
ln -s /bin/true $GOPATH/bin/git
make dev-ui

%install
# starts out in %{name}-src-%{version} directory
mkdir -p %{buildroot}%{_bindir}/
cp -p %{name}-%{version}/bin/%{name} %{buildroot}%{_bindir}/

cd ../%{name}-rpm-%{version}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}.d
cp -p vault.hcl %{buildroot}%{_sysconfdir}/%{name}.d

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

mkdir -p %{buildroot}/usr/lib/systemd/system/
cp -p vault.service %{buildroot}/usr/lib/systemd/system/

%clean
export GOPATH="`pwd`/gopath"
export PATH=$PWD/go/bin:$GOPATH/bin:$PATH
go clean -modcache
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-*-%{version}

%files
%verify(not caps) %{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.d/%{name}.hcl
%attr(0750,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
/usr/lib/systemd/system/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
    useradd -r -d %{_sharedstatedir}/%{name} -g %{name} \
    -s /sbin/nologin -c "Vault secret management tool" %{name}
exit 0

%post
/usr/bin/systemctl daemon-reload
%systemd_post %{name}.service
/sbin/setcap cap_ipc_lock=+ep %{_bindir}/%{name}

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Tue May  2 2023 Dave Dykstra <dwd@fnal.gov> 1.13.2-1
- Update to upstream 1.13.2

* Tue Apr 11 2023 Dave Dykstra <dwd@fnal.gov> 1.13.1-1
- Update to upstream 1.13.1

* Thu Nov 10 2022 Dave Dykstra <dwd@fnal.gov> 1.12.1-1
- Update to upstream 1.12.1

* Thu Jul 28 2022 Dave Dykstra <dwd@fnal.gov> 1.11.1-1
- Update to upstream 1.11.1, which includes a fix to avoid denial of
  service on HA installation.
- Remove $GOPATH/mod/*.* from the source tarball, leaving just
  $GOPATH/mod/cache/download.  That saves about 300M while still
  allowing offline builds.

* Wed Mar 23 2022 Dave Dykstra <dwd@fnal.gov> 1.10.0-1
- Update to upstream 1.10.0

* Tue Feb 15 2022 Dave Dykstra <dwd@fnal.gov> 1.9.3-1
- Update to upstream 1.9.3

* Wed Dec  1 2021 Dave Dykstra <dwd@fnal.gov> 1.9.0-1
- Update to upstream 1.9.0

* Thu Nov  4 2021 Dave Dykstra <dwd@fnal.gov> 1.8.4-1
- Update to upstream 1.8.4

* Fri Aug 27 2021 Dave Dykstra <dwd@fnal.gov> 1.8.2-1
- Update to upstream 1.8.2

* Thu Aug  5 2021 Dave Dykstra <dwd@fnal.gov> 1.8.1-1
- Update to upstream 1.8.1

* Wed Aug  4 2021 Dave Dykstra <dwd@fnal.gov> 1.8.0-1
- Update to upstream 1.8.0

* Thu Jun 17 2021 Dave Dykstra <dwd@fnal.gov> 1.7.3-1
- Update to upstream 1.7.3

* Thu May 20 2021 Dave Dykstra <dwd@fnal.gov> 1.7.2-1
- Update to upstream 1.7.2, a security release.

* Wed Apr 21 2021 Dave Dykstra <dwd@fnal.gov> 1.7.1-1
- Update to upstream 1.7.1.  Add patch for el7 to allow go 1.15.5.
- Stop disabling vault service on upgrade.

* Wed Mar 31 2021 Dave Dykstra <dwd@fnal.gov> 1.7.0-2
- Add %verify(not caps) to the vault binary to make rpm -V happy

* Thu Mar 25 2021 Dave Dykstra <dwd@fnal.gov> 1.7.0-1
- Update to upstream 1.7.0

* Wed Feb 17 2021 Dave Dykstra <dwd@fnal.gov> 1.6.2-1
- Initial build
