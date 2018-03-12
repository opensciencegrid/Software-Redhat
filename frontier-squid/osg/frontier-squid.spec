# set squidsufix to 2 instead of %{nil} to build frontier-squid2
%define squidsuffix %{nil}

Summary: The Frontier distribution of the Squid proxy caching server
Name: frontier-squid%{?squidsuffix}
Version: 3.5.27
%define release4source 3
%define releasenum 1%{?dist}
Release: %{?release4source}.%{?releasenum}
Epoch: 11
License: GPL
Group: System Environment/Daemons

%define frontiersquidutils frontier-squid-utils
%define distname squid
%define squidversion %{distname}-%{version}
%define frontiersquidrpm %{name}-%{version}-%{release4source}
%define frontiersquidtarball frontier-squid-%{version}-%{release4source}
# Caution: If defaultsquiduser is changed here, it should also be changed at frontier-awstats accordingly!
%define defaultsquiduser squid

# For LOG_DIR
%define logdirsquid /var/log/squid%{?squidsuffix}
# For CACHE_DIR
%define cachedirsquid /var/cache/squid%{?squidsuffix}
# For RUN_DIR
%define rundirsquid /var/run/squid%{?squidsuffix}
# For ETC_DIR
%define etcdirsquid /etc/squid%{?squidsuffix}
# %{_libexecdir} is (/usr/sbin - or maybe) /usr/libexec/
%define libexecdirsquid %{_libexecdir}/squid 
# For SHARE_DIR: /usr/share/squid%{?squidsuffix}
# Equivalent: %define datadirsquid /usr/share/squid%{?squidsuffix}
%define datadirsquid %{_datadir}/squid%{?squidsuffix}
# directory for systemd config file that creates run directory
%define tmpfilesconfdir /usr/lib/tmpfiles.d
# directory for systemd service control config file
%define serviceconfdir /usr/lib/systemd/system


Source0: http://frontier.cern.ch/dist/%{frontiersquidtarball}.tar.gz
Source1: %{name}.tar.gz
Conflicts: squid
Conflicts: frontier-awstats < 6.9-4
Requires: logrotate
BuildRequires: openldap-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Squid is a high-performance proxy caching server for Web clients,
supporting FTP, gopher, and HTTP data objects. Unlike traditional
caching software, Squid handles all requests in a single,
non-blocking, I/O-driven process. Squid keeps meta data and especially
hot objects cached in RAM, caches DNS lookups, supports non-blocking
DNS lookups, and implements negative caching of failed requests.  This
squid distribution has been expecially tuned to work with the Frontier
server to cache Database entries retrieved from an ORACLE back-end,
particularly its need for the http standard If-Modified-Since feature.

%prep
%setup -n %{frontiersquidtarball} -q
tar zxf %{SOURCE1}

%build

# unpack squid code and patch it
cd ./squid
make INSTALL_DIR=$RPM_BUILD_ROOT PORT_ROOT=$PWD/.. unpack .common_patch

cd ../squid/work/%{squidversion}/
# put this package's version name in as the version for remote monitoring
sed -i "s/VERSION='\(.*\)'/VERSION='%{frontiersquidrpm}.%{releasenum}'/" configure
# The main reason for specifying enable-auth-basic is to avoid extra
#  dependencies, in particular on "perl(Authen::Smb)".  Would include PAM
#  except as of 3.5.4, it could not be built, at least on RHEL5.
./configure \
   --prefix=/ \
   --exec_prefix=%{_usr} \
   --bindir=%{_bindir} \
   --libdir=%{_libdir} \
   --libexecdir=%{libexecdirsquid} \
   --localstatedir=%{_var} \
   --sysconfdir=%{etcdirsquid} \
   --datadir=%{datadirsquid} \
   --program-suffix="%{?squidsuffix}" \
   --disable-wccp \
   --enable-snmp \
   --disable-ident-lookups \
   --enable-storeio="ufs aufs diskd rock"\
   --disable-auth-ntlm \
   --enable-auth-basic="getpwnam,NIS" \
   --disable-auth-digest \
   --disable-external-acl-helpers \
   --disable-arch-native \
   --with-large-files

# Remark: Without this command, squid looks for configuration at a wrong directory 
make %{?_smp_mflags} "AM_MAKEFLAGS=DEFAULT_LOG_PREFIX=%{logdirsquid} DEFAULT_SWAP_DIR=%{cachedirsquid} DEFAULT_PID_FILE=%{rundirsquid}/squid.pid"

%install
rm -rf $RPM_BUILD_ROOT

# Consider; change not to need cd, as was before
cd ./squid/work/%{squidversion}/
%makeinstall \
   prefix=$RPM_BUILD_ROOT \
   sysconfdir=$RPM_BUILD_ROOT%{etcdirsquid} \
   localstatedir=$RPM_BUILD_ROOT/var \
   bindir=$RPM_BUILD_ROOT/%{_bindir} \
   libdir=$RPM_BIULD_ROOT/%{_libdir} \
   libexecdir=$RPM_BUILD_ROOT%{libexecdirsquid}\
   datadir=$RPM_BUILD_ROOT%{datadirsquid} \
   "AM_MAKEFLAGS=DEFAULT_LOG_PREFIX=$RPM_BUILD_ROOT%{logdirsquid} DEFAULT_SWAP_DIR=$RPM_BUILD_ROOT%{cachedirsquid} DEFAULT_PID_FILE=$RPM_BUILD_ROOT%{rundirsquid}/squid.pid"

