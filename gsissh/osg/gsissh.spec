# gsissh is openssh with support for GSI authentication
# This gsissh specfile is based on the openssh specfile

%global WITH_SELINUX 1
%if %{WITH_SELINUX}
# Audit patch applicable only over SELinux patch
%global WITH_AUDIT 1
%else
%global WITH_AUDIT 0
%endif

# OpenSSH privilege separation requires a user & group ID
%global sshd_uid    74
%global sshd_gid    74

# Build position-independent executables (requires toolchain support)?
%global pie 1

# Do we want kerberos5 support (1=yes 0=no)
# It is not possible to support kerberos5 and GSI at the same time
%global kerberos5 0

# Do we want GSI support (1=yes 0=no)
%global gsi 1

# Do we want NSS tokens support
%global nss 1

# Whether or not /sbin/nologin exists.
%global nologin 1

Summary: An implementation of the SSH protocol with GSI authentication
Name: gsissh
Version: 4.3p2
Release: 1%{?dist}
URL: http://www.openssh.com/portable.html
#Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
#Source1: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.sig
# This package differs from the upstream OpenSSH tarball in that it
# removes the ACSS cipher.
Source0: openssh-%{version}-noacss.tar.bz2
Source1: openssh-nukeacss.sh
Patch0: openssh-4.3p1-redhat.patch
Patch2: openssh-4.3p2-skip-initial.patch
Patch3: openssh-3.8.1p1-krb5-config.patch
Patch4: openssh-4.3p1-vendor.patch
Patch5: openssh-3.9p1-noinitlog.patch
Patch12: openssh-4.3p2-selinux.patch
Patch16: openssh-4.3p1-audit.patch
Patch21: openssh-3.9p1-safe-stop.patch
Patch22: openssh-3.9p1-askpass-keep-above.patch
Patch23: openssh-3.9p1-no-log-signal.patch
Patch24: openssh-4.3p1-fromto-remote.patch
Patch25: openssh-4.3p2-scp-print-err.patch
Patch26: openssh-4.2p1-pam-no-stack.patch
Patch27: openssh-3.9p1-log-in-chroot.patch
Patch30: openssh-4.0p1-exit-deadlock.patch
Patch31: openssh-3.9p1-skip-used.patch
Patch35: openssh-4.2p1-askpass-progress.patch
Patch36: openssh-4.3p2-buffer-len.patch
Patch37: openssh-4.3p2-configure-typo.patch
Patch38: openssh-4.3p2-askpass-grab-info.patch
Patch39: openssh-4.3p2-no-v6only.patch
Patch40: openssh-4.3p2-coverity-memleaks.patch
Patch41: openssh-4.3p2-gssapi-no-spnego.patch
Patch42: openssh-4.3p2-no-dup-logs.patch
Patch43: openssh-4.3p2-localtime.patch
Patch44: openssh-4.3p2-allow-ip-opts.patch
Patch45: openssh-4.3p2-cve-2006-4924.patch
Patch46: openssh-3.9p1-cve-2006-5051.patch
Patch47: openssh-4.3p2-cve-2006-5794.patch
Patch48: openssh-4.3p2-initscript.patch
Patch49: openssh-4.3p2-pam-session.patch
Patch50: openssh-4.3p2-gssapi-canohost.patch
Patch51: openssh-4.3p2-mls.patch
Patch52: openssh-4.3p2-selinux-rolechg.patch
Patch53: openssh-4.3p2-cve-2006-5052.patch
Patch54: openssh-4.3p2-nss-keys.patch
Patch55: openssh-4.3p2-cve-2007-3102.patch
Patch56: openssh-4.3p2-sftp-drain-acks.patch
Patch57: openssh-4.3p2-cve-2007-4752.patch
Patch58: openssh-4.3p2-fips.patch
Patch59: openssh-3.9p1-scp-manpage.patch
Patch60: openssh-4.3p2-latency.patch
Patch61: openssh-4.3p2-init-status.patch
Patch62: openssh-4.3p2-sftp-log.patch
Patch63: openssh-4.3p2-chroot.patch
Patch64: openssh-4.3p2-hangexit.patch
Patch65: openssh-4.3p2-cbc.patch
Patch66: openssh-4.3p2-keygen.patch
Patch67: openssh-4.3p2-sshsocketleak.patch
Patch68: openssh-4.3p2-randclean.patch
Patch69: openssh-4.3p2-stderr.patch
Patch70: openssh-4.3p2-forced.patch
Patch71: openssh-4.3p2-engine.patch
Patch73: openssh-4.3p2-biguid.patch
Patch74: openssh-4.3p2-crypto-audit.patch

