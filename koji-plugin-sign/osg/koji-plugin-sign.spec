Name:           koji-plugin-sign
Version:        1.4.0
Release:        7%{?dist}
Summary:        GPG signing plugin for koji-hub

Group:          Applications/System
License:        Unknown
URL:            https://fedorahosted.org/koji/ticket/203
Source0:        sign.conf
Source1:        sign.py
Patch0:         allow_disable.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       koji-hub, pexpect

%description
GPG signing plugin for koji-hub

%prep
cp $RPM_SOURCE_DIR/sign.conf .
cp $RPM_SOURCE_DIR/sign.py .
%patch0 -p1
exit 0

%build
exit 0


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
install -D sign.conf -m 0600 $RPM_BUILD_ROOT/etc/koji-hub/plugins/sign.conf
install -D sign.py -m 0755 $RPM_BUILD_ROOT/usr/lib/koji-hub-plugins/sign.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %attr(0600,apache,apache) /etc/koji-hub/plugins/sign.conf
%attr(0755,root,root) /usr/lib/koji-hub-plugins/sign.py*



%changelog
* Thu Oct 17 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-7
- Rebuild with dist tag

* Thu Sep 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-6
- fixed disabling not working with previous patch

* Thu Sep 22 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-5
- added patch to allow enabling/disabling signing for a tag (or by default)

* Thu Sep 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.4.0-4
- added pexpect dependency

* Thu Sep 15 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-3
- Set package to be noarch
- sign.py moved to /usr/lib/koji-hub-plugins to match what the package koji-hub-plugins is doing

* Fri Aug 5 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-1
- Created

