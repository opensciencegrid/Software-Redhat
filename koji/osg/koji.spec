# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

# Enable Python 3 builds for Fedora + EPEL >5
# NOTE: do **NOT** change 'epel' to 'rhel' here, as this spec is also
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
# If the definition isn't available for python3_pkgversion, define it
%{?!python3_pkgversion:%global python3_pkgversion 3}
%else
%bcond_with python3
%endif

# Compatibility with RHEL. These macros have been added to EPEL but
# not yet to RHEL proper.
# https://bugzilla.redhat.com/show_bug.cgi?id=1307190
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%global install_opt TYPE=sysv
%endif

Name: koji
Version: 1.16.2
Release: 1.1%{?dist}
# koji.ssl libs (from plague) are GPLv2+
License: LGPLv2 and GPLv2+
Summary: Build system tools
URL: https://pagure.io/koji/
Source0: https://releases.pagure.org/koji/koji-%{version}.tar.bz2

# Fix is_conn_error bug which commonly caused operations that wait a
# long time to fail out prematurely on Python 3
# https://pagure.io/koji/issue/1192
# https://pagure.io/koji/pull-request/1203
Patch0: 0001-Fix-is_conn_error-for-Python-3.3-change-to-socket.er.patch

# OSG patches
Patch102: kojid_setup_dns.patch
Patch103: kojid_scmbuild_check_spec_after_running_sourcecmd.patch
Patch106: kojicli_setup_dns.patch
Patch112: Fix-type-in-add-group-pkg.patch
Patch113: kojira-accept-sleeptime-option.patch
Patch114: 1635-os_path_join.patch


BuildArch: noarch
%if 0%{with python3}
Requires: python3-%{name} = %{version}-%{release}
Requires: python3-pycurl
Requires: python3-libcomps
%else
Requires: python2-%{name} = %{version}-%{release}
%if 0%{?fedora}
Requires: python2-libcomps
Requires: python2-pycurl
%endif
%if 0%{?rhel}
Requires: python-pycurl
%endif
%if ! 0%{?osg} && 0%{?rhel} >= 7
Requires: python-libcomps
%endif
%endif
BuildRequires: python
BuildRequires: python-sphinx
%if %{use_systemd}
BuildRequires: systemd
BuildRequires: pkgconfig
%endif

# For backwards compatibility, we want to Require: python2-koji for Fedora <= 26 so dependent
# packages have some time to switch their Requires lines to python2-koji instead of Koji.
%if 0%{?fedora} && 0%{?fedora} <= 26
Requires: python2-%{name} = %{version}-%{release}
Requires: python2-pycurl
Requires: python2-libcomps
%endif

%description
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.

%package -n python2-%{name}
Summary: Build system tools python library
%{?python_provide:%python_provide python2-%{name}}
BuildRequires: python2-devel
Requires: python-krbV >= 1.0.13
Requires: rpm-python
Requires: pyOpenSSL
Requires: python-requests
Requires: python-requests-kerberos
Requires: python-dateutil
Requires: python-six

%description -n python2-%{name}
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.

%if 0%{with python3}
%package -n python3-%{name}
Summary: Build system tools python library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires: python3-devel
Requires: python3-rpm
Requires: python3-pyOpenSSL
Requires: python3-requests
Requires: python3-requests-kerberos
Requires: python3-dateutil
Requires: python3-six

%description -n python3-%{name}
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.
%endif

%package -n python2-%{name}-cli-plugins
Summary: Koji client plugins
License: LGPLv2
Requires: %{name} = %{version}-%{release}

%description -n python2-%{name}-cli-plugins
Plugins to the koji command-line interface

%if 0%{with python3}
%package -n python3-%{name}-cli-plugins
Summary: Koji client plugins
License: LGPLv2
Requires: %{name} = %{version}-%{release}

%description -n python3-%{name}-cli-plugins
Plugins to the koji command-line interface
%endif

%package hub
Summary: Koji XMLRPC interface
License: LGPLv2 and GPLv2
# rpmdiff lib (from rpmlint) is GPLv2 (only)
Requires: httpd
Requires: mod_wsgi
Requires: python-psycopg2
Requires: python2-%{name} = %{version}-%{release}

