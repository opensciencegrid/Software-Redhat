Name:           koji-plugin-sign
Version:        1.4.0
Release:        1%{?dist}
Summary:        GPG signing plugin for koji-hub

Group:          Applications/System
License:        TODO
URL:            https://fedorahosted.org/koji/ticket/203
Source0:        sign.conf
Source1:        sign.py
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
install -D $RPM_SOURCE_DIR/sign.py -m 0755 $RPM_BUILD_ROOT/etc/koji-hub/plugins/sign.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %attr(0600,apache,apache) /etc/koji-hub/plugins/sign.conf
%attr(0755,root,root) /etc/koji-hub/plugins/sign.py*



%changelog
* Fri Aug 5 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.4.0-1
- Created

