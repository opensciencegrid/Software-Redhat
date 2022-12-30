#
# frontier_awstats :   RPM Spec file for frontier_awstats conf files
# Author: Flavia Donno <Flavia.Donno@cern.ch>
# Creation Date: 28 Jul 2010
#

Summary: Awstats config files for Frontier Servers
Name: frontier-awstats
Version: 7.7
%define releasenum 9.1
Release: %{?releasenum}%{?dist}
License: GPL
Group: System/Server
Source0: https://sourceforge.net/projects/awstats/files/AWStats/%{version}/awstats-%{version}.tar.gz
Source1: run_awstats.sh
Source2: frontier-awstats.cron
Source3: frontier-awstats.logrotate
Source4: collect_pages_data.py
Patch0: https://github.com/eldy/awstats/pull/99.patch
Patch1: awstats_own_changes.patch

Requires: perl-libwww-perl
Requires: perl-Net-IP
Requires: perl-Net-DNS
Requires: perl-Socket6
Requires: perl-IO-Socket-INET6
Requires: python3
Requires: wget
Conflicts: awstats

%define frontieruser squid
%define squidconf /etc/squid/squidconf

%define usrsharedir /usr/share
%define frontierascriptdir  %{usrsharedir}/%{name}
%define datadir /var/lib/%{name}
%define etcdir /etc/awstats

%define passwordFile %{etcdir}/password-file

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Configuration and script files for monitoring frontier server through awstats.
The monitoring information are collected by the node frontier.cern.ch.
The %version signifies awstats version that this rpm is based on.

%prep
%setup -n awstats-%{version}
%patch0 -p1
%patch1 -p1

%build

%install
/bin/rm -rf %{buildroot}

mkdir -p %{buildroot}%{frontierascriptdir}
mkdir -p %{buildroot}%{etcdir}
mkdir -p %{buildroot}%{datadir}
mkdir -p %{buildroot}/etc/cron.d
mkdir -p %{buildroot}/etc/logrotate.d

install -m 755 %{SOURCE1} %{buildroot}%{etcdir}/run_awstats.sh
install -m 644 %{SOURCE2} %{buildroot}/etc/cron.d/%{name}
install -m 644 %{SOURCE3} %{buildroot}/etc/logrotate.d/%{name}
install -m 755 %{SOURCE4} %{buildroot}%{etcdir}/collect_pages_data.py

# remove wwwroot/cgi-bin/awdownloadcsv.pl and wwwroot/cgi-bin/awredir.pl files, rename wwwroot/cgi-bin to awstats and remove other directories
rm wwwroot/cgi-bin/awdownloadcsv.pl
rm wwwroot/cgi-bin/awredir.pl
mv wwwroot/cgi-bin awstats
ls | grep -v awstats | xargs rm -r

cd awstats
find * |cpio -pd %{buildroot}%{frontierascriptdir}

# this is installed in a different directory
install -m 644 %{buildroot}%{frontierascriptdir}/awstats.model.conf %{buildroot}%{etcdir}
/bin/rm -f %{buildroot}%{frontierascriptdir}/awstats.model.conf


%post
if [ -s %{squidconf} ]; then
    source %{squidconf}
fi
if [ -z ${FRONTIER_USER} ]; then
    export FRONTIER_USER=%{frontieruser}
fi

# change permissions for frontier-awstats data files
find %{datadir} -type f ! -perm 644 | xargs -r chmod 644

