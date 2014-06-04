Name:      osg-version
Summary:   OSG Version
Version:   3.1.35
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org
BuildArch: noarch

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:   osg-version

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo %{version} > $RPM_BUILD_ROOT%{_sysconfdir}/osg-version
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/osg-version

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -pm 755 %{SOURCE0}  $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sysconfdir}/osg-version
%{_bindir}/osg-version

%changelog
* Wed Jun 04 2014 Brian Lin <blin@cs.wisc.edu> - 3.1.35-1
- Updated to 3.1.35-1

* Thu May 22 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.1.34-1
- Updated to 3.1.34-1

* Tue May 06 2014 Tim Theisen <tim@cs.wisc.edu> - 3.1.33-1
- Updated to 3.1.33-1

* Mon Mar 31 2014 Brian Lin <blin@cs.wisc.edu> - 3.1.32-1
- Updated to 3.1.32-1

* Tue Mar 04 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.1.31-1
- Updated to 3.1.31-1

* Fri Feb 07 2014 Brian Lin <blin@cs.wisc.edu> - 3.1.30-1
- Updated to 3.1.30-1

* Wed Jan 08 2014 Tim Theisen <tim@cs.wisc.edu> - 3.1.29-1
- Updated to 3.1.29-1

* Fri Dec 13 2013 Tim Theisen <tim@cs.wisc.edu> - 3.1.28-1
- Updated to 3.1.28-1

* Thu Dec 05 2013 Tim Theisen <tim@cs.wisc.edu> - 3.1.27-1
- Updated to 3.1.27-1

* Fri Nov 07 2013 Brian Lin <blin@cs.wisc.edu> - 3.1.26-1
- Updated to 3.1.26-1

* Mon Oct 07 2013 Tim Theisen <tim@cs.wisc.edu> - 3.1.25-1
- Updated to 3.1.25-1

* Mon Sep 23 2013 Tim Theisen <tim@cs.wisc.edu> - 3.1.24-1
- Updated to 3.1.24-1

* Mon Sep 09 2013 Brian Lin <blin@cs.wisc.edu> - 3.1.23-1
- Updated to 3.1.23-1

* Mon Aug 12 2013 Brian Lin <blin@cs.wisc.edu> - 3.1.22-1
- Updated to 3.1.22-1

* Mon Jul 08 2013 Tim Theisen <tim@cs.wisc.edu> - 3.1.21-1
- Updated to 3.1.21-1

* Thu Jun 20 2013 Tim Theisen <tim@cs.wisc.edu> - 3.1.20-1
- Updated to 3.1.20-1

* Mon Jun 10 2013 Brian Lin <blin@cs.wisc.edu> - 3.1.19-1
- Updated to 3.1.19-1

* Mon May 13 2013 Tim Theisen <tim@cs.wisc.edu> - 3.1.18-1
- Updated to 3.1.18-1

* Mon Apr 29 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.17-1
- Updated to 3.1.17-1

* Tue Apr 02 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.16-2
- Updated to work with tarball client

* Mon Apr 01 2013 Brian Lin <blin@cs.wisc.edu> - 3.1.16-1
- Updated to 3.1.16-1

* Mon Mar 04 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.1.15-1
- Updated to 3.1.15-1

* Mon Feb 11 2013 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.1.14-1
- Updated to 3.1.14-1

* Mon Jan 28 2013 Tim Cartwright <cat@cs.wisc.edu> 3.1.13-1
- Updated to 3.1.13-1

* Mon Dec 10 2012 Doug Strain <dstrain@fnal.gov> 3.1.12-1
- Updated to 3.1.12-1

* Mon Nov 5 2012 Doug Strain <dstrain@fnal.gov> 3.1.11-1
- Updated to 3.1.11-1

* Mon Oct 8 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.1.10-1
- Updated to 3.1.10-1

* Tue Sep 24 2012 Tim Cartwright <cat@cs.wisc.edu> 3.1.9-1
- Updated to 3.1.9-1

* Tue Aug 14 2012 Matyas Selmeci <matyas@cs.wisc.edu> 3.1.8-1
- Updated to 3.1.8-1

* Mon Jul 30 2012 Alain Roy <roy@cs.wisc.edu> 3.1.7-1
- Updated to 3.1.7-1

* Mon Jul 09 2012 Scot Kronenfeld <kronenfe@cs.wisc.edu> 3.1.6-1
- Updated to 3.1.6-1

* Mon Jun 11 2012 Suchandra Thapa <sthapa@ci.uchicago.edu> -3.1.4-1
- Updated to 3.1.4-1

* Mon May 21 2012 Alain Roy <roy@cs.wisc.edu> - 3.1.3-1
- Updated to 3.1.3-1

* Tue May 15 2012 Alain Roy <roy@cs.wisc.edu> - 3.1.2-1
- Updated to 3.1.2-1

* Thu May 03 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.1.1-1
- Updated to 3.1.1-1

* Tue Apr 24 2012 Alain Roy <roy@cs.wisc.edu> - 3.1.0-1
- Updated to 3.1.0-1

* Tue Apr 10 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.10-1
- Updated to 3.0.10-1

* Tue Mar 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.9-1
- Updated to 3.0.9-1

* Tue Feb 28 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.8-1
- Updated to 3.0.8-1

* Mon Feb 13 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.7-1
- Updated to 3.0.7-1

* Mon Jan 30 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 3.0.6-1
- Updated to 3.0.6-1

* Mon Dec 12 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.5-1
- Updated to 3.0.5-1

* Mon Dec 05 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.4-1
- Updated to 3.0.4-1

* Mon Nov 14 2011 Alain Roy <roy@cs.wisc.edu> - 3.0.3-1
- Updated version of 3.0.3