%description hub
koji-hub is the XMLRPC interface to the koji database

%package hub-plugins
Summary: Koji hub plugins
License: LGPLv2
Requires: %{name}-hub = %{version}-%{release}
Requires: python-qpid >= 0.7
Requires: python-qpid-proton
Requires: cpio

%description hub-plugins
Plugins to the koji XMLRPC interface

%package builder
Summary: Koji RPM builder daemon
License: LGPLv2 and GPLv2+
#mergerepos (from createrepo) is GPLv2+
Requires: python2-%{name} = %{version}-%{release}
Requires: mock >= 0.9.14
Requires(pre): /usr/sbin/useradd
Requires: squashfs-tools
Requires: python2-multilib
%if %{use_systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
%endif
Requires: /usr/bin/cvs
Requires: /usr/bin/svn
Requires: /usr/bin/git
Requires: python-cheetah
Requires: createrepo >= 0.9.2

%description builder
koji-builder is the daemon that runs on build machines and executes
tasks that come through the Koji system.

%package vm
Summary: Koji virtual machine management daemon
License: LGPLv2
Requires: python2-%{name} = %{version}-%{release}
%if %{use_systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
%endif
Requires: libvirt-python
Requires: libxml2-python
Requires: /usr/bin/virt-clone
Requires: qemu-img

%description vm
koji-vm contains a supplemental build daemon that executes certain tasks in a
virtual machine. This package is not required for most installations.

%package utils
Summary: Koji Utilities
License: LGPLv2
Requires: python-psycopg2
Requires: python2-%{name} = %{version}-%{release}
%if %{use_systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description utils
Utilities for the Koji system

%package web
Summary: Koji Web UI
License: LGPLv2
Requires: httpd
Requires: mod_wsgi
# https://bugzilla.redhat.com/show_bug.cgi?id=1497923 - "koji-web requires mod_auth_gssapi but that is not available in RHEL6 or EPEL6"
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
Requires: mod_auth_gssapi
%else
Requires: mod_auth_kerb
%endif
Requires: python-psycopg2
Requires: python-cheetah
Requires: python2-%{name} = %{version}-%{release}
Requires: python-krbV >= 1.0.13

%description web
koji-web is a web UI to the Koji system.

%prep
%setup -q
%patch0 -p1 -b .connerror

# OSG patches
%patch102 -p1
%patch103 -p1
%patch106 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT %{?install_opt} install
%if 0%{with python3}
cd koji
make DESTDIR=$RPM_BUILD_ROOT PYTHON=python3 %{?install_opt} install
cd ../cli
make DESTDIR=$RPM_BUILD_ROOT PYTHON=python3 %{?install_opt} install
cd ../plugins
make DESTDIR=$RPM_BUILD_ROOT PYTHON=python3 %{?install_opt} install
# alter python interpreter in koji CLI
sed -i 's/\#\!\/usr\/bin\/python2/\#\!\/usr\/bin\/python3/' $RPM_BUILD_ROOT/usr/bin/koji
%endif

%files
%{_bindir}/*
%config(noreplace) /etc/koji.conf
%dir /etc/koji.conf.d
%doc docs Authors COPYING LGPL

%files -n python2-%{name}
%{python2_sitelib}/%{name}
%{python2_sitelib}/koji_cli

%if 0%{with python3}
%files -n python%{python3_pkgversion}-koji
%{python3_sitelib}/%{name}
%{python3_sitelib}/koji_cli
%endif

%files -n python2-%{name}-cli-plugins
%{python2_sitelib}/koji_cli_plugins
# we don't have config files for default plugins yet
#%%dir %%{_sysconfdir}/koji/plugins
#%%config(noreplace) %%{_sysconfdir}/koji/plugins/*.conf

%if 0%{with python3}
%files -n python%{python3_pkgversion}-%{name}-cli-plugins
%{python3_sitelib}/koji_cli_plugins
# we don't have config files for default plugins yet
#%%dir %%{_sysconfdir}/koji/plugins
#%%config(noreplace) %%{_sysconfdir}/koji/plugins/*.conf
%endif

%files hub
%{_datadir}/koji-hub
%dir %{_libexecdir}/koji-hub
%config(noreplace) /etc/httpd/conf.d/kojihub.conf
%dir /etc/koji-hub
%config(noreplace) /etc/koji-hub/hub.conf
%dir /etc/koji-hub/hub.conf.d

%files hub-plugins
%dir %{_prefix}/lib/koji-hub-plugins
%{_prefix}/lib/koji-hub-plugins/*.py*
%dir /etc/koji-hub/plugins
/etc/koji-hub/plugins/*.conf

%files utils
%{_sbindir}/kojira
%if %{use_systemd}
%{_unitdir}/kojira.service
%else
%{_initrddir}/kojira
%config(noreplace) /etc/sysconfig/kojira
%endif
%dir /etc/kojira
%config(noreplace) /etc/kojira/kojira.conf
%{_sbindir}/koji-gc
%dir /etc/koji-gc
%config(noreplace) /etc/koji-gc/koji-gc.conf
%{_sbindir}/koji-shadow
%dir /etc/koji-shadow
%config(noreplace) /etc/koji-shadow/koji-shadow.conf

%files web
%{_datadir}/koji-web
%dir /etc/kojiweb
%config(noreplace) /etc/kojiweb/web.conf
%config(noreplace) /etc/httpd/conf.d/kojiweb.conf
%dir /etc/kojiweb/web.conf.d

%files builder
%{_sbindir}/kojid
%dir %{_libexecdir}/kojid
%{_libexecdir}/kojid/mergerepos
%defattr(-,root,root)
%dir %{_prefix}/lib/koji-builder-plugins
%{_prefix}/lib/koji-builder-plugins/*.py*
%if %{use_systemd}
%{_unitdir}/kojid.service
%else
%{_initrddir}/kojid
%config(noreplace) /etc/sysconfig/kojid
%endif
%dir /etc/kojid
%dir /etc/kojid/plugins
%config(noreplace) /etc/kojid/kojid.conf
%config(noreplace) /etc/kojid/plugins/runroot.conf
%config(noreplace) /etc/kojid/plugins/save_failed_tree.conf
%attr(-,kojibuilder,kojibuilder) /etc/mock/koji

%pre builder
/usr/sbin/useradd -r -s /bin/bash -G mock -d /builddir -M kojibuilder 2>/dev/null ||:

%if %{use_systemd}

%post builder
%systemd_post kojid.service

%preun builder
%systemd_preun kojid.service

%postun builder
%systemd_postun kojid.service

%else

%post builder
/sbin/chkconfig --add kojid

%preun builder
if [ $1 = 0 ]; then
  /sbin/service kojid stop &> /dev/null
  /sbin/chkconfig --del kojid
fi
%endif

%files vm
%{_sbindir}/kojivmd
#dir %%{_datadir}/kojivmd
%{_datadir}/kojivmd/kojikamid
%if %{use_systemd}
%{_unitdir}/kojivmd.service
%else
%{_initrddir}/kojivmd
%config(noreplace) /etc/sysconfig/kojivmd
%endif
%dir /etc/kojivmd
%config(noreplace) /etc/kojivmd/kojivmd.conf

%if %{use_systemd}

%post vm
%systemd_post kojivmd.service

%preun vm
%systemd_preun kojivmd.service

%postun vm
%systemd_postun kojivmd.service

%else

%post vm
/sbin/chkconfig --add kojivmd

%preun vm
if [ $1 = 0 ]; then
  /sbin/service kojivmd stop &> /dev/null
  /sbin/chkconfig --del kojivmd
fi
%endif

%if %{use_systemd}

%post utils
%systemd_post kojira.service

%preun utils
%systemd_preun kojira.service

%postun utils
%systemd_postun kojira.service

%else
%post utils
/sbin/chkconfig --add kojira
/sbin/service kojira condrestart &> /dev/null || :
%preun utils
if [ $1 = 0 ]; then
  /sbin/service kojira stop &> /dev/null || :
  /sbin/chkconfig --del kojira
fi
%endif

%changelog
* Mon Mar 23 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.16.2-1.1.osg
- Update to 1.16.2-1 from Fedora/EPEL
  Fedora's changelog since 1.15.3:
    * Thu Feb 21 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.16.2-1
    - Rebase to 1.16.2 for CVE-2018-1002161

    * Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-4
    - Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

    * Wed Jan 09 2019 Adam Williamson <awilliam@redhat.com> - 1.16.1-3
    - Backport fix for Python 3 connection failure bug (#1192, PR #1203)

    * Fri Sep 14 2018 Kevin Fenzi <kevin@scrye.com> - 1.16.1-2
    - Fix bad sed that caused python32 dep.

    * Thu Sep 13 2018 Kevin Fenzi <kevin@scrye.com> - 1.16.1-1
    - Update to 1.16.1

    * Tue Jul 31 2018 Kevin Fenzi <kevin@scrye.com> - 1.16.0-1
    - Update to 1.16.0

  Drop OSG patches that no longer apply:
  - Don-t-warn-on-compatrequests.patch
  - Don-t-warn-on-use_old_ssl-OSG-still-relies-on-it.patch
  - koji_passwd_cache.patch
  - koji_passwd_retry.patch
  - koji_proxy_cert.patch

* Fri Dec 06 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.15.3-1.2.osg
- Update based on Fedora's 1.15.1-3 spec file and upstream's 1.15.3 tarball.
  Fedora's changelog:
    * Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-3
    - Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

    * Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.15.1-2
    - Rebuilt for Python 3.7

    * Tue Apr 03 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.15.1-1
    - Rebase to 1.15.1
    - Fixes CVE-2018-1002150

    * Fri Mar 16 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.0-7
    - Backport PR #841 to allow configurable timeout for oz

    * Tue Feb 20 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-6
    - Backport PR #796

    * Sun Feb 18 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-5
    - Add  workaround patch for bug #808

    * Fri Feb 16 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-4
    - Backport patch from PR#794
    - Fix macro escaping in comments

    * Mon Feb 12 2018 Owen Taylor <otaylor@redhat.com> - 1.15.0-3
    - Make hub, builder, etc, require python2-koji not koji

    * Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
    - Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

    * Sat Jan 27 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-1
    - Rebase to koji 1.15.0

* Fri Nov 22 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.14.3-1.2.osg
- Update based on Fedora's 1.14.0-4 spec file and upstream's 1.14.3 tarball.
  Fedora's changelog:
    * Mon Jan 22 2018 Troy Dawson <tdawson@redhat.com> - 1.14.0-4
    - Update conditional

    * Thu Dec 07 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.14.0-3
    - Backport py3 runroot encoding patch (PR#735)

    * Mon Dec 04 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.14.0-2
    - Backport py3 keytab patch (PR#708)
    - Backport patches for exit code (issue#696)

    * Tue Sep 26 2017 Dennis Gilmore <dennis@ausil.us> - 1.14.0-1
    - update to upstream 1.14.0

* Fri Nov 22 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.13.2-1.1.osg
- Update based on Fedora's spec file and upstream's 1.13.2 tarball.
  Fedora's changelog:
    * Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-4
    - Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

    * Wed Jul 12 2017 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.13.0-3
    - Remove the 2 postfix for pycurl and libcomps on RHEL

    * Tue Jul 11 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.13.0-2
    - Require python2-koji on Fedora <= 26.

* Fri Nov 22 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.12.2-1.1.osg
- Add missing python-multilib and python-psycopg2 dependencies

* Fri Nov 15 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.12.2-1.osg
- Update to 1.12.2

* Wed Oct 09 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.1-1.2.osg
- Add patch for https://pagure.io/koji/pull-request/1635

* Thu Mar 14 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.1-1.1.osg
- Drop python-libcomps requirement

* Thu Feb 21 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.1-1.osg
- Update to 1.11.1 (SOFTWARE-3595)
- Build from developer tarball

* Tue Oct 30 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.0-1.7
- Add kojira-accept-sleeptime-option.patch

* Fri Dec 22 2017 Mátyás Selmeci <matyas@cs.wisc.edu>
- Drop el5-isms (SOFTWARE-3050)
- Drop createrepo_sha1.patch -- was only required for el5

* Wed Aug 23 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.0-1.6
- Fix `koji add-group-pkg` to set the correct type (SOFTWARE-2870)

* Sat Jun 03 2017 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.12.0-5
- Add patch for completing #349 fix

* Sat Jun 03 2017 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.12.0-4
- Add upstreamed patch for #349

* Tue May 23 2017 Dennis Gilmore <dennis@ausil.us> - 1.12.0-3
- add some upstreamed patches needed to fix some things in fedora

* Wed Apr 19 2017 Dennis Gilmore <dennis@ausil.us> - 1.12.0-2
- add patch so that kojid starts without ssl auth configured

* Tue Apr 18 2017 Dennis Gilmore <dennis@ausil.us> - 1.12.0-1
- update to upstream 1.12.0
- remove rhel 5 conditionals as its no longer supported in epel

* Thu Jan 19 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.0-1.5
- Require python-requests-2.6.0 (fixes "call 8 (rawUpload) failed: syntax error: line 1, column 49" error in kojid)

* Thu Jan 12 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.0-1.4
- Add db-upgrade-1.10-to-1.11.patch to fix a failing constraint in DB upgrade
  script from 1.10 to 1.11

* Wed Jan 11 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.0-1.2
- Add kojiweb_getfile_nontext_fix.patch to fix an error with 'getfile' kojiweb
  URLs

* Sun Jan 08 2017 Till Maas <opensource@till.name> - 1.11.0-5
- Do not apply faulty CheckClientIP patch

* Sun Jan 08 2017 Till Maas <opensource@till.name> - 1.11.0-4
- Add patch for keytab kerberos client config
- Move non upstreamable Fedora patch to the end to ease rebasing to future
  upstream release
- Move license comment before license tag

* Sat Jan 07 2017 Till Maas <opensource@till.name> - 1.11.0-3
- Add patches for proxy IP forwarding

* Fri Jan 06 2017 Till Maas <opensource@till.name> - 1.11.0-2
- Update upstream URLs
- Add upstream koji-gc kerberos patches
- Use Source0

* Tue Jan 03 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.11.0-1.1
- Merge OSG changes

* Fri Dec 09 2016 Dennis Gilmore <dennis@ausil.us> - 1.11.0-1
- update to 1.11.0
- setup fedora config for kerberos and flag day

* Tue Oct 04 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.10.1-10.1
- Merge OSG changes
    - Drop koji_no_sslv3.patch
    - Drop pkgorigins_filename.patch
    - Update other OSG patches

* Wed Sep 28 2016 Adam Miller <maxamillion@fedoraproject.org> - 1.10.1-13
- Patch new-chroot functionality into runroot plugin

* Tue Aug 23 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-12
- add patch to disable bind mounting into image tasks chroots

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-11
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May 26 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-10
- add patch to enable dns in runroot chroots

* Tue May 24 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-9
- update to git master upstream, add lmc cosmetic fixes
- add patch to disable login in koji-web

* Fri Apr 08 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-8
- do not remove the - for project on livemedia
- fix the sending of messages on image completion

* Thu Apr 07 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-7
- --product had to be --project
- add missing Requires for koji-builder on python2-multilib

* Wed Apr 06 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-6
- add --product to livemedia-creator calls rhbz#1315110

* Wed Apr 06 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-5
- enable dns in runroots
- add koji signed repo support
- Run plugin callbacks when image builds finish

* Thu Mar 03 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-4
- add a patch to install the runroot builder plugin in the correct place

* Tue Mar 01 2016 Dennis Gilmore <dennis@ausil.us> - 1.10.1-3
- update to git e8201aac8294e6125a73504886b0800041b58868
- https://pagure.io/fork/ausil/koji/branch/fedora-infra

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Dennis Gilmore <dennis@ausil.us> - 1.10.1-1
- update to 1.10.1
- Requires yum in the cli rhbz#1230888

* Thu Sep 24 2015 Kalev Lember <klember@redhat.com> - 1.10.0-2
- Backport two patches to fix ClientSession SSL errors

* Thu Jul 16 2015 Dennis Gilmore <dennis@ausil.us> - 1.10.0=1
- update to 1.10.0 release

* Mon Jul 06 2015 Dennis Gilmore <dennis@ausil.us> - 1.9.0-13.20150607gitf426fdb
- update the git snapshot to latest head
- enable systemd units for f23 up

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-12.20150423git52a0188
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Dennis Gilmore <dennis@ausil.us> - 1.9.0-11.20150423git52a0188
- update to latest git

* Fri Jan 30 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 1.6.0-10
- Patch kojid to request sha1 when running createrepo, for el5 compatibility
  (SOFTWARE-1442)

* Thu Jan 29 2015 Carl Edquist <edquist@cs.wisc.edu> - 1.6.0-9
- Bring in upstream fix to parse repomd.xml for pkgorigins filename,
  required for el6 koji upgrade (SOFTWARE-1442)

* Tue Jan 27 2015 Dennis Gilmore <dennis@ausil.us> - 1.9.0-10.gitcd45e886
- update to git tarball

* Thu Dec 11 2014 Dennis Gilmore <dennis@ausil.us> - 1.9.0-9
- add upstream patch switching to TLS1 from sslv3

* Thu Oct 16 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.6.0-8
- Add patch to allow using TLSv1 instead of SSLv3 (SOFTWARE-1637)

* Tue Sep 30 2014 Dennis Gilmore <dennis@ausil.us> - 1.9.0-8
- don't exclude koji-vm from ppc and ppc64

* Fri Sep 26 2014 Till Maas <opensource@till.name> - 1.9.0-7
- Use https for kojipkgs
- Update URL

* Mon Aug 04 2014 Dennis Gilmore <dennis@ausil.us> - 1.9.0-6
- add patch to fix kickstart parsing

* Mon Aug 04 2014 Dennis Gilmore <dennis@ausil.us> - 1.9.0-5
- add upstream patches for better docker support

* Tue Jul 29 2014 Dennis Gilmore <dennis@ausil.us> - 1.9.0-4
- add upstream patch to compress docker images

* Thu Jun 12 2014 Dennis Gilmore <dennis@ausil.us> - 1.9.0-3
- add patch to move builder workdir to /var/tmp
- add support for making raw.xz images

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 Dennis Gilmore <dennis@ausil.us> - 1.9.0-1
- update to upstream 1.9.0

* Wed Jul 31 2013 Dennis Gilmore <dennis@ausil.us> - 1.8.0-2
- update from git snapshot

* Wed May 22 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-7
- Add use_host_resolv to opts in koji cli so koji --mock-config makes configs with DNS set up

* Mon Apr 01 2013 Dennis Gilmore <dennis@ausil.us> - 1.8.0-1
- update to upstream 1.8.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Dennis Gilmore <dennis@ausil.us> - 1.7.1-2
- revert "avoid baseurl option in createrepo" patch
- fix integer overflow issue in checkUpload handler

* Wed Nov 21 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.1-1
- update to upstream 1.7.1 release

* Wed Oct 31 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-6
- Add Brian Bockelman's patch to allow using proxy certs

* Sat Sep 01 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.0-7
- add the patch that we had previously had hotapplied in fedora infra

* Sat Sep 01 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.0-6
- remove even trying to make devices i the chroots

* Sat Sep 01 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.0-5
- add patch to check for /dev/loopX before making them

* Fri Aug 31 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.0-4
- add patch to only make /dev/urandom if it doesnt exist
- add upstream patch for taginfo fixes with older servers

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-5
- Allow user to retry entering SSL key password

* Tue Jun 05 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.0-2
- use topurl not pkgurl in the fedora config

* Fri Jun 01 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.0-1
- update to 1.7.0 many bugfixes and improvements
- now uses mod_wsgi

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-4
- add patch to check for spec file only after running source_cmd in a build from an scm

* Tue Oct 11 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.6.0-3
- add setup_dns to rootopts in kojid

* Mon Aug 08 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.6.0-2
- Cache passwords to decrypt SSL key in memory.

* Mon Jan 03 2011 Dennis Gilmore <dennis@ausil.us> - 1.6.0-1.1
- drop Requires on qemu-img on epel for koji-vm
- add readme note on epel

* Fri Dec 17 2010 Dennis Gilmore <dennis@ausil.us> - 1.6.0-1
- update to 1.6.0

