# This package depends on selective manual byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 0

%bcond_without python2
%bcond_without python3

# We can build varying amounts of Koji for python2 and python3 based on
# the py[23]_support macro values. Valid values are:
#   undefined or 0 -- do not build
#   1 -- build just the cli and lib
#   2 -- build everything we can
# For executable scripts, py3 wins if we build it
# The following rules tweak these settings based on options and environment

# Default to building both fully
%define py2_support 2
%define py3_support 2

%if 0%{?rhel} >= 8
# and no python2 on rhel8+
%define py2_support 0
%else
%if 0%{?rhel}
# No python3 for older rhel
%define py3_support 0
%endif
%endif

%if 0%{?fedora} > 28
# no py2 after F31
%define py2_support 0
%define py3_support 2
%else
# Keep some minimal python2 in f30 for now
%if 0%{?fedora} == 28
%define py2_support 1
%define py3_support 2
%else
%if 0%{?fedora}
# match what the older Fedoras already have
%define py2_support 2
%define py3_support 1
%endif
%endif
%endif

# Lastly enforce the bcond parameters
%if %{without python2}
%define py2_support 0
%endif
%if %{without python3}
%define py3_support 0
%endif

%if ! %{py2_support}
# use python3
%define __python %{__python3}
%endif

# Compatibility with RHEL. These macros have been added to EPEL but
# not yet to RHEL proper.
# https://bugzilla.redhat.com/show_bug.cgi?id=1307190
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}

# If the definition isn't available for python3_pkgversion, define it
%{?!python3_pkgversion:%global python3_pkgversion 3}

%if 0%{?rhel} && 0%{?rhel} < 7
%global use_systemd 0
%global install_opt TYPE=sysv
%else
%global use_systemd 1
%endif

Name: koji
Version: 1.17.0
Release: 10%{?dist}
# the included arch lib from yum's rpmUtils is GPLv2+
License: LGPLv2 and GPLv2+
Summary: Build system tools
URL: https://pagure.io/koji/
Source0: https://releases.pagure.org/koji/koji-%{version}.tar.bz2

# Patches proposed upstream
## Use createrepo_c by default now (we already do this in Fedora infra anyway)
## From: https://pagure.io/koji/pull-request/1278
Patch10: koji-PR1278-use-createrepo_c-by-default.patch

# Download only the repomd.xml instead of all the repodata
Patch11: https://pagure.io/koji/pull-request/1398.patch

# Allow generating seperate srpm repos in buildroot repos
Patch12: https://pagure.io/koji/pull-request/1273.patch

# Handle 'bare' merge mode for repos
Patch13: https://pagure.io/koji/pull-request/1411.patch

# Expose dynamic_buildrequires mock setting
# Upstream: https://pagure.io/koji/pull-request/1466.patch
# Rebased for 1.17.0 in https://src.fedoraproject.org/rpms/koji/pull-request/6
Patch14: https://src.fedoraproject.org/rpms/koji/c/9828bc3dd8ed0679159aceb902409600b21f803c.patch

# Patch to fix kerberos auth in kojid with python3
Patch15: https://pagure.io/koji/pull-request/1468.patch

# Path to provide lower level versions of build_target functions
# Required for side tags
Patch16: https://pagure.io/koji/pull-request/1331.patch

# Fix bare repo gen blocklist usage
Patch17: https://pagure.io/koji/pull-request/1502.patch

# Fix bare mode to use --all for mergeing repos
Patch18: https://pagure.io/koji/pull-request/1516.patch

# use _writeInheritanceData in _create_tag
Patch19: https://pagure.io/koji/pull-request/1555.patch

# don't add noarch rpms to src-only repos
# rebased from https://pagure.io/koji/c/3aba7412500cfdf048c742c474620b8ba60489dc.patch
Patch20: no-noarch-in-src-repos.patch

# Adjust xz params to favor speed
Patch21: https://pagure.io/koji/pull-request/1576.patch

# OSG patches
Patch102: kojid_setup_dns.patch
Patch103: kojid_scmbuild_check_spec_after_running_sourcecmd.patch
Patch106: kojicli_setup_dns.patch
Patch112: Fix-type-in-add-group-pkg.patch
Patch113: kojira-add-sleeptime-to-conf.patch
Patch116: Fix-1.15-1.16-schema-upgrade-script.patch


