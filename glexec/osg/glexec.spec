Summary: User identity switching tool based on grid credentials
Name: glexec
Version: 0.8.10
Release: 2%{?dist}
License: ASL 2.0
Group: Applications/System
URL: http://www.nikhef.nl/pub/projects/grid/gridwiki/index.php/Site_Access_Control
Source0: http://software.nikhef.nl/security/%{name}/%{name}-%{version}.tar.gz
Source1: glexec.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: lcmaps-interface
Requires: logrotate

# Since liblcmaps.so is dlopen'd we need this explicit requirement.
Requires: lcmaps

%description
gLExec is a program that acts as a light-weight 'gatekeeper'. it takes
Grid credentials as input, and takes the local site policy into
account to authenticate and authorize the credentials. It will then
switch to a new execution sandbox and execute the given command as the
switched identity. gLExec is also capable of functioning as a
light-weight control point which offers a binary yes/no result in
logging-only mode.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# OSG default config
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/glexec.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE 
%config(noreplace) /etc/logrotate.d/glexec
%config(noreplace) /etc/glexec.conf
%config(noreplace) /etc/lcmaps/lcmaps-glexec.db
%{_datadir}/man/man5/glexec.conf.5*
%{_datadir}/man/man1/glexec.1*
%attr(6755, root, root) /usr/sbin/glexec

%changelog
* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.8.10-2
- Use OSG default config.

* Wed Jun 29 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 0.8.10-1
- Remove Vendor tag

* Mon Mar 14 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.4-2a
- removed lcas.db
- updated sources

* Fri Mar 11 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.4-1
- new version including lcas/lcmaps db files

* Tue Mar  8 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.2-3
- setup config fiiles noreplace

* Fri Mar  4 2011 Dennis van Dok <dennisvd@nikhef.nl> 0.8.2-2
- fixed configuration files and license string

* Fri Feb 25 2011 Dennis van Dok <dennisvd@nikhef.nl> 
- Initial build.
