# gsi-openssh is openssh with support for GSI authentication
# This gsi-openssh specfile is based on the openssh specfile

# Do we want SELinux & Audit
%if 0%{?!noselinux:1}
%global WITH_SELINUX 1
%else
%global WITH_SELINUX 0
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

# Do we want libedit support
%global libedit 1

# Do we want LDAP support
%global ldap 1

%global openssh_ver 7.4p1
%global openssh_rel 2

Summary: An implementation of the SSH protocol with GSI authentication
Name: gsi-openssh
Version: %{openssh_ver}
Release: %{openssh_rel}%{?dist}
Provides: gsissh = %{version}-%{release}
Obsoletes: gsissh < 5.8p2-2
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source2: gsisshd.pam
Source7: gsisshd.sysconfig
Source9: gsisshd@.service
Source10: gsisshd.socket
Source11: gsisshd.service
Source12: gsisshd-keygen.service
Source13: gsisshd-keygen
Source99: README.sshd-and-gsisshd

#?
Patch100: openssh-7.4p1-coverity.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1889
Patch103: openssh-5.8p1-packet.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1402
# https://bugzilla.redhat.com/show_bug.cgi?id=1171248
# record pfs= field in CRYPTO_SESSION audit event
Patch200: openssh-7.4p1-audit.patch
# Do not write to one socket from more processes (#1310684)
Patch202: openssh-6.6p1-audit-race-condition.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1641 (WONTFIX)
Patch400: openssh-7.4p1-role-mls.patch
#https://bugzilla.redhat.com/show_bug.cgi?id=781634
Patch404: openssh-6.6p1-privsep-selinux.patch

#?-- unwanted child :(
Patch501: openssh-6.6p1-ldap.patch
#?
Patch502: openssh-6.6p1-keycat.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=1644
Patch601: openssh-6.6p1-allow-ip-opts.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1893
Patch604: openssh-6.6p1-keyperm.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1925
Patch606: openssh-5.9p1-ipv6man.patch
#?
Patch607: openssh-5.8p2-sigpipe.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1789
Patch609: openssh-5.5p1-x11.patch

#?
Patch700: openssh-7.4p1-fips.patch
#?
# drop? Patch701: openssh-5.6p1-exit-deadlock.patch
#?
Patch702: openssh-5.1p1-askpass-progress.patch
#?
Patch703: openssh-4.3p2-askpass-grab-info.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=205842
# drop? Patch704: openssh-5.9p1-edns.patch
#?
Patch706: openssh-6.6.1p1-localdomain.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1635 (WONTFIX)
Patch707: openssh-6.6p1-redhat.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1890 (WONTFIX) need integration to prng helper which is discontinued :)
Patch708: openssh-6.6p1-entropy.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1640 (WONTFIX)
Patch709: openssh-6.2p1-vendor.patch
# warn users for unsupported UsePAM=no (#757545)
Patch711: openssh-6.6p1-log-usepam-no.patch
# make aes-ctr ciphers use EVP engines such as AES-NI from OpenSSL
Patch712: openssh-6.3p1-ctr-evp-fast.patch
# add cavs test binary for the aes-ctr
Patch713: openssh-7.4p1-ctr-cavstest.patch
# add SSH KDF CAVS test driver
Patch714: openssh-7.4p1-kdf-cavs.patch

