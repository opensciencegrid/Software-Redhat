Name:      osg-version
Summary:   OSG Version
Version:   3.4.45
Release:   1%{?dist}
License:   Apache 2.0
URL:       http://www.opensciencegrid.org
BuildArch: noarch

# This is a OSG Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:   osg-version


%description
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo %{version} > $RPM_BUILD_ROOT%{_sysconfdir}/osg-version
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/osg-version

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -pm 755 %{SOURCE0}  $RPM_BUILD_ROOT%{_bindir}/

%files
%{_sysconfdir}/osg-version
%{_bindir}/osg-version

%changelog
* Tue Mar 10 2020 Tim Theisen <tim@cs.wisc.edu> 3.4.45-1
- Updated to 3.4.45-1

* Mon Feb 17 2020 Tim Theisen <tim@cs.wisc.edu> 3.4.44-1
- Updated to 3.4.44-1

* Thu Feb 06 2020 Tim Theisen <tim@cs.wisc.edu> 3.4.43-1
- Updated to 3.4.43-1

* Wed Jan 08 2020 Tim Theisen <tim@cs.wisc.edu> 3.4.42-1
- Updated to 3.4.42-1

* Mon Dec 16 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.41-1
- Updated to 3.4.41-1

* Mon Nov 25 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.40-1
- Updated to 3.4.40-1

* Thu Nov 14 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.39-1
- Updated to 3.4.39-1

* Wed Oct 23 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.38-1
- Updated to 3.4.38-1

* Wed Oct 16 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.37-1
- Updated to 3.4.37-1

* Wed Oct 09 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.36-1
- Updated to 3.4.36-1

* Thu Sep 19 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.35-1
- Updated to 3.4.35-1

* Tue Aug 27 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.34-1
- Updated to 3.4.34-1

* Thu Aug 01 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.33-1
- Updated to 3.4.33-1

* Thu Jul 25 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.32-1
- Updated to 3.4.32-1

* Wed Jun 12 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.31-1
- Updated to 3.4.31-1

* Thu May 16 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.30-1
- Updated to 3.4.30-1

* Thu May 02 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.29-1
- Updated to 3.4.29-1

* Wed Apr 24 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.28-1
- Updated to 3.4.28-1

* Thu Apr 11 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.27-1
- Updated to 3.4.27-1

* Wed Mar 13 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.26-1
- Updated to 3.4.26-1

* Wed Mar 06 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.25-1
- Updated to 3.4.25-1

* Wed Feb 20 2019 Carl Edquist <edquist@cs.wisc.edu> - 3.4.24-1
- Updated to 3.4.24-1

* Tue Jan 15 2019 Tim Theisen <tim@cs.wisc.edu> 3.4.23-1
- Updated to 3.4.23-1

* Wed Dec 19 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.22-1
- Updated to 3.4.22-1

* Wed Dec 12 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.21-1
- Updated to 3.4.21-1

* Wed Oct 31 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.20-1
- Updated to 3.4.20-1

* Wed Oct 24 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.19-1
- Updated to 3.4.19-1

* Wed Sep 26 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.18-1
- Updated to 3.4.18-1

* Thu Aug 16 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.17-1
- Updated to 3.4.17-1

* Tue Jul 31 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.16-1
- Updated to 3.4.16-1

* Thu Jul 05 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.15-1
- Updated to 3.4.15-1

* Fri Jun 29 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.14-1
- Updated to 3.4.14-1

* Thu Jun 07 2018 Carl Edquist <edquist@cs.wisc.edu> - 3.4.13-1
- Updated to 3.4.13-1

* Wed May 09 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.12-1
- Updated to 3.4.12-1

* Mon Apr 30 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.11-1
- Updated to 3.4.11-1

* Fri Apr 13 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.10-1
- Updated to 3.4.10-1

* Wed Mar 07 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.9-1
- Updated to 3.4.9-1

* Tue Feb 06 2018 Brian Lin <blin@cs.wisc.edu> 3.4.8-1
- Updated to 3.4.8-1

* Mon Jan 29 2018 Tim Theisen <tim@cs.wisc.edu> 3.4.7-1
- Updated to 3.4.7-1

* Mon Dec 18 2017 Tim Theisen <tim@cs.wisc.edu> 3.4.6-1
- Updated to 3.4.6-1

* Thu Nov 09 2017 Tim Theisen <tim@cs.wisc.edu> 3.4.5-1
- Updated to 3.4.5-1

* Thu Oct 05 2017 Tim Theisen <tim@cs.wisc.edu> 3.4.4-1
- Updated to 3.4.4-1

* Wed Sep 06 2017 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.4.3-1
- Updated to 3.4.3-1

* Wed Jul 05 2017 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.4.2-1
- Updated to 3.4.2-1

* Wed Jul 05 2017 Tim Theisen <tim@cs.wisc.edu> 3.4.1-1
- Updated to 3.4.1-1

