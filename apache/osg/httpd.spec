%define contentdir /var/www
%define suexec_caller apache
%define mmn 20051115
%define vstring CentOS 
%define distro CentOS Enterprise Linux
# Minimum version of OpenSSL having support for the secure TLS reneg API
%define opensslver 0.9.8e-12.el5_4.4

Summary: Apache HTTP Server
Name: httpd
Version: 2.2.3
Release: 45%{?dist}.1
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/httpd/httpd-%{version}.tar.gz
Source1: centos_index.html
Source3: httpd.logrotate
Source4: httpd.init
Source5: httpd.sysconf
Source8: centos_powered_by_rh.png
Source10: httpd.conf
Source11: ssl.conf
Source12: welcome.conf
Source13: manual.conf
Source14: proxy_ajp.conf
# Documentation
Source30: migration.xml
Source31: migration.css
Source32: html.xsl
Source33: README.confd
# build/scripts patches
Patch1: httpd-2.1.10-apctl.patch
Patch2: httpd-2.1.10-apxs.patch
Patch3: httpd-2.0.45-deplibs.patch
Patch4: httpd-2.1.10-disablemods.patch
Patch5: httpd-2.1.10-layout.patch
Patch6: httpd-2.2.2-ac260.patch
# Features/functional changes
Patch20: httpd-2.0.48-release.patch
Patch21: httpd-2.0.40-xfsz.patch
Patch22: httpd-2.1.10-pod.patch
Patch23: httpd-2.0.45-export.patch
Patch24: httpd-2.0.48-corelimit.patch
Patch25: httpd-2.0.54-selinux.patch
Patch26: httpd-2.2.3-proxysessid.patch
Patch27: httpd-2.2.3-proxypmatch.patch
Patch28: httpd-2.2.3-nbchunk.patch
Patch29: httpd-2.2.3-sslrenegsize.patch
Patch30: httpd-2.2.3-ldapdyngrp.patch
Patch31: httpd-2.2.3-modsubst.patch
# Bug fixes
Patch50: httpd-2.0.45-encode.patch
Patch54: httpd-2.2.0-authnoprov.patch
Patch55: httpd-2.2.3-proxyopt.patch
Patch56: httpd-2.2.3-proxyoride.patch
Patch57: httpd-2.0.52-logresline.patch
Patch58: httpd-2.2.3-ldappool.patch
Patch59: httpd-2.2.3-ssldynlock.patch
Patch60: httpd-2.0.52-escaperrs.patch
Patch61: httpd-2.2.3-eventdlock.patch
Patch62: httpd-2.2.3-hdrsedit.patch
Patch63: httpd-2.2.3-dummyreq.patch
Patch64: httpd-2.2.3-proxysslhost.patch
Patch65: httpd-2.2.3-pr46428.patch
Patch66: httpd-2.2.3-cgierror.patch
Patch67: httpd-2.2.3-pr43562.patch
Patch68: httpd-2.2.3-logports.patch
Patch69: httpd-2.2.3-graceful-ebadf.patch
Patch70: httpd-2.2.3-sslrenegredir.patch
Patch71: httpd-2.2.3-rewritelll.patch
Patch72: httpd-2.2.3-extfiltereos.patch
Patch73: httpd-2.2.3-cgierror2.patch
Patch74: httpd-2.2.3-pngmagic.patch
Patch75: httpd-2.2.3-defpidlog.patch
Patch76: httpd-2.2.3-rewritedpi.patch
Patch77: httpd-2.2.3-ldapremuser.patch
Patch78: httpd-2.2.3-ldappassauth.patch
Patch79: httpd-2.2.3-noxpad.patch
Patch80: httpd-2.2.3-ajpbuffer.patch
Patch81: httpd-2.2.3-sslflush.patch
Patch82: httpd-2.2.3-expectnoka.patch
Patch83: httpd-2.2.3-ssloidval.patch
Patch84: httpd-2.2.3-sslreneg.patch
Patch85: httpd-2.2.3-pr49328.patch
Patch86: httpd-2.2.3-aboverflow.patch
Patch87: httpd-2.2.3-pr40232.patch
Patch88: httpd-2.2.3-davputfail.patch
Patch89: httpd-2.2.3-dbdcleanup.patch
Patch90: httpd-2.2.3-sslproxyio.patch
# Security Fixes
Patch100: httpd-2.2.3-CVE-2006-5752.patch
Patch101: httpd-2.2.3-CVE-2007-1863.patch
Patch102: httpd-2.2.3-CVE-2007-3304.patch
Patch103: httpd-2.2.3-CVE-2007-3847.patch
Patch104: httpd-2.2.3-CVE-2007-5000.patch
Patch105: httpd-2.2.3-CVE-2007-4465.patch
Patch106: httpd-2.2.3-CVE-2007-6421.patch
Patch107: httpd-2.2.3-CVE-2007-6422.patch
Patch108: httpd-2.2.3-CVE-2007-6388.patch
Patch109: httpd-2.2.3-prftpcset.patch
Patch110: httpd-2.2.3-CVE-2007-3304-update.patch
Patch111: httpd-2.2.3-CVE-2008-2939.patch
Patch112: httpd-2.2.3-CVE-2008-1678.patch
Patch113: httpd-2.2.3-CVE-2009-1195.patch
Patch114: httpd-2.2.3-ssicompat.patch
Patch115: httpd-2.2.10-CVE-2009-1890.patch
Patch116: httpd-2.2.10-CVE-2009-1891.patch
Patch117: httpd-2.2.3-CVE-2009-3555.patch
Patch118: httpd-2.2.3-CVE-2009-3094.patch
Patch119: httpd-2.2.3-CVE-2009-3095.patch
Patch120: httpd-2.2.3-CVE-2009-3555-p2.patch
Patch121: httpd-2.2.3-CVE-2010-0434.patch
Patch122: httpd-2.2.3-CVE-2010-0408.patch
Patch123: httpd-2.2.3-CVE-2010-1452.patch
Patch124: httpd-2.2.3-CVE-2010-2791.patch
# Rebases
Patch200: httpd-2.2.3-proxy229.patch
Patch201: httpd-2.2.3-cache229.patch
Patch202: httpd-2.2.3-deflate2215.patch
# VDT
Patch300: vdt-apachectl.patch

