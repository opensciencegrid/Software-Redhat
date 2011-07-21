Name:           edg-mkgridmap.spec
Version:        10
Release:        1%{?dist}
Summary:        Contains the init.d script and crontab for edg-mkgridmap

Group:          system environment/base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Source0:        edg-mkgridmap
Source1:	edg-mkgridmap-cron

# Steps to make tarball (correctly packaged):
# Get GOC's tarball, edg-mkgridmap-10.tar.gz
# tar xzf edg-mkgridmap-10.tar.gz
# cp edg-mkgridmap ./
# cp edg-mkgridmap-cron ./

%description
%{summary}

%prep

%build


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/edg-mkgridmap
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/edg-mkgridmap-cron

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/rc.d/init.d/edg-mkgridmap
%{_sysconfdir}/cron.d/edg-mkgridmap-cron

%changelog
* Thu Jul 21 2011 Neha Sharma <neha@fnal.gov> - 10-1
- Initial build of edg-mkgridmap cron and init.d package