#http://www.sxw.org.uk/computing/patches/openssh.html
#changed cache storage type - #848228
Patch800: openssh-7.4p1-gsskex.patch
#http://www.mail-archive.com/kerberos@mit.edu/msg17591.html
Patch801: openssh-6.6p1-force_krb.patch
# add new option GSSAPIEnablek5users and disable using ~/.k5users by default (#1169843)
# CVE-2014-9278
Patch802: openssh-6.6p1-GSSAPIEnablek5users.patch
# Respect k5login_directory option in krk5.conf (#1328243)
Patch803: openssh-6.6p1-k5login_directory.patch
Patch900: openssh-6.1p1-gssapi-canohost.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1780
Patch901: openssh-7.4p1-kuserok.patch
# use default_ccache_name from /etc/krb5.conf (#991186)
Patch902: openssh-6.3p1-krb5-use-default_ccache_name.patch
# Change GSSAPIStrictAcceptor to yes as it ever was (#1488982)
Patch903: openssh-7.4p1-gss-strict-acceptor.patch
# Run ssh-copy-id in the legacy mode when SSH_COPY_ID_LEGACY variable is set (#969375
Patch905: openssh-7.4p1-legacy-ssh-copy-id.patch
# Use tty allocation for a remote scp (#985650)
Patch906: openssh-6.4p1-fromto-remote.patch
# log when a client requests an interactive session and only sftp is allowed (#1130198)
Patch914: openssh-6.6.1p1-log-sftp-only-connections.patch
# log via monitor in chroots without /dev/log (#1083482)
Patch918: openssh-7.4p1-log-in-chroot.patch
# MLS labeling according to chosen sensitivity (#1202843)
Patch919: openssh-6.6.1p1-mls-fix-labeling.patch
# sshd test mode show all config values (#1187597)
Patch920: openssh-6.6p1-test-mode-all-values.patch
# Add sftp option to force mode of created files (#1191055)
Patch921: openssh-6.6p1-sftp-force-permission.patch
# fix memory problem (#1223218)
Patch924: openssh-6.6p1-memory-problems.patch
# Enhance AllowGroups documentation in man page (#1150007)
Patch925: openssh-6.6p1-allowGroups-documentation.patch
# provide option GssKexAlgorithms to disable vulnerable groun1 kex
Patch928: openssh-7.4p1-gssKexAlgorithms.patch
# make s390 use /dev/ crypto devices -- ignore closefrom (#1318760)
Patch935: openssh-6.6p1-s390-closefrom.patch
# expose more information to PAM (#1312304)
Patch938: openssh-7.4p1-expose-pam.patch
# Move MAX_DISPLAYS to a configuration option (#1341302)
Patch939: openssh-6.6p1-x11-max-displays.patch
# Add systemd stuff so it can track running service (#1381997)
Patch942: openssh-6.6p1-systemd.patch
# Permit root login to preserve backward compatibility
Patch943: openssh-7.4p1-permit-root-login.patch
# Restore TCP wrappers support
Patch944: openssh-7.4p1-debian-restore-tcp-wrappers.patch
# Set sane whitelist for PKCS#11 modules in ssh-agent
Patch945: openssh-7.4p1-pkcs11-whitelist.patch
# Allow legacy algorithms and formats for key exchange after rebase
Patch946: openssh-7.4p1-legacy-algorithms.patch
# Show more fingerprints
Patch947: openssh-7.4p1-show-more-fingerprints.patch
# Fix newline in the end of server ident banner (upstream 5b9070)
Patch948: openssh-7.4p1-newline-banner.patch
# Do not utilize SHA1 by default for digital signatures (#1322911)
Patch949: openssh-7.4p1-sha2-signatures.patch
# Canonize pkcs11 provider path when removing smartcard (#2682)
Patch950: openssh-7.4p1-canonize-pkcs11-provider.patch
# Do not segfault sshd if it loads RSA1 keys (#2686)
Patch951: openssh-7.4p1-rsa1-segfault.patch
# OpenSSH 7.5 fixes CBC cipher weakness
Patch952: openssh-7.4p1-cbc-weakness.patch
# sandbox-seccomp filter is not denying socketcall() on ppc64le (#1443916)
Patch953: openssh-7.4p1-sandbox-ppc64le.patch
# ControlPath too long should not be fatal (#1447561)
Patch954: openssh-7.4p1-ControlPath_too_long.patch
# sandbox-seccomp for ibmca engine from upstream (#1451809)
Patch955: openssh-7.4p1-sandbox-ibmca.patch
# Back to UseDNS=yes by default (#1478175)
Patch956: openssh-7.4p1-usedns-yes.patch
# Clatch between ClientAlive timeouts and rekeying (#1480510)
Patch957: openssh-7.4p1-rekeying-timeouts.patch
# WinSCP 5.10+ compatibility (#1496808)
Patch958: openssh-7.4p1-winscp-compat.patch
# SSH AuthorizedKeysCommand hangs when output is too large (#1496467)
Patch959: openssh-7.4p1-authorized_keys_command.patch
# Fix for CVE-2017-15906 (#1517226)
Patch960: openssh-7.5p1-sftp-empty-files.patch

