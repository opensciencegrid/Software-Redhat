
Name:      osg-ca-scripts
Version:   0.0.1
Release:   2%{?dist}
Summary:   CA Certificate helper scripts

Group:     System Environment/Base
License:   Apache 2.0
URL:       http://vdt.cs.wisc.edu/releases/2.0.0/certificate_authorities.html

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: /usr/bin/openssl

Provides: grid-certificates = 6
Conflicts: osg-ca-certs
Conflicts: osg-ca-certs-experimental
Conflicts: igtf-ca-certs
Conflicts: igtf-ca-certs-experimental

%description
%{summary}


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Install executables
install -d $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT%{_sbindir}/
install -d $RPM_BUILD_ROOT%{_libexecdir}/
install -m 0755 bin/osg-ca-certs-status $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 sbin/osg-ca-manage $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 sbin/osg-update-certs $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 libexec/osg-setup-ca-certificates $RPM_BUILD_ROOT%{_libexecdir}/

# Install configuration
install -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 0644 etc/osg-update-certs.conf $RPM_BUILD_ROOT%{_sysconfdir}/

install -d $RPM_BUILD_ROOT/%{perl_vendorlib}
install -m 0644 lib/OSGCerts.pm $RPM_BUILD_ROOT/%{perl_vendorlib}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%{_bindir}/osg-ca-certs-status
%{_sbindir}/osg-ca-manage
%{_sbindir}/osg-update-certs
%{_libexecdir}/osg-setup-ca-certificates
%{perl_vendorlib}/OSGCerts.pm

%config(noreplace) %{_sysconfdir}/osg-update-certs.conf


%changelog
* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.1-2
- Fix up RPM metadata to be compatible with other CA packages.

* Wed Aug 17 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Created an initial osg-ca-scripts RPM