# This is the patch that adds GSI support
# Based on http://grid.ncsa.illinois.edu/ssh/dl/patch/openssh-4.3p2.patch
Patch99: openssh-4.3p2-gsissh.patch
Patch100: sigchld.patch

License: BSD
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{nologin}
Requires: /sbin/nologin
%endif

Requires: initscripts >= 5.20
# We must require the FIPS version of openssl
Requires: openssl >= 0.9.8e

BuildRequires: autoconf, automake, perl, tcp_wrappers, zlib-devel
BuildRequires: audit-libs-devel >= 1.7.18
BuildRequires: util-linux, groff, man
BuildRequires: pam-devel
BuildRequires: fipscheck-devel
BuildRequires: openssl-devel >= 0.9.8e

%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{gsi}
BuildRequires: globus-gss-assist-devel
%endif

%if %{nss}
BuildRequires: nss-devel
%endif

%if %{WITH_SELINUX}
Requires: libselinux >= 1.27.7
BuildRequires: libselinux-devel >= 1.27.7
%endif

%if %{WITH_AUDIT}
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

BuildRequires: xauth

%package clients
Summary: SSH client applications with GSI authentication
Requires: %{name} = %{version}-%{release}
Group: Applications/Internet

%package server
Summary: SSH server daemon with GSI authentication
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires(post): chkconfig >= 0.9, /sbin/service
Requires(pre): /usr/sbin/useradd
Requires: /etc/pam.d/system-auth, /%{_lib}/security/pam_loginuid.so

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features. This version of OpenSSH
has been modified to support GSI authentication.

This package includes the core files necessary for both the gsissh
client and server. To make this package useful, you should also
install gsissh-clients, gsissh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.

This version of OpenSSH has been modified to support GSI authentication.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server.

This version of OpenSSH has been modified to support GSI authentication.

%prep

%setup -q -n openssh-%{version}
%patch0 -p1 -b .redhat
%patch2 -p1 -b .skip-initial
%patch3 -p1 -b .krb5-config
%patch4 -p1 -b .vendor
%patch5 -p1 -b .noinitlog

%if %{WITH_SELINUX}
#SELinux
%patch12 -p1 -b .selinux
%endif

%if %{WITH_AUDIT}
%patch16 -p1 -b .audit
%endif

