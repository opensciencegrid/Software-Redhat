Name:           npad
Version:        1.5.6
Release:        2.2%{?dist}
Summary:        Network Diagnostic Tool

Group:          Applications/Networking
License:        BSDish
URL:            http://e2epi.internet2.edu/ndt/
Vendor:         MCNC - Advanced Services
Source0:        %{name}-%{version}.tar.gz
Source1:        npad-init
Patch0:         rhel5_python_fix.patch
Patch1:         rhel5_python_web100_swig_update.patch
Patch2:         rhel5_web100_fix.patch
Patch3:         config_xml.patch
Patch4:         dont_create_users.patch
Patch5:         diag_form_html.patch
Patch6:         makefile_rpm_fix.patch
Patch7:         pathdiag-makefile-dynlink.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  web100_userland
BuildRequires:  python-devel
BuildRequires:  chrpath
Requires:       web100_userland
Requires:       shadow-utils
Requires:       chkconfig
Requires:       initscripts

%description
NPAD/pathdiag diagnostic servers can automatically diagnose most flaws in end-systems and last-mile networks that affect end-to-end application performance. See the end-user documentation or more details on the diagnostic methods and target audience.

%package client
Summary: The Network Path and Application Diagnosis (NPAD) client.
Group: Applications/Networking

%description client
The Network Path and Application Diagnosis (NPAD) client.

%prep
%setup

# Fix an issue with NPAD and the CentOS 5.4 python version
%patch0 -p1
# Update the swig bindings to avoid problems on CentOS 5.4
%patch1 -p1
# Change the web100.h location so that it points at the proper location
%patch2 -p1

# Add the configuration file used by config.py
%patch3 -p0

# Change the Makefile to avoid creating users
%patch4 -p1

# Run the configuration script
./config.py

# Patch the html file to make it generic
%patch5 -p1

# Change the generated Makefile.config file so that it installs in the
# appropriate place for RPM
%patch6 -p1

# OSG addition: Fix pathdiag/Makefile to link using $(CC), not ld directly
%patch7 -p0

%build
make %{?_smp_mflags}

# OSG addition: Build the client
cd diag_server
gcc diag-client.c -o diag-client

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chrpath --delete %{buildroot}/opt/npad/_pathlib.so

%{__install} -D -m 0755 %SOURCE1 %{buildroot}%{_initrddir}/%{name}

# OSG addition: Package the client
%{__install} -D -m 0755 diag_server/diag-client %{buildroot}%{_bindir}/diag-client

%clean
rm -rf $RPM_BUILD_ROOT

%post

/usr/sbin/groupadd npad 2> /dev/null || :
/usr/sbin/useradd -g npad -r -s /sbin/nologin -c "NPAD User" -d /tmp npad 2> /dev/null || :

if [ $1 -gt 1 ]; then
	/sbin/service npad restart > /dev/null 2>&1 || :
fi

/sbin/chkconfig --add %{name} || :

%preun
if [ $1 = 0 ]; then
	/sbin/service npad stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del %{name} || :
fi


%files
%defattr(-,root,root,-)
/opt/npad/*
/var/lib/npad/*
%config(noreplace) %{_initrddir}/%{name}

%files client
%defattr(-,root,root,-)
%{_bindir}/diag-client

%changelog
* Wed Mar 05 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.5.6-2.2
- Remove rpath (SOFTWARE-1395)

* Thu May 23 2013 Tim Cartwright <cat@cs.wisc.edu> - 1.5.6-2.1
- Added the client subpackage.

* Thu Jan 06 2011 Aaron Brown <aaron@internet2.edu> - 1.5.6-2
- Fix an issue with stopping the server using the init script

* Tue May 04 2010 Aaron Brown <aaron@internet2.edu> - 1.5.6-1
- initial package build based on Tom Throckmorton's NDT spec
