Name:           koji-plugin-sign
Version:        1.4.0
Release:        3%{?dist}
Summary:        GPG signing plugin for koji-hub

Group:          Applications/System
License:        Unknown
URL:            https://fedorahosted.org/koji/ticket/203
Source0:        sign.conf
Source1:        sign.py
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       koji-hub

%description
GPG signing plugin for koji-hub

%prep
exit 0

%build
exit 0


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
install -D $RPM_SOURCE_DIR/sign.conf -m 0600 $RPM_BUILD_ROOT/etc/koji-hub/plugins/sign.conf
install -D $RPM_SOURCE_DIR/sign.py -m 0755 $RPM_BUILD_ROOT/usr/lib/koji-hub-plugins/sign.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %attr(0600,apache,apache) /etc/koji-hub/plugins/sign.conf
%attr(0755,root,root) /usr/lib/koji-hub-plugins/sign.py*



%changelog
* Thu Sep 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-3
- Set package to be noarch
- sign.py moved to /usr/lib/koji-hub-plugins to match what the package koji-hub-plugins is doing

* Fri Aug 5 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-1
- Created