# This is the patch that adds GSI support
# Based on http://grid.ncsa.illinois.edu/ssh/dl/patch/openssh-6.6p1.patch
Patch98: openssh-7.4p1-gsissh.patch

License: BSD
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: /sbin/nologin

%if %{ldap}
BuildRequires: openldap-devel
%endif
BuildRequires: autoconf, automake, perl, zlib-devel
BuildRequires: audit-libs-devel >= 2.0.5
BuildRequires: util-linux, groff
BuildRequires: pam-devel
BuildRequires: tcp_wrappers-devel
BuildRequires: fipscheck-devel >= 1.3.0
BuildRequires: openssl-devel >= 0.9.8j
BuildRequires: systemd-devel

%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{gsi}
BuildRequires: globus-gss-assist-devel >= 8
BuildRequires: globus-gssapi-gsi-devel >= 12.12
BuildRequires: globus-common-devel >= 14
BuildRequires: globus-usage-devel >= 3
%endif

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{WITH_SELINUX}
Conflicts: selinux-policy < 3.13.1-92
Requires: libselinux >= 1.27.7
BuildRequires: libselinux-devel >= 1.27.7
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

BuildRequires: xauth

%package clients
Summary: SSH client applications with GSI authentication
Provides: gsissh-clients = %{version}-%{release}
Obsoletes: gsissh-clients < 5.8p2-2
Group: Applications/Internet
Requires: %{name} = %{version}-%{release}
Requires: fipscheck-lib%{_isa} >= 1.3.0

%package server
Summary: SSH server daemon with GSI authentication
Provides: gsissh-server = %{version}-%{release}
Obsoletes: gsissh-server < 5.8p2-2
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires: pam >= 1.0.1-3
Requires: fipscheck-lib%{_isa} >= 1.3.0
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features.

This version of OpenSSH has been modified to support GSI authentication.

This package includes the core files necessary for both the gsissh
client and server. To make this package useful, you should also
install gsi-openssh-clients, gsi-openssh-server, or both.

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

%patch103 -p1 -b .packet

%if %{WITH_SELINUX}
%patch400 -p1 -b .role-mls
%patch404 -p1 -b .privsep-selinux
%endif

%if %{ldap}
%patch501 -p1 -b .ldap
%endif
%patch502 -p1 -b .keycat

%patch601 -p1 -b .ip-opts
%patch604 -p1 -b .keyperm
%patch606 -p1 -b .ipv6man
%patch607 -p1 -b .sigpipe
%patch609 -p1 -b .x11

# drop? %patch701 -p1 -b .exit-deadlock
%patch702 -p1 -b .progress
%patch703 -p1 -b .grab-info
# investigate - https://bugzilla.redhat.com/show_bug.cgi?id=205842
# probably not needed anymore %patch704 -p1 -b .edns
%patch706 -p1 -b .localdomain
%patch707 -p1 -b .redhat
%patch708 -p1 -b .entropy
%patch709 -p1 -b .vendor
%patch711 -p1 -b .log-usepam-no
%patch712 -p1 -b .evp-ctr
%patch713 -p1 -b .ctr-cavs
%patch714 -p1 -b .kdf-cavs

%patch800 -p1 -b .gsskex
%patch801 -p1 -b .force_krb