BuildArch: noarch
%if 0%{py3_support}
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Requires: python%{python3_pkgversion}-libcomps
%else
Requires: python2-%{name} = %{version}-%{release}
%if ! 0%{?osg} && (0%{?fedora} || 0%{?rhel} >= 7)
Requires: python-libcomps
%endif
%endif
%if %{use_systemd}
BuildRequires: systemd
BuildRequires: pkgconfig
%endif

%description
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.

%if 0%{py2_support}
%package -n python2-%{name}
Summary: Build system tools python library
%{?python_provide:%python_provide python2-%{name}}
BuildRequires: python2-devel
%if 0%{?fedora} >= 25 || 0%{?rhel} >= 8
Requires: python2-rpm
%else
Requires: rpm-python
%endif
Requires: pyOpenSSL
Requires: python-requests
%if 0%{?fedora} >= 23 || 0%{?rhel} >= 7
Requires: python-requests-kerberos
%else
Requires: python-krbV >= 1.0.13
%endif
Requires: python-dateutil
Requires: python-six

%description -n python2-%{name}
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.
%endif

%if 0%{py3_support}
%package -n python%{python3_pkgversion}-%{name}
Summary: Build system tools python library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
BuildRequires: python%{python3_pkgversion}-devel
%if 0%{?fedora} >= 25 || 0%{?rhel} >= 8
Requires: python%{python3_pkgversion}-rpm
%else
Requires: rpm-python%{python3_pkgversion}
%endif
Requires: python%{python3_pkgversion}-pyOpenSSL
Requires: python%{python3_pkgversion}-requests
Requires: python%{python3_pkgversion}-requests-kerberos
Requires: python%{python3_pkgversion}-dateutil
Requires: python%{python3_pkgversion}-six

%description -n python%{python3_pkgversion}-%{name}
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.
%endif

%if 0%{py2_support}
%package -n python2-%{name}-cli-plugins
Summary: Koji client plugins
License: LGPLv2
Requires: python2-%{name} = %{version}-%{release}

%description -n python2-%{name}-cli-plugins
Plugins to the koji command-line interface
%endif

%if 0%{py3_support}
%package -n python%{python3_pkgversion}-%{name}-cli-plugins
Summary: Koji client plugins
License: LGPLv2
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}-cli-plugins
Plugins to the koji command-line interface
%endif

%package hub
Summary: Koji XMLRPC interface
License: LGPLv2
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hub-code
%if 0%{?fedora} || 0%{?rhel} > 7
Suggests: python%{python3_pkgversion}-%{name}-hub
Suggests: python%{python3_pkgversion}-%{name}-hub-plugins
%endif

%description hub
koji-hub is the XMLRPC interface to the koji database

%if 0%{py2_support} > 1
%package -n python2-%{name}-hub
Summary: Koji XMLRPC interface
License: LGPLv2 and GPLv2
# rpmdiff lib (from rpmlint) is GPLv2 (only)
Requires: httpd
Requires: mod_wsgi
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
Requires: mod_auth_gssapi
%endif
Requires: python-psycopg2
Requires: python2-%{name} = %{version}-%{release}
# py2 xor py3
Provides: %{name}-hub-code = %{version}-%{release}

%description -n python2-%{name}-hub
koji-hub is the XMLRPC interface to the koji database
%endif

%if 0%{py3_support} > 1
%package -n python%{python3_pkgversion}-%{name}-hub
Summary: Koji XMLRPC interface
License: LGPLv2 and GPLv2
# rpmdiff lib (from rpmlint) is GPLv2 (only)
Requires: httpd
Requires: python%{python3_pkgversion}-mod_wsgi
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
Requires: mod_auth_gssapi
%endif
Requires: python%{python3_pkgversion}-psycopg2
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
# py2 xor py3
Provides: %{name}-hub-code = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}-hub
koji-hub is the XMLRPC interface to the koji database
%endif

%package hub-plugins
Summary: Koji hub plugins
License: LGPLv2
Requires: %{name}-hub-plugins-code = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Suggests: python%{python3_pkgversion}-%{name}-hub-plugins
%endif

