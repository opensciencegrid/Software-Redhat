Summary: OASIS-specific configuration and metapackage for CVMFS
Name: oasis-config
Version: 1
Release: 1%{?dist}
License: ASL 2.0
Group: Applications/Grid
Source0: opensciencegrid.org.pub
Source1: opensciencegrid.org.conf
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: cvmfs

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
* Wed Jan 16 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1-1
- Initial version



# vim:ft=spec