%patch900 -p1 -b .canohost
%patch901 -p1 -b .kuserok
%patch902 -p1 -b .ccache_name
%patch903 -p1 -b .gss-strict
%patch905 -p1 -b .legacy-ssh-copy-id
%patch906 -p1 -b .fromto-remote
%patch914 -p1 -b .log-sftp-only
%patch918 -p1 -b .log-in-chroot
%patch919 -p1 -b .mls-labels
%patch802 -p1 -b .GSSAPIEnablek5users
%patch803 -p1 -b .k5login
%patch920 -p1 -b .sshd-t
%patch921 -p1 -b .sftp-force-mode
%patch924 -p1 -b .memory-problems
%patch925 -p1 -b .allowGroups
%patch928 -p1 -b .gsskexalg
%patch935 -p1 -b .s390
%patch938 -p1 -b .expose-pam
%patch939 -p1 -b .x11max
%patch942 -p1 -b .patch
%patch943 -p1 -b .permit-root
%patch944 -p1 -b .tcp_wrappers
%patch945 -p1 -b .pkcs11-whitelist
%patch946 -p1 -b .legacy
%patch947 -p1 -b .fingerprint
%patch948 -p1 -b .newline-banner
%patch949 -p1 -b .sha2
%patch950 -p1 -b .smartcard
%patch951 -p1 -b .rsa1
%patch952 -p1 -b .cbc
%patch953 -p1 -b .seccomp
%patch954 -p1 -b .ControlPath
%patch955 -p1 -b .ibmca
%patch956 -p1 -b .usedns
%patch957 -p1 -b .rekey-timeout
%patch958 -p1 -b .winscp
%patch959 -p1 -b .large-command
%patch960 -p1 -b .sftp-empty

%patch200 -p1 -b .audit
%patch202 -p1 -b .audit-race
%patch700 -p1 -b .fips

%patch100 -p1 -b .coverity

%patch98 -p1 -b .gsi

sed 's/sshd.pid/gsisshd.pid/' -i pathnames.h
sed 's!$(piddir)/sshd.pid!$(piddir)/gsisshd.pid!' -i Makefile.in

cp -p %{SOURCE99} .

autoreconf

%build
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%if %{pie}
%ifarch s390 s390x sparc sparcv9 sparc64
CFLAGS="$CFLAGS -fPIC"
%else
CFLAGS="$CFLAGS -fpic"
%endif
LDFLAGS="$LDFLAGS -pie -z relro -z now"

export CFLAGS
export LDFLAGS

%endif
%if %{kerberos5}
if test -r /etc/profile.d/krb5-devel.sh ; then
	source /etc/profile.d/krb5-devel.sh
fi
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
	--with-default-path=/usr/local/bin:/usr/bin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin \
	--with-privsep-path=%{_var}/empty/gsisshd \
	--enable-vendor-patchlevel="RHEL7-%{openssh_ver}-%{openssh_rel}" \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
	--with-ipaddr-display \
	--with-systemd \
	--with-ssh1 \
%if %{ldap}
	--with-ldap \
%endif
	--with-pam \
%if %{WITH_SELINUX}
	--with-selinux --with-audit=linux \
%ifnarch ppc
	--with-sandbox=seccomp_filter \
%else
	--with-sandbox=rlimit \
%endif
%endif
%if %{kerberos5}
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
	--without-kerberos5 \
%endif
%if %{gsi}
	--with-gsi \
%else
	--without-gsi \
%endif
%if %{libedit}
	--with-libedit
%else
	--without-libedit
%endif

make SSH_PROGRAM=%{_bindir}/gsissh \
     ASKPASS_PROGRAM=%{_libexecdir}/openssh/ssh-askpass

# Add generation of HMAC checksums of the final stripped binaries
%global __spec_install_post \
    %%{?__debug_package:%%{__debug_install_post}} \
    %%{__arch_install_post} \
    %%{__os_install_post} \
    fipshmac -d $RPM_BUILD_ROOT%{_libdir}/fipscheck $RPM_BUILD_ROOT%{_bindir}/gsissh $RPM_BUILD_ROOT%{_sbindir}/gsisshd \