%description hub-plugins
Plugins to the koji XMLRPC interface

%if 0%{py2_support} > 1
%package -n python2-%{name}-hub-plugins
Summary: Koji hub plugins
License: LGPLv2
Requires: python2-%{name}-hub = %{version}-%{release}
Requires: python2-qpid-proton
Requires: cpio
Provides: %{name}-hub-plugins-code = %{version}-%{release}

%description -n python2-%{name}-hub-plugins
Plugins to the koji XMLRPC interface
%endif

%if 0%{py3_support} > 1
%package -n python%{python3_pkgversion}-%{name}-hub-plugins
Summary: Koji hub plugins
License: LGPLv2
Requires: python%{python3_pkgversion}-%{name}-hub = %{version}-%{release}
Requires: python%{python3_pkgversion}-qpid-proton
Requires: cpio
Provides: %{name}-hub-plugins-code = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}-hub-plugins
Plugins to the koji XMLRPC interface
%endif

%package builder-plugins
Summary: Koji builder plugins
License: LGPLv2
Requires: %{name} = %{version}-%{release}
Requires: %{name}-builder = %{version}-%{release}

%description builder-plugins
Plugins for the koji build daemon

%package builder
Summary: Koji RPM builder daemon
%if 0%{py3_support} > 1
License: LGPLv2
%else
License: LGPLv2 and GPLv2+
#mergerepos (from createrepo) is GPLv2+
%endif
Requires: mock >= 0.9.14
Requires(pre): /usr/sbin/useradd
Requires: squashfs-tools
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
Requires: createrepo_c >= 0.10.0
%if 0%{py3_support} > 1
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Requires: python%{python3_pkgversion}-librepo
Requires: python%{python3_pkgversion}-multilib
Requires: python%{python3_pkgversion}-cheetah
%else
Requires: python2-%{name} = %{version}-%{release}
Requires: python2-multilib
Requires: python-cheetah
%endif

%description builder
koji-builder is the daemon that runs on build machines and executes
tasks that come through the Koji system.

%package vm
Summary: Koji virtual machine management daemon
License: LGPLv2
Requires: %{name} = %{version}-%{release}
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
%if 0%{py3_support} > 1
Requires: python%{python3_pkgversion}-libvirt
Requires: python%{python3_pkgversion}-libxml2
%else
Requires: libvirt-python
Requires: libxml2-python
%endif
Requires: /usr/bin/virt-clone
Requires: qemu-img

%description vm
koji-vm contains a supplemental build daemon that executes certain tasks in a
virtual machine. This package is not required for most installations.

%package utils
Summary: Koji Utilities
License: LGPLv2
Requires: %{name} = %{version}-%{release}
%if 0%{py3_support} > 1
Requires: python%{python3_pkgversion}-psycopg2
%else
Requires: python-psycopg2
%endif
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
Requires: %{name} = %{version}-%{release}
Requires: %{name}-web-code = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Suggests: python%{python3_pkgversion}-%{name}-web
%endif

%description web
koji-web is a web UI to the Koji system.

%if 0%{py2_support} > 1
%package -n python2-%{name}-web
Summary: Koji Web UI
License: LGPLv2
%{?python_provide:%python_provide python2-%{name}-web}
Requires: httpd
Requires: mod_wsgi
# https://bugzilla.redhat.com/show_bug.cgi?id=1497923 - "koji-web requires mod_auth_gssapi but that is not available in RHEL6 or EPEL6"
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
Requires: mod_auth_gssapi
%else
Requires: mod_auth_kerb
Requires: python-krbV >= 1.0.13
%endif
Requires: python-psycopg2
Requires: python-cheetah
Requires: python2-%{name} = %{version}-%{release}
Provides: %{name}-web-code = %{version}-%{release}

%description -n python2-%{name}-web
koji-web is a web UI to the Koji system.
%endif

%if 0%{py3_support} > 1
%package -n python%{python3_pkgversion}-%{name}-web
Summary: Koji Web UI
License: LGPLv2
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}-web}
Requires: httpd
Requires: python%{python3_pkgversion}-mod_wsgi
Requires: mod_auth_gssapi
Requires: python%{python3_pkgversion}-psycopg2
Requires: python%{python3_pkgversion}-cheetah
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Provides: %{name}-web-code = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}-web
koji-web is a web UI to the Koji system.
%endif

