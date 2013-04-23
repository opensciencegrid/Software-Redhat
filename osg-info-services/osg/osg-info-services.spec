
Name:      osg-info-services
Summary:   OSG Information Services uploader
Version:   0.11
Release:   2%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

# Performed on 26 February 2012; r4612
# svn export svn://t2.unl.edu/brian/osg_info_services osg-info-services-0.11
# tar zcf osg-info-services-0.11.tar.gz osg-info-services-0.11/
Source0:   %{name}-%{version}.tar.gz

Patch0: fix-bool.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: gip

%description
%{summary}

%prep
%setup -q

%patch0 -p0

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
* Mon Apr 22 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 0.11-2
- Fix reporting of boolean values.

* Sun Feb 26 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.11-1
- Fix for directory ownership issues in GIP 1.3.4.

* Fri Feb 03 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 0.10-2
- Adding dist tag to osg-info-services

* Wed Dec 14 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.10-1
- Improved error message.

* Wed Aug 03 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 0.9-1
- Initial packaging of osg-info-services.