%{nil}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/gsissh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/gsissh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/gsisshd
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gsissh/ldap.conf

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/sysconfig/
install -d $RPM_BUILD_ROOT%{_libexecdir}/gsissh
install -d $RPM_BUILD_ROOT%{_libdir}/fipscheck
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/gsisshd
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/gsisshd
install -m755 %{SOURCE13} $RPM_BUILD_ROOT/%{_sbindir}/sshd-keygen
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 %{SOURCE9} $RPM_BUILD_ROOT/%{_unitdir}/gsisshd@.service
install -m644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/gsisshd.socket
install -m644 %{SOURCE11} $RPM_BUILD_ROOT/%{_unitdir}/gsisshd.service
install -m644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/gsisshd-keygen.service

rm $RPM_BUILD_ROOT%{_bindir}/ssh-add
rm $RPM_BUILD_ROOT%{_bindir}/ssh-agent
rm $RPM_BUILD_ROOT%{_bindir}/ssh-keyscan
rm $RPM_BUILD_ROOT%{_libexecdir}/gsissh/ctr-cavstest
rm $RPM_BUILD_ROOT%{_libexecdir}/gsissh/ssh-cavs
rm $RPM_BUILD_ROOT%{_libexecdir}/gsissh/ssh-cavs_driver.pl
rm $RPM_BUILD_ROOT%{_libexecdir}/gsissh/ssh-ldap-helper
rm $RPM_BUILD_ROOT%{_libexecdir}/gsissh/ssh-ldap-wrapper
rm $RPM_BUILD_ROOT%{_libexecdir}/gsissh/ssh-keycat
rm $RPM_BUILD_ROOT%{_libexecdir}/gsissh/ssh-pkcs11-helper
rm $RPM_BUILD_ROOT%{_mandir}/man1/ssh-add.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/ssh-agent.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/ssh-keyscan.1*
rm $RPM_BUILD_ROOT%{_mandir}/man5/ssh-ldap.conf.5*
rm $RPM_BUILD_ROOT%{_mandir}/man8/ssh-ldap-helper.8*
rm $RPM_BUILD_ROOT%{_mandir}/man8/ssh-pkcs11-helper.8*

for f in $RPM_BUILD_ROOT%{_bindir}/* \
	 $RPM_BUILD_ROOT%{_sbindir}/* \
	 $RPM_BUILD_ROOT%{_mandir}/man*/* ; do
    mv $f `dirname $f`/gsi`basename $f`
done
ln -sf gsissh $RPM_BUILD_ROOT%{_bindir}/gsislogin
ln -sf gsissh.1 $RPM_BUILD_ROOT%{_mandir}/man1/gsislogin.1

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group ssh_keys >/dev/null || groupadd -r ssh_keys || :

%pre server
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :

%post server
%systemd_post gsisshd.service gsisshd.socket

%preun server
%systemd_preun gsisshd.service gsisshd.socket

%postun server
%systemd_postun_with_restart gsisshd.service

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license LICENCE LICENSE.globus_usage
%doc CREDITS ChangeLog INSTALL OVERVIEW PROTOCOL* README README.platform README.privsep README.tun README.dns README.sshd-and-gsisshd TODO
%attr(0755,root,root) %dir %{_sysconfdir}/gsissh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/gsissh/moduli
%attr(0755,root,root) %{_bindir}/gsissh-keygen
%attr(0644,root,root) %{_mandir}/man1/gsissh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/gsissh
%attr(2755,root,ssh_keys) %{_libexecdir}/gsissh/ssh-keysign
%attr(0644,root,root) %{_mandir}/man8/gsissh-keysign.8*

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/gsissh
%attr(0644,root,root) %{_libdir}/fipscheck/gsissh.hmac
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
%attr(0755,root,root) %{_sbindir}/gsisshd
%attr(0755,root,root) %{_sbindir}/gsisshd-keygen
%attr(0644,root,root) %{_libdir}/fipscheck/gsisshd.hmac
%attr(0755,root,root) %{_libexecdir}/gsissh/sftp-server
%attr(0644,root,root) %{_mandir}/man5/gsisshd_config.5*
%attr(0644,root,root) %{_mandir}/man5/gsimoduli.5*
%attr(0644,root,root) %{_mandir}/man8/gsisshd.8*
%attr(0644,root,root) %{_mandir}/man8/gsisftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/gsissh/sshd_config
%attr(0644,root,root) %config(noreplace) /etc/pam.d/gsisshd
%attr(0640,root,root) %config(noreplace) /etc/sysconfig/gsisshd
%attr(0644,root,root) %{_unitdir}/gsisshd.service
%attr(0644,root,root) %{_unitdir}/gsisshd@.service
%attr(0644,root,root) %{_unitdir}/gsisshd.socket
%attr(0644,root,root) %{_unitdir}/gsisshd-keygen.service