%prep
%autosetup -p1

%build
# Nothing to build


%install
%if 0%{py2_support} < 2  &&  0%{py3_support} < 2
echo "At least one python must be built with full support"
exit 1
%endif

# python2 build
%if 0%{py2_support} > 1
make DESTDIR=$RPM_BUILD_ROOT PYTHON=%{__python2} %{?install_opt} install
%else
%if 0%{py2_support}
for d in koji cli plugins ; do
    pushd $d
    make DESTDIR=$RPM_BUILD_ROOT KOJI_MINIMAL=1 PYTHON=%{__python2} %{?install_opt} install
    popd
done
%endif
%endif


# python3 build
%if 0%{py3_support} > 1
make DESTDIR=$RPM_BUILD_ROOT PYTHON=%{__python3} %{?install_opt} install
# alter python interpreter in koji CLI
scripts='%{_bindir}/koji %{_sbindir}/kojid %{_sbindir}/kojira %{_sbindir}/koji-shadow
         %{_sbindir}/koji-gc %{_sbindir}/kojivmd'
for fn in $scripts ; do
    sed -i 's|#!/usr/bin/python2|#!/usr/bin/python3|' $RPM_BUILD_ROOT$fn
done
%else
%if 0%{py3_support}
# minimal
for d in koji cli plugins ; do
    pushd $d
    make DESTDIR=$RPM_BUILD_ROOT KOJI_MINIMAL=1 PYTHON=%{__python3} %{?install_opt} install
    popd
done
# alter python interpreter in koji CLI
sed -i 's|#!/usr/bin/python2|#!/usr/bin/python3|' $RPM_BUILD_ROOT/usr/bin/koji
%endif
%endif

%if 0%{?fedora} >= 28
# handle extra byte compilation
extra_dirs='
    %{_prefix}/lib/koji-builder-plugins
    %{_prefix}/koji-hub-plugins
    %{_datadir}/koji-hub
    %{_datadir}/koji-web/lib/kojiweb
    %{_datadir}/koji-web/scripts'
%if 0%{py2_support} > 1
for fn in $extra_dirs ; do
    %py_byte_compile %{__python2} %{buildroot}$fn
done
%endif
%if 0%{py3_support} > 1
for fn in $extra_dirs ; do
    %py_byte_compile %{__python3} %{buildroot}$fn
done
%endif
%endif

%if 0%{py2_support} < 1
# With no python2 support, remove/do not ship internal mergerepos
rm -f %{buildroot}/%{_libexecdir}/kojid/mergerepos
%endif

