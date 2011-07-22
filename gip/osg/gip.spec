Summary: Generic Information Provider
Name: gip
Version: 1.3.0alpha2
Release: 1%{?dist}
License: TODO
Group: Applications/Grid
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#Packager: VDT <vdt-support@opensciencegrid.org>
#BuildRequires: 
Requires: python
#Requires:           initscripts
#Requires(post):     chkconfig, /sbin/ldconfig
#Requires(preun):    chkconfig
#Requires(postun):   /sbin/ldconfig
AutoReq: yes
AutoProv: yes

Source0: %{name}-%{version}.tgz

%description

The Generic Information Provider.  More text to go here.

%prep
%setup -q

%install
rm -rf %{buildroot}

# Set the Python version
%define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

install -d %{buildroot}%{python_sitelib}
cp -a gip/lib/python/* %{buildroot}%{python_sitelib}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libexecdir}/%{name}/plugins
install -d %{buildroot}%{_libexecdir}/%{name}/providers
install -d %{buildroot}%{_libexecdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_localstatedir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}

install -m 644 gip/etc/logging.conf %{buildroot}%{_sysconfdir}/%{name}
cp -a gip/etc/logging.conf %{buildroot}%{_sysconfdir}/%{name}
cp -a gip/plugins %{buildroot}%{_libexecdir}/%{name}
cp -a gip/providers %{buildroot}%{_libexecdir}/%{name}
cp -a gip/templates %{buildroot}%{_datadir}/%{name}
cp gip/libexec/* %{buildroot}%{_libexecdir}/%{name}


cp -a gip/var/ldif %{buildroot}%{_localstatedir}/%{name}
cp -a gip/var/tmp %{buildroot}%{_localstatedir}/%{name}

cp gip/bin/* %{buildroot}%{_bindir}

%files
%defattr(-,daemon,daemon,-)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libexecdir}/*
%{python_sitelib}/*
%{_datadir}/%{name}
%{_sysconfdir}/%{name}
%attr(-, daemon, daemon) %{_localstatedir}/%{name}

%clean
rm -rf %buildroot


%define _unpackaged_files_terminate_build 1




%changelog
* Wed Jul 20 2011 Burt Holzman <burt@fnal.gov> 1.3.0alpha2-1
- Initial build


