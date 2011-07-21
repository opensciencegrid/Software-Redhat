
Name:      rsv-consumers
Version:   3.4.0
Release:   1%{?dist}
Summary:   RSV Consumers Infrastructure

Group:     Applications/Monitoring
License:   Apache 2.0
URL:       https://twiki.grid.iu.edu/bin/view/MonitoringInformation/RSV

Source0:   %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  mock
Requires:  rpm-build
Requires:  createrepo
#Requires:  apache #TODO

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
%{summary}


%prep
%setup -q


%install
rm -fr $RPM_BUILD_ROOT

# Create the web output directory
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

# Install executables
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/rsv
cp -r libexec/consumers $RPM_BUILD_ROOT%{_libexecdir}/rsv/

# Install configuration
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta
cp -r etc/meta/consumers $RPM_BUILD_ROOT%{_sysconfdir}/rsv/meta/
cp -r etc/consumers $RPM_BUILD_ROOT%{_sysconfdir}/rsv/
cp etc/rsv-nagios.conf $RPM_BUILD_ROOT%{_sysconfdir}/rsv/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)

# This package owns this directory and everything in it
%{_libexecdir}/rsv/consumers/

%config %{_sysconfdir}/rsv/meta/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/consumers/*
%config(noreplace) %{_sysconfdir}/rsv/rsv-nagios.conf


%changelog
* Thu Jul 20 2011 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.4.0-1
- Creating a first RPM for rsv-consumers
