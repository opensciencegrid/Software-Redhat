# set squidsufix to 2 instead of %%{nil} to build frontier-squid2
%define squidsuffix %{nil}

%define shoalversion 1.0.2

# exclude shoal-agent from automatic dependency generation
%global __requires_exclude_from ^%{_libexecdir}/squid/shoal-agent/

Summary: The Frontier distribution of the Squid proxy caching server
Name: frontier-squid%{?squidsuffix}
Version: 5.9
%define release4source 2
%define releasenum 2%{?dist}
Release: %{?release4source}.%{?releasenum}
Epoch: 11
License: GPL
Group: System Environment/Daemons
ExclusiveArch: x86_64

%define frontiersquidutils frontier-squid-utils
%define distname squid
%define squidversion %{distname}-%{version}
%define frontiersquidrpm %{name}-%{version}-%{release4source}
%define frontiersquidtarball frontier-squid-%{version}-%{release4source}
# Caution: If defaultsquiduser is changed here, it should also be changed at frontier-awstats accordingly!
%define defaultsquiduser squid
%define shoalname shoal-agent-%{shoalversion}

# For LOG_DIR
%define logdirsquid /var/log/squid%{?squidsuffix}
# For CACHE_DIR
%define cachedirsquid /var/cache/squid%{?squidsuffix}
# For RUN_DIR
%define rundirsquid /run/squid%{?squidsuffix}
# For ETC_DIR
%define etcdirsquid /etc/squid%{?squidsuffix}
# %%{_libexecdir} is (/usr/sbin - or maybe) /usr/libexec/
%define libexecdirsquid %{_libexecdir}/squid 
# For SHARE_DIR: /usr/share/squid%%{?squidsuffix}
# Equivalent: %%define datadirsquid /usr/share/squid%%{?squidsuffix}
%define datadirsquid %{_datadir}/squid%{?squidsuffix}
# directory for squid account home
%define homedirsquid /var/lib/squid%{?squidsuffix}
# directory for systemd config file that creates run directory
%define tmpfilesconfdir /usr/lib/tmpfiles.d
# directory for systemd service control config file
%define serviceconfdir /usr/lib/systemd/system


Source0: http://frontier.cern.ch/dist/%{frontiersquidtarball}.tar.gz
Source1: frontier-squid.tar.gz
Source2: https://github.com/hep-gc/shoal/archive/%{shoalname}.tar.gz
Source3: shoal-downloads.tar.gz
Conflicts: squid
Conflicts: frontier-awstats < 6.9-4
Requires: chkconfig

# procps-ng is needed for /usr/sbin/sysctl
Requires: procps-ng
Requires: logrotate
Requires: /sbin/restorecon
BuildRequires: pam-devel
BuildRequires: systemd-devel
%if 0%{?rhel} >= 9
BuildRequires: g++
%endif

#shoal build requirements
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: redhat-rpm-config
BuildRequires: libffi-devel
BuildRequires: cargo

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
%setup -b 0 -n %{frontiersquidtarball} -q
tar zxf %{SOURCE1}
# nil debug_package here because shoal has no binaries with symbols to extract
%global debug_package %{nil}
# also eliminate .build-id links on el8, they make python packages clash
%global _build_id_links none
# extra shoal- prefix because github adds the repository name to the tag
%setup -b 2 -n shoal-%{shoalname} -q
%setup -b 3 -n shoal-downloads -q


%build
# starts out in the shoal-downloads directory

set -ex
PYVERS="python3$(python3 -V|cut -d. -f2)"
PYDIR=$PWD/$PYVERS/.local
PATH=$PYDIR/bin:$PATH

# install pyinstaller and required python packages to build shoal-agent

# install in reverse order of their download (because dependency downloads
#   come after requested packages)
PKGS="$(tar tf %{SOURCE3} | grep "/$PYVERS/." | sed 's,^shoal-downloads/,,' | grep -v "^$PYVERS/\.local" | tac)"
PKGS="$(echo "$PKGS"|paste -sd ' ')"

if [ -d $PYDIR ]; then
    # for the sake of a newer version of pip3
    export PYTHONPATH="`echo $PYDIR/lib*/python*/site-packages|sed 's/ /:/g'`"
fi

# --no-build-isolation is needed for offline build of pyinstaller as per
#  https://github.com/pyinstaller/pyinstaller/issues/4557
HOME=$PWD/$PYVERS pip3 install --no-cache-dir --no-build-isolation --user $PKGS

# in case it wasn't set above
export PYTHONPATH="`echo $PYDIR/lib*/python*/site-packages|sed 's/ /:/g'`"

cd ../shoal-%{shoalname}
cd shoal-agent

PYIOPTS="--log-level=WARN"
$PYDIR/bin/pyi-makespec $PYIOPTS --noconsole --specpath=dist shoal-agent

# Exclude system libraries from the bundle as documented at
#  https://pyinstaller.readthedocs.io/en/stable/spec-files.html#posix-specific-options
awk '
    {if ($1 == "pyz") print "a.exclude_system_libraries()"}
    {print}
