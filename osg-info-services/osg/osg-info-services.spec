
Name:      osg-info-services
Summary:   OSG Information Services uploader
Version:   1.0.2
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch


# Performed on 19 February 2015
# svn export https://vdt.cs.wisc.edu/svn/software/osg-info-services/tags/1.0.2 osg-info-services-1.0.2
# tar czf osg-info-services-1.0.2.tar.gz osg-info-services-1.0.2
Source0:   %{name}-%{version}.tar.gz

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
* Thu Feb 19 2015 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.2-1
- Bypass http proxy (SOFTWARE-1797)

* Fri Feb 21 2014 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0.1-1
- Quiet cron job (SOFTWARE-1383)

* Mon Nov 25 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.0-2
- Upstreamed patches
- Do not hardcode ConsumerURL (SOFTWARE-1224)
- Fix ownership of /var/log/gip/gip.log (SOFTWARE-1273)
- Don't print a stack backtrace when dying due to missing user-vo-map (also SOFTWARE-1273)
- Fix exception in the fix to SOFTWARE-1225
- Bump to 1.0

* Thu Oct 31 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.12-4
- Add patch to improve error message when uploading fails (SOFTWARE-1225)

* Wed Oct 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.12-3
- Add patch to work around command-line argument bug (SOFTWARE-1223)

* Tue Oct 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.12-2
- Bump to rebuild with sources from SVN

* Mon Oct 07 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.12-1
- Update to 0.12

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