mkdir -p ${RPM_BUILD_ROOT}%{cachedirsquid} ${RPM_BUILD_ROOT}%{logdirsquid}
mkdir -p ${RPM_BUILD_ROOT}%{datadirsquid} ${RPM_BUILD_ROOT}%{etcdirsquid}
mkdir -p ${RPM_BUILD_ROOT}%{rundirsquid} ${RPM_BUILD_ROOT}%{tmpfilesconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{serviceconfdir}

# file created when new squid.conf is generated; create for %ghost entry
touch ${RPM_BUILD_ROOT}%{etcdirsquid}/squid.conf.old

cd %{_builddir}/%{frontiersquidtarball}/squid
make INSTALL_DIR=$RPM_BUILD_ROOT SQUID_SUFFIX=%{?squidsuffix} proto_install
cd ../%{frontiersquidutils}
make INSTALL_DIR=$RPM_BUILD_ROOT SQUID_SUFFIX=%{?squidsuffix} proto_install

# Variables for unproto
UNPROTO_VARS="NET_LOCAL CACHE_MEM CACHE_DIR_SIZE EFFECTIVE_USER EFFECTIVE_GROUP ETC_DIR LIBEXEC_DIR LOG_DIR SHARE_DIR CACHE_DIR BIN_DIR LIB_DIR VARLIB_DIR CONF_DIR SBIN_DIR CRON_DIR RUN_DIR AWSTATS_SCRIPT INIT_SCRIPT SQUID_SUFFIX"

export NET_LOCAL="10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 fc00::/7 fe80::/10"
export CACHE_MEM=128
export CACHE_DIR_SIZE=10000
export EFFECTIVE_USER=%{defaultsquiduser}
export EFFECTIVE_GROUP=%{defaultsquiduser}
export ETC_DIR=%{etcdirsquid}
export LIBEXEC_DIR=%{libexecdirsquid}
export LOG_DIR=%{logdirsquid}
export SHARE_DIR=%{datadirsquid}
export CACHE_DIR=%{cachedirsquid}
export BIN_DIR=/usr/sbin
export LIB_DIR=%{_libdir}
export VARLIB_DIR=%{_var}/lib
export CONF_DIR=%{etcdirsquid}
export SBIN_DIR=/usr/sbin
export CRON_DIR=%{datadirsquid}/cron
export RUN_DIR=%{rundirsquid}
export AWSTATS_SCRIPT=/etc/awstats/run_awstats.sh
export INIT_SCRIPT="service %{name}"
export SQUID_SUFFIX=%{?squidsuffix}

UNPROTO_SCRIPT=%{_builddir}/%{frontiersquidtarball}/unproto.sh 
${UNPROTO_SCRIPT} ${RPM_BUILD_ROOT}/usr/sbin/fn-local-squid%{?squidsuffix}.sh.proto 1 755 ${UNPROTO_VARS}
${UNPROTO_SCRIPT} ${RPM_BUILD_ROOT}%{etcdirsquid}/customize.sh.proto 1 755 ${UNPROTO_VARS}
mkdir -p ${RPM_BUILD_ROOT}/etc/init.d
mv ${RPM_BUILD_ROOT}%{etcdirsquid}/init.d/%{name}.sh.proto ${RPM_BUILD_ROOT}/etc/init.d/%{name}.proto
rmdir ${RPM_BUILD_ROOT}%{etcdirsquid}/init.d
${UNPROTO_SCRIPT} ${RPM_BUILD_ROOT}/etc/init.d/%{name}.proto 1 755 ${UNPROTO_VARS}
mv ${RPM_BUILD_ROOT}%{etcdirsquid}/squid.conf.proto ${RPM_BUILD_ROOT}%{etcdirsquid}/squid.conf.frontierdefault.proto
${UNPROTO_SCRIPT} ${RPM_BUILD_ROOT}%{etcdirsquid}/squid.conf.frontierdefault.proto 1 644 ${UNPROTO_VARS}
${UNPROTO_SCRIPT} ${RPM_BUILD_ROOT}$CRON_DIR/daily.sh.proto 1 755 ${UNPROTO_VARS}
${UNPROTO_SCRIPT} ${RPM_BUILD_ROOT}$CRON_DIR/hourly.sh.proto 1 755 ${UNPROTO_VARS}
${UNPROTO_SCRIPT} ${RPM_BUILD_ROOT}$CRON_DIR/crontab.dat.proto 1 644 ${UNPROTO_VARS}

# make default tmpfiles.d configuration for EL7, without leading '/var'
echo "d `echo %{rundirsquid}|sed 's,^/var,,'` 0755 %{defaultsquiduser} %{defaultsquiduser} -" >${RPM_BUILD_ROOT}%{tmpfilesconfdir}/%{name}.conf

# make systemd service file
cat >${RPM_BUILD_ROOT}%{serviceconfdir}/%{name}.service <<!EOF!
[Unit]
Description=The Frontier Squid server
After=network.target remote-fs.target nss-lookup.target
Documentation=man:squid(8)

[Service]
Type=forking
ExecStart=/etc/init.d/frontier-squid start
ExecReload=/etc/init.d/frontier-squid reload
ExecStop=/etc/init.d/frontier-squid stop
TimeoutStartSec=90
TimeoutStopSec=60
# We want systemd to give squid some time to finish gracefully, but still want
# it to kill squid after TimeoutStopSec if something went wrong during the
# graceful stop. Normally, Systemd sends SIGTERM signal right after the
# ExecStop, which would kill squid. We are sending useless SIGCONT here to give
# squid time to finish.
KillSignal=SIGCONT

[Install]
WantedBy=multi-user.target
!EOF!

CRONDIRFILE=${RPM_BUILD_ROOT}/etc/cron.d/%{name}.cron
mkdir -p `dirname $CRONDIRFILE`
# insert username as the 6th column
sed "s,\([^ ]*[ ]*[^ ]*[ ]*[^ ]*[ ]*[^ ]*[ ]*[^ ]* \)\(.*\),\1${EFFECTIVE_USER} \2," ${RPM_BUILD_ROOT}$CRON_DIR/crontab.dat >$CRONDIRFILE
chmod 644 $CRONDIRFILE
rm -f ${RPM_BUILD_ROOT}$CRON_DIR/crontab.dat


%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/sbin/fn-local-squid%{?squidsuffix}.sh
/usr/sbin/squid%{?squidsuffix}
/usr/bin/*
%{libexecdirsquid}
%{datadirsquid}
%{serviceconfdir}/%{name}.service
%verify(not user group) %dir %{rundirsquid}
%verify(not user group) %{etcdirsquid}
%verify(not user group size md5 mtime) %config(noreplace) %{etcdirsquid}/customize.sh
%verify(not user group size md5 mtime) %{etcdirsquid}/squid.conf.frontierdefault
%verify(not user group size md5 mtime) %{etcdirsquid}/cachemgr.conf
# the init.d, cron.d, and tmpfiles.d scripts are edited in post-install
%verify(not size md5 mtime) /etc/init.d/%{name}
# removed the %config(noreplace) on the cron because it was too hard to manage
%verify(not size md5 mtime) /etc/cron.d/%{name}.cron
%verify(not size md5 mtime) %{tmpfilesconfdir}/%{name}.conf
# squid.conf is a %ghost file so rpm won't overwrite an existing one if
#  someone is upgrading from a non-frontier squid
%ghost %{etcdirsquid}/squid.conf
# squid.conf.old is a ghost file so it will be deleted when
#  this rpm is uninstalled
%ghost %{etcdirsquid}/squid.conf.old
# cachedirsquid and logdirsquid are ghost in case someone turned them
#  into symlinks (since they're commonly relocated); if we let rpm install 
#  these directories it will change the symlink target's owner to root
%ghost %{cachedirsquid}
%ghost %{logdirsquid}
/usr/share/man/man1
/usr/share/man/man8

# The %pre step uses a temporary file to tell the %post step if 
#  the service was running.  It can't be in world-writable /tmp
#  because of the risk of race conditions.
%define wasrunningfile %{etcdirsquid}/.%{name}-wasrunning

%pre
mkdir -p %{etcdirsquid}
rm -f %{wasrunningfile}
if [ $1 -gt 1 ]; then
   # an upgrade
   if /sbin/service %{name} status; then
      # already running. stop it before any files are installed because
      #  some of them are owned by root
      /sbin/service %{name} stop
      # restart after the file ownerships are changed
      touch %{wasrunningfile}
    fi
fi

%post
if [ -f %{wasrunningfile} ]; then
  rm -f %{wasrunningfile}
  STARTSERVICE=true
else
  STARTSERVICE=false
fi

SCFILE=%{etcdirsquid}/squidconf
if [ -s ${SCFILE} ]; then
	source ${SCFILE}
else
	export FRONTIER_USER=%{defaultsquiduser}
fi
if [ -z "${FRONTIER_USER}" ]; then
	echo "ERROR: missing FRONTIER_USER"
	exit 1
fi
if [ "${FRONTIER_USER}" == 'root' ]; then
	echo "ERROR: FRONTIER_USER can not be 'root'."
	exit 1
fi
if [ -z "${FRONTIER_GROUP}" ]; then
	FRONTIER_GROUP=%{defaultsquiduser}
fi


if ! getent group ${FRONTIER_GROUP} >/dev/null 2>&1 ; then
	echo "WARNING: Adding missing group: ${FRONTIER_GROUP}."
	if ! /usr/sbin/groupadd -r ${FRONTIER_GROUP} ; then
		echo "ERROR: failed to groupadd ${FRONTIER_GROUP}"
		exit 1
	fi
fi

if ! getent passwd ${FRONTIER_USER} >/dev/null 2>&1 ; then
	echo "WARNING: Adding missing user: ${FRONTIER_USER}."
	if ! /usr/sbin/useradd -r -g ${FRONTIER_GROUP} ${FRONTIER_USER} ; then
		echo "ERROR: failed to useradd ${FRONTIER_USER}"
		exit 1
	fi
	# Block shell access for user ${FRONTIER_USER} 
	if ! /usr/sbin/usermod -s /sbin/nologin ${FRONTIER_USER} ; then
		echo "ERROR: failed to usermod ${FRONTIER_USER}"
		exit 1
	fi
fi

# create the home directory if it doesn't exist
# if this is not done, on RHEL6-derived systems cron fails to run user's jobs
eval FRONTIER_HOME=~${FRONTIER_USER}
if [ ! -d ${FRONTIER_HOME} ]; then
	mkdir ${FRONTIER_HOME}
	chown ${FRONTIER_USER}:${FRONTIER_GROUP} ${FRONTIER_HOME}
	chmod 755 ${FRONTIER_HOME}
fi

# create these ghost directories if they don't exist
mkdir -p %{logdirsquid} %{cachedirsquid}

if [ "$FRONTIER_USER" != %{defaultsquiduser} ]; then
  # set username as the 6th column of the cron.d file
  CRONDST=/etc/cron.d/%{name}.cron
  sed -i "s,\([^ ]* *[^ ]* *[^ ]* *[^ ]* *[^ ]* *\)[^ ]*,\1${FRONTIER_USER}," $CRONDST
fi

# override effective user and group in squid.conf 
sed -i "s/^cache_effective_user.*/cache_effective_user ${FRONTIER_USER}/;s/^cache_effective_group.*/cache_effective_group ${FRONTIER_GROUP}/" %{etcdirsquid}/squid.conf.frontierdefault
# set FRONTIER_USER in the init.d script
sed -i -e "s/^\(FRONTIER_USER=\).*/\1${FRONTIER_USER}/" /etc/init.d/%{name}
# set file ownerships
find %{cachedirsquid} %{logdirsquid} %{rundirsquid} %{etcdirsquid} \
	\( ! -user ${FRONTIER_USER} -o ! -group ${FRONTIER_GROUP} \) | \
	xargs --no-run-if-empty chown -h ${FRONTIER_USER}:${FRONTIER_GROUP}
# set user and group in tmpfiles.d configuration, 4th and 5th column
sed -i "s,\([^ ]* *[^ ]* *[^ ]* *\)[^ ]* *[^ ]*,\1${FRONTIER_USER} ${FRONTIER_GROUP}," %{tmpfilesconfdir}/%{name}.conf

/sbin/chkconfig --add %{name}

if $STARTSERVICE; then
  /sbin/service %{name} start
fi


SPOOLCRONFILE=/var/spool/cron/${FRONTIER_USER}
if [ -s ${SPOOLCRONFILE} ]; then
  # clean up crontab entries from older rpm
  sed -i '/etc\/squid\/cron\/.*\.sh/d' ${SPOOLCRONFILE}
  if [ ! -s ${SPOOLCRONFILE} ]; then
    rm -f ${SPOOLCRONFILE}
  fi
fi

#clean up files that may be left from an older rpm
rm -f	%{etcdirsquid}/init.d/%{name}.sh \
	%{etcdirsquid}/cron/crontab.dat \
	%{etcdirsquid}/cron/daily.log* \
	%{etcdirsquid}/squid.conf.frontierdefault.proto

%preun
if [ $1 -eq 0 ]; then
   # full uninstall
   if /sbin/service %{name} status; then
      /sbin/service %{name} stop
   fi
   /sbin/service %{name} removecache
   /sbin/chkconfig --del %{name}

   # The following intends to avoid missing old squid.conf at upgrade.
   if [ -f %{etcdirsquid}/squid.conf.old ]; then 
       cp %{etcdirsquid}/squid.conf `mktemp /tmp/squid.confXXXX` 
   fi
fi

%changelog
* Wed Jan 24 2018 Dave Dykstra <dwd@fnal.gov> 3.5.27-3.1
- Upgrade to 3.5.27-3 tarball with the following release notes:
 - Add configuration options to always honor "Pragma: no-cache" from a
   client, even if the client also sends a "Cache-control" header, as
   the current frontier-client (v2.8.20) always does.
     https://bugs.squid-cache.org/show_bug.cgi?id=4809
 - Included provided patches from the squid project related to two
   denial of service security advisories which they say could affect
   all reverse proxies.
    http://www.squid-cache.org/Advisories/SQUID-2018_1.txt
    http://www.squid-cache.org/Advisories/SQUID-2018_2.txt
   For example frontier server launchpad squids are configured as
   reverse proxies.

* Fri Dec 08 2017 Dave Dykstra <dwd@fnal.gov> 3.5.27-2.1
- Upgrade to 3.5.27-2 tarball with the following release note:
 - Add openhtc.io aliases to CMS_FRONTIER, ATLAS_FRONTIER, and MAJOR_CVMFS
   acls.

* Fri Sep 01 2017 Dave Dykstra <dwd@fnal.gov> 3.5.27-1.1
- Upgrade to 3.5.27-1 tarball with the following release notes:
 - Upgrade to squid-3.5.27.  The release announcement hasn't been
   published yet but here is the ChangeLog:
     https://github.com/squid-cache/squid/blob/v3.5/ChangeLog
   Release notes from prior releases since last frontier-squid release:
     https://www.spinics.net/lists/squid/msg86349.html (3.5.26)
     https://www.spinics.net/lists/squid/msg85634.html (3.5.25)
 - Remove the patch from #2833 because it was updated and included in
    the 3.5.27 release.
 - Add a patch from #4767 for making IPv6 SNMP queries work with
    multiple worker processes instead of causing a crash & restart.
 - Add IHEP and UNL stratum ones to the MAJOR_CVMFS access control list.

* Wed Mar 22 2017 Dave Dykstra <dwd@fnal.gov> 3.5.24-3.1
- Upgrade to 3.5.24-3 tarball with the following release notes:
 - Change quick_abort_min and quick_abort_max once again, this time to
   0 KB, because someone doing a different repeatable test found that
   the 1 GB value still caused some crashes but 0 KB didn't.

* Fri Mar 17 2017 Dave Dykstra <dwd@fnal.gov> 3.5.24-2.1
- Upgrade to 3.5.24-2 tarball with the following release notes:
 - Change the default setting of quick_abort_min from -1 KB to 1 GB and
   the default setting of quick_abort_max from 16 KB to 1 GB.  This is
   to work around the squid crash documented in squid bug #4554.  A
   consequence is that when a client aborts an object download, the
   object won't get cached even though it is highly likely that
   another client will soon want the same object.

* Tue Jan 31 2017 Dave Dykstra <dwd@fnal.gov> 3.5.24-1.1
- Upgrade to 3.5.24-1 tarball with the following release notes:
 - Upgrade to squid-3.5.24 with release notes at
     https://www.spinics.net/lists/squid/msg85024.html
   The bug fixes we had been including are not yet in this release, so
   all the same patches are kept.  The most notable change affecting
   WLCG in this release was a fix for a bug that caused 'cache deny'
   to not have any effect.  That is used for some cvmfs stratum 1s,
   and perhaps other applications.

* Thu Jan 26 2017 Dave Dykstra <dwd@fnal.gov> 3.5.23-6.1
- Upgrade to 3.5.23-6 tarball with the following release notes:
 - Replace the bug #2833 fix with a newer version from the consultant.  The
   full name is SQUID-252-collapsed-slaves-non-sharable-responses-3.5-t10.
   This one might be final.
 - Add patch from squid bug #4616, since two users had reported the "mem"
   assertion failure in store_client.cc.  The full name of the patch is
   bug4616-cf-mem-assert-t1.

* Wed Jan 25 2017 Dave Dykstra <dwd@fnal.gov> 3.5.23-5.1
- Upgrade to 3.5.23-5 tarball with the following release note:
 - Replace the bug #2833 fix with a newer version from the consultant.  The
   full name is SQUID-252-collapsed-slaves-non-sharable-responses-3.5-t9.
   The previous version is suspected in a crash at one grid site. This
   version required a couple of small changes to apply and compile cleanly.

* Fri Jan 13 2017 Dave Dykstra <dwd@fnal.gov> 3.5.23-4.1
- Upgrade to 3.5.23-4 tarball with the following release notes:
 - Replace the bug #2833 fix with a newer version from the consultant.  The
   full name is SQUID-252-collapsed-slaves-non-sharable-responses-3.5-t6.
   It is probably not the final patch.
 - Add creation of /var/run/squid in the init.d script, if it did not
   exist.  This is because systemd-based systems (EL7) do not preserve
   the directory across boots, and on some systems the systemd
   configuration file to create it at boot time does not work.  That
   can happen if the system gets user ids from the network, so the
   squid user id might not yet be available when the systemd
   configuration file is used.
- Add a systemd service descriptor configuration, primarily to make sure
   that frontier-squid is started after networking services.  Uses the
   same "After" and "Wantedby" targets as apache httpd.

* Tue Dec 27 2016 Dave Dykstra <dwd@fnal.gov> 3.5.23-3.1
- Upgrade to 3.5.23-3 tarball with the following release note:
 - Replace my patch that comments out the fix for security advisory
   SQUID-2016:10 with a patch from the consultant for bug #2833.  This
   patch makes collapsed forwarding work again with If-Modified-Since
   while leaving the security advisory fixed.

* Tue Dec 20 2016 Dave Dykstra <dwd@fnal.gov> 3.5.23-2.1
- Upgrade to 3.5.23-2 tarball with the following release note:
 - Comment out the fix for security advisory SQUID-2016:10, because it
   caused collapsed forwarding to break for If-Modified-Since requests.
   It was probably implemented incorrectly; discussion is in the
   reopened squid bug report #2833.

* Mon Dec 19 2016 Dave Dykstra <dwd@fnal.gov> 3.5.23-1.1
- Upgrade to 3.5.23-1 tarball with the following release notes:
 - Upgrade to squid-3.5.23 with release notes at
     http://www.spinics.net/lists/squid/msg84536.html
   The most notable changes are fixes for two privacy vulnerabilities.
   They don't affect the applications primarily used with frontier-squid
   but may affect other applications.
 - Add the CERN IPv6 monitoring address range to the HOST_MONITOR acl.
 - Add IPv6 private net addresses to default setting of NET_LOCAL.

* Fri Oct 14 2016 Dave Dykstra <dwd@fnal.gov> 3.5.22-2.1
- Upgrade to 3.5.22-2 tarball with the following release note:
 - Change default value of dns_v4_first to "on", so it will always try
   ipv4 first if available and then ipv6.  The default was "off" which
   always tries ipv6 first.

* Thu Oct 13 2016 Dave Dykstra <dwd@fnal.gov> 3.5.22-1.1
- Upgrade to 3.5.22-1 tarball with the following release notes:
 - Upgrade to squid-3.5.22 with release notes at
    http://www.spinics.net/lists/squid/msg83740.html
 - Remove patches from Alex Rousskov because they are now in the
   official squid 3.5 release.

* Tue Sep 20 2016 Dave Dykstra <dwd@fnal.gov> 3.5.21-2.1
- Upgrade to 3.5.21-2 tarball with the following release note:
 - Fix error in the new logformat.  It should be "%>Hs", not ">%Hs".

* Tue Sep 13 2016 Dave Dykstra <dwd@fnal.gov> 3.5.21-1.1
- Upgrade to 3.5.21-1 tarball with the following release notes:
 - Upgrade to squid-3.5.21 with release notes at
    http://www.spinics.net/lists/squid/msg83169.html
 - Remove patch for bug #4428, it is now in the release.
 - Apply patch from Alex Rousskov for squid bug #4471, fixing collapsed
    forwarding revalidation when there is no If-Modified-Since.
 - Change "%Hs" in the default log format to the new style ">%Hs" for
    squid-3.
 - Change the default cache_dir size in squid.conf.proto to 10000 MB in
    case someone deletes the default 10000 MB line in customize.sh.
 - Change the script that applies patches to exit with an error if any
    of the patches are not completely applied.

* Mon Aug 22 2016 Dave Dykstra <dwd@fnal.gov> 3.5.20-3.1
- Upgrade to 3.5.20-3 tarball with the following release notes:
 - Apply patch from the squid team for bug #4428.  This bug causes 
    the Cache-control: stale-if-error header, which Frontier uses,
    to be malformed in cached objects.
 - Fix bug that caused access logs shared by multiple workers to be
    rotated multiple times, once for each worker, instead of just once.
 - When using compressed logs and SQUID_CLEAN_CACHE_ON_START is true
   (both of which are default), then truncate the swap.state file
   in ufs cache directories each time logs are rotated.  Otherwise the
   file grows without bounds.
 - When using the 'restart' function, clean ufs cache directories the
   same way as when doing 'start'.

* Mon Aug 08 2016 Dave Dykstra <dwd@fnal.gov> 3.5.20-2.1
- Upgrade to 3.5.20-2 tarball with the following release notes:
 - The infamous squid bug #7 had partially cropped up again.  The Date
   headers on cached 304 Not Modified responses on large objects was
   returning the original Date rather than a new re-validated Date,
   even though the Age header was correct.   This causes many
   duplicated queries to get sent upstream.  This release works around
   the problem as discussed here:
    http://bugs.squid-cache.org/show_bug.cgi?id=7#c79

* Thu Jul 21 2016 Dave Dykstra <dwd@fnal.gov> 3.5.20-1.1
- Upgrade to 3.5.20-1 tarball with the following release notes:
 - Upgrade to squid-3.5.20.  This is the release announcement:
    http://www.spinics.net/lists/squid/msg82165.html
 - Replace my own patches for squid bugs #4311 and #4471 with a big
   patch from Alex Rousskov fixing collapsed revalidation.  It
   addresses bug #4311 and more importantly bug #2833, where collapsed
   forwarding did not work with If-Modified-Since on expired objects.
   Unfortunately it breaks the functionality formerly fixed in the
   patch for bug #4471; that is, collapsed forwarding now does not
   work on expired objects that do *not* have a Last-Modified header.
   This should be no problem for the Frontier application because any
   response without Last-Modified is given a year expiration time.
   However, this is a potential issue for CVMFS because the stratum 1s
   currently expire most objects after 3 days.  At least the issue
   will be relatively infrequent, and if a fix for this bug does not
   come soon we can probably eventually get the stratum 1
   configurations changed to increase the expiration time.

* Wed Jul 13 2016 Dave Dykstra <dwd@fnal.gov> 3.5.19-3.2
- Disable external acl helpers, auth digest helpers, and the LDAP
  auth basic helper, because they interfered with having an el5
  rpm be upward compatible to el7 (in particular, libsasl and libdb).

* Thu Jun 16 2016 Dave Dykstra <dwd@fnal.gov> 3.5.19-3.1
- Upgrade to 3.5.19-3 tarball with the following release note:
 - Change default minimum_expiry_time to 0 seconds.  Without this
   change, squid will not cache any objects that are loaded for the
   first time during the last minute of their lifetime; instead, all
   requests for that object during that minute are sent upstream.  It
   only affects squids that are fed by other squids.

* Fri Jun 10 2016 Dave Dykstra <dwd@fnal.gov> 3.5.19-2.1
- Upgrade to 3.5.19-2 tarball with the following release note:
 - Add support for SQUID_CUSTOMIZE environment variable.  If set to
   false it skips generating squid.conf from squid.conf.frontierdefault
   and customize.sh.  Instead, the user is on his or her own to manage
   squid.conf.  It is recommended to start from squid.conf.default
   because that is less likely to change between releases.  The default
   setting of SQUID_CUSTOMIZE is true.

* Mon May 23 2016 Dave Dykstra <dwd@fnal.gov> 3.5.19-1.2
- Add "Conflicts: frontier-awstats < 6.9-4" in order to ensure there's
    no version that does not support IPv6.

* Wed May 11 2016 Dave Dykstra <dwd@fnal.gov> 3.5.19-1.1
- Upgrade to 3.5.19-1 tarball with the following release notes:
 - Upgrade to squid-3.5.19.  This is the release announcement:
    http://www.spinics.net/lists/squid/msg81196.html
 - Add hepvm.cern.ch to the MAJOR_CVMFS acl

* Mon Mar 28 2016 Dave Dykstra <dwd@fnal.gov> 3.5.15-2.1
- Add --disable-arch-native configure option to avoid illegal instruction
  errors as documented at
    http://wiki.squid-cache.org/KnowledgeBase/IllegalInstructionError
- Upgrade to 3.5.15-2 tarball with the following release notes:
 - Disable memory_cache_shared by default, and make it an error if somebody
   tries to turn it on without rock cache.
 - Replace patch for bug #4312 with the one for #4311.  It has the same
   effect and is simpler.

* Wed Mar 24 2016 Dave Dykstra <dwd@fnal.gov> 3.5.15-1.1
- Upgrade to 3.5.15-1 tarball with the following release notes:
 - Upgrade to squid-3.5.15.  This is the release announcement:
    http://www.spinics.net/lists/squid/msg79992.html
 - Apply patch for squid bug #2831, to send Cache-control header through
    on 304 Not Modified responses.
 - Apply patch for squid bug #4471, to make collapsed forwarding work
    when there's a previously cached but expired object.  It still does
    not work with If-Modified-Since 304 Not Modified responses (bug #2833).
    So this makes it work with CVMFS but not yet Frontier.

* Wed Oct 15 2015 Dave Dykstra <dwd@fnal.gov> 3.5.9-1.1
- Upgrade to 3.5.9-1 tarball with the following release notes:
 - Upgrade to squid-3.5.9.  This is the release announcement:
    http://www.spinics.net/lists/squid/msg77242.html
 - Pass the SQUID variables in /etc/sysconfig/frontier-squid to the daily
   log rotation cron, in particular so SQUID_NUM_SERVICES will apply.
 - When installing with the "proto_install" make target, for rpm, install
   cron scripts in /usr/share/squid/cron instead of /etc/squid/cron.
- Move scripts that were in /etc/squid/cron to /usr/share/squid/cron.
- Removed the %config(noreplace) on /etc/cron.d/frontier-squid.cron,
  because that referred to the above path and it has to get changed.
  Also it was always difficult to allow administrator edits because
  the rpm also edits it when $FRONTIER_USER is set to something other
  than 'squid'.

* Thu Sep 16 2015 Dave Dykstra <dwd@fnal.gov> 3.5.7-1.1
- Add creation of config file in /usr/lib/tmpfiles.d to create /run/squid
  directory on reboot of EL7-based systems.
- Remove creation of /etc/squid/errors symlink, it's not needed by squid3.
- Upgrade to 3.5.7-1 tarball with the following release notes:
 - Upgrade to squid-3.5.7.  This is the release announcement:
    http://www.spinics.net/lists/squid/msg76566.html
 - Extend the "setoption" macro in customize.sh to work with options
   that are only identified by a "TAG:" comment in squid.conf, because not
   all options have a commented example like they did in squid2.
 - Add support for workers > 1, especially including recognizing the SMP
   macros that split up directories for separate worker processes.  Ensure
   that the user has either enabled this for the cache directory or chosen
   rock cache type.  For details on the SMP macros see "SMP-Related Macros"
   in squid.conf comments.
 - Enable support for the "rock" cache_dir store type, for sharing a cache
   between multiple SMP workers.  Note that this cache type is still
   susceptible to squid bug #7 so it should be considered only experimental
   at this point.  It may be safely used if it is guaranteed that no
   application will use If-Modified-Since (for example, if it is only
   used for CVMFS).
 - Enable support for the "diskd" cache_dir store type, which is just like
   "ufs" except that it uses a separate process for disk i/o.
 - Add support for running multiple independent squid services via the
   environment variable SQUID_NUM_SERVICES.  This assigns each squid
   a "service name" that is a number from 0 to $SQUID_NUM_SERVICES-1.
   This value can be accessed with the macro ${service_name} which must
   be included in the cache_dir, access_log, cache_log, and pid_filename
   options.  Add new customize.sh macro "setserviceoption" for setting
   options with a numerical value (e.g. http_port) to a different value
   per service.  The value may also be a comma separated list of numbers
   (e.g. cpu_affinity_map). For usage see customhelps.awk.  Each
   service may have multiple workers if desired.
 - Remove old wrapper script support for multiple processes since squid3
   does everything natively in squid.conf.  That includes removing
   support for automatically setting the core affinity on the separate
   processes.  Instead set the option cpu_affinity_map to get the most
   performance out of each core.  Setting core affinity improves
   performance by about 15%.
 - Reduce the verbose debug messages that were coming out at startup.
 - Add a patch for bug http://bugs.squid-cache.org/show_bug.cgi?id=3952
   to prevent the initialization of the cache directory with multiple
   workers from running in the background.
 - Add a patch for bug http://bugs.squid-cache.org/show_bug.cgi?id=4312
   to add a configuration option collapsed_forwarding_shared_entries_limit.
   This enables controlling the sharing of collapsed forwarding between
   SMP workers.  This sharing causes deadlocks with the default ufs cache
   type, so this is set to zero in the default squid.conf.  It does not
   cause deadlocks with rock cache, so to enable it use the comment()
   macro in customize.sh to drop back to the compiled-in default.
 - Extend the rotate lock to also cover awstats generation, to prevent
   more than one from running at a time.

* Fri May 22 2015 Dave Dykstra <dwd@fnal.gov> 3.5.4-1.1
- Remove selection of PAM basic auth module at configure time because
   it could not be built.
- Upgrade to frontier-squid-3.5.4-1 tarball with the following release notes:
 - Upgrade to squid-3.5.4, including a fix for a security vulnerability, 
   release announcement here:
     http://www.spinics.net/lists/squid/msg75017.html
 - Merge changes from frontier-squid 2.7.STABLE9-22-1 and 2.7.STABLE9-23-1,
   which were (in addition to multiple-squid related things which don't
   function in frontier-squid3):
   - Support a "daemon:" prefix on access_log and cache_log, a poorly
     documented squid feature that uses a separate process to handle
     writing to log files so the main squid process doesn't have to
     wait for disk I/O.  This was added because log compression was
     observed on one machine to interfere with squid I/O accesses.
     Make this the default for access_log.
   - Run log rotation with ionice -n7.
   - Make slight correction to MAJOR_CVMFS acl regular expression.
   - Expand the server names allowed at RAL in the ATLAS_FRONTIER acl.

* Mon Apr 06 2015 Dave Dykstra <dwd@fnal.gov> 3.5.3-1.1
- Upgrade to frontier-squid-3.5.3-1 tarball with the following release notes:
 - Upgrade to squid-3.5.3, release announcement here:
   http://lists.squid-cache.org/pipermail/squid-announce/2015-March/000014.html

* Thu Feb 19 2015 Dave Dykstra <dwd@fnal.gov> 3.5.2-1.1
- Upgrade to frontier-squid-3.5.2-1 tarball with the following release notes:
 - Upgrade to squid-3.5.2, release announcement here:
    http://lists.squid-cache.org/pipermail/squid-announce/2015-February/000012.html

* Wed Jan 21 2015 Dave Dykstra <dwd@fnal.gov> 3.5.1-1.1
- Upgrade to frontier-squid-3.5.1-1 tarball with the following release note:
 - Upgrade to first full squid3.5 release, 3.5.1

* Mon Dec 22 2014 Dave Dykstra <dwd@fnal.gov> 3.5.0.4-1.1
- Upgrade to frontier-squid-3.5.0.4-1 tarball which has the following
  release notes:
 - Upgrade to squid beta release 3.5.0.4, release announcement here:
    http://lists.squid-cache.org/pipermail/squid-announce/2014-December/000007.html
 - Merge changes from frontier-squid-2.7.STABLE9-21 which were:
  - Fix redirection of stderr in the hourly and daily crons so error
    messages properly go to squidcron.log.
  - Only require the minimum 4096 file descriptors when doing one
    of the commands that contain "start" (that is, "start", "restart",
    or "condrestart") with multiple squids.
  - Add the script that generates squid.conf to the list of files that
    trigger regenerating squid.conf if they're newer than squid.conf.
  - Only generate the per-squid configuration files used with multiple
    squids when squid.conf is newer than them.
 - NOTE: starting multiple squids the frontier-squid way (with squidN
   subdirectories under cache directory) doesn't work with squid-3,
   but so far the startup script capability is preserved just to keep
   as much as possible in common with frontier-squid-2 for now.  Instead,
   to run multiple processes set the 'workers' configuration option.
 - Merge change from a pre-release of frontier-squid-2:
   - Make slight correction to MAJOR_CVMFS acl regular expression

* Mon Nov 10 2014 Dave Dykstra <dwd@fnal.gov> 3.5.0.2-1.1
- Upgrade to frontier-squid-3.5.0.2-1 tarball which has the 
  following release note:
 - Upgrade to squid beta release 3.5.0.2.  Made as minimal changes
   as possible to the frontier-squid packaging for an early first
   look at a squid-3 with most of the features required by grid
   applications.

* Thu Nov 06 2014 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-20.1
- Upgrade to frontier-squid-2.7.STABLE9-20 tarball which has the
  following release notes:
 - Increase the maximum number of squids that may be started from 4
   to 16
 - When running N > 1 squids, limit each squid to the hard limit on
   file descriptors divided by N.  This limiting greatly reduces or
   eliminates the number of failed accesses to cache files indicated
   by TCP_SWAPFAIL_MISS entries in access.log.  Require a minimum of
   4096 file descriptors for each squid, unless customize.sh sets a
   value below the calculated limit.  
 - Support use of SQUID_SUFFIX to add a suffix to all the files.
   This is not supported for use in the standalone tarball, just
   for use within an rpm.
- Add logrotate as a dependency

* Mon Sep 16 2014 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-19.1
- Upgrade to frontier-squid-2.7.STABLE9-19 tarball, which has the 
  following release notes:
 - Make the default SQUID_MAX_ACCESS_LOG be 5G instead of 1G unless
   log compression is disabled.  This should take about the same 
   maximum space (~11Gbytes) as uncompressed log files did with a
   max size of 1G.
 - Add the TRIUMF CVMFS stratum 1 to the list in MAJOR_CVMFS.

* Wed Sep 03 2014 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-18.1
- Upgrade to frontier-squid-2.7.STABLE9-18 tarball, which has the 
  following release notes:
 - Protect rotate operations with a lock, because now that they
   compress files they can take a long time.  This is especially
   important for the one minute between the daily cron and the
   first hourly cron.
 - Fix bug introduced in last release where if access_log is set to
   "none", the cache log is rotated every 15 minutes.

* Thu Aug 22 2014 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-17.1
- Remove the cache when doing a full uninstall
- When $FRONTIER_USER is not the default value 'squid', automatically
  manage the /etc/cron.d/frontier-squid.cron.rpmnew file that is always
  created
- Upgrade to frontier-squid-2.7.STABLE9-17 tarball, which has the 
  following release notes:
 - Update the CERN Hungary Data Center's LHCOPN IP address range in
   the HOST_MONITOR access control list from the incorrect
   188.185.0.0/17 to the correct 188.184.128.0/17 and 188.185.128.0/17.
 - Add commented-out acls CMS_FRONTIER, ATLAS_FRONTIER, and MAJOR_CVMFS
   that can be uncommented and used in place of RESTRICT_DEST to
   restrict outgoing connections to the corresponding servers.  This
   allows updating the lists via frontier-squid package upgrades
   rather than requiring individual administrators to know how to keep
   the lists up to date.
 - Include the real time zone in the access.log timestamp instead of
   always +0000, and include milliseconds after the seconds.
 - Add the "cvmfs-info" header to the same double-quoted log entry that
   now has "X-Frontier-Id".  Since no client sends both headers, only
   one will show at a time; frontier entries will end with " -" and
   cvmfs entries will start with "- ".  Cvmfs clients currently only
   send cvmfs-info if configured with CVMFS_SEND_INFO_HEADER=yes so
   if that's not the case their log entries will show "- -".
 - Accept SQUID_MAX_ACCESS_LOG as the variable setting the maximum
   access log file size in place of LARGE_ACCESS_LOG (which is still
   accepted for backward compatibility).  Also if the value ends in
   'M' it indicates megabytes and if it ends in 'G' it indicates
   gigabytes; the default is bytes.
 - Run the "hourly" cron 4 times an hour, to catch faster when a log
   file has gone over the max size limit.
 - Compress log files by default, using logrotate.  If environment
   variable SQUID_COMPRESS_LOGS is exported and set to 'false', fall
   back to the previous method of telling squid to rotate the log
   files without compression.  In either case the logfile_rotate
   configuration parameter is used to define the maximum number of
   rotated files.  If frontier-awstats is also installed, the first
   file is left uncompressed.  When switching either way between
   compressed and uncompressed, removes all log files of the old type.
 - Rotate cache.log even if the access_log configuration parameter is
   "none".
 - Add a new "removecache" option to the init script to simply remove
   all of the cache, for use when removing the package.

* Fri May 10 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-16.1
- Fix /etc/init.d/frontier-squid so if an alternate $FRONTIER_USER is
  set in /etc/squid/squidconf, then it will verify the existence of
  that user's home directory rather than the squid user's home directory.
- Update to frontier-squid-2.7.STABLE9-16 tarball which rearranged the
  /etc/init.d script to be easier to modify at post-install time by
  the rpm, and which changed the delay after starting squid from 3 to
  10 seconds before checking to see if it is running.  That was the
  previous delay before the changes in the last release, and a system
  with 2 squids and slow disk access while cleaning cache in the
  background apparently didn't get started within 3 seconds.

* Thu May 9 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-15.1
- Create the squid user's home directory if it doesn't exist at install
  time, because on RHEL6-derived systems a missing home directory prevents
  cron from running the squid log rotation.
- Update to frontier-squid-2.7.STABLE9-15 tarball which has the following
  release notes:
  - Put squidcron.log in the same directory as cache.log rather than
    access.log, in case the access_log option is set to "none".  In
    the previous version it would put squidcron.log in the squid
    user's home directory if access_log was "none".
  - Change the init.d startup script to abort with an error message if
    the squid user's home directory does not exist, because on
    RHEL6-derived systems if a user's home directory doesn't exist then
    cron won't run the user's jobs.
  - Run squid without the -S option so it will never run an audit of
    the cache files.  During a normal start the cache is deleted so
    it doesn't matter, and the audit operation can take a very long
    time on a large cache during a restart.  Also an analysis showed
    that the typical types of errors the audit catches (missing files)
    are survivable.
  - Allow multiple background cache cleans to be happening at the same
    time, in case the cache is very large and someone does multiple
    stop/start operations.
  - Add environment variable SQUID_CLEAN_CACHE_ON_START which defaults
    to true and when set to false prevents clearing the cache on start.
    It can be set and exported in the package's /etc/sysconfig file.

* Wed Feb 6 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-13.5
- Change /var/cache/squid and /var/log/squid to be %ghost and created in
  the post install step in case someone had relocated them with a symlink.
  A symlink in one of those places with the previous version caused the
  target of the symlink to get changed to root ownership.

* Mon Feb 4 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-13.4
- Add /var/cache/squid, /var/log/squid, and /var/run/squid to the list
  of directories installed; they had been accidentally left out

* Mon Feb 4 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-13.3
- Change the chkconfig behavior to more precisely match Redhat squid's
  package; an administrator will now have to do "chkconfig frontier-squid on"
  instead of "chkconfig --add frontier-squid"
- Do a few other internal cleanup things to frontier-squid.spec

* Thu Feb 1 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-13.2
- Make /etc/squid/squid.conf a %ghost file so if someone is upgrading
  from a non-frontier squid it won't be overwritten

* Thu Feb 1 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-13.1
- Update to frontier-squid-2.7.STABLE9-13 tarball which moves the
  output of cron jobs from daily.log in the directory the cron scripts
  are in (/etc/squid/cron) to the directory of the other squid
  logs (default /var/log/squid).
- Remove the ability to use --prefix at rpm install time to
  relocate, because this greatly simplifies the rpm code including
  no longer needing to install .proto files with the package.
- Change the cron jobs from being run from the squid user's
  /var/spool/cron (crontab) file to instead being run from 
  /etc/cron.d/frontier-squid.cron.
- When a user id (default "squid") needs to be created, create it
  as a system account (that is, with a UID lower than the value of
  UID_MIN in /etc/login.defs).
- If the requested group (default "squid") is missing, create it
  just like a missing user id.
- Set the ownership of all files under /etc/squid to be the squid
  user instead of leaving some as root.
- Remove execute permission from files in /etc/squid that don't
  need it.
- Remove bogus squid doc files from /usr/share/doc.
- Move the restart of a running process from the post-uninstall to the
  post-install actions.  Note: this has a side effect of causing it to
  restart twice the first time a package is upgraded from the previous
  style to this style.
- Move the release notes to the rpm changelog.

* Fri Jan 25 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-12.1
- Update to frontier-squid-2.7.STABLE9-12 tarball which only
  changes a comment in customize.sh so it can make more sense for
  the rpm
- Change initial install to not start squid or do chkconfig -add
  to match what the standard Redhat squid rpm does
- Change upgrades so squid will only be restarted if it was
  running at the time of the upgrade
- Fix bug that prevented stopping squid when removing the rpm
  while squid is running

* Mon Jan 14 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-11.1
- Update to frontier-squid-2.7.STABLE9-11 tarball, which adds the
  Referer and User-Agent headers to the default logformat, and 
  includes the upstream squid source so it self-contained.
- Fix a rpm spec bug that kept rpmbuild -ba from working

* Fri Dec 21 2012 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-10.1
- Update to frontier-squid-2.7.STABLE9-10 tarball, which changes
  the default SNMP monitoring addresses accepted to be all of the
  WLCG addresses at the main CERN center and the backup CERN
  Hungary data center, and disables the ICP port by default
- Remove sl5 from the rpm name, as the rpm works for both sl5 & sl6

* Wed Sep 5 2012 David Front <dfront@gmail.com> 2.7.STABLE9-8.1
- Change the init.d 'rotate' command to first remove the oldest log
  files, rather than asking squid to do it, because it can take a long
  time to delete large access logs and squid stops servicing requests
  during the rotate process.

* Thu Aug 2 2012 David Front <dfront@gmail.com> 2.7.STABLE9-7.1
- Use a fix of Dave Dykstra: fixed a small bug in the frontier-squid tarball
  that prevented the hourly cron from reading /etc/sysconfig/frontier-squid 
  for the setting of the LARGE_ACCESS_LOG variable, so it was impossible for
  the user to be able to control the size of the log files kept.  

* Tue Jun 26 2012 David Front <dfront@gmail.com> 2.7.STABLE9-6.1
- Use new release of frontier-squid tarball.  The most significant
  new feature is that multiple squids can be started on the same
  port.  For details of that feature and other tarball changes, see
    http://frontier.cern.ch/dist/frontier-squid-releasenotes.txt
- Use more of the tarball directly, especially the proto files
- Use the full version of the rpm to identify the squid process in
  SNMP monitoring
- A small technical change at the spec file to support source rpms for
  frontier rpms
- Use symbolic link to unproto.sh to simplify source tar ball creation

* Wed Jun 13 2012 David Front <dfront@gmail.com> 2.7.STABLE9-5.24
- Following the recommendation of Dave Dykstra, change /etc/squid/squid.conf
  to be %ghost at the spec file, and hence not installed by the rpm
  but yes removed at rpm uninstall.  As a result, the one line place
  holder of this file is no more needed, and also no need to check for
  small file when testing if this config file should be regenerated,
  at fn-local-squid.sh.proto.

* Wed Apr 18 2012 David Front <dfront@gmail.com> 2.7.STABLE9-5.23
- Change the default NET_LOCAL at /etc/squid/customize.sh to be
  10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 rather than 0.0.0.0/32

  Related: At release notes for frontier-squid-2.7.STABLE9-5:
  at http://frontier.cern.ch/dist/frontier-squid-releasenotes.txt:
  Remove the hidden default of always allowing incoming access to
  private network addresses 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16.
  Instead, make that default explicit in the first customize.sh that
  is generated so if the administrator doesn't want that it can be
  easily changed.

* Wed Dec 21 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.22
- Change $AWSTATS_SCRIPT at fn-local-squid.sh.proto 
  from /etc/awstats/squid_rotate_run_awstats.sh
  to /etc/awstats/run_awstats.sh

* Tue Dec 20 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.21
- Undo the following, from frontier-squid-2.7.STABLE9-5.15, because
  not accepted by Dave Dykstra:
     'Create squid.conf only if it does not exist or at start, not at
     stop or status.'
  Hence, once squid.conf has to be recreated, it will be created at
  each call to fn-local-squid.sh.
  A (unpleasent) consequence of this:
  If fontier-squid is running, 
  and any of the following variables is going to be changed at the new
  configuration:
      1 CACHE_DIR
      2 CACHE_LOG
      3 ACCESS_LOG
      4 PID_FILENAME
  the new configuration that will be created at 
      service frontier-squid stop
  will not be aware of the previou related value,
  and as a result may cause various failures.
  This rare situation should be handled manually by the administrator.
  The following help file may be consulted to do this:
      http://frontier.cern.ch/dist/rpms/frontierRpmInstallationError.txt

* Sun Dec 18 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.20
- Conditionally call the awstats script, if it exists,
  to prevent related bugs and simplify the code

* Sun Dec 11 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.19 
- src/frontier-squid-utils/bin/fn-local-squid.sh.proto: 
    Fix bug, change for $PIDINODE, as suggested by Dave Dykstra, at
    https://savannah.cern.ch/bugs/?89488#comment32 

* Thu Dec 8 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.18
- Apply patch by Dave Dykstra on frontier-squid-utils/bin/fn-local-squid.sh.proto:
    https://savannah.cern.ch/support/download.php?file_id=22825
        
* Tue Nov 29 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.17
- Attempt to complete supporting rpm verify, command:'rpm -V':
  -- Do not remove *.unproto files (after usage).
  -- Do less attribute checks to files: 
       /etc/squid/cachemgr.conf
       /etc/squid/customize.sh
       /etc/squid/squid.conf

* Sun Nov 27 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.16
- Supporting rpm verify, command:'rpm -V':
  -- Add the prefix '%verify(not user group)' to each %files entry,
     in order to prevent complaints from 'rpm -V', like:
        .....UG.    <fileName>
  -- Note, however, that 'rpm -V' may still create misleading complaints like:
        missing   ... <fileName>.proto

* Tue Nov 22 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.15
- Change default pid_filename to be /var/run/squid/squid.pid
- Change directory and file defaults: ownership to be:
  frontierUser:frontierGroup, and mode to be: 755
- Attempt to correct bug: replace squid.conf.default by
  squid.conf.proto at src/frontier-squid-utils/etc
- Refuse to answer a service status query while building a configuration
  file
- Create squid.conf only if it does not exist or at start, not at stop
  or status
- Fix bug at postinstall.sh, previously attempted to stop non existing
  service: squid

* Thu Nov 10 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.14
- Fix bugs related to frontier group and automicatic creation of
  default log, run and cache dirs.
- If /etc/squid/squidconf file is missing, do not create it but rather
  assume that the forntier user is squid

* Thu Oct 27 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.13
- The group of frontier user is not controlled anymore.
  (Whatever group this user has, is used for chmod files from root to
  frontier user.)

* Sun Oct 23 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.12
- Commenting out error if /etc/squid/squid.conf is writable

* Fri Oct 21 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.11
- %defaultsquidgroup should be 'squid' and not 'users', as it was by
  mistake previously
- Change the default of logs dir to be under standard /var/log rather
  than /var/logs as it used to be
- Avoid directory names that begin by //

* Thu Sep 22 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.10
- Do clean cache at initial restart

* Thu Sep 20 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.9
- Attempt to handle an installation error related to a (mysterious)
  /etc/init.d/frontier-squid.sh sybmolic link by taking care to rm
  such files at rpm remove

* Mon Sep 19 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.8
- Another code change attempting to avoid recursive erasal of / at rpm
  upgrade
- rpm rearranged to use the files at frontier-squid tarball as much as
  possible, avoid duplicating such files where not needed
- Fix failure to upgrade frontier-squid rpm while previous release is running,
    by replacing the command /sbin/service frontier-squid start 
    by           the command /sbin/service frontier-squid restart 
    at postinstall.sh, in this case
- In case of failure at %post, change the error messages to be more clear,
  referring to 'as if' installed, as explained at
  http://frontier.cern.ch/dist/rpms/frontierRpmInstallationError.txt

* Fri Aug 12 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.7
- Attempt to avoid recursive erasal of / at rpm upgrade

* Fri Jul 29 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.6
- Fix bug: Change order of post install operations, to prevent
  possible attempt to refer to file /etc/squid/squid.conf before it
  has been created.
- Instead of removing /etc/squid/squid.conf.old at rpm uninstall, do:
    /bin/mv /etc/squid/squid.conf.old `mktemp /tmp/squid.conf.oldXXXX`

* Wed Jul 27 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.5
- Fix bug at fn-local-squid.sh.template that prevents log rotation of
  squid logs if awstats rpm is not installed

* Wed Jul 20 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.4
- For #3 at https://savannah.cern.ch/bugs/?77447:
  Like, squid standard rpm, do create the user with the safest
  permission (nologin as shell and no password).
    - Support non /data base dir (edited at /etc/squid/customize.sh)

* Fri Jun 10 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.3

* Thu Apr 21 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.2
- Initial release 
  Originating from http://grid-deployment.web.cern.ch/grid-deployment/flavia/frontier-squid-2.7.STABLE9-5.1.sl5.src.rpm
  Changes:
    - Added examples for customize.sh: 
        /etc/squid/customize.sh.example_launchpad_CERN 
        /etc/squid/customize.sh.example_non_launchpad_CERN