License: Apache Software License
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: autoconf, perl, pkgconfig, xmlto >= 0.0.11, findutils
BuildRequires: db4-devel, expat-devel, zlib-devel, libselinux-devel
BuildRequires: apr-devel >= 1.2.0, apr-util-devel >= 1.2.0, pcre-devel >= 5.0, 
Requires: /etc/mime.types, gawk, /usr/share/magic.mime, /usr/bin/find
Requires: initscripts >= 8.36
Obsoletes: httpd-suexec
Prereq: /sbin/chkconfig, /bin/mktemp, /bin/rm, /bin/mv
Prereq: sh-utils, textutils, /usr/sbin/useradd
Provides: webserver
Provides: httpd-mmn = %{mmn}
Obsoletes: apache, secureweb, mod_dav, mod_gzip, stronghold-apache, stronghold-htdocs
Obsoletes: mod_put, mod_roaming
Conflicts: pcre < 4.0

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package devel
Group: Development/Libraries
Summary: Development tools for the Apache HTTP server.
Obsoletes: secureweb-devel, apache-devel, stronghold-apache-devel
Requires: apr-devel, apr-util-devel, pkgconfig
Requires: httpd = %{version}-%{release}

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server.
Requires: httpd = %{version}-%{release}
Obsoletes: secureweb-manual, apache-manual

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/2.2/.

%package -n mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP server
Epoch: 1
BuildRequires: openssl-devel >= %{opensslver}, distcache-devel
Requires(post): openssl >= 0.9.7f-4, /bin/cat
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmn}
Requires: openssl >= %{opensslver}
Obsoletes: stronghold-mod_ssl

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%prep
%setup -q
%patch1 -p1 -b .apctl
%patch2 -p1 -b .apxs
%patch3 -p1 -b .deplibs
%patch4 -p1 -b .disablemods
%patch5 -p1 -b .layout
%patch6 -p1 -b .ac260

%patch21 -p0 -b .xfsz
%patch22 -p1 -b .pod
%patch23 -p1 -b .export
%patch24 -p1 -b .corelimit
%patch25 -p1 -b .selinux
%patch26 -p1 -b .proxysessid
%patch27 -p1 -b .proxypmatch
%patch28 -p1 -b .nbchunk
%patch29 -p1 -b .sslrenegsize
%patch30 -p1 -b .ldapdyngrp
%patch31 -p1 -b .modsubst

# no -b to prevent droplets in install root
%patch50 -p1
%patch54 -p1 -b .authnoprov
%patch55 -p1 -b .proxyopt
%patch56 -p1 -b .proxyoride
%patch57 -p1 -b .logresline
%patch58 -p1 -b .ldappool
%patch59 -p1 -b .ssldynlock
%patch60 -p1 -b .escaperrs
%patch61 -p1 -b .eventdlock
%patch62 -p1 -b .hdrsedit
%patch63 -p1 -b .dummyreq
%patch64 -p1 -b .proxysslhost
%patch65 -p1 -b .pr46428
%patch66 -p1 -b .cgierror
%patch67 -p1 -b .pr43562
%patch68 -p1 -b .logports
%patch69 -p1 -b .graceful-ebadf
%patch70 -p1 -b .sslrenegredir
%patch71 -p1 -b .rewritelll
%patch72 -p1 -b .extfiltereos
%patch73 -p1 -b .cgierror2
%patch74 -p1 -b .pngmagic
%patch75 -p1 -b .defpidlog
%patch76 -p1 -b .rewritedpi
%patch77 -p1 -b .ldapremuser
%patch78 -p1 -b .ldappassauth
%patch79 -p1 -b .noxpad
#patch80 applied after proxy changes
%patch81 -p1 -b .sslflush
#patch82 applied after proxy changes
%patch83 -p1 -b .ssloidval
#patch84 applied after mod_ssl security fixes
%patch85 -p1 -b .pr49328
%patch86 -p1 -b .aboverflow
%patch87 -p1 -b .pr40232
%patch88 -p1 -b .davputfail
%patch89 -p1 -b .dbdcleanup
%patch90 -p1 -b .sslproxyio

