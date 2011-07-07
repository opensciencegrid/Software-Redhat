Summary: Network Diagnostic Tool
Name: ndt
Version: 3.6.4
Release: 1%{?dist}
License: TODO
Group: Applications/Grid
Source0: %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Packager: VDT <vdt-support@opensciencegrid.org>
BuildRequires: zlib-devel
#Requires:           initscripts
#Requires(post):     chkconfig, /sbin/ldconfig
#Requires(preun):    chkconfig
#Requires(postun):   /sbin/ldconfig
AutoReq: yes
AutoProv: yes

%description




%prep
%setup




%build
# Go through build steps only if we don't have a prebuilt tarball
%configure
pushd src
%__make web100clt
popd






%install
[[ -n "%buildroot" && "%buildroot" != / ]] && rm -rf %buildroot
mkdir -p %buildroot/%_bindir
mkdir -p %buildroot/%_mandir
mkdir -p %buildroot/%_docdir
cp src/web100clt %buildroot/%_bindir
cp doc/web100clt.man %buildroot/%_mandir





%clean
[[ -n "%buildroot" && "%buildroot" != / ]] && rm -rf %buildroot



%define _unpackaged_files_terminate_build 1
%files
%{_bindir}/web100clt
%{_mandir}/web100clt.man



%changelog
* Fri Jun 17 2011 matyas@cs.wisc.edu - 3.6.4-1
- Initial build


# vim:ft=spec

