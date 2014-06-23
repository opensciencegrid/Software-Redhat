Summary: OASIS-specific configuration
Name: oasis-config
Version: 7
Release: 2%{?dist}
License: ASL 2.0
Group: Applications/Grid
Source0: serverorder.sh
Source1: 60-oasis.conf
Source2: opensciencegrid.org.pub
Source3: opensciencegrid.org.conf
Source4: oasis.opensciencegrid.org.conf
Source5: egi.eu.pub
Source6: egi.eu.conf
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: cvmfs
Requires: curl
Conflicts: cvmfs-keys >= 1.5

%description
%{summary}



%prep
exit 0




%build
exit 0








%install
[[ %{buildroot} != / ]] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/default.d
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/keys
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/domain.d
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/config.d
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/cvmfs
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cvmfs/default.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cvmfs/keys 
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/cvmfs/domain.d
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/cvmfs/config.d
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/cvmfs/keys 
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/cvmfs/domain.d



%clean
[[ %{buildroot} != / ]] && rm -rf %{buildroot}




%files
%{_sysconfdir}/cvmfs/*.sh
%{_sysconfdir}/cvmfs/default.d/*
%{_sysconfdir}/cvmfs/keys/*
%{_sysconfdir}/cvmfs/domain.d/*
%{_sysconfdir}/cvmfs/config.d/*



%postun
if [ $1 = 0 ]; then rm -f %{_sysconfdir}/cvmfs/domain.d/*.serverorder; fi



%changelog
* Mon Jun 23 2014 Dave Dykstra <dwd@fnal.gov> 7-2
- Include the opensciencegrid.org.pub key in egi.eu.conf, so the 
  repositories can be replaced by OSG in an emergency.

* Fri Jun 20 2014 Dave Dykstra <dwd@fnal.gov> 7-1
- Add egi.eu configuration and key.  Add serverorder.sh and a conflicts
  with cvmfs-keys >= 1.5.  Add a %postun to remove .serverorder files.

* Mon Apr 21 2014 Dave Dykstra <dwd@fnal.gov> 6-1
- Add /etc/cvmfs/default.d/60-oasis.conf to set CVMFS_SEND_INFO_HEADER=yes
  (which is a new feature for cvmfs 2.1.18)

* Wed Mar 19 2014 Dave Dykstra <dwd@fnal.gov> 5-1
- Use cvmfs-s1*.opensciencegrid.org DNS aliases for stratum 1s
- Redirect errors from rm -f $SERVER_ORDER_FILE to /dev/null because
  it is possible that it gets run as an unprivileged user from 
  cvmfs_config after an rpm upgrade

* Thu Aug 22 2013 Dave Dykstra <dwd@fnal.gov> 4-2
- Move the setting of OASIS_CERTIFICATES to where it more properly belongs
  in new file /etc/cvmfs/config.d/oasis.opensciencegrid.org.conf

* Thu Aug 22 2013 Dave Dykstra <dwd@fnal.gov> 4-1
- Add default setting for OASIS_CERTIFICATES

* Wed Jul 24 2013 Dave Dykstra <dwd@fnal.gov> 3-4
- Remove metapackage designation and specific version requirement on cvmfs.
  Instead a new metapackage osg-oasis has been created.

* Wed Jul 12 2013 Dave Dykstra <dwd@fnal.gov> 3-3
- Require cvmfs 2.1.12

* Wed Jun 26 2013 Dave Dykstra <dwd@fnal.gov> 3-2
- Require latest version of cvmfs

* Wed Jun 26 2013 Dave Dykstra <dwd@fnal.gov> 3-1
- Add BNL stratum 1

* Wed May 29 2013 Dave Dykstra <dwd@fnal.gov> 2-2
- Add --no-proxy to the wget probe in case $http_proxy is somehow set.

* Wed May 29 2013 Dave Dykstra <dwd@fnal.gov> 2-1
- Change from using the stratum 0 to using the GOC stratum 1 and
    the FNAL stratum 1 as servers.  Add logic to compute the best order
    between the servers the first time they are accessed after an rpm
    upgrade, and to store the order in a file.

* Wed Jan 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1-1
- Initial version



# vim:ft=spec