%patch100 -p1 -b .cve5752
%patch101 -p1 -b .cve1853
%patch102 -p1 -b .cve3304
%patch103 -p1 -b .cve3847
%patch104 -p1 -b .cve5000
%patch105 -p1 -b .cve4465
%patch106 -p1 -b .cve6421
%patch107 -p1 -b .cve6422
%patch108 -p1 -b .cve6388
%patch109 -p1 -b .prftpcset
%patch110 -p1 -b .cve3304-update
%patch111 -p1 -b .cve2939
%patch112 -p1 -b .cve1678
%patch113 -p1 -b .cve1195
# Not a security fix, but a fix for the -1195 patch:
%patch114 -p1 -b .ssicompat
#patch115 applied after proxy changes
%patch116 -p1 -b .cve1891
%patch117 -p1 -b .cve3555
%patch118 -p1 -b .cve3094
%patch119 -p1 -b .cve3095
%patch120 -p1 -b .cve3555-p2
%patch121 -p1 -b .cve0434
%patch122 -p1 -b .cve0408
%patch123 -p1 -b .cve1452
#patch124 applied after proxy changes

# Rebases -- any changes to proxy/cache modules must come later:
%patch200 -p1 -b .proxy229
%patch201 -p1 -b .cache229
%patch202 -p1 -b .deflate2215

%patch80 -p1 -b .ajpbuffer
%patch82 -p1 -b .expectnoka

%patch115 -p1 -b .cve1890
%patch124 -p1 -b .cve2791

%patch84 -p1 -b .sslreneg

%patch300 -p1 -b .vdt-apachectl

# Patch in vendor/release string
sed "s/@VENDOR@/%{vstring}/;s/@RELEASE@/%{release}/" < %{PATCH20} | patch -p1 -b -z .release

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}.
   : Update the mmn macro and rebuild.
   exit 1
fi

: Building for '%{distro}' with MMN %{mmn} and vendor string '%{vstring}'

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Limit size of CHANGES to recent history
echo '1,/Changes with Apache MPM/wq' | ed CHANGES

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
	support/apxs.in
# update location of migration guide in apachectl
%{__perl} -pi -e "s:\@docdir\@:%{_docdir}/%{name}-%{version}:g" \
	support/apachectl.in

# Build the migration guide
sed 's/@DISTRO@/%{distro}/' < $RPM_SOURCE_DIR/migration.xml > migration.xml
xmlto -x $RPM_SOURCE_DIR/html.xsl html-nochunks migration.xml
cp $RPM_SOURCE_DIR/migration.css . # make %%doc happy

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
SH_LDFLAGS="-Wl,-z,relro"
export CFLAGS SH_LDFLAGS

# Forcibly disable use of rsync to install (#557049)
export ac_cv_path_RSYNC=

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

function mpmbuild()
{
mpm=$1; shift
mkdir $mpm; pushd $mpm
../configure \
 	--prefix=%{_sysconfdir}/httpd \
 	--exec-prefix=%{_prefix} \
 	--bindir=%{_bindir} \
 	--sbindir=%{_sbindir} \
 	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir}/httpd/conf \
	--includedir=%{_includedir}/httpd \
	--libexecdir=%{_libdir}/httpd/modules \
	--datadir=%{contentdir} \
        --with-installbuilddir=%{_libdir}/httpd/build \
	--with-mpm=$mpm \
        --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
	--enable-suexec --with-suexec \
	--with-suexec-caller=%{suexec_caller} \
	--with-suexec-docroot=%{contentdir} \
	--with-suexec-logfile=%{_localstatedir}/log/httpd/suexec.log \
	--with-suexec-bin=%{_sbindir}/suexec \
	--with-suexec-uidmin=500 --with-suexec-gidmin=100 \
        --enable-pie \
        --with-pcre \
	$*

make %{?_smp_mflags}
popd
}

# Build everything and the kitchen sink with the prefork build
mpmbuild prefork \
        --enable-mods-shared=all \
	--enable-ssl --with-ssl --enable-distcache \
	--enable-proxy \
        --enable-cache --enable-mem-cache \
        --enable-file-cache --enable-disk-cache \
        --enable-ldap --enable-authnz-ldap \
        --enable-cgid \
        --enable-authn-anon --enable-authn-alias

# For the other MPMs, just build httpd and no optional modules
mpmbuild worker --enable-modules=none
mpmbuild event --enable-modules=none

%install
rm -rf $RPM_BUILD_ROOT