%patch21 -p1 -b .safe-stop
%patch22 -p1 -b .keep-above
%patch23 -p1 -b .signal
%patch24 -p1 -b .fromto-remote
%patch25 -p1 -b .print-err
%patch26 -p1 -b .stack
%patch27 -p1 -b .log-chroot
%patch30 -p1 -b .exit-deadlock
%patch31 -p1 -b .skip-used
%patch35 -p1 -b .progress
%patch36 -p0 -b .buffer-len
%patch37 -p1 -b .typo
%patch38 -p1 -b .grab-info
%patch39 -p1 -b .no-v6only
%patch40 -p1 -b .memleaks
%patch41 -p1 -b .no-spnego
%patch42 -p1 -b .no-dups
%patch43 -p1 -b .localtime
%patch44 -p1 -b .ip-opts
%patch45 -p1 -b .deattack-dos
%patch46 -p1 -b .sig-no-cleanup
%patch47 -p1 -b .verify
%patch48 -p1 -b .initscript
%patch49 -p1 -b .pam-sesssion
%patch50 -p1 -b .canohost
%patch51 -p1 -b .mls
%patch52 -p1 -b .rolechg
%patch53 -p1 -b .cve-2006-5052
%patch54 -p1 -b .nss-keys
%patch55 -p1 -b .inject-fix
%patch56 -p1 -b .drain-acks
%patch57 -p1 -b .cve-2007-4752
%patch58 -p1 -b .fips
%patch59 -p0 -b .manpage
%patch60 -p1 -b .latency
%patch61 -p1 -b .status
%patch62 -p1 -b .sftp-log
%patch63 -p1 -b .chroot
%patch64 -p1 -b .hangexit
%patch65 -p1 -b .cbc
%patch66 -p1 -b .keygen
%patch67 -p0 -b .socketleak
%patch68 -p1 -b .randclean
%patch69 -p1 -b .stderr
%patch70 -p1 -b .forced
%patch71 -p1 -b .engine
%patch73 -p1 -b .biguid
%patch74 -p1 -b .cryptoaudit
%patch99 -p1 -b .gsi
%patch100 -p0

sed 's/sshd.pid/gsisshd.pid/' -i pathnames.h
sed 's!$(piddir)/sshd.pid!$(piddir)/gsisshd.pid!' -i Makefile.in

autoreconf

%build
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%if %{pie}
%ifarch s390 s390x sparc sparc64
CFLAGS="$CFLAGS -fPIE"
%else
CFLAGS="$CFLAGS -fpie"
%endif
export CFLAGS
LDFLAGS="$LDFLAGS -pie"; export LDFLAGS
%endif
%if %{kerberos5}
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
	CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
	LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
	krb5_prefix=
	CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi
%endif

%configure \
	--sysconfdir=%{_sysconfdir}/gsissh \
	--libexecdir=%{_libexecdir}/gsissh \
	--datadir=%{_datadir}/gsissh \
	--with-tcp-wrappers \
	--with-rsh=%{_bindir}/rsh \
	--with-default-path=/usr/local/bin:/bin:/usr/bin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \
	--with-privsep-path=%{_var}/empty/gsisshd \
	--enable-vendor-patchlevel="FC-%{version}-%{release}" \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
%if %{nss}
	--with-nss \
%endif
	--with-pam \
%if %{WITH_SELINUX}
	--with-selinux \
%endif
%if %{WITH_AUDIT}
	--with-linux-audit \
%endif
%if %{kerberos5}
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
	--without-kerberos5 \
%endif
%if %{gsi}
	--with-gsi
%else
	--without-gsi
%endif

make SSH_PROGRAM=%{_bindir}/gsissh \
     ASKPASS_PROGRAM=%{_libexecdir}/openssh/ssh-askpass

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    #fipshmac $RPM_BUILD_ROOT%{_bindir}/gsissh \
    #fipshmac $RPM_BUILD_ROOT%{_sbindir}/gsisshd \
%{nil}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/gsissh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/gsissh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/gsisshd/etc
make install DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT%{_var}/empty/gsisshd/etc/localtime
install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_libexecdir}/gsissh
install -m644 contrib/redhat/sshd.pam $RPM_BUILD_ROOT/etc/pam.d/gsisshd
install -m755 contrib/redhat/sshd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gsisshd

rm $RPM_BUILD_ROOT%{_bindir}/ssh-add
rm $RPM_BUILD_ROOT%{_bindir}/ssh-agent
rm $RPM_BUILD_ROOT%{_bindir}/ssh-keyscan
rm $RPM_BUILD_ROOT%{_mandir}/man1/ssh-add.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/ssh-agent.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/ssh-keyscan.1*
rm $RPM_BUILD_ROOT%{_datadir}/gsissh/Ssh.bin

