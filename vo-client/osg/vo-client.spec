Name:           vo-client
Version:        38
Release:        7%{?dist}
Summary:        Contains vomses file for use with user authentication and edg-mkgridmap.conf file that contains configuration information for edg-mkgridmap.

Group:          system environment/base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       osg-ca-certs

Source0:        %{name}-%{version}-1.tar.gz

# Steps to make tarball (correctly packaged):
# Get GOC's tarball, vo-client-38.tar.gz
# tar xzf vo-client-38.tar.gz
# cp vomses ./
# cp edg-mkgridmap.conf ./

# Generate LSC files
# /usr/sbin/osg-make-vomsdir --vomsdir vomsdir --vomses vomses


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
tar -xz -C $RPM_BUILD_DIR --strip-components=1 -f %{SOURCE0}
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
mv $RPM_BUILD_DIR/vomses $RPM_BUILD_ROOT/%{_sysconfdir}/
mv $RPM_BUILD_DIR/edg-mkgridmap.conf $RPM_BUILD_ROOT/%{_sysconfdir}/

chmod 644 $RPM_BUILD_ROOT/%{_sysconfdir}/vomses $RPM_BUILD_ROOT/%{_sysconfdir}/edg-mkgridmap.conf

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/
mv $RPM_BUILD_DIR/vomsdir $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/
find $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir -type f -exec chmod 644 {} \;
find $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir -type d -exec chmod 755 {} \;

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/vomses
%config(noreplace) %{_sysconfdir}/grid-security/vomsdir

%files edgmkgridmap
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/edg-mkgridmap.conf


%changelog
* Wed Aug 03 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-7
- Fixed engage's lsc file

* Fri Jul 22 2011 Igor Sfiligoi <isfiligoi@ucsd.edu> - 38-6
- Change RPM to extract directly from the upstream tarball
- Expect the vomsdir to be in the upstream tarball

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