# Classify ab and logresolve as section 1 commands, as they are in /usr/bin
mv docs/man/ab.8 docs/man/ab.1
mv docs/man/logresolve.8 docs/man/logresolve.1

pushd prefork
make DESTDIR=$RPM_BUILD_ROOT install
popd

# install alternative MPMs
install -m 755 worker/httpd $RPM_BUILD_ROOT%{_sbindir}/httpd.worker
install -m 755 event/httpd $RPM_BUILD_ROOT%{_sbindir}/httpd.event

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README
for f in ssl.conf welcome.conf manual.conf proxy_ajp.conf; do
  install -m 644 $RPM_SOURCE_DIR/$f $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
done

rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf
install -m 644 $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 $RPM_SOURCE_DIR/httpd.sysconf \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/httpd

# for holding mod_dav lock database
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dav

# create a prototype session cache
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/mod_ssl
touch $RPM_BUILD_ROOT%{_localstatedir}/cache/mod_ssl/scache.{dir,pag,sem}

# create cache root
mkdir $RPM_BUILD_ROOT%{_localstatedir}/cache/mod_proxy

# move utilities to /usr/bin
mv $RPM_BUILD_ROOT%{_sbindir}/{ab,htdbm,logresolve,htpasswd,htdigest} \
   $RPM_BUILD_ROOT%{_bindir}

# Make the MMN accessible to module packages
echo %{mmn} > $RPM_BUILD_ROOT%{_includedir}/httpd/.mmn

# docroot
mkdir $RPM_BUILD_ROOT%{contentdir}/html
install -m 644 $RPM_SOURCE_DIR/centos_index.html \
	$RPM_BUILD_ROOT%{contentdir}/error/noindex.html

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# added for branding
install -m 644 %{SOURCE8} \
        $RPM_BUILD_ROOT%{contentdir}/icons/powered_by_rh.png

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# logs
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/logs
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/httpd

# symlinks for /etc/httpd
ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s ../..%{_localstatedir}/run $RPM_BUILD_ROOT/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

# install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m755 $RPM_SOURCE_DIR/httpd.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/httpd
%{__perl} -pi -e "s:\@docdir\@:%{_docdir}/%{name}-%{version}:g" \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/httpd	

# install log rotation stuff
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m644 $RPM_SOURCE_DIR/httpd.logrotate \
	$RPM_BUILD_ROOT/etc/logrotate.d/httpd

# fix man page paths
sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/httpd/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/httpd/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|/var/log/httpd/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|/var/log/httpd/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|/var/run/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/httpd|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/special.mk

# Remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/ap?-config \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,dbmmanage,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}

# Make suexec a+rw so it can be stripped.  %%files lists real permissions
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/suexec

%pre
# Add the "apache" user
/usr/sbin/useradd -c "Apache" -u 48 \
	-s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :

%triggerpostun -- apache < 2.0, stronghold-apache < 2.0
/sbin/chkconfig --add httpd

# Prevent removal of index.html on upgrades from 1.3
%triggerun -- apache < 2.0, stronghold-apache < 2.0
if [ -r %{contentdir}/index.html -a ! -r %{contentdir}/index.html.rpmold ]; then
  mv %{contentdir}/index.html %{contentdir}/index.html.rpmold
fi

%post
# Register the httpd service
/sbin/chkconfig --add httpd

%preun
if [ $1 = 0 ]; then
	/sbin/service httpd stop > /dev/null 2>&1
	/sbin/chkconfig --del httpd
fi

%define sslcert %{_sysconfdir}/pki/tls/certs/localhost.crt
%define sslkey %{_sysconfdir}/pki/tls/private/localhost.key

%post -n mod_ssl
umask 077