' dist/shoal-agent.spec >dist/shoal-agent-lesslibs.spec
$PYDIR/bin/pyinstaller $PYIOPTS --noconfirm --clean dist/shoal-agent-lesslibs.spec

if [ -d dist/shoal-agent/_internal ]; then
    chmod -x dist/shoal-agent/_internal/*.*
else
    chmod -x dist/shoal-agent/*.*
fi

# shoal-agent looks first in its own install dir for shoal_agent.conf so
#  symlink it to %{etcdirsquid} to be with other squid config files
ln -s %{etcdirsquid}/shoal_agent.conf dist/shoal-agent/

cd ..

# unpack squid code and patch it
cd ../%{frontiersquidtarball}/squid
make INSTALL_DIR=$RPM_BUILD_ROOT PORT_ROOT=$PWD/.. unpack .common_patch

cd work/%{squidversion}/
# put this package's version name in as the version for remote monitoring
sed -i "s/VERSION='\(.*\)'/VERSION='%{frontiersquidrpm}.%{releasenum}'/" configure
# The main reason for specifying enable-auth-basic is to avoid extra
#  dependencies, in particular on "perl(Authen::Smb)".
# --disable-security-cert-validators is also to avoid a perl dependency,
#  on "perl(Crypt::OpenSSL::X509)".
%if 0%{?rhel} >= 8
# Do not include NIS authentication because of
# https://bugzilla.redhat.com/show_bug.cgi?id=1531540
AUTHBASIC="getpwnam,PAM"
%else
AUTHBASIC="getpwnam,NIS,PAM"
%endif
./configure \
   --prefix=/ \
   --exec_prefix=%{_usr} \
   --bindir=%{_bindir} \
   --libdir=%{_libdir} \
   --libexecdir=%{libexecdirsquid} \
   --localstatedir=%{_var} \
   --sysconfdir=%{etcdirsquid} \
   --datadir=%{datadirsquid} \
   --program-suffix='%{?squidsuffix}' \
   --disable-wccp \
   --enable-snmp \
   --disable-ident-lookups \
   --enable-storeio='ufs aufs diskd rock' \
   --disable-auth-ntlm \
   --enable-auth-basic=$AUTHBASIC \
   --disable-security-cert-validators \
   --disable-auth-digest \
   --disable-external-acl-helpers \
   --disable-arch-native \
   --disable-esi \
   --with-large-files

# Remark: Without this command, squid looks for configuration at a wrong directory 
make %{?_smp_mflags} "AM_MAKEFLAGS=DEFAULT_LOG_PREFIX=%{logdirsquid} DEFAULT_SWAP_DIR=%{cachedirsquid} DEFAULT_PID_FILE=%{rundirsquid}/squid.pid"

%install
# starts out in shoal-downloads

rm -rf $RPM_BUILD_ROOT

pushd ../%{frontiersquidtarball}/squid/work/%{squidversion}/
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
mkdir -p ${RPM_BUILD_ROOT}%{serviceconfdir} ${RPM_BUILD_ROOT}%{homedirsquid}

# file created when new squid.conf is generated; create for %ghost entry
touch ${RPM_BUILD_ROOT}%{etcdirsquid}/squid.conf.old

cd %{_builddir}/%{frontiersquidtarball}/squid
make INSTALL_DIR=$RPM_BUILD_ROOT SQUID_SUFFIX=%{?squidsuffix} proto_install
cd ../%{frontiersquidutils}
make INSTALL_DIR=$RPM_BUILD_ROOT SQUID_SUFFIX=%{?squidsuffix} proto_install

# Variables for unproto
UNPROTO_VARS="NET_LOCAL CACHE_MEM CACHE_DIR_SIZE EFFECTIVE_USER EFFECTIVE_GROUP ETC_DIR LIBEXEC_DIR LOG_DIR SHARE_DIR CACHE_DIR BIN_DIR LIB_DIR VARLIB_DIR CONF_DIR SBIN_DIR CRON_DIR RUN_DIR AWSTATS_SCRIPT REINIT_SCRIPT RELOAD_SCRIPT SQUID_SUFFIX"

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
export REINIT_SCRIPT="/etc/init.d/frontier-squid"
export RELOAD_SCRIPT="systemctl reload %{name}"
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

# Finally, install the shoal files
popd
cd ../shoal-%{shoalname}
# fix bad permissions on cryptography directory (causes problem on src rebuild)
find shoal-agent/dist/shoal-agent -type d ! -perm -1|xargs -r chmod +x
cp -r shoal-agent/dist/shoal-agent ${RPM_BUILD_ROOT}/%{libexecdirsquid}
# Create the frontierdefault file, source for the generated shoal_agent.conf
(echo "# ***Do not edit** changes to this file are not preserved"
 echo "#"
 cat shoal-agent/conf/shoal_agent.conf) \
    >${RPM_BUILD_ROOT}%{etcdirsquid}/shoal_agent.conf.frontierdefault
# generated file; touch for %ghost entry
touch ${RPM_BUILD_ROOT}%{etcdirsquid}/shoal_agent.conf

# make symlink for shoal_agent.conf https://github.com/hep-gc/shoal/issues/168
mkdir ${RPM_BUILD_ROOT}/etc/shoal
ln -s ../squid/shoal_agent.conf ${RPM_BUILD_ROOT}/etc/shoal

# In the squid4 to squid5 update, there is a problem in yum (not rpm) where
# files in the "es" directory cause conflict errors in the transaction test.
# As a work-around, we change "es" to a link. See the pretrans section
# for more.
cd ${RPM_BUILD_ROOT}/usr/share/squid/errors/
mv es es-default
ln -s es-default es
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/sbin/fn-local-squid%{?squidsuffix}.sh
/usr/sbin/squid%{?squidsuffix}
/usr/bin/*
%config(noreplace) %verify(not owner group mtime) /etc/shoal/shoal_agent.conf
%{libexecdirsquid}
%{datadirsquid}
%{homedirsquid}
%{serviceconfdir}/%{name}.service
%verify(not user group) %dir %{rundirsquid}
%verify(not user group) %dir %{etcdirsquid}
%verify(not user group) %{etcdirsquid}/cachemgr.conf*
%verify(not user group) %{etcdirsquid}/customhelps.awk
%verify(not user group) %{etcdirsquid}/errorpage.css*
%verify(not user group) %{etcdirsquid}/mime.conf*
%verify(not user group) %{etcdirsquid}/squid.conf.default
%verify(not user group) %{etcdirsquid}/squid.conf.documented
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
%verify(not user group mode) %ghost %{etcdirsquid}/squid.conf
# squid.conf.old is a ghost file so it will be deleted when
#  this rpm is uninstalled
%verify(not user group mode) %ghost %{etcdirsquid}/squid.conf.old
# shoal_agent.conf is a ghost file because it is generated
%verify(not user group mode) %ghost %{etcdirsquid}/shoal_agent.conf
%verify(not user group size md5 mtime) %{etcdirsquid}/shoal_agent.conf.frontierdefault
# cachedirsquid and logdirsquid are ghost in case someone turned them
#  into symlinks (since they're commonly relocated); if we let rpm install 
#  these directories it will change the symlink target's owner to root
%verify(not user group) %ghost %{cachedirsquid}
%verify(not user group) %ghost %{logdirsquid}
/usr/share/man/man1
/usr/share/man/man8

# In the squid4 to squid5 update, rpm/yum cannot handle the change of the "es-mx"
# link to a directory. To fix this, the old "es-mx" link is deleted here.
# Also, the contents of the "es" directory cause transaction errors in yum, which
# are fixed by changing it to a link. In this pretrans step, we move the old "es"
# directory to make way for the new link.

%pretrans -p <lua>
path = "/usr/share/squid/errors/es-mx"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end
path = "/usr/share/squid/errors/es"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end

%pre
# The %%pre step uses a temporary file to tell the %post step if 
#  the service was running.  It can't be in world-writable /tmp
#  because of the risk of race conditions.
%define wasrunningfile %{etcdirsquid}/.%{name}-wasrunning
mkdir -p %{etcdirsquid}
rm -f %{wasrunningfile}
if [ $1 -gt 1 ]; then
   # an upgrade
   if systemctl is-active --quiet %{name}; then
      # already running. stop it before any files are installed because
      #  some of them are owned by root
      systemctl stop %{name}
      # restart after the file ownerships are changed
      touch %{wasrunningfile}
    fi
fi

%post
# Delete the old "es.rpmmoved" directory that was created in pretrans.
rm -rf /usr/share/squid/errors/es.rpmmoved*
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
	if ! /usr/sbin/useradd -r -g ${FRONTIER_GROUP} -d %{homedirsquid} ${FRONTIER_USER} ; then
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

# this supports SELinux
/sbin/restorecon %{cachedirsquid}
/sbin/restorecon %{logdirsquid}  

systemctl daemon-reload
if $STARTSERVICE; then
  systemctl start %{name}
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
   if systemctl is-active --quiet %{name}; then
      systemctl stop %{name}
   fi
   /etc/init.d/frontier-squid removecache
   # This is needed for cleaning up after versions <= 4.13-5.2
   /sbin/chkconfig --del %{name}

   # The following intends to avoid missing old squid.conf at upgrade.
   if [ -f %{etcdirsquid}/squid.conf.old ]; then 
       cp %{etcdirsquid}/squid.conf `mktemp /tmp/squid.confXXXX` 
   fi
fi

%changelog

* Thu Oct 10 2024 Matt Westphall <westphall@wisc.edu> 5.9-2.2
  - Limit osg builds to x86_64

* Thu Jan 11 2024 Carl Vuosalo <carl.vuosalo@cern.ch> 5.9-2.1
 - Apply security patches from Squid 6 to address security concerns since 
    a version of Squid 6 suitable for frontier-squid is not available yet.
 - The following security vulnerabilities have been addressed with patches:
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46724
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46847
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46848
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-49285
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-50269
    https://github.com/squid-cache/squid/security/advisories/GHSA-j83v-w3p4-5cqh
 - The following two vulnerabilities are addressed by disabling Gopher and TRACE
    requests, respectively, in the squid.conf.proto file:
    https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-46728
    https://megamansec.github.io/Squid-Security-Audit/trace-uaf.html
 - To support SELinux, require /sbin/restorecon and apply it to the log directory,
    in addition to the cache directory.
 - Update to shoal-1.0.2 to fix setting of external_ip.

* Tue Aug 15 2023 Carl Vuosalo <carl.vuosalo@cern.ch> 5.9-1.2
 - With the addtion of an EL9 repository, this release includes an EL9 RPM that was
    compiled on EL9 and that fully supports Web Proxy Auto Discovery. The EL7/EL8
    RPM in this release is unchanged from 5.9-1.1, except for version number.

* Tue May 23 2023 Carl Vuosalo <carl.vuosalo@cern.ch> 5.9-1.1
 - Update to squid-5.9, with announcement at
    http://lists.squid-cache.org/pipermail/squid-announce/2023-May/000147.html and
    release notes at http://www.squid-cache.org/Versions/v5/squid-5.9-RELEASENOTES.html.
    squid-5.9 contains small fixes including improvement of debug logging related to the
    reply_body_max_size parameter.
 - Consistent with squid5, disallow the combination of multiple workers, ufs cache,
    and memory_cache_shared even if collapsed_forwarding is off.
 - Limit the  maximum number of file descriptors to 65536 even if the OS would allow
    a higher number.

* Tue Mar 28 2023 Carl Vuosalo <carl.vuosalo@cern.ch> 5.8-2.1
 - For EL9, in this spec file replace calls to obsolete "service" and add new package
   requirements.

* Fri Mar 17 2023 Carl Vuosalo <carl.vuosalo@cern.ch> 5.8-1.1
 - Update to squid-5.8 with release notes at
    https://www.squid-cache.org/Versions/v5/squid-5.8-RELEASENOTES.html and announcement at
    http://lists.squid-cache.org/pipermail/squid-announce/2023-February/000145.html
    Most important new features in 5.8:
    - A predefined ACL named "to_linklocal" which matches traffic attempting to access
     link-local network services has been added. It is set to "deny" in
     squid/files/postinstall/squid.conf.proto.
    - Bug fixed where cache manager API erroneously returns "mgr_index" instead of requested
     data.
 - Add support for rpmbuild on el9
 - Add object-*.cloud to the computecanada portion of MAJOR_CVMFS in
    squid/files/postinstall/squid.conf.proto.

* Tue Jan 31 2023 Carl Vuosalo <carl.vuosalo@cern.ch> 5.7-2.1
- Fix bug where old caches were not always cleaned up.

* Fri Jan 13 2023 Carl Vuosalo <carl.vuosalo@cern.ch> 5.7-1.3
- Complete the fix from 5.7-1.2. An additional work-around was needed
   for the squid-4 to squid-5 upgrade to change a directory that was generating
   yum transaction errors into a link, which silenced the errors.

* Fri Dec 09 2022 Carl Vuosalo <carl.vuosalo@cern.ch> 5.7-1.2
- Add pretrans scriplet to this spec file to fix problem with squid-4 to
   squid-5 upgrade where a link becomes a directory.

* Thu Dec 08 2022 Carl Vuosalo <carl.vuosalo@cern.ch> 5.7-1.1
- Upgrade to 5.7-1 tarball with the following release notes:
 - Update to squid-5.7 with release notes at https://wiki.squid-cache.org/Squid-5 and
    http://www.squid-cache.org/Versions/v5/RELEASENOTES.html.
    Most important new feature in 5.7:
    - "Happy Eyeballs" feature uses the first destination IP address that responds
       from DNS, whether it is IPv4 (A records) or IPv6 (AAAA records). A consequence
       of this feature is that the dns_v4_first directive is no longer supported.
 - Add sites cvmfs-stratum-one.cc.kek.jp and cvmfs*.sdcc.bnl.gov
    to MAJOR_CVMFS in squid/files/postinstall/squid.conf.proto.
 - Remove obsolete frontier*.racf.bnl.gov from ATLAS_FRONTIER
    in squid/files/postinstall/squid.conf.proto.

* Wed Sep 21 2022 Carl Vuosalo <carl.vuosalo@cern.ch> 4.17-2.1
- Upgrade to 4.17-2 tarball with the following release notes:
 - Add sites sampacs*.if.usp.br and cvmfs-*.hpc.swin.edu.au to MAJOR_CVMFS in
     squid/files/postinstall/squid.conf.proto.

* Tue Oct 12 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 4.17-1.1
- Upgrade to 4.17-1 tarball with the following release notes:
 - Update to squid-4.17.  Includes squid-4.16 with release announcement at
     http://lists.squid-cache.org/pipermail/squid-announce/2021-July/000134.html
    and squid-4.17 with release announcement at
     http://lists.squid-cache.org/pipermail/squid-announce/2021-October/000137.html
    The latter includes a security fix, but it is to code disabled in
    frontier-squid.
- Avoid including standard system libraries with pyinstaller.

* Fri Jun  4 2021 Dave Dykstra <dwd@fnal.gov> 4.15-2.1
- Upgrade to 4.15-2 tarball with the following release notes:
 - Fix SQUID_COMPRESS_LOGS=false, which was broken since 4.13-3.  Change
    it to also use the external logrotate command instead of the squid
    builtin log rotation.

* Tue May 11 2021 Dave Dykstra <dwd@fnal.gov> 4.15-1.2
- Filter out unneeded python3 dependency with the __requires_exclude_from
  macro.

* Mon May 10 2021 Dave Dykstra <dwd@fnal.gov> 4.15-1.1
- Upgrade to 4.15-1 tarball with the following release notes:
 - Update to squid-4.15 with release announcement at
     http://lists.squid-cache.org/pipermail/squid-announce/2021-May/000127.html
    The update includes security fixes, and at least one (SQUID-2020:11)
    is relevant because it enables someone that is allowed by access
    controls to use squid for some purpose to bypass any other access
    controls and use it for any purpose.  That one can be worked around
    with "uri_whitespace deny", but other denial of service vulnerabilities
    fixed in this version have no workaround.
 - Set "uri_whitespace deny" by default to avoid any other related
    vulnerabilities in the future.
 - Exit with an error if either of the two required logfile_rotate entries
    are not in squid.conf.  This is for the protection of who are using
    SQUID_CUSTOMIZE=false and have not properly merged the changes from
    squid.conf.frontierdefault.
 - Update the customhelps.awk function setoption() to work correctly
    after a setoptionparameter().
 - Allow cache_dir null type which means no disk cache, for systems that
    have very large cache_mem and maximum_object_size_in_memory.

* Thu Apr 22 2021 Dave Dykstra <dwd@fnal.gov> 4.13-5.3
- Change to use systemctl instead of service commands where possible.

* Tue Mar 30 2021 Dave Dykstra <dwd@fnal.gov> 4.13-5.2
- Fix bad permissions on one of the shoal-agent dependency directories.
  Only caused a problem when rebuilding from src rpm.

* Mon Mar 29 2021 Dave Dykstra <dwd@fnal.gov> 4.13-5.1
- Upgrade to 4.13-5 tarball with the following release notes:
 - Use /bin/bash instead of $SHELL in fn-local-squid.sh because $SHELL
    is sometimes set to /bin/nologin (in particular when the squid user
    directly invokes fn-local-squid.sh).  This affected cleaning out old
    cache files and starting shoal.
 - Do not attempt to set net.core.somaxconn higher than the kernel
    maximum of 65335.

* Fri Mar 19 2021 Dave Dykstra <dwd@fnal.gov> 4.13-4.1
- Increase shoal-agent version to 1.0.0.
- Upgrade to 4.13-4 tarball with the following release notes:
 - Add Compute Canada stratum 1s to MAJOR_CVMFS
 - Add any parameters passed in by $SQUID_START_ARGS to the starting of
    squid.  This is set to --foreground by the OSG frontier-squid docker
    container.

* Thu Mar 18 2021 Dave Dykstra <dwd@fnal.gov> 4.13-3.2
- Fix the building of shoal-agent to be able to work again with no network
  access (for OSG koji).

* Wed Mar 17 2021 Dave Dykstra <dwd@fnal.gov> 4.13-3.1
- Upgrade to 4.13-3 tarball with the following release notes:
 - Change log rotates to no longer use reconfigure signal but to instead
    set logfile_rotate to zero and use the rotate signal.  This is much
    lighter weight and works around squid bug #5113.  Administrators can
    still set logfile_rotate to non-default values, but it is used only
    by fn-local-squid.sh and overridden for squid.
 - With multiple squid services, send the rotate signal only once to each
    squid.
 - Add timestamps to squidcron.log for the beginning and end of rotation.
- Remove el6 support

* Mon Sep 28 2020 Dave Dykstra <dwd@fnal.gov> 4.13-2.1
- Upgrade to 4.13-2 tarball with the following release note:
 - Move temporary logrotate config file to the log directory, to keep
   SELinux on CentOS8 happy.

* Mon Jun 29 2020 Dave Dykstra <dwd@fnal.gov> 4.13-1.1
- Upgrade to 4.13-1 tarball with the following release notes:
 - Update to squid-4.13 with release announcement at
     https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00117.html
    It includes a couple of relevant security advisories related to
    cache poisoning.
 - Remove patch for bug 5051 since it is included in the 4.13 release.
- Remove the recursion on the restorecon for SELinux in the %post install
    step, to avoid taking a long time when going through a large cache.

* Mon Jun 29 2020 Dave Dykstra <dwd@fnal.gov> 4.12-2.1
- Upgrade to 4.12-2 tarball with the following release notes (from 4.12-1
   and 4.12-2):
 - Update to squid-4.12 with release announcement at
     https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00114.html
    It includes a couple of security advisories, but they are on
    features that as far as I know are not used by frontier-squid users.
 - Remove patches for bug #5030 and #5041 which are included in 4.12
 - Slightly update patch for bug #5051 as recommended by squid consultant
 - Note that an additional, more relevant squid advisory fixed in 4.12 was
    published late:
     https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00116.html
 - Support the "stdio:" prefix for access_log

* Thu Jun 11 2020 Dave Dykstra <dwd@fnal.gov> 4.11-4.3
- Require systemd-devel on non-el6 systems, so squid's configure will
  recognize that it is on a systemd-based system.
- Update to shoal-agent-0.9.9, and remove python3 patch because that
  is now merged.

* Thu Jun 11 2020 Dave Dykstra <dwd@fnal.gov> 4.11-4.2
- Fix quoting on el6 build options to select the correct types of basic
  authentication.  The bug accidentally enabled ldap authentication which
  prevented an el6 rpm from installing on el7.
- Remove openldap-devel build dependency.

* Tue Jun 9 2020 Dave Dykstra <dwd@fnal.gov> 4.11-4.1
- Upgrade to 4.11-4 tarball with the following release note:
  - Apply patch for bug #5041 which broke compilation in squid-4.11 on
    el7 with systemd.
- Update rpm spec to build on el8.
- Use python3 for shoal instead of python2 because that has the greatest
  portability across operating systems.  On el6, use the scl add-on
  package from Red Hat.  Apply a patch to shoal to work with python3.  
- Pre-download python pip packages into shoal-downloads.tar.gz to include
  them in the src rpm.
- Disable NIS basic-authentication on el8 because required header files
  are missing

* Wed Jun 3 2020 Dave Dykstra <dwd@fnal.gov> 4.11-3.1
- Upgrade to 4.11-3 tarball with the following release notes:
 - Apply patch for bug #5051 which prevents a negative cache from
    persisting indefinitely with if-modified-since and collapsed forwarding.
 - Fix shoal when there are multiple squid workers.
 - Add cc.*\.in2p3\.fr to MAJOR_CVMFS.  It was already in ATLAS_FRONTIER
    so it was included for installations that accept both, but not for
    those that accept only MAJOR_CVMFS.

* Thu Apr 23 2020 Dave Dykstra <dwd@fnal.gov> 4.11-2.1
- Upgrade to 4.11-2 tarball with the following release notes:
 - The 4.11 release announcement is now at
     https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00108.html
    The announcement was delayed because security vulnerabilities were
    being double-checked.
 - frontier-squid was not susceptible to the ESI vulnerability, because of
    missing libraries on the build machine.  Add --disable-esi to make
    sure it doesn't get accidentally enabled.

* Tue Apr 21 2020 Dave Dykstra <dwd@fnal.gov> 4.11-1.1
- Upgrade to 4.11-1 tarball with the following release notes:
 - Update to squid-4.11.  There's no announcement yet but the change log
    is at http://www.squid-cache.org/Versions/v4/changesets/.
 - Remove patches for bugs #5022 and #5036 which are in version 4.11. The
    patch for #5030 is still applied.

* Mon Apr 13 2020 Dave Dykstra <dwd@fnal.gov> 4.10-4.1
- Upgrade to 4.10-4 tarball with the following release note:
 - Add patch for bug 5036 which caused a varying number of capital 'L's
    to appear at the beginning of access.log lines when the log buffer
    overflows.

* Mon Mar 16 2020 Dave Dykstra <dwd@fnal.gov> 4.10-3.1
- Upgrade to 4.10-3 tarball with the following release notes:
 - Update patch for squid bug #5022 to final version.
 - Add patch for squid bug #5030 which reported that negative caching
    was not working.  This is an important feature for keeping load
    down on CVMFS stratum 1s that are not hosting a repository.

* Thu Feb 13 2020 Dave Dykstra <dwd@fnal.gov> 4.10-2.1
- Upgrade to 4.10-2 tarball with the following release notes:
 - Apply patch for squid bug #5022, to prevent a reconfigure from crashing
    the coordinator process when there are multiple workers.
 - Use reconfigure signal for log rotation in all cases again.

* Mon Feb 03 2020 Dave Dykstra <dwd@fnal.gov> 4.10-1.1
- Upgrade to 4.10-1 tarball with the following release notes:
 - Update to squid-4.10, with release notes at
    https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00103.html
   including a fix for a serious security vulnerability affecting
   reverse proxies and a potential information leak when proxying ftp.
 - Remove patch for bug #4735, as it has been included in the 4.10 release.
 - Change compressing log rotation back to use copytruncate when there
   are multiple workers, because the reconfigure signal triggers an
   SNMP bug when there are multiple workers (squid bug #5022).
 - Disable log rotatation when SQUID_MAX_ACCESS_LOG=0.  Using this is
    highly discouraged since standard logrotate is usually unable to
    keep up with the high volume of logs typically generated by squid.
    It also interferes with frontier-awstats support.
 - Change log rotating cron scripts to ignore commented lines in
    /etc/sysconfig/frontier-squid

* Mon Jan 27 2020 Dave Dykstra <dwd@fnal.gov> 4.9-5.1
- Upgrade to 4.9-4 tarball with the following release note:
 - Change compressing log rotation to not use logrotate's copytruncate.
    Instead, use create and a postrotate that sends squid a reconfigure
    signal.  This is needed when using rsyslog's imfile module to copy
    to syslog, but also greatly speeds up rotation when log files are
    large.

* Thu Jan 02 2020 Dave Dykstra <dwd@fnal.gov> 4.9-4.1
- Upgrade to 4.9-4 tarball with the following release note:
 - Limit the hard nofile ulimit check to the "start" operation.

* Tue Dec 31 2019 Dave Dykstra <dwd@fnal.gov> 4.9-3.1
- Upgrade to 4.9-3 tarball with the following release notes:
 - Apply a patch for bug #4735, to prevent caching an object when its
    http/1.1 last chunk (that is, zero-length chunk) is missing.
 - Disable the URN proto by default, to avoid potential future security
    vulnerabilities.
 - Fail if the hard nofile ulimit for the squid user is less than 4096
    (which is unlikely since it is the default value on RHEL6 & 7) and
    increase the soft nofile ulimit to match the hard limit.  Squid
    uses the soft limit as the default max_filedescriptors.  Previously
    the root portion of the startup script attempted to increase the
    soft limit to 4096, but it turned out to have no effect because
    runuser resets it to its default for that user.

* Sun Nov 10 2019 Dave Dykstra <dwd@fnal.gov> 4.9-2.1
- Upgrade to 4.9-2 tarball with the following release note:
 - Fix bug in daily cron that prevented it from rotating any logs

* Fri Nov 08 2019 Dave Dykstra <dwd@fnal.gov> 4.9-1.1
- Upgrade to 4.9-1 tarball with the following release notes:
 - Update to squid-4.9 with release notes at
    http://squid-web-proxy-cache.1019090.n4.nabble.com/squid-announce-Squid-4-9-is-available-td4688506.html
 - Add cvmfs01.nikhef.nl, cvmfs-stratum-one.zeuthen.desy.de, and
    grid-cvmfs-one.desy.de to the MAJOR_CVMFS acl.

* Thu Aug 29 2019 Dave Dykstra <dwd@fnal.gov> 4.8-2.1
- Upgrade to 4.8-2 tarball with the following release note:
 - Add support for starting and stopping shoal-agent when installed and
   enabled by SQUID_AUTO_DISCOVER=true
- Add compilation and installation for shoal-agent

* Wed Jul 17 2019 Dave Dykstra <dwd@fnal.gov> 4.8-1.1
- Upgrade to 4.8-1 tarball with the following release notes:
 - Update to squid-4.8 with release notes at
    https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00096.html
   There was no 4.7 announcement but here's the ChangeLog:
    https://github.com/squid-cache/squid/blob/f977bfa698ab92e9474c775cef0e01fb756a4b0f/ChangeLog

* Wed Jul 17 2019 Dave Dykstra <dwd@fnal.gov> 4.4-2.1
- Upgrade the 4.4-1.1 version to the 4.4-2 tarball with the following
   release note:
 - Apply security patch for CVE-2019-12527
      http://www.squid-cache.org/Advisories/SQUID-2019_5.txt
    which can (before being patched) be exploited through the ftp protocol.

* Fri May 17 2019 Dave Dykstra <dwd@fnal.gov> 4.6-2.1
- Upgrade to 4.6-2 tarball with the following release notes:
 - Add support for sending access_log through syslog
 - Add additional allowed monitoring host CERN IP range of 188.185.48.0/20

* Mon Apr 08 2019 Dave Dykstra <dwd@fnal.gov> 4.6-1.1
- Upgrade to 4.6-1 tarball with the following release notes:
 - Update to squid-4.6 with release notes at
    https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00090.html
   squid-4.5 release notes are at
    https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00089.html
 - If a rotate is blocked because processing awstats logs is running long,
   do the rotate during the next rotateiflarge cron instead.

* Wed Oct 31 2018 Dave Dykstra <dwd@fnal.gov> 4.4-1.1
- Upgrade to 4.4-1 tarball with the following release notes:
 - Update to squid-4.4 with release notes at
    https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00086.html
   including one fairly significant security fix for a potential denial
   of service due to memory leaks on rejected SNMP queries.
 - If different squid services have different numbers of workers (for
    example by using setserviceoption on "workers") then use the biggest
    number when creating cache and log directories.

* Thu Oct 04 2018 Dave Dykstra <dwd@fnal.gov> 4.3-1.1
- Upgrade to 4.3-1 tarball with the following release notes:
 - Major update to squid-4.3.
 - Removed patch for bug 4616 (patch was already applied in 4.3).
 - Replaced patch for bug 3952 with new --foreground option.
 - Ported patch for bug 7 forward.
- Compile with devtoolset-2-toolchain on el6, in order to use c++11
- Add PAM basic authentication module
- Disable security-cert-validators to avoid perl Crypt::OpenSSL:X509
  dependency

* Tue Aug 28 2018 Dave Dykstra <dwd@fnal.gov> 3.5.28-2.1
- Upgrade to 3.5.28-2 tarball with the following release notes:
 - Set umask and PATH in fn-local-squid.sh because /etc/init.d/functions
   used to set them.  This fixes problems with log rotation from cron.
 - Invoke /etc/init.d/functions from /etc/init.d/frontier-squid if it
   exists, because that is how systemd-based systems invoke systemctl
   to keep track of the service.  If it does not exist, set the PATH.

* Thu Aug 23 2018 Dave Dykstra <dwd@fnal.gov> 3.5.28-1.1
- Upgrade to 3.5.28-1 tarball with the following release notes:
 - Update to squid-3.5.28.  Here is the release announcement:
    https://www.mail-archive.com/squid-announce@lists.squid-cache.org/msg00083.html
    Removed patches for advisories SQUID-2018_1 and SQUID-2018_2 and
    for bug 4767 because fixes are included in the release.
 - Remove including /etc/init.d/functions from fn-local-squid.sh and from
   /etc/init.d/frontier-squid.  It wasn't being used and isn't in some
   docker containers such as slc6-lite.
 - If there are *.log.0.gz files in the presence of awstats, remove
   them before rotating.  They prevented rotation from working on el7.
- When creating an account for running squid under, use a home directory of
   /var/lib/squid instead of defaulting to /home/${FRONTIER_USER:-squid}.
   The old default doesn't work on systems with automounted /home.

* Thu Jul 19 2018 Dave Dykstra <dwd@fnal.gov> 3.5.27-5.2
- Add %verify (not user group) to the %ghost statements for cache dir
  and log dir, and add %verify (not user group mode) on squid.conf and
  squid.conf.old.  Without those, rpm -V complains on el7 only, not el6.

* Fri Jul 06 2018 Dave Dykstra <dwd@fnal.gov> 3.5.27-5.1
- Upgrade to 3.5.27-5 tarball with the following release note:
 - Avoid a reverse DNS lookup for every client connection by using the
   workaround in https://bugs.squid-cache.org/show_bug.cgi?id=4575,
   which is to override the defaults for url_rewrite_extras and
   store_id_extras.

* Wed Apr 18 2018 Dave Dykstra <dwd@fnal.gov> 3.5.27-4.2
- Support SELinux by default by doing resorecon -R /var/cache/squid
  during postinstall.

* Thu Mar 01 2018 Dave Dykstra <dwd@fnal.gov> 3.5.27-4.1
- Upgrade to 3.5.27-4 tarball with the following release note:
 - If the maximum listen backlog (sysctl net.core.somaxconn) is less than
   1/4th the file descriptor limit (ulimit -n) when starting squid,
   increase it to that amount.  That's the listen backlog that squid
   requests, and the larger backlog helps when a server is hit so hard
   with requests that squid can't keep up.

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

* Thu Mar 24 2016 Dave Dykstra <dwd@fnal.gov> 3.5.15-1.1
- Upgrade to 3.5.15-1 tarball with the following release notes:
 - Upgrade to squid-3.5.15.  This is the release announcement:
    http://www.spinics.net/lists/squid/msg79992.html
 - Apply patch for squid bug #2831, to send Cache-control header through
    on 304 Not Modified responses.
 - Apply patch for squid bug #4471, to make collapsed forwarding work
    when there's a previously cached but expired object.  It still does
    not work with If-Modified-Since 304 Not Modified responses (bug #2833).
    So this makes it work with CVMFS but not yet Frontier.

* Thu Oct 15 2015 Dave Dykstra <dwd@fnal.gov> 3.5.9-1.1
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

* Wed Sep 16 2015 Dave Dykstra <dwd@fnal.gov> 3.5.7-1.1
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

* Tue Sep 16 2014 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-19.1
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

* Fri Aug 22 2014 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-17.1
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

* Fri Feb 1 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-13.2
- Make /etc/squid/squid.conf a %ghost file so if someone is upgrading
  from a non-frontier squid it won't be overwritten

* Fri Feb 1 2013 Dave Dykstra <dwd@fnal.gov> 2.7.STABLE9-13.1
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

* Tue Sep 20 2011 David Front <dfront@gmail.com> 2.7.STABLE9-5.9
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
