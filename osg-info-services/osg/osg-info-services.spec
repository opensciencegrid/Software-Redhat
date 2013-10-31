
Name:      osg-info-services
Summary:   OSG Information Services uploader
Version:   0.12
Release:   4%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

# Performed on 08 October 2013
# svn export https://vdt.cs.wisc.edu/svn/software/osg-info-services/tags/v0.12 osg-info-services-0.12
# tar czf osg-info-services-0.12.tar.gz osg-info-services-0.12
Source0:   %{name}-%{version}.tar.gz

Patch0: fix-bool.patch
Patch1: 1223-cmdline-args.patch
Patch2: 1225-error-msg.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: gip

%description
%{summary}

%prep
%setup -q

%patch0 -p0
%patch1 -p0
%patch2 -p0

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


