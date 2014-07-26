%define name panda-server-mysql
%define version 0.0.2
%define unmangled_version 0.0.2
%define release 0.7
%define panda_user  pansrv
%define panda_group pansrv

Summary: MySQL branch of the PanDA Server Package
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{unmangled_version}.tar.gz
Patch0: setup_mysql.patch
Patch1: templates.patch
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Panda Team <hn-atlas-panda-pathena@cern.ch>
Packager: Panda Team <hn-atlas-panda-pathena@cern.ch>
Provides: panda-server-mysql
Requires: python panda-common
Requires(pre): /usr/sbin/useradd
Url: https://twiki.cern.ch/twiki/bin/view/PanDA/PanDA

%description
This package contains PanDA Server Components

%prep
%setup -n %{name}-%{unmangled_version}
%patch0 -p1
#rename .rpmnew. . templates/*.rpmnew.template
#rename .sh.     . templates/*.sh.exe.template
%patch1 -p1

%build
python setup_mysql.py build

%install
python setup_mysql.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -pm 0755 $RPM_BUILD_ROOT/var/log/panda/wsgisocks
mkdir -pm 0755 $RPM_BUILD_ROOT/var/cache/pandaserver

%pre
getent group %{panda_group} >/dev/null || groupadd -r %{panda_group} || :
getent passwd %{panda_user} >/dev/null || \
  useradd -c "PanDA Server" -g %{panda_group} -r %{panda_user} || :

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%config(noreplace) /etc/panda/panda_server.cfg
%config(noreplace) /etc/panda/panda_server-httpd.conf
%config(noreplace) /etc/panda/panda_server-httpd-FastCGI.conf
%config(noreplace) /etc/sysconfig/panda_server
%dir %attr(-,%{panda_user},%{panda_group}) /var/log/panda
%dir %attr(-,%{panda_user},%{panda_group}) /var/log/panda/wsgisocks
%dir %attr(-,%{panda_user},%{panda_group}) /var/cache/pandaserver