# remove a DNS cache file
rm -f %{datadir}/*/dnscachelastupdate.*.txt

# clean out old awstatsconf, if any, so a fresh one will be generated
rm -f %{etcdir}/awstatsconf

if [ ! -e %{passwordFile} ]; then
    > %{passwordFile}
fi
chmod 600 %{passwordFile}
if getent passwd ${FRONTIER_USER} >/dev/null 2>&1; then
    chown -R ${FRONTIER_USER} %{etcdir} %{datadir}
fi

if [ -e /var/spool/cron/${FRONTIER_USER} ]; then
    # Removing lines from crontab, in case upgrading from previous release
    #  that had cron lines with %{name} or chkthread.log in it
    sed -i -e '/^1,16,31,46.*\/'%{name}'/d' \
           -e '/^59 23.*\/'%{name}'/d' \
	   -e '/chkthread.log/d' \
	   /var/spool/cron/${FRONTIER_USER}
    if [ ! -s /var/spool/cron/${FRONTIER_USER} ]; then
      # remove if now empty
      rm -f /var/spool/cron/${FRONTIER_USER}
    fi
fi

# remove logdir from previous release, if any
LOG_DIR_OLD=/var/log/%{name}
if [ -d ${LOG_DIR_OLD} ]; then
    /bin/rm -r ${LOG_DIR_OLD}
fi

# remove unused generated files from previous release, if any
/bin/rm -f %{etcdir}/awstats.conf %{etcdir}/chkthread.sh %{etcdir}/chkthread.log*
/bin/rm -rf %{etcdir}/chkthread_* %{etcdir}/.chkthread_parsestart.num
/bin/rm -f %{etcdir}/squidmodifiedqueries.logrotate %{etcdir}/squidmodifiedqueries.logrotate.status
/bin/rm -f /var/log/squid/squidmodifiedqueries.*

%preun
if [ $1 -eq 0 ]; then
   # full uninstall
   rm -rf /var/lib/%{name}/*
fi

%clean
%{__rm} -rf %{buildroot}

%files
%verify(not user group) %{datadir}/
%verify(not user group) %{frontierascriptdir}/
%verify(not user group) %{etcdir}/
%verify(not user group) /etc/cron.d/%{name}
%verify(not user group) /etc/logrotate.d/%{name}

%changelog
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 7.7-9.1
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Wed Sep 15 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-9
- Rename DNS last update cache file to another file instead of deleting
  it.

* Thu Aug 12 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-8
- Append lines to the end of awstatscron.log instead of overwriting the
  file.
- Make run_awstats.sh more efficient at looking up host names.

* Mon May 03 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-7
- Support processing squid syslog logs in collect_pages_data.py.

* Mon Apr 26 2021 Dave Dykstra <dwd@fnal.gov> 7.7-6
- Remove precheck for the $FRONTIER_USER account because it is not
  required for apache-only awstats.

* Thu Apr 22 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-5
- Make apache and squid paths consistent.

* Thu Mar 11 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-4
- Treat characters as bytes when run_awstats.py generates TMPFILE file.

* Fri Mar 05 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-3
- Use binary mode instead of text mode when collect_pages_data.py reads
  input file.

* Tue Feb 23 2021 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-2
- Increase number of records to save in DNS last update cache file from 500
  to 10000.
- Clear DNS last update cache file once per day.
- Change run_awstats.sh rsync options from the rsync -av to rsync -rlptv.
- Process the new data of squid log instead of the whole squid log.
- Add source collect_pages_data.py. It counts for all combinations of IP
  addresses and the 2 path components.
- Add Python 3 requirement.
- Remove 0 from ValidHTTPCodes.

* Wed Sep 09 2020 Dave Dykstra <dwd@fnal.gov> 7.7-1.2
- Make failure to find httpd alias in mapping file to be non-fatal, because
  that is the normal case on stratum 1s using a frontier-squid frontend.

* Mon Mar 30 2020 Edita Kizinevic <edita.kizinevic@cern.ch> 7.7-1.1
- Upgrade to awstats-7.7
- Download awstats from official page.
- Add patch files. wwwroot/cgi-bin/awdownloadcsv.pl and
  wwwroot/cgi-bin/awredir.pl files are removed, wwwroot/cgi-bin
  directory is renamed to awstats. Other directories are removed.

* Mon Aug 12 2019 Dave Dykstra <dwd@fnal.gov> 6.9-5.3
- Fix the shortening of URLs with syslog logs.
- Remove %config on /etc/awstats so any edits will be overwritten.

* Thu Aug 01 2019 Edita Kizinevic <edita.kizinevic@cern.ch> 6.9-5.2
- Add source frontier-awstats.cron.
- Add source frontier-awstats.logrotate.
- Remove frontier-squid requirement.
- Make changes to run_awstats.sh in order to include httpd access log.

* Mon Jun 17 2019 Edita Kizinevic <edita.kizinevic@cern.ch> 6.9-5.1
- Change permissions for frontier-awstats data files.
  SaveDatabaseFilesWithPermissionsForEveryone is set to 0 instead of 1.

* Fri May 17 2019 Dave Dykstra <dwd@fnal.gov> 6.9-4.5
- Support processing squid logs that have been sent through syslog.

* Tue Apr 23 2019 Edita Kizinevic <edita.kizinevic@cern.ch> 6.9-4.4
- Enable IPv6 transport by requiring perl-Socket6 and perl-IO-Socket-INET6
  packages.
- Add timestamp in the log when the awstats client is finished running.
- Remove a DNS cache file.

* Mon Feb 19 2018 Dave Dykstra <dwd@fnal.gov> 6.9-4.3
- Clean out existing /etc/awstats/awstatsconf if any, during post install.
  This was added because at some point a mistake in the mapping file
  caused extra lines to be added to awstatsconf which were causing
  non-fatal error messages.
- Take only the first match of a node from the mapping file when generating
  awstatsconf.

* Mon Feb 19 2018 Dave Dykstra <dwd@fnal.gov> 6.9-4.2
- Add rsync timeouts to prevent it from hanging indefinitely.
- Add Requires: wget.

* Mon May 23 2016 Dave Dykstra <dwd@fnal.gov> 6.9-4.1
- Enable IPv6 plugin.  Requires perl-Net-IP and perl-Net-DNS.

* Thu Sep 10 2015 Dave Dykstra <dwd@fnal.gov> 6.9-3.3
- Move a temporary file from /tmp to the same directory as the input log
  in case /tmp is too small.

* Wed Apr 22 2015 Dave Dykstra <dwd@fnal.gov> 6.9-3.2
- Keep separate configuration and data directories when frontier-squid is
  configured to run multiple squids, to separately keep statistics on
  each of the squids.

* Fri Dec 19 2014 Dave Dykstra <dwd@fnal.gov> 6.9-3.1
- Update to 6.9-3 tarball which only removes a couple of unused files
- Remove chkthread monitor generation from this rpm (it is moved to
  frontier-maxthreads rpm)
- Change awstats monitoring host to be wlcg-squid-monitor.cern.ch
  instead of frontier.cern.ch
- Remove generation of squidmodifiedqueries, which was a squid log subset
- Remove relocatability of rpm to simplify it
- Fully clean up files in /var/lib/frontier-awstats on final uninstall
- Move release notes into %changelog instead of separate file

* Fri Aug 29 2014 Dave Dykstra <dwd@fnal.gov> 6.9-1.2
- Remove requirement that /etc/awstats/password-file exists before
  rpm installation.  Create it at install time as an empty file if
  it doesn't exist.
- Do not install the chkthread cron entries if frontier-tomcat is
  not installed.

* Fri Sep 07 2012 Dave Dykstra <dwd@fnal.gov> 6.9-1.1
- Change release numbers to be based on the underlying awstats
  package release number from the internet.
- Add chkthread data collection to be able to plot frontier
  servlet threads, response time, and database response times, if
  the frontier tomcat log exists.  This has little to do with
  awstats except that it is needed on the same machines (frontier
  launchpads) and uses the same mechanism for uploading data
  (rsync to frontier.cern.ch).  This data is collected every 5
  minutes instead of the once an hour collection of awstats.
- Keep track of previously downloaded node name alias and 
  site+project name, in /etc/awstats/awstatsconf.  Then if the
  download (from frontier.cern.ch) fails, re-use the previous
  values.  The chkthread data collection then uses the same file
  so it doesn't need to know how to do the download.
- Keep the awstats config template in /etc/awstats/awstats.model.conf
  instead of /etc/awstats/awstats.conf so people don't think it is
  an actively used configuration.
- Keep the first two components of URLs from the squid log instead
  of just the first one; that causes no harm for Frontier (the second
  URL component is always "Frontier") and is helpful for CVMFS.
- Change directory of support files from /usr/share/awstats to
  /usr/share/frontier-awstats.
- Remove support for /etc/awstats/customize.sh

* Thu Jun 28 2012 David Front <dfront@gmail.com> 6.0-17
- A small technical change at the spec file to support source rpms for
  frontier rpms 
- Use symbolic link to unproto.sh to simplify source tar ball creation

* Wed Dec 21 2011 David Front <dfront@gmail.com> 6.0-16
- At upgrade, remove no-more-needed directory/file/lines:
  -- logs dir: ${RPM_INSTALL_PREFIX}/var/log/fontier-awstats
  -- file: ${RPM_INSTALL_PREFIX}/usr/share/awstats/squid_rotate_run_awstats.sh
  -- awstats crontab entries
- Rename /etc/awstats/squid_rotate_run_awstats.sh to /etc/awstats/run_awstats.sh
- Simplify run_awstats.sh: No need to set LogFile at awstats configuration
  file, because this is over ridden by an argument to awstats.pl
- Cause run_awstats.sh to be more robust:
  If configuration creation fails, exit, and do not overwrite previous
  configuration.

* Sun Dec 18 2011 David Front <dfront@gmail.com> 6.0-15
- Apply fix at src/usr/share/awstats/squid_rotate_run_awstats.sh.proto
  by Dave Dykstra to support non aliased DNS names. 
- Remove ${RPM_INSTALL_PREFIX}/usr/share/awstats/squid_rotate.sh 
  This script is installed by cms awstats tar, but is not used by the rpm.
- Now, squid calls the awstats script, if it exists,
  to prevent related bugs and simplify the code.

* Tue Nov 29 2011 David Front <dfront@gmail.com> 6.0-14
- Complete support of rpm verify, command:'rpm -V':
  Do not remove *.unproto files (after usage), in order to cause "rpm
  -V" to pass.

* Sun Nov 27 2011 David Front <dfront@gmail.com> 6.0-13
- Supporting rpm verify, command:'rpm -V':
  -- Add the prefix '%verify(not user group)' to each %files entry, 
     in order to prevent complaints from 'rpm -V', like:
	.....UG.    <fileName>
  -- Note, however, that 'rpm -V' may still create misleading complaints like:
	missing   ... <fileName>.proto

* Sun Nov 13 2011 David Front <dfront@gmail.com> 6.0-12
- Remove the recent kludges to clean BEGIN_SIDER and to handle IP
- Add test that password-file exists as prerequisite to install
- Rotate of modifiedqueries.log moved from frontier-tomcat to frontier-awstats
  rpm, to avoid dependency between user of frontier-tomcat and frontier-squid
  rpms'
- support default squid user being squid (if the file /etc/squid/squidconf is
  missing).

* Sun Oct 30 2011 David Front <dfront@gmail.com> 6.0-11
- Kludge to artificially avoid huge awstats logs:
  At src/usr/share/awstats/squid_rotate_run_awstats.sh.proto:
  If /etc/awstats/customize.sh has a record like
     export RM_BEGIN_SIDER=1
  then remove all records of awstats files between BEGIN_SIDER and END_SIDER.

* Sun Oct 30 2011 David Front <dfront@gmail.com> 6.0-10
- At src/usr/share/awstats/squid_rotate_run_awstats.sh.proto
- preprocess log to have only the last ip and no surrounding " character

* Thu Oct 27 2011 David Front <dfront@gmail.com> 6.0-9
- at src/usr/share/awstats/squid_rotate_run_awstats.sh.proto
  - code taken from cmsfrontier1:~dbfrontier/local/etc/squid_rotate.sh
    added, with comment starting as:
      Change the URL into just the servlet name

* Mon Oct 24 2011 David Front <dfront@gmail.com> 6.0-8
- Shorten the time awstats files are kept locally from 40 to 20 days,
  in order to prevent the /var partition to fill up.

* Tue Oct 18 2011 David Front <dfront@gmail.com> 6.0-7
- change src/usr/share/awstats/squid_rotate_run_awstats.sh.proto
  to be generic for all hosts that should report awstats.
  For this, a central new file is used, to map siteProjects to their
  'DNS alias' and 'awstats name':
      http://frontier.cern.ch/dist/rpms/awstatsSiteProjectNodesMapping

* Sun Sep 04 2011 David Front <dfront@gmail.com> 6.0-6
- fix bug at /usr/share/awstats/squid_rotate_run_awstats.sh.proto 

* Sun Aug 28 2011 David Front <dfront@gmail.com> 6.0-5
- Following remarks from Emmanouil Vamvakopoulos and Dave Dykstra
    Changed script src/usr/share/awstats/squid_rotate_run_awstats.sh.proto
    to allow setting DirData at /etc/awstats/customize.sh

    Example: sed_conf DirData       /data/dbfrontier/frontier-awstats

    Remark: Contrary to previous remarks at /etc/awstats/customize.sh.example_CERN,
    the use of 'quoted values' (a "value" for value with more than one word)
    is needed for values with more than one word, 
    not for single vorder value like DirData

* Sun Jul 31 2011 David Front <dfront@gmail.com> 6.0-4
- At spec file. 
    Add: 
	Requires: perl-libwww-perl
    Remove:
	Requires: frontier-squid >= 2.7.STABLE9-5.5
	Fix bug: attempted to source a wrong configuration file at install

* Wed Jul 27 2011 David Front <dfront@gmail.com> 6.0-3
- Fix bug: awstats did not update squid_logs upon change of it at /etc/squid/customize.sh

* Wed Jul 20 2011 David Front <dfront@gmail.com> 6.0-2
- Added dependancy on frontier-squid rpm
- Base dir is taken from squid and may differ from the default: /data 
- User to install at is taken from may differ from the default: dbfrontier

* Thu Jun 2 2011 David Front <dfront@gmail.com> 6.0-1
- Following discussions with Barry Blumenfeld and Dave Dykstra, it has
  been understood that relying on awstats original code, rather than
  on the code changed by cms causes the result frontier-awstats data
  to miss "Request size" and "Request time" numbers.  Hence, this
  release relies on cms tar ball (that is based on awtats 6.0) rather
  than on awstats rpm.
- The script untemplate.sh is being replaced by unproto.sh.  In
  essence, they do the same, but unproto.sh expects files calles
  X.proto (rather than X.template).  In addition, after applying
  unproto on a file, its X.proto file is removed, and after applying
  unproto to all proto files, the unproto.sh script is removed (may be
  found at rpm or svn)
- Verious bug fixes. In particular, reloaction is now supported,
  except for files at /etc/awstats.

* Sun May 22 2011 David Front <dfront@gmail.com> 6.95-1
- The version signifies the dependent version of awstats rpm
- frontier-awstats scripts moved to /usr/share/awstats
- The content of configurator.sh has been made smaller and was moved
  into the spec file

* Sun Mar 27 2011 David Front <dfront@gmail.com> 1.0-2
- Initial release
- Originating from http://grid-deployment.web.cern.ch/grid-deployment/flavia/frontier-awstats-1.0-1.*.rpm 
- Changes:
    - awstats.pl is resident at the rpm, rather than being taken from
      awstats.prm as was the case previously.
    - (Hence) the dependency of awstats rpm has been removed.
    - The directory of awstats.pl file has been moved.
    - The file /data/dbfrontier/frontier-awstats/password-file has
      been removed from the rpm, and hence has to be installed
      manually.
    - Many parameters may be edited manually, per site (per server
      machine), as detailed at the frontier-awstatsREADME file
    - Correctly support SQUID_RELOCATION at squid_rotate.sh
    - Support installa at standard linux directories (or relacate)
