%define version 1.0.0
%define release 1
%define BINARY_FILE condor_root_switchboard

Name:       glideinwms-switchboard
Version:    %{version}
Release:    %{release}%{?dist}
Summary:    This package is used in all Factories to prevent permissions problems
Group:      System Environment/Libraries
License:    Fermitools Software Legal Information (Modified BSD License)
URL:        http://glideinwms.fnal.gov
Source:     glideinwms-switchboard-v1_0_0.tar.gz

%description
This is a package to prevent permissions problems when privilege separation is
used in all Factories to write log files (stdout/err and condor log for glideins)
and credentials as the owners are different .
Clean out of client log and proxy files use it as well.

%prep
%setup -q -n glideinwms-switchboard

%build
make %{BINARY_FILE}

%install
mkdir -p "%{buildroot}%{_sbindir}"
cp %{BINARY_FILE} "%{buildroot}%{_sbindir}/"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sbindir}/%{BINARY_FILE}
%attr(6755, root, root) %{_sbindir}/%{BINARY_FILE}

%changelog
* Wed May 16 2018 Lorena Lobato Pardavila <llobato@fnal.gov> - v1_0_0
- Initial build.