* Thu May 25 2017 Brian Lin <blin@cs.wisc.edu> 3.4.0-1
- Updated to 3.4.0-1

* Wed Apr 26 2017 Tim Theisen <tim@cs.wisc.edu> 3.3.24-1
- Updated to 3.3.24-1

* Tue Apr 03 2017 Brian Lin <blin@cs.wisc.edu> 3.3.23-1
- Updated to 3.3.23-1

* Tue Mar 07 2017 Tim Theisen <tim@cs.wisc.edu> 3.3.22-1
- Updated to 3.3.22-1

* Wed Feb 08 2017 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.3.21-1
- Updated to 3.3.21-1

* Thu Jan 05 2017 Brian Lin <blin@cs.wisc.edu> 3.3.20-1
- Updated to 3.3.20-1

* Tue Dec 06 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.19-1
- Updated to 3.3.19-1

* Mon Oct 31 2016 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.3.18-1
- Updated to 3.3.18-1

* Mon Oct 03 2016 Brian Lin <tim@cs.wisc.edu> 3.3.17-1
- Updated to 3.3.17-1

* Thu Sep 01 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.16-1
- Updated to 3.3.16-1

* Fri Aug 05 2016 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.3.15-1
- Updated to 3.3.15-1

* Fri Jul 08 2016 Brian Lin <blin@cs.wisc.edu> 3.3.14-1
- Updated to 3.3.14-1

* Tue Jun 07 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.13-1
- Updated to 3.3.13-1

* Thu May 05 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.12-1
- Updated to 3.3.12-1

* Tue Apr 05 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.11-1
- Updated to 3.3.11-1

* Wed Feb 24 2016 Tim Theisen <tim@cs.wisc.edu> 3.3.10-1
- Updated to 3.3.10-1

* Wed Feb 03 2016 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.3.9-1
- Updated to 3.3.9-1

* Wed Jan 06 2016 Brian Lin <blin@cs.wisc.edu> 3.3.8-1
- Updated to 3.3.8-1

* Thu Dec 10 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.7-1
- Updated to 3.3.7-1

* Wed Dec 01 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.6-1
- Updated to 3.3.6-1

* Wed Nov 17 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.3.5-1
- Updated to 3.3.5-1

* Wed Nov 04 2015 Brian Lin <blin@cs.wisc.edu> 3.3.4-1
- Updated to 3.3.4-1

* Fri Oct 30 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.3-1
- Updated to 3.3.3-1

* Fri Oct 09 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> 3.3.2-1
- Updated to 3.3.2-1

* Wed Sep 02 2015 Tim Theisen <tim@cs.wisc.edu> 3.3.1-1
- Updated to 3.3.1-1

* Wed Jun 10 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 3.3.0-1
- Updated to 3.3.0-1

* Wed Apr 08 2015 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.22-1
- Updated to 3.2.22-1

* Thu Mar 05 2015 Brian Lin <blin@cs.wisc.edu> - 3.2.21-1
- Updated to 3.2.21-1

* Fri Feb 06 2015 Tim Theisen <tim@cs.wisc.edu> - 3.2.20-1
- Updated to 3.2.20-1

* Tue Jan 09 2015 Brian Lin <blin@cs.wisc.edu> - 3.2.19-1
- Updated to 3.2.19-1

* Fri Dec 04 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.18-1
- Updated to 3.2.18-1

* Tue Nov 04 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.17-1
- Updated to 3.2.17-1

* Fri Oct 10 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.16-1
- Updated to 3.2.16-1

* Tue Aug 28 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.15-1
- Updated to 3.2.15-1

* Tue Aug 05 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.14-1
- Updated to 3.2.14-1

* Thu Jul 17 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.13-1
- Updated to 3.2.13-1

* Thu Jul 03 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.12-1
- Updated to 3.2.12-1

* Wed Jun 04 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.11-1
- Updated to 3.2.11-1

* Thu May 22 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.10-1
- Updated to 3.2.10-1

* Tue May 06 2014 Tim Theisen <tim@cs.wisc.edu> - 3.2.9-1
- Updated to 3.2.9-1

* Mon Mar 31 2014 Brian Lin <blin@cs.wisc.edu> 3.2.8-1
- Updated to 3.2.8-1

* Thu Mar 20 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.2.7-1
- Updated to 3.2.7-1

* Tue Mar 4 2014 Suchandra Thapa <sthapa@ci.uchicago.edu> - 3.2.6-1
- Updated to 3.2.6-1

* Tue Feb 25 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.5-1
- Updated to 3.2.5-1

* Fri Feb 07 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.4-1
- Updated to 3.2.4-1

* Fri Dec 13 2013 Tim Theisen <tim@cs.wisc.edu> - 3.2.2-1
- Updated to 3.2.2-1

* Thu Dec 05 2013 Tim Theisen <tim@cs.wisc.edu> - 3.2.1-1
- Updated to 3.2.1-1

* Tue Oct 29 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2.0-1
- Updated to 3.2.0-1 -- forked from 3.1.25-1

