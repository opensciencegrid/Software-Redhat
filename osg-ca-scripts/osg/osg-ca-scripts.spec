Name:      osg-ca-scripts
Version:   1.1.5
Release:   1%{?dist}
Summary:   CA Certificate helper scripts

Group:     System Environment/Base
License:   Apache 2.0
URL:       http://vdt.cs.wisc.edu/releases/2.0.0/certificate_authorities.html

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: /usr/bin/openssl
Requires: logrotate

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

# Install perl module
install -d $RPM_BUILD_ROOT/%{perl_vendorlib}
install -m 0644 lib/OSGCerts.pm $RPM_BUILD_ROOT/%{perl_vendorlib}

# Install configuration
install -d $RPM_BUILD_ROOT%{_sysconfdir}/osg/
install -m 0644 etc/osg-update-certs.conf $RPM_BUILD_ROOT%{_sysconfdir}/osg/

# Install cron job
install -d $RPM_BUILD_ROOT/%{_initrddir}/
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/
install -m 755 init.d/osg-update-certs-cron $RPM_BUILD_ROOT/%{_initrddir}/
install -m 644 cron.d/osg-update-certs $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/

# Log rotation
install -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 logrotate/osg-ca-scripts.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/osg-ca-scripts

# Create state directory
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/osg
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/osg-ca-certs

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

%{_bindir}/osg-ca-certs-status
%{_sbindir}/osg-ca-manage
%{_sbindir}/osg-update-certs
%{_libexecdir}/osg-setup-ca-certificates
%{perl_vendorlib}/OSGCerts.pm
%{_initrddir}/osg-update-certs-cron
%{_sysconfdir}/cron.d/osg-update-certs

%config(noreplace) %{_sysconfdir}/osg/osg-update-certs.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/osg-ca-scripts

%dir %attr(0755,root,root) %{_localstatedir}/lib/osg-ca-certs

%changelog
* Wed Feb 12 2014 Brian Lin <blin@cs.wisc.edu> 1.1.5-1
- Add --nosymlink option to prevent symlinks being made when specifying a location

* Thu Jul 25 2013 Brian Lin <blin@cs.wisc.edu> 1.1.4-1
- Fix cron.d entry to output to /dev/null

* Mon May 20 2013 Brian Lin <blin@cs.wisc.edu> 1.1.3-1
- Fix --location bug

* Fri May 10 2013 Brian Lin <blin@cs.wisc.edu> 1.1.2-1
- Fix log-rotation for rpm installs

* Fri Mar 22 2013 Brian Lin <blin@cs.wisc.edu> 1.1.1-1
- Improve default locations for `osg-ca-manage setupca`
- Bug fixes

* Tue Mar 19 2013 Brian Lin <blin@cs.wisc.edu> 1.1.0-1
- Corrected build errors of previous version

* Mon Mar 18 2013 Brian Lin <blin@cs.wisc.edu> 1.0.0-2
- Overhauled scripts for use with tarball installs

* Fri Feb 22 2013 Tim Cartwright <cat@cs.wisc.edu> 1.0.0-1
- Overhauled Fetch CRL code to work with v2/v3 and RPM names
- Updated Makefile to fit OSG conventions (except install target)

* Wed Nov 09 2011 Anand Padmanabhan <apadmana@uiuc.edu> 0.0.9-2
-  Added a line to create the directory /var/lib/osg-ca-certs
 
* Wed Sep 14 2011 Anand Padmanabhan <apadmana@uiuc.edu> 0.0.8-1
-  Changed the names of the url shortcuts in osg-ca-manage to match with RPM names.
 
* Wed Sep 07 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.0.7-1
- Added logrotation

* Mon Aug 22 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.0.4-1
- Bug fixes

* Mon Aug 22 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.0.2-1
- Added cron job

* Thu Aug 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.1-2
- Fix up RPM metadata to be compatible with other CA packages.

* Wed Aug 17 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 0.0.1-1
- Created an initial osg-ca-scripts RPM