for f in $RPM_BUILD_ROOT%{_bindir}/* \
	 $RPM_BUILD_ROOT%{_sbindir}/* \
	 $RPM_BUILD_ROOT%{_mandir}/man*/* ; do
    mv $f `dirname $f`/gsi`basename $f`
done
ln -sf gsissh $RPM_BUILD_ROOT%{_bindir}/gsislogin
ln -sf gsissh.1 $RPM_BUILD_ROOT%{_mandir}/man1/gsislogin.1

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

rm -f README.nss.nss-keys
%if ! %{nss}
rm -f README.nss
%endif

# Add some defaults so the gsisshd service will work out-of-the-box.
sed -i 's|#Port 22|Port 23|' $RPM_BUILD_ROOT/etc/gsissh/sshd_config
sed -i 's|#HostKey /etc/gsissh/ssh_host_rsa_key|HostKey /etc/ssh/ssh_host_rsa_key|' $RPM_BUILD_ROOT/etc/gsissh/sshd_config
sed -i 's|#HostKey /etc/gsissh/ssh_host_dsa_key|HostKey /etc/ssh/ssh_host_dsa_key|' $RPM_BUILD_ROOT/etc/gsissh/sshd_config

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
%if %{nologin}
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :
%else
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /dev/null -r -d /var/empty/sshd sshd 2> /dev/null || :
%endif

%post server
/sbin/chkconfig --add gsisshd

%postun server
/sbin/service gsisshd condrestart > /dev/null 2>&1 || :

%preun server
if [ "$1" = 0 ]
then
	/sbin/service gsisshd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del gsisshd
fi

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog INSTALL LICENCE OVERVIEW README* RFC* TODO WARNING*
%attr(0755,root,root) %dir %{_sysconfdir}/gsissh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/gsissh/moduli
%attr(0755,root,root) %{_bindir}/gsissh-keygen
%attr(0644,root,root) %{_mandir}/man1/gsissh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/gsissh
%attr(4755,root,root) %{_libexecdir}/gsissh/ssh-keysign
%attr(0644,root,root) %{_mandir}/man8/gsissh-keysign.8*

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/gsissh
#%attr(0644,root,root) %{_bindir}/.gsissh.hmac
%attr(0644,root,root) %{_mandir}/man1/gsissh.1*
%attr(0755,root,root) %{_bindir}/gsiscp
%attr(0644,root,root) %{_mandir}/man1/gsiscp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/gsissh/ssh_config
%attr(0755,root,root) %{_bindir}/gsislogin
%attr(0644,root,root) %{_mandir}/man1/gsislogin.1*
%attr(0644,root,root) %{_mandir}/man5/gsissh_config.5*
%attr(0755,root,root) %{_bindir}/gsisftp
%attr(0644,root,root) %{_mandir}/man1/gsisftp.1*

%files server
%defattr(-,root,root)
%dir %attr(0711,root,root) %{_var}/empty/gsisshd
%dir %attr(0755,root,root) %{_var}/empty/gsisshd/etc
%ghost %verify(not md5 size mtime) %{_var}/empty/gsisshd/etc/localtime
%attr(0755,root,root) %{_sbindir}/gsisshd
#%attr(0644,root,root) %{_sbindir}/.gsisshd.hmac
%attr(0755,root,root) %{_libexecdir}/gsissh/sftp-server
%attr(0644,root,root) %{_mandir}/man5/gsisshd_config.5*
%attr(0644,root,root) %{_mandir}/man8/gsisshd.8*
%attr(0644,root,root) %{_mandir}/man8/gsisftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/gsissh/sshd_config
%attr(0644,root,root) %config(noreplace) /etc/pam.d/gsisshd
%attr(0755,root,root) /etc/rc.d/init.d/gsisshd

%changelog
* Sun Mar 06 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.3p2-1
- Inital packaging
- Based on openssh-4.3p2-72.el5
