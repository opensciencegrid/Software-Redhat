%define version 1.0.0
%define release 1
BINARY_FILE=condor_root_switchboard
PKG_NAME=glideinwms-switchboard

Name:       glideinwms-switchboard
Version:    %{version}
Release:    %{release}%{?dist}
Summary:    This package is used in all Factories to prevent permissions problems
Group:      System Environment/Libraries
License:    Fermitools Software Legal Information (Modified BSD License)
URL:        http://glideinwms.fnal.gov
BuildArch:  noarch
Source:     glideinwms-switchboard.tar.gz

%description
This is a package to prevent permissions problems when privilege separation is
used in all Factories to write log files (stdout/err and condor log for glideins)
and credentials as the owners are different .
Clean out of client log and proxy files use it as well.

%prep
%setup -q -n glideinwms-switchboard

%build
make $BINARY_FILE

%install
mkdir -p "%{buildroot}/opt/${PKG_NAME}"
cp $BINARY_FILE "%{buildroot}/opt/${PKG_NAME}/"

%clean
rm -rf $RPM_BUILD_ROOT

%files
/opt/${PKG_NAME}/${BINARY_FILE}

%changelog
* Wed May 16 2018 Lorena Lobato Pardavila <llobato@fnal.gov> - 1.0.0
- Initial build.
