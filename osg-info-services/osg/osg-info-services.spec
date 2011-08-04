
Name:      osg-info-services
Summary:   OSG Information Services uploader
Version:   0.9
Release:   1
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

# Performed on 3 August 2011; r4507
# svn export svn://t2.unl.edu/brian/osg_info_services osg-info-services-0.9
# tar zcf osg-info-services-0.9.tar.gz osg-info-services-0.9/
Source0:   osg-info-services-0.9.tar.gz

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: gip

%description
%{summary}

%prep
%setup -q

%build
# No building - just a few python scripts!

%install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -m 755 osg-info-services.init $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
install -m 644 osg-info-services.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 755 osg-info-services $RPM_BUILD_ROOT%{_sbindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%{_sbindir}/%{name}

%changelog
* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.9-1
- Initial packaging of osg-info-services.


