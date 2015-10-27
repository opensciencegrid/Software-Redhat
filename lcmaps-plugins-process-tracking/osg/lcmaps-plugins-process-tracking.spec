Summary: Process tracking plugin for the LCMAPS authorization framework
Name: lcmaps-plugins-process-tracking
Version: 0.3
Release: 1%{?dist}
License: Public Domain
Group: System Environment/Libraries
# The tarball was created from Subversion using the following commands:
# svn co svn://t2.unl.edu/brian/lcmaps-plugin-process-tracking
# cd lcmaps-plugin-process-tracking
# ./bootstrap
# ./configure
# make dist
Source0: %{name}-%{version}.tar.gz

BuildRequires: lcmaps-interface

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This plugin utilizes the Kernel proc connector interface to 
track the processes spawned by glexec.

%prep
%setup -q

%build

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT/%{_libdir}/lcmaps/liblcmaps_process_tracking.la
rm $RPM_BUILD_ROOT/%{_libdir}/lcmaps/liblcmaps_process_tracking.a
mv $RPM_BUILD_ROOT%{_libdir}/lcmaps/liblcmaps_process_tracking.so $RPM_BUILD_ROOT%{_libdir}/lcmaps/lcmaps_process_tracking.mod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/lcmaps/lcmaps_process_tracking.mod
%{_datadir}/%{name}/process-tracking

%changelog
* Mon Aug 13 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.2-1
- Integrate with the pool accounts package to provide solution for anonymous accounts.

* Sun Feb 05 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1.1-1
- Small bugfixes for RHEL6 platforms.

* Sun Jan 08 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1.0-2
- Update to the new LCMAPS modules directory.

* Sun Jan 08 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1.0-1
- Factor process tracking into a separate executable.

* Wed Sep 28 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.5-1
- Correctly call waitpid to avoid zombie.  A few code warning cleanups.

* Fri Sep 23 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.0.4-1
- Initial build of the process tracking plugin.
