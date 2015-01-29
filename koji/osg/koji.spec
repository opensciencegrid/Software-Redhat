%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name: koji
Version: 1.6.0
Release: 9%{?dist}
License: LGPLv2 and GPLv2+
# koji.ssl libs (from plague) are GPLv2+
Summary: Build system tools
Group: Applications/System
URL: http://fedorahosted.org/koji
Patch0: fedora-config.patch
Patch1: koji_passwd_cache.patch
Patch2: kojid_setup_dns.patch
Patch3: kojid_scmbuild_check_spec_after_running_sourcecmd.patch
Patch4: koji_passwd_retry.patch
Patch5: koji_proxy_cert.patch
Patch6: kojicli_setup_dns.patch
Patch7: koji_no_sslv3.patch
Patch8: pkgorigins_filename.patch

Source: https://fedorahosted.org/releases/k/o/koji/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: python-krbV >= 1.0.13
Requires: rpm-python
Requires: pyOpenSSL
Requires: python-urlgrabber
BuildRequires: python

%description
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.

%package hub
Summary: Koji XMLRPC interface
Group: Applications/Internet
License: LGPLv2 and GPLv2
# rpmdiff lib (from rpmlint) is GPLv2 (only)
Requires: httpd
Requires: mod_python
Requires: postgresql-python
Requires: %{name} = %{version}-%{release}

%description hub
koji-hub is the XMLRPC interface to the koji database

%package hub-plugins
Summary: Koji hub plugins
Group: Applications/Internet
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hub = %{version}-%{release}

%description hub-plugins
Plugins to the koji XMLRPC interface

%package builder
Summary: Koji RPM builder daemon
Group: Applications/System
License: LGPLv2 and GPLv2+
#mergerepos (from createrepo) is GPLv2+
Requires: %{name} = %{version}-%{release}
Requires: mock >= 0.9.14
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(pre): /usr/sbin/useradd
Requires: /usr/bin/cvs
Requires: /usr/bin/svn
Requires: /usr/bin/git
Requires: rpm-build
Requires: redhat-rpm-config
Requires: pykickstart                                                                               
Requires: pycdio
Requires: python-cheetah
%if 0%{?fedora} || 0%{?rhel} > 5
Requires: createrepo >= 0.9.6
%endif
%if 0%{?rhel} == 5
Requires: python-createrepo >= 0.9.6
Requires: python-hashlib
Requires: createrepo
%endif

%description builder
koji-builder is the daemon that runs on build machines and executes
tasks that come through the Koji system.

%package vm
Summary: Koji virtual machine management daemon
Group: Applications/System
License: LGPLv2
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires: libvirt-python
Requires: libxml2-python
Requires: python-virtinst
Requires: qemu-img

%description vm
koji-vm contains a supplemental build daemon that executes certain tasks in a
virtual machine. This package is not required for most installations.

%package utils
Summary: Koji Utilities
Group: Applications/Internet
Requires: postgresql-python
Requires: %{name} = %{version}-%{release}

%description utils
Utilities for the Koji system

%package web
Summary: Koji Web UI
Group: Applications/Internet
Requires: httpd
Requires: mod_python
Requires: mod_auth_kerb
Requires: postgresql-python
Requires: python-cheetah
Requires: %{name} = %{version}-%{release}
Requires: python-krbV >= 1.0.13

%description web
koji-web is a web UI to the Koji system.

%prep
%setup -q
%patch0 -p1 -b .orig
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p1
%patch8 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{python_sitelib}/%{name}
%config(noreplace) %{_sysconfdir}/koji.conf
%doc docs Authors COPYING LGPL

%files hub
%defattr(-,root,root)
%{_datadir}/koji-hub
%{_libexecdir}/koji-hub/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/kojihub.conf
%config(noreplace) %{_sysconfdir}/koji-hub/hub.conf

