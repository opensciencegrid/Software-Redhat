Name:           vo-client
Version:        38
Release:        5%{?dist}
Summary:        Contains vomses file for use with user authentication and edg-mkgridmap.conf file that contains configuration information for edg-mkgridmap.

Group:          system environment/base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       osg-ca-certs

Source0:        vomses
Source1:	edg-mkgridmap.conf

# Steps to make tarball (correctly packaged):
# Get GOC's tarball, vo-client-38.tar.gz
# tar xzf vo-client-38.tar.gz
# cp vomses ./
# cp edg-mkgridmap.conf ./

# Generate LSC files
# ./osg/root/usr/sbin/vdt-make-vomsdir --vomsdir osg/root/etc/grid-security/vomsdir --vomses osg/root/etc/vomses


%description
%{summary}

%package edgmkgridmap
Summary:	edg-mkgridmap.conf file that contains configuration information for edg-mkgridmap 
Group:          system environment/base
Requires:       %{name} = %{version}-%{release}
Requires:       vo-client-edgmkgridmap

%description edgmkgridmap 
%{summary}

%prep

%build


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}/vomses
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/edg-mkgridmap.conf

#install -d $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir
#cp -r etc/grid-security/vomsdir/* $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/vomses

%files edgmkgridmap
%defattr(-,root,root,-)
%{_sysconfdir}/edg-mkgridmap.conf


%changelog
* Thu Jul 21 2011 Neha Sharma <neha@fnal.gov> - 38-5
- Modified the directory structure. Only needs files at top level

* Wed Jul 20 2011 Neha Sharma <neha@fnal.gov> - 38-4
- Added vo-client-edgmkgridmap

* Tue Jul 19 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-3
- Removed vdt-make-vomsdir.  It now has it's own rpm

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-2
- Added vdt-make-vomsdir and cleaned up packaging

* Fri Jul 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-1
- Initial build of vo-client