if [ ! -f %{sslkey} ] ; then
%{_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 1024 > %{sslkey} 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=localhost.localdomain
fi

if [ ! -f %{sslcert} ] ; then
cat << EOF | %{_bindir}/openssl req -new -key %{sslkey} \
         -x509 -days 365 -set_serial $RANDOM \
         -out %{sslcert} 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF
fi

%check
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi

# Verify that the same modules were built into the httpd binaries
./prefork/httpd -l | grep -v prefork > prefork.mods
for mpm in worker; do
  ./${mpm}/httpd -l | grep -v ${mpm} > ${mpm}.mods
  if ! diff -u prefork.mods ${mpm}.mods; then
    : Different modules built into httpd binaries, will not proceed
    exit 1
  fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc migration.html migration.css

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/welcome.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy_ajp.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic

%config(noreplace) %{_sysconfdir}/logrotate.d/httpd
%config %{_sysconfdir}/rc.d/init.d/httpd

%dir %{_sysconfdir}/httpd/conf.d
%{_sysconfdir}/httpd/conf.d/README

%config(noreplace) %{_sysconfdir}/sysconfig/httpd

%{_bindir}/*
%{_sbindir}/ht*
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%attr(4510,root,%{suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod*.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so

%dir %{contentdir}
%dir %{contentdir}/cgi-bin
%dir %{contentdir}/html
%dir %{contentdir}/icons
%dir %{contentdir}/error
%dir %{contentdir}/error/include
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/noindex.html
%config %{contentdir}/error/*.var
%config %{contentdir}/error/include/*.html

%attr(0700,root,root) %dir %{_localstatedir}/log/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/dav
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/mod_proxy

%{_mandir}/man?/*
%exclude %{_mandir}/man8/apxs.8*

%files manual
%defattr(-,root,root)
%{contentdir}/manual
%config %{_sysconfdir}/httpd/conf.d/manual.conf

%files -n mod_ssl
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/mod_ssl
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.sem

%files devel
%defattr(-,root,root)
%{_includedir}/httpd
%{_sbindir}/apxs
%{_mandir}/man8/apxs.8*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh

%changelog
* Wed May  4 2011 Johnny Hughes <johnny@centos.org> - 2.2.3 -45.1.centos
- Rolled in CentOS Branding

* Fri Apr 15 2011 Joe Orton <jorton@redhat.com> - 2.2.3-45.1
- mod_ssl: fix handling of incomplete lines w/rev. proxy (#694158)

* Mon Dec  6 2010 Joe Orton <jorton@redhat.com> - 2.2.3-45
- ab: fail gracefully for OOM allocating stats structures (#645845)
- init script: use $STOP_DELAY as delay before SIGKILL of parent (#644223)
- mod_dav: don't delete the existing resource if a PUT fails (#572910)
- core: don't replace Date header when acting as reverse proxy (#565865)
- mod_dbd: fix pool usage (#633955)

* Thu Aug 19 2010 Joe Orton <jorton@redhat.com> - 2.2.3-44
- mod_ssl: improved fix for SSLRequire's OID() function (#614423)
- add security fixes for CVE-2010-1452, CVE-2010-2791 (#623211)
- mod_deflate: rebase to 2.2.15 (#612211)
- stop multiple invocations of filter init functions (#570628)

* Thu Mar  4 2010 Joe Orton <jorton@redhat.com> - 2.2.3-43
- add security fixes for CVE-2010-0408, CVE-2010-0434 (#570441)

* Tue Feb 23 2010 Joe Orton <jorton@redhat.com> - 2.2.3-42
- require and BR a version of OpenSSL with the secure reneg API (#566659)

* Tue Feb 23 2010 Joe Orton <jorton@redhat.com> - 2.2.3-41
- mod_ssl: add SSLInsecureRenegotiation (#566659)

* Mon Feb  1 2010 Joe Orton <jorton@redhat.com> - 2.2.3-40
- mod_ssl: further fix for OID() handling (#552942)

* Thu Jan 28 2010 Joe Orton <jorton@redhat.com> - 2.2.3-39
- prevent use of rsync during "make install" (#557049)

* Thu Jan 28 2010 Joe Orton <jorton@redhat.com> - 2.2.3-38
- mod_ssl: fix additional case for OID() handling (#552942)
- mod_authnz_ldap: fix handling of empty filter in group defn (#252038)

* Tue Jan 19 2010 Joe Orton <jorton@redhat.com> - 2.2.3-37
- mod_ssl: use ASN1_STRING_print() in SSLRequire's OID() (#552942)

* Sun Dec 20 2009 Joe Orton <jorton@redhat.com> - 2.2.3-36
- mod_ssl: add further mitigation for CVE-2009-3555 (#534042)
- add mod_substitute (#539256)

* Fri Dec 18 2009 Joe Orton <jorton@redhat.com> - 2.2.3-35.el5
- mod_authnz_ldap: dynamic group fixes (#252038)

* Thu Dec 17 2009 Joe Orton <jorton@redhat.com> - 2.2.3-34.el5
- mod_authnz_ldap: add support for dynamic group lookup (#252038)

* Wed Dec 16 2009 Joe Orton <jorton@redhat.com> - 2.2.3-33.el5
- add security fixes for CVE-2009-3555, CVE-2009-3094,
  CVE-2009-3095 (#534042)

* Wed Dec  2 2009 Joe Orton <jorton@redhat.com> - 2.2.3-32.el5
- fix hard-coded default pidfile to match default config (#505002)
- mod_ssl: fix potential hang in renegotiation (#510515)
- drop legacy X-Pad header from short responses (#526110)
- mod_proxy_ajp: fix handling of large uploads (#528640)
- mod_authnz_ldap: add AuthLDAPRemoteUserAttribute directive (#520838)
- mod_rewrite: add DiscardPathInfo flag (#517500)
- mod_authnz_ldap: don't fail authz if no ldap-* configured (#448350)
- disable keepalive for Expect: 100-continue and error response (#533407)

* Tue Jul 14 2009 Joe Orton <jorton@redhat.com> 2.2.3-31.el5
- mod_rewrite: correct backport of URI escaping fix (#480604)

* Fri Jul 10 2009 Joe Orton <jorton@redhat.com> 2.2.3-30.el5
- add security fixes for CVE-2009-1890, CVE-2009-1891 (#509783)

* Mon Jun 22 2009 Joe Orton <jorton@redhat.com> 2.2.3-29.el5
- add image/png to conf/magic (#240844)

* Tue Jun 16 2009 Joe Orton <jorton@redhat.com> 2.2.3-28.el5
- fix backwards compat for CVE-2009-1195 fix (#502998)

* Wed May 20 2009 Joe Orton <jorton@redhat.com> 2.2.3-27.el5
- mod_cgi, mod_cgid: fix logging on input read error (#498170)
- mod_rewrite: don't serialize logfile access (#493023)
- mod_ext_filter: fix spurious error log output (#479463)

* Fri May 15 2009 Joe Orton <jorton@redhat.com> 2.2.3-26.el5
- add security fixes for CVE-2008-1678, CVE-2009-1195 (#499285)

* Fri Apr 17 2009 Joe Orton <jorton@redhat.com> 2.2.3-25.el5
- mod_rewrite: fix URI escaping with [P] in directory context (#480604)
- mod_cgi: fix headers/status in error responses (#480932)
- mod_speling: fix handling of directory names (#485524)
- init script: use ${pidfile} in more places (#491135)
- mod_log_config: support remote/local with 'p' format (#493070)
- remove Obsolete for mod_jk (#493592)
- mod_ssl: fix SSL per-dir-reneg buffering with internal redirects (#488886)
- fix spurious error messages on graceful restart (#233955)

* Wed Mar 18 2009 Joe Orton <jorton@redhat.com> 2.2.3-24.el5
- mod_ssl: add SSLRenegBufferSize directive (#479806)

* Fri Feb  6 2009 Joe Orton <jorton@redhat.com> 2.2.3-23.el5
- mod_proxy: set c->remote_host for backend SSL connection (#479410)

* Wed Nov 12 2008 Joe Orton <jorton@redhat.com> 2.2.3-22.el5
- add security fixes for CVE-2008-2939 (#468841)
- note that the mod_proxy 2.2.9 rebase fixed CVE-2008-2634

* Tue Oct 21 2008 Joe Orton <jorton@redhat.com> 2.2.3-21.el5
- avoid strict-aliasing warnings (#462877)

* Tue Oct 21 2008 Joe Orton <jorton@redhat.com> 2.2.3-20.el5
- mod_proxy: scoreboard access fix (#252024)

* Thu Sep 18 2008 Joe Orton <jorton@redhat.com> 2.2.3-19.el5
- mod_proxy: various backport fixes (#252024)

* Thu Sep 18 2008 Joe Orton <jorton@redhat.com> 2.2.3-17.el5
- fix mod_proxy symbol use

* Mon Sep 15 2008 Joe Orton <jorton@redhat.com> 2.2.3-16.el5
- mod_proxy*, mod_cache*: rebase to 2.2.9 (#252024, #249534,
  #439842)
- backport changes to make chunk filter non-blocking (#454098)

* Fri Sep 12 2008 Joe Orton <jorton@redhat.com> 2.2.3-15.el5
- mod_ldap: fix memory lifetime issues (#440259)
- mod_ssl: configure OpenSSL dynamic lock callbacks (#462044)
- escape the Request-Method in canned error responses (#445888)
- build the event MPM and fix a deadlock therein (#444643)
- mod_headers: support "RequestHeader edit" (#428253)
- use "OPTIONS *" rather than "GET /" in dummy connection (#367981)

* Thu Aug 14 2008 Joe Orton <jorton@redhat.com> 2.2.3-14.el5
- mod_proxy: add ProxyPassMatch support (#449159)

* Mon Jul 21 2008 Joe Orton <jorton@redhat.com> 2.2.3-13.el5
- mod_proxy_balancer: allow alternative string to match for
  stickysession parameter (#439218)
- fix dist tag in Release (#440615)

* Fri Jan 11 2008 Joe Orton <jorton@redhat.com> 2.2.3-12.el5_1.3
- further update to backport for CVE-2007-6421 (#427240)

* Fri Jan 11 2008 Joe Orton <jorton@redhat.com> 2.2.3-12.el5_1.2
- updated backport for CVE-2007-6421 (#427240)

* Mon Jan  7 2008 Joe Orton <jorton@redhat.com> 2.2.3-11.el5_1.1
- add security fixes for CVE-2007-6388, CVE-2007-6421
  and CVE-2007-6422 (#427240)
- add security fix for CVE-2007-4465, CVE-2007-5000 (#421631)
- add security fix for mod_proxy_ftp UTF-7 XSS (#427745)

* Mon Aug  6 2007 Joe Orton <jorton@redhat.com> 2.2.3-11.el5
- mark httpd.conf config(noreplace) (#247881)

* Fri Aug  3 2007 Joe Orton <jorton@redhat.com> 2.2.3-10.el5
- add security fix for CVE-2007-3847 (#250761)

* Wed Aug  1 2007 Joe Orton <jorton@redhat.com> 2.2.3-9.el5
- load mod_version by default (#247881)

* Tue Jun 26 2007 Joe Orton <jorton@redhat.com> 2.2.3-8.el5
- add 'ServerTokens Full-Release' config option (#240857)
- use init script in logrotate postrotate (#241680)
- fix mod_proxy option inheritance (#245719)
- fix ProxyErrorOverride to only affect 4xx, 5xx responses (#240024)
- bump logresolve line buffer length to 10K (#245763)
- add security fixes for CVE-2007-1863, CVE-2007-3304,
  and CVE-2006-5752 (#244666)

* Wed Nov 29 2006 Joe Orton <jorton@redhat.com> 2.2.3-6.el5
- fix path to instdso.sh in special.mk (#217677)
- fix detection of links in "apachectl fullstatus"

* Tue Sep 19 2006 Joe Orton <jorton@redhat.com> 2.2.3-5.el5
- rebuild

* Fri Aug 11 2006 Joe Orton <jorton@redhat.com> 2.2.3-3.el5
- use RHEL branding

* Thu Aug  3 2006 Joe Orton <jorton@redhat.com> 2.2.3-3
- init: use killproc() delay to avoid race killing parent

* Fri Jul 28 2006 Joe Orton <jorton@redhat.com> 2.2.3-2
- update to 2.2.3
- trim %%changelog to >=2.0.52

* Thu Jul 20 2006 Joe Orton <jorton@redhat.com> 2.2.2-8
- fix segfault on dummy connection failure at graceful restart (#199429)

* Wed Jul 19 2006 Joe Orton <jorton@redhat.com> 2.2.2-7
- fix "apxs -g"-generated Makefile
- fix buildconf with autoconf 2.60

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.2-5.1
- rebuild

* Wed Jun  7 2006 Joe Orton <jorton@redhat.com> 2.2.2-5
- require pkgconfig for -devel (#194152)
- fixes for installed support makefiles (special.mk et al)
- BR autoconf

* Fri Jun  2 2006 Joe Orton <jorton@redhat.com> 2.2.2-4
- make -devel package multilib-safe (#192686)

* Thu May 11 2006 Joe Orton <jorton@redhat.com> 2.2.2-3
- build DSOs using -z relro linker flag

* Wed May  3 2006 Joe Orton <jorton@redhat.com> 2.2.2-2
- update to 2.2.2

* Thu Apr  6 2006 Joe Orton <jorton@redhat.com> 2.2.0-6
- rebuild to pick up apr-util LDAP interface fix (#188073)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - (none):2.2.0-5.1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - (none):2.2.0-5.1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Joe Orton <jorton@redhat.com> 2.2.0-5.1
- mod_auth_basic/mod_authn_file: if no provider is configured,
  and AuthUserFile is not configured, decline to handle authn
  silently rather than failing noisily.

* Fri Feb  3 2006 Joe Orton <jorton@redhat.com> 2.2.0-5
- mod_ssl: add security fix for CVE-2005-3357 (#177914)
- mod_imagemap: add security fix for CVE-2005-3352 (#177913)
- add fix for AP_INIT_* designated initializers with C++ compilers
- httpd.conf: enable HTMLTable in default IndexOptions
- httpd.conf: add more "redirect-carefully" matches for DAV clients

* Thu Jan  5 2006 Joe Orton <jorton@redhat.com> 2.2.0-4
- mod_proxy_ajp: fix Cookie handling (Mladen Turk, r358769)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Joe Orton <jorton@redhat.com> 2.2.0-3
- strip manual to just English content

* Mon Dec  5 2005 Joe Orton <jorton@redhat.com> 2.2.0-2
- don't strip C-L from HEAD responses (Greg Ames, #110552)
- load mod_proxy_balancer by default
- add proxy_ajp.conf to load/configure mod_proxy_ajp
- Obsolete mod_jk
- update docs URLs in httpd.conf/ssl.conf

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 2.2.0-1
- update to 2.2.0

* Wed Nov 30 2005 Joe Orton <jorton@redhat.com> 2.1.10-2
- enable mod_authn_alias, mod_authn_anon
- update default httpd.conf

* Fri Nov 25 2005 Joe Orton <jorton@redhat.com> 2.1.10-1
- update to 2.1.10
- require apr >= 1.2.0, apr-util >= 1.2.0

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> 2.0.54-16
- rebuilt against new openssl

* Thu Nov  3 2005 Joe Orton <jorton@redhat.com> 2.0.54-15
- log notice giving SELinux context at startup if enabled
- drop SSLv2 and restrict default cipher suite in default
 SSL configuration

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 2.0.54-14
- mod_ssl: add security fix for SSLVerifyClient (CVE-2005-2700)
- add security fix for byterange filter DoS (CVE-2005-2728)
- add security fix for C-L vs T-E handling (CVE-2005-2088)
- mod_ssl: add security fix for CRL overflow (CVE-2005-1268)
- mod_ldap/mod_auth_ldap: add fixes from 2.0.x branch (upstream #34209 etc)
- add fix for dummy connection handling (#167425)
- mod_auth_digest: fix hostinfo comparison in CONNECT requests
- mod_include: fix variable corruption in nested includes (upstream #12655)
- mod_ssl: add fix for handling non-blocking reads
- mod_ssl: fix to enable output buffering (upstream #35279)
- mod_ssl: buffer request bodies for per-location renegotiation (upstream #12355)

* Sat Aug 13 2005 Joe Orton <jorton@redhat.com> 2.0.54-13
- don't load by default: mod_cern_meta, mod_asis
- do load by default: mod_ext_filter (#165893)

* Thu Jul 28 2005 Joe Orton <jorton@redhat.com> 2.0.54-12
- drop broken epoch deps

* Thu Jun 30 2005 Joe Orton <jorton@redhat.com> 2.0.54-11
- mod_dav_fs: fix uninitialized variable (#162144)
- add epoch to dependencies as appropriate
- mod_ssl: drop dependencies on dev, make
- mod_ssl: mark post script dependencies as such

* Mon May 23 2005 Joe Orton <jorton@redhat.com> 2.0.54-10
- remove broken symlink (Robert Scheck, #158404)

* Wed May 18 2005 Joe Orton <jorton@redhat.com> 2.0.54-9
- add piped logger fixes (w/Jeff Trawick)

* Mon May  9 2005 Joe Orton <jorton@redhat.com> 2.0.54-8
- drop old "powered by Red Hat" logos

* Wed May  4 2005 Joe Orton <jorton@redhat.com> 2.0.54-7
- mod_userdir: fix memory allocation issue (upstream #34588)
- mod_ldap: fix memory corruption issue (Brad Nicholes, upstream #34618)

* Tue Apr 26 2005 Joe Orton <jorton@redhat.com> 2.0.54-6
- fix key/cert locations in post script

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> 2.0.54-5
- create default dummy cert in /etc/pki/tls
- use a pseudo-random serial number on the dummy cert
- change default ssl.conf to point at /etc/pki/tls
- merge back -suexec subpackage; SELinux policy can now be
  used to persistently disable suexec (#155716)
- drop /etc/httpd/conf/ssl.* directories and Makefiles
- unconditionally enable PIE support
- mod_ssl: fix for picking up -shutdown options (upstream #34452)

* Mon Apr 18 2005 Joe Orton <jorton@redhat.com> 2.0.54-4
- replace PreReq with Requires(pre) 

* Mon Apr 18 2005 Joe Orton <jorton@redhat.com> 2.0.54-3
- update to 2.0.54

* Tue Mar 29 2005 Joe Orton <jorton@redhat.com> 2.0.53-6
- update default httpd.conf:
 * clarify the comments on AddDefaultCharset usage (#135821)
 * remove all the AddCharset default extensions
 * don't load mod_imap by default
 * synch with upstream 2.0.53 httpd-std.conf
- mod_ssl: set user from SSLUserName in access hook (upstream #31418)
- htdigest: fix permissions of created files (upstream #33765)
- remove htsslpass

* Wed Mar  2 2005 Joe Orton <jorton@redhat.com> 2.0.53-5
- apachectl: restore use of $OPTIONS again

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 2.0.53-4
- update to 2.0.53
- move prefork/worker modules comparison to %%check

* Mon Feb  7 2005 Joe Orton <jorton@redhat.com> 2.0.52-7
- fix cosmetic issues in "service httpd reload"
- move User/Group higher in httpd.conf (#146793)
- load mod_logio by default in httpd.conf
- apachectl: update for correct libselinux tools locations

* Tue Nov 16 2004 Joe Orton <jorton@redhat.com> 2.0.52-6
- add security fix for CVE CAN-2004-0942 (memory consumption DoS)
- SELinux: run httpd -t under runcon in configtest (Steven Smalley)
- fix SSLSessionCache comment for distcache in ssl.conf
- restart using SIGHUP not SIGUSR1 after logrotate
- add ap_save_brigade fix (upstream #31247)
- mod_ssl: fix possible segfault in auth hook (upstream #31848)
- add htsslpass(1) and configure as default SSLPassPhraseDialog (#128677)
- apachectl: restore use of $OPTIONS
- apachectl, httpd.init: refuse to restart if $HTTPD -t fails
- apachectl: run $HTTPD -t in user SELinux context for configtest
- update for pcre-5.0 header locations

* Sat Nov 13 2004 Jeff Johnson <jbj@redhat.com> 2.0.52-5
- rebuild against db-4.3.21 aware apr-util.

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 2.0.52-4
- rebuild against db-4.3-21.

* Thu Sep 28 2004 Joe Orton <jorton@redhat.com> 2.0.52-3
- add dummy connection address fixes from HEAD
- mod_ssl: add security fix for CAN-2004-0885

* Tue Sep 28 2004 Joe Orton <jorton@redhat.com> 2.0.52-2
- update to 2.0.52

