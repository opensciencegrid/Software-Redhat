Summary: OASIS-specific configuration and metapackage for CVMFS
Name: oasis-config
Version: 2
Release: 1%{?dist}
License: ASL 2.0
Group: Applications/Grid
Source0: opensciencegrid.org.pub
Source1: opensciencegrid.org.conf
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: cvmfs
Requires: wget

%description
%{summary}



%prep
exit 0




%build
exit 0








%install
[[ %{buildroot} != / ]] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/keys
mkdir -p %{buildroot}%{_sysconfdir}/cvmfs/domain.d
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/cvmfs/keys 
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cvmfs/domain.d



%clean
[[ %{buildroot} != / ]] && rm -rf %{buildroot}




%files
%{_sysconfdir}/cvmfs/keys/*
%{_sysconfdir}/cvmfs/domain.d/*





%changelog
* Wed May 29 2013 Dave Dykstra <dwd@fnal.gov> 2-1
- Change from using the stratum 0 to using the GOC stratum 1 and
    the FNAL stratum 1 as servers.  Add logic to compute the best order
    between the servers the first time they are accessed after an rpm
    upgrade, and to store the order in a file.

* Wed Jan 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1-1
- Initial version



# vim:ft=spec
