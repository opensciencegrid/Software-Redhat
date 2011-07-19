Name:           vo-client
Version:        38
Release:        3%{?dist}
Summary:        Vomses file for use with user authentication

Group:          system environment/base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       osg-ca-certs


# Steps to make tarball (correctly packaged):
# Get GOC's tarball, vo-client-38.tar.gz
# tar xzf vo-client-38.tar.gz
# cp voms/etc/vomses osg/root/etc/vomses

# Generate LSC files
# ./osg/root/usr/sbin/vdt-make-vomsdir --vomsdir osg/root/etc/grid-security/vomsdir --vomses osg/root/etc/vomses



%description
%{summary}

%prep
tar xzf %{SOURCE0}


%build


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -m 644 etc/vomses $RPM_BUILD_ROOT/%{_sysconfdir}/vomses

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir
cp -r etc/grid-security/vomsdir/* $RPM_BUILD_ROOT/%{_sysconfdir}/grid-security/vomsdir/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/vomses
%{_sysconfdir}/grid-security/vomsdir


%changelog
* Tue Jul 19 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-3
- Removed vdt-make-vomsdir.  It now has it's own rpm

* Mon Jul 18 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-2
- Added vdt-make-vomsdir and cleaned up packaging

* Fri Jul 15 2011 Derek Weitzel <dweitzel@cse.unl.edu> - 38-1
- Initial build of vo-client


