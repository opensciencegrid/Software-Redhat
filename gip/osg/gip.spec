Summary: Generic Information Provider
Name: gip
Version: 1.3.10
Release: 4%{?dist}
License: TODO
Group: Applications/Grid
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: globus-proxy-utils 
Source0: %{name}-%{version}.tgz
Patch0: 1382-info-services-rename.patch
Patch1: 1315-gip-user.patch

%description

The Open Science Grid (OSG) Generic Information Provider (GIP) is a core part of the OSG Information Infrastructure.
The GIP is a grid information service that aggregates static and dynamic resource information for use with 
LDAP-based information systems.  It produces information based on the GLUE schema.  This information
then can be sent via external services to information collection servers such as ReSS and BDII.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf %{buildroot}

# Set the Python version
%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

install -d %{buildroot}%{python_sitelib}
cp -a gip/lib/python/* %{buildroot}%{python_sitelib}

install -d %{buildroot}%{_bindir}
mkdir gip/plugins
install -d %{buildroot}%{_libexecdir}/%{name}/plugins
install -d %{buildroot}%{_libexecdir}/%{name}/providers
install -d %{buildroot}%{_libexecdir}/%{name}

install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}/ldif.d
install -d %{buildroot}/var/cache/%{name}

install -m 644 gip/etc/logging.conf %{buildroot}%{_sysconfdir}/%{name}
cp -a gip/plugins %{buildroot}%{_libexecdir}/%{name}
cp -a gip/providers %{buildroot}%{_libexecdir}/%{name}
cp -a gip/templates %{buildroot}%{_datadir}/%{name}
rm %{buildroot}%{_datadir}/%{name}/templates/Questions.py

cp gip/libexec/* %{buildroot}%{_libexecdir}/%{name}
# If we don't remove the .py extension, RPM will automatically compile these.
for i in `ls %{buildroot}%{_libexecdir}/%{name}/providers/*.py`; do
    without_py=`echo $i | sed 's|.py||'`
    mv $i $without_py
done
# We want to be able to import osg_info_wrapper
mv %{buildroot}%{_libexecdir}/%{name}/osg_info_wrapper.py %{buildroot}%{python_sitelib}/
# Remove deprecated cruft:
rm -f %{buildroot}%{_libexecdir}/%{name}/*.py || :
rm -f %{buildroot}%{_libexecdir}/%{name}/*.pyc || :

cp gip/bin/* %{buildroot}%{_bindir}
rm %{buildroot}%{_bindir}/gip-validator.py
rm %{buildroot}%{_bindir}/TestRunner.py
rm %{buildroot}%{_bindir}/run_gip.sh.se_only.example

#install -d %{buildroot}%{_libexecdir}/%{name}/plugins
#install -d %{buildroot}%{_libexecdir}/%{name}/providers

mkdir -p $RPM_BUILD_ROOT/var/log/%{name}

touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.conf
touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/add-attributes.conf
touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/alter-attributes.conf
touch $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/remove-attributes.conf

%pre
getent group gip >/dev/null || groupadd -r gip || :
getent passwd gip >/dev/null || useradd -r gip -g gip -s /sbin/nologin -c "GIP" 2>/dev/null || :

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libexecdir}/%{name}/osg-info-wrapper
%attr(755,root,root) %{_libexecdir}/%{name}/providers/*
%dir %{_libexecdir}/%{name}/plugins
%dir %{_libexecdir}/%{name}/providers
%{python_sitelib}/*
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/gip.conf
%config(noreplace) %{_sysconfdir}/%{name}/alter-attributes.conf
%config(noreplace) %{_sysconfdir}/%{name}/add-attributes.conf
%config(noreplace) %{_sysconfdir}/%{name}/remove-attributes.conf
%config(noreplace) %{_sysconfdir}/%{name}/logging.conf
%config(noreplace) %{_sysconfdir}/%{name}/ldif.d
%attr(-, gip, gip) /var/log/%{name}
%attr(-, gip, gip) /var/cache/%{name}

%clean
rm -rf %buildroot

%changelog
* Wed Feb 19 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.3.10-4
- Change the default GIP user from tomcat to gip. Add a gip user if one doesn't
  already exist. (SOFTWARE-1315)

* Tue Feb 04 2014 Matyas Selmeci <matyas@cs.wisc.edu> 1.3.10-3
- Add patch to read Infoservices section from OSG config file if present (SOFTWARE-1382)

* Wed Oct 16 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.3.10-2
- Remove glite-ce-monitor dependency (SOFTWARE-1231)

* Wed May 22 2013 Burt Holzman <burt@fnal.gov> - 1.3.10-1
- Updated to GIP 1.3.10

* Mon May 20 2013 Burt Holzman <burt@fnal.gov> - 1.3.9-1
- Update to GIP 1.3.9

* Tue Jun 19 2012 Burt Holzman <burt@fnal.gov> - 1.3.8-2
- Add globus-proxy-utils dependency (for grid-proxy-init)

* Thu Jun 12 2012 Burt Holzman <burt@fnal.gov> - 1.3.8-1
- Update to GIP 1.3.8

* Thu May 17 2012 Burt Holzman <burt@fnal.gov> - 1.3.7-2
- Add glite-ce-monitor dependency
- Change default ownership of /var/log/gip and /var/cache/gip to tomcat

* Thu Apr 19 2012 Burt Holzman <burt@fnal.gov> - 1.3.7-1
- Update to GIP 1.3.7

* Thu Mar 29 2012 Burt Holzman <burt@fnal.gov> - 1.3.6-1
- Update to GIP 1.3.6

* Mon Mar 12 2012 Burt Holzman <burt@fnal.gov> - 1.3.5rc1-2
- Update to GIP 1.3.5

* Wed Feb 29 2012 Burt Holzman <burt@fnal.gov> - 1.3.5rc1-1
- Update to GIP 1.3.5rc1
- Check for duplicate key/values (ignoring case) -- RFC4512 forbids it
- Ignore comment lines in read_ldap
- Remove GlueLocation stanzas for software publication
- Remove configure_gip placeholder

* Tue Jan 17 2012 Anthony Tiradani <tiradani@fnal.gov> - 1.3.4
- Update to GIP 1.3.4
- Changed ownership of directories to root since osg-configure will set proper ownership and root is guaranteed to exist

* Fri Dec 23 2011 Anthony Tiradani <tiradani@fnal.gov> - 1.3.3rc1-3
- Changed the ownership attributes from tomcat to daemon to eliminate rpm errors

* Thu Nov 17 2011 Burt Holzman <burt@fnal.gov> - 1.3.3rc1-2
- Create plugin directory

* Thu Nov 17 2011 Burt Holzman <burt@fnal.gov> - 1.3.3rc1-1
- Update to GIP 1.3.3rc1

* Wed Oct 12 2011 Burt Holzman <burt@fnal.gov> - 1.3.1-1
- Don't error out if there's no config.ini -- bugfix

* Tue Oct 11 2011 Burt Holzman <burt@fnal.gov> - 1.3.0-1
- Enable new config.ini reading

* Thu Aug 04 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.0alpha3-2
- Minor ownership issues found in testing

* Thu Aug 04 2011 Burt Holzman <burt@fnal.gov> - 1.3.0alpha3-1
- Bump to alpha3

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.0alpha2-4
- Fix ownership of files.

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.3.0alpha2-3
- Improve FHS compliance.

* Fri Jul 22 2011 Burt Holzman <burt@fnal.gov> - 1.3.0alpha2-2
- Added description and cleaned up specfile

* Wed Jul 20 2011 Burt Holzman <burt@fnal.gov> 1.3.0alpha2-1
- Initial build