%files hub-plugins
%defattr(-,root,root)
%dir %{_prefix}/lib/koji-hub-plugins
%{_prefix}/lib/koji-hub-plugins/*.py*
%dir %{_sysconfdir}/koji-hub/plugins/
%config(noreplace) %{_sysconfdir}/koji-hub/plugins/messagebus.conf
%config(noreplace) %{_sysconfdir}/koji-hub/plugins/rpm2maven.conf

%files utils
%defattr(-,root,root)
%{_sbindir}/kojira
%{_sbindir}/koji-gc
%{_sbindir}/koji-shadow
%{_initrddir}/kojira
%config(noreplace) %{_sysconfdir}/sysconfig/kojira
%dir %{_sysconfdir}/kojira
%config(noreplace) %{_sysconfdir}/kojira/kojira.conf
%dir %{_sysconfdir}/koji-gc
%config(noreplace) %{_sysconfdir}/koji-gc/koji-gc.conf
%config(noreplace) %{_sysconfdir}/koji-shadow/koji-shadow.conf

%files web
%defattr(-,root,root)
%{_datadir}/koji-web
%{_sysconfdir}/kojiweb
%config(noreplace) /etc/httpd/conf.d/kojiweb.conf

%files builder
%defattr(-,root,root)
%{_sbindir}/kojid
%{_initrddir}/kojid
%{_libexecdir}/kojid/
%config(noreplace) %{_sysconfdir}/sysconfig/kojid
%dir %{_sysconfdir}/kojid
%config(noreplace) %{_sysconfdir}/kojid/kojid.conf
%attr(-,kojibuilder,kojibuilder) /etc/mock/koji

%pre builder
/usr/sbin/useradd -r -s /bin/bash -G mock -d /builddir -M kojibuilder 2>/dev/null ||:

%post builder
/sbin/chkconfig --add kojid
/sbin/service kojid condrestart &> /dev/null || :

%preun builder
if [ $1 = 0 ]; then
  /sbin/service kojid stop &> /dev/null
  /sbin/chkconfig --del kojid
fi

%files vm
%defattr(-,root,root)
%{_sbindir}/kojivmd
%{_datadir}/kojivmd
%{_initrddir}/kojivmd
%config(noreplace) %{_sysconfdir}/sysconfig/kojivmd
%dir %{_sysconfdir}/kojivmd
%config(noreplace) %{_sysconfdir}/kojivmd/kojivmd.conf

%post vm
/sbin/chkconfig --add kojivmd

%preun vm
if [ $1 = 0 ]; then
  /sbin/service kojivmd stop &> /dev/null
  /sbin/chkconfig --del kojivmd
fi

%post utils
/sbin/chkconfig --add kojira
/sbin/service kojira condrestart &> /dev/null || :
%preun utils
if [ $1 = 0 ]; then
  /sbin/service kojira stop &> /dev/null || :
  /sbin/chkconfig --del kojira
fi

%changelog
* Thu Jan 29 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.6.0-9
- Bring in upstream fix to parse repomd.xml for pkgorigins filename,
  required for el6 koji upgrade (SOFTWARE-1442)

* Thu Oct 16 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.6.0-8
- Add patch to allow using TLSv1 instead of SSLv3 (SOFTWARE-1637)

* Wed May 22 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-7
- Add use_host_resolv to opts in koji cli so koji --mock-config makes configs with DNS set up

* Wed Oct 31 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-6
- Add Brian Bockelman's patch to allow using proxy certs

* Wed Jun 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-5
- Allow user to retry entering SSL key password

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-4
- add patch to check for spec file only after running source_cmd in a build from an scm

* Tue Oct 11 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-3
- add setup_dns to rootopts in kojid

* Mon Aug 08 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.6.0-2
- Cache passwords to decrypt SSL key in memory.

* Fri Dec 17 2010 Dennis Gilmore <dennis@ausil.us> - 1.6.0-1
- update to 1.6.0

* Wed Dec 01 2010 Dennis Gilmore <dennis@ausil.us> - 1.5.0-1
- update to 1.5.0

* Tue Aug  3 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.0-4
- fix python 2.7 incompatibilities (rhbz 619276)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 10 2010 Dennis Gilmore <dennis@ausil.us> - 1.4.0-2
- add missing Requires: python-cheetah from koji-builder

* Fri Jul 09 2010 Dennis Gilmore <dennis@ausil.us> - 1.4.0-1
- update to 1.4.0
- Merge mead branch: support for building jars with Maven *
- support for building appliance images *
- soft dependencies for LiveCD/Appliance features
- smarter prioritization of repo regenerations
- package list policy to determine if package list changes are allowed
- channel policy to determine which channel a task is placed in
- edit host data via webui
- description and comment fields for hosts *
- cleaner log entries for kojihub
- track user data in versioned tables *
- allow setting retry parameters for the cli
- track start time for tasks *
- allow packages built from the same srpm to span multiple external repos
- make the command used to fetch sources configuable per repo
- kojira: remove unexpected directories
- let kojid to decide if it can handle a noarch task
- avoid extraneous ssl handshakes
- schema changes to support starred items

* Fri Nov 20 2009 Dennis Gilmore <dennis@ausil.us> - 1.3.2-1
- update to 1.3.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Dennis Gilmore <dennis@ausil.us> - 1.3.1-1
- update to 1.3.1

* Wed Feb 18 2009 Dennis Gilmore <dennis@ausil.us> - 1.3.0-1
- update to 1.3.0

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.6-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Dennis Gilmore <dennis@ausil.us> - 1.2.6-1
- update to 1.2.6
- make sure we have to correct version of createrepo on Fedora 8 

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.5-2
- fix conditional (line 5)
- fix license tag

* Fri Jan 25 2008 jkeating <jkeating@redhat.com> 1.2.5-1
- Put createrepo arguments in correct order

* Thu Jan 24 2008 jkeating <jkeating@redhat.com> 1.2.4-1
- Use the --skip-stat flag in createrepo calls.
- canonicalize tag arches before using them (dgilmore)
- fix return value of delete_build
- Revert to getfile urls if the task is not successful in emails
- Pass --target instead of --arch to mock.
- ignore trashcan tag in prune-signed-copies command
- add the "allowed_scms" kojid parameter
- allow filtering builds by the person who built them

* Fri Dec 14 2007 jkeating <jkeating@redhat.com> 1.2.3-1
- New upstream release with lots of updates, bugfixes, and enhancements.

* Tue Jun  5 2007 Mike Bonnet <mikeb@redhat.com> - 1.2.2-1
- only allow admins to perform non-scratch builds from srpm
- bug fixes to the cmd-line and web UIs

* Thu May 31 2007 Mike Bonnet <mikeb@redhat.com> - 1.2.1-1
- don't allow ExclusiveArch to expand the archlist (bz#239359)
- add a summary line stating whether the task succeeded or failed to the end of the "watch-task" output
- add a search box to the header of every page in the web UI
- new koji download-build command (patch provided by Dan Berrange)

* Tue May 15 2007 Mike Bonnet <mikeb@redhat.com> - 1.2.0-1
- change version numbering to a 3-token scheme
- install the koji favicon

* Mon May 14 2007 Mike Bonnet <mikeb@redhat.com> - 1.1-5
- cleanup koji-utils Requires
- fix encoding and formatting in email notifications
- expand archlist based on ExclusiveArch/BuildArchs
- allow import of rpms without srpms
- commit before linking in prepRepo to release db locks
- remove exec bit from kojid logs and uploaded files (patch by Enrico Scholz)

* Tue May  1 2007 Mike Bonnet <mikeb@redhat.com> - 1.1-4
- remove spurious Requires: from the koji-utils package

* Tue May  1 2007 Mike Bonnet <mikeb@redhat.com> - 1.1-3
- fix typo in BuildNotificationTask (patch provided by Michael Schwendt)
- add the --changelog param to the buildinfo command
- always send email notifications to the package builder and package owner
- improvements to the web UI

* Tue Apr 17 2007 Mike Bonnet <mikeb@redhat.com> - 1.1-2
- re-enable use of the --update flag to createrepo

* Mon Apr 09 2007 Jesse Keating <jkeating@redhat.com> 1.1-1
- make the output listPackages() consistent regardless of with_dups
- prevent large batches of repo deletes from holding up regens
- allow sorting the host list by arches

* Mon Apr 02 2007 Jesse Keating <jkeating@redhat.com> 1.0-1
- Release 1.0!

* Wed Mar 28 2007 Mike Bonnet <mikeb@redhat.com> - 0.9.7-4
- set SSL connection timeout to 12 hours

* Wed Mar 28 2007 Mike Bonnet <mikeb@redhat.com> - 0.9.7-3
- avoid SSL renegotiation
- improve log file handling in kojid
- bug fixes in command-line and web UI

* Sun Mar 25 2007 Mike Bonnet <mikeb@redhat.com> - 0.9.7-2
- enable http access to packages in kojid
- add Requires: pyOpenSSL
- building srpms from CVS now works with the Extras CVS structure
- fixes to the chain-build command
- bug fixes in the XML-RPC and web interfaces

* Tue Mar 20 2007 Jesse Keating <jkeating@redhat.com> - 0.9.7-1
- Package up the needed ssl files

* Tue Mar 20 2007 Jesse Keating <jkeating@redhat.com> - 0.9.6-1
- 0.9.6 release, mostly ssl auth stuff
- use named directories for config stuff
- remove -3 requires on creatrepo, don't need that specific anymore

* Tue Feb 20 2007 Jesse Keating <jkeating@redhat.com> - 0.9.5-8
- Add Authors COPYING LGPL to the docs of the main package

* Tue Feb 20 2007 Jesse Keating <jkeating@redhat.com> - 0.9.5-7
- Move web files from /var/www to /usr/share
- Use -p in install calls
- Add rpm-python to requires for koji

* Mon Feb 19 2007 Jesse Keating <jkeating@redhat.com> - 0.9.5-6
- Clean up spec for package review

* Sun Feb 04 2007 Mike McLean <mikem@redhat.com> - 0.9.5-1
- project renamed to koji