%files
%{_bindir}/*
%config(noreplace) /etc/koji.conf
%dir /etc/koji.conf.d
%doc docs Authors COPYING LGPL

%if 0%{py2_support}
%files -n python2-%{name}
%{python2_sitelib}/%{name}
%{python2_sitelib}/koji_cli
%endif

%if 0%{py3_support}
%files -n python%{python3_pkgversion}-koji
%{python3_sitelib}/%{name}
%{python3_sitelib}/koji_cli
%endif

%if 0%{py2_support}
%files -n python2-%{name}-cli-plugins
%{python2_sitelib}/koji_cli_plugins
# we don't have config files for default plugins yet
#%%dir %%{_sysconfdir}/koji/plugins
#%%config(noreplace) %%{_sysconfdir}/koji/plugins/*.conf
%endif

%if 0%{py3_support}
%files -n python%{python3_pkgversion}-%{name}-cli-plugins
%{python3_sitelib}/koji_cli_plugins
# we don't have config files for default plugins yet
#%%dir %%{_sysconfdir}/koji/plugins
#%%config(noreplace) %%{_sysconfdir}/koji/plugins/*.conf
%endif

%files hub
%config(noreplace) /etc/httpd/conf.d/kojihub.conf
%dir /etc/koji-hub
%config(noreplace) /etc/koji-hub/hub.conf
%dir /etc/koji-hub/hub.conf.d

%if 0%{py2_support} > 1
%files -n python2-%{name}-hub
%{_datadir}/koji-hub/*.py*
%endif

%if 0%{py3_support} > 1
%files -n python%{python3_pkgversion}-%{name}-hub
%{_datadir}/koji-hub/*.py
%{_datadir}/koji-hub/__pycache__
%endif

%files hub-plugins
%dir /etc/koji-hub/plugins
%config(noreplace) /etc/koji-hub/plugins/*.conf

%if 0%{py2_support} > 1
%files -n python2-%{name}-hub-plugins
%{_prefix}/lib/koji-hub-plugins/*.py*
%endif

%if 0%{py3_support} > 1
%files -n python%{python3_pkgversion}-%{name}-hub-plugins
%{_prefix}/lib/koji-hub-plugins/*.py
%{_prefix}/lib/koji-hub-plugins/__pycache__
%endif

%files builder-plugins
%dir /etc/kojid/plugins
%config(noreplace) /etc/kojid/plugins/*.conf
%dir %{_prefix}/lib/koji-builder-plugins
%{_prefix}/lib/koji-builder-plugins/*.py*
%if 0%{py3_support} > 1
%{_prefix}/lib/koji-builder-plugins/__pycache__
%endif

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
%dir /etc/kojiweb
%config(noreplace) /etc/kojiweb/web.conf
%config(noreplace) /etc/httpd/conf.d/kojiweb.conf
%dir /etc/kojiweb/web.conf.d

%if 0%{py2_support} > 1
%files -n python2-%{name}-web
%{_datadir}/koji-web
%endif

%if 0%{py3_support} > 1
%files -n python%{python3_pkgversion}-%{name}-web
%{_datadir}/koji-web
%endif

%files builder
%{_sbindir}/kojid
%if 0%{py2_support} > 1
%dir %{_libexecdir}/kojid
%{_libexecdir}/kojid/mergerepos
%endif
%if %{use_systemd}
%{_unitdir}/kojid.service
%else
%{_initrddir}/kojid
%config(noreplace) /etc/sysconfig/kojid
%endif
%dir /etc/kojid
%config(noreplace) /etc/kojid/kojid.conf
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
%endif

%changelog
* Fri Mar 27 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.17.0-10.1.osg
- Update to 1.17.0-10 from Fedora
  Fedora's changelog since 1.16.2:
    * Tue Jul 09 2019 Kevin Fenzi <kevin@scrye.com> - 1.17.0-9
    - Add backport for user sidetags: https://src.fedoraproject.org/rpms/koji/pull-request/7
    - Add patch to use --all for merging bare repos: https://pagure.io/koji/pull-request/1516

    * Wed Jun 19 2019 Kevin Fenzi <kevin@scrye.com> - 1.17.0-8
    - Add https://pagure.io/koji/pull-request/1502.patch

    * Thu May 30 2019 Kevin Fenzi <kevin@scrye.com> - 1.17.0-7
    - Add patch to fix koji kerberos auth with python3.
    - Drop internal mergerepos so we can go all python3. Fixes bug #1715257

    * Wed May 29 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.17.0-7
    - Expose dynamic_buildrequires mock setting

    * Tue May 28 2019 Kevin Fenzi <kevin@scrye.com> - 1.17.0-6
    - Switch kojid back to python3 as imagefactory and oz have moved.
    - Backport patch to download only repomd.xml instead of all repodata.
    - Backport patch to allow 'bare' repo merging for modularity.
    - Backport patch to allow for seperate srpm repos in buildroot repos.

    * Mon Mar 11 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-5
    - Switch kojid back to Python 2 so that imgfac doesn't get disabled

    * Sun Mar 10 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-4
    - Add patch proposed upstream to use createrepo_c by default to drop yum dependency

    * Sun Mar 10 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-3
    - Remove remnants of unused /usr/libexec/koji-hub

    * Thu Mar 07 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-2
    - Enable Python 3 for Fedora 30+ and EL8+
    - Sync packaging changes from upstream

    * Thu Mar 07 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.17.0-1
    - Rebase to 1.17.0

* Tue Mar 24 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.16.2-1.3.osg
- Backport CVE-2019-17109 patch from 1.16.3; this replaces the 1635-os_path_join.patch
- Fix 1.15->1.16 schema upgrade script

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