%changelog
* Tue Apr 10 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 7.4p1-2
- Based on openssh-7.4p1-16.el7

* Sun Nov 12 2017 Mattias Ellert <nattias.ellert@physics.uu.se> - 7.4p1-1
- Based on openssh-7.4p1-13.el7_4

* Mon Jul 31 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.6.1p1-8
- Based on openssh-6.6.1p1-35.el7_3
- Update GSI patch with more openssl 1.1.0 fixes from Globus

* Fri Feb 24 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.6.1p1-7
- Based on openssh-6.6.1p1-33.el7_3

* Thu Dec 15 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.6.1p1-6
- Adding mechanism OID negotiation with the introduction of micv2 OID

* Wed Dec 14 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.6.1p1-5
- Based on openssh 6.6.1p1-31.el7

* Sun Jun 26 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.6.1p1-4
- Based on openssh-6.6.1p1-25.el7_2

* Tue Jan 19 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.6.1p1-3
- Based on openssh-6.6.1p1-23.el7_2

* Wed Aug 05 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.6.1p1-2
- Fix typos in gsisshd.service file

* Sun Jul 05 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.6.1p1-1
- Based on openssh-6.6.1p1-12.el7_1

* Wed Jul 16 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.4p1-2
- Based on openssh-6.4p1-8.el7

* Tue Jan 28 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.4p1-1
- Based on openssh-6.4p1-1.el7

* Thu Dec 12 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.2p2-4
- Based on openssh-6.2p2-7.fc19

* Tue Nov 26 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.2p2-3
- Based on openssh-6.2p2-6.fc19

* Fri Aug 23 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.2p2-2
- Based on openssh-6.2p2-5.fc19

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2p2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.2p2-1
- Based on openssh-6.2p2-3.fc19

* Fri Apr 26 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.2p1-3
- Based on openssh-6.2p1-4.fc19

* Wed Apr 17 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.2p1-2
- Based on openssh-6.2p1-3.fc19

* Wed Apr 10 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.2p1-1
- Based on openssh-6.2p1-2.fc19

* Sat Apr 06 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1p1-5
- Based on openssh-6.1p1-7.fc19
- Security fix for vulnerability
    http://grid.ncsa.illinois.edu/ssh/pamuserchange-2013-01.adv
    https://wiki.egi.eu/wiki/SVG:Advisory-SVG-2013-5168

* Tue Feb 26 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1p1-4
- Based on openssh-6.1p1-6.fc18

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1p1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1p1-3
- Based on openssh-6.1p1-4.fc18

* Thu Nov 01 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1p1-2
- Based on openssh-6.1p1-2.fc18

* Tue Sep 18 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.1p1-1
- Based on openssh-6.1p1-1.fc18

* Mon Aug 13 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.0p1-1
- Based on openssh-6.0p1-1.fc18

* Mon Aug 13 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9p1-7
- Based on openssh-5.9p1-26.fc17

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9p1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9p1-6
- Based on openssh-5.9p1-22.fc17

* Wed Feb 08 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9p1-5
- Based on openssh-5.9p1-19.fc17

* Sun Jan 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9p1-4
- Drop openssh-5.8p2-unblock-signals.patch - not needed for GT >= 5.2
- Based on openssh-5.9p1-16.fc17

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9p1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9p1-3
- Based on openssh-5.9p1-13.fc17

* Thu Nov 17 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9p1-2
- Based on openssh-5.9p1-11.fc17

* Thu Oct 06 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.9p1-1
- Initial packaging
- Based on openssh-5.9p1-7.fc17
