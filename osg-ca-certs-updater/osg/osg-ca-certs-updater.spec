Name:           osg-ca-certs-updater
Version:        2.0
Release:        1.3%{?dist}
Summary:        Automatic CA certs updates for OSG

Group:          System Environment/Tools
License:        Apache 2.0

Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3
%define __python /usr/bin/python3
BuildRequires:  /usr/bin/repoquery
Requires:       /usr/bin/repoquery

%description
%{summary}



%prep
%setup -q

%install
make install DESTDIR=%{buildroot} PYTHON=%{__python}
mkdir -p %{buildroot}/%{_localstatedir}/{lock/subsys,lib}
touch %{buildroot}/%{_localstatedir}/lock/subsys/%{name}-cron
touch %{buildroot}/%{_localstatedir}/lib/%{name}-lastrun

%post
/sbin/chkconfig --add %{name}-cron

%preun
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-cron stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-cron
fi

%files
%{_sbindir}/%{name}
%{_initrddir}/%{name}-cron
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%ghost %{_localstatedir}/lock/subsys/%{name}-cron
%ghost %{_localstatedir}/lib/%{name}-lastrun
%doc %{_mandir}/man8/%{name}.8*
%doc %{_defaultdocdir}/%{name}-%{version}/README*

%changelog
* Thu Feb 16 2023 Carl Edquist <edquist@cs.wisc.edu> - 2.0-1.2
- Bump to rebuild for RPM GPG key (SOFTWARE-5457)

* Tue Dec 13 2022 Carl Edquist <edquist@cs.wisc.edu> - 2.0-1.1
- Bump to rebuild (SOFTWARE-5384)

* Mon Feb 15 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 2.0-1
- Python 3/EL8 support

* Wed Apr 25 2018 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.8-1
- Replace grid.iu.edu URL with current link (SOFTWARE-3216)

* Mon Dec 18 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.7-1
- Link to CA certs docs (SOFTWARE-3083)

* Fri Dec 15 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.6-1
- Replace references to OSG Twiki with links to current docs (SOFTWARE-3083)
- Replace help email (SOFTWARE-3015)

* Thu Jan 28 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4-1
- Remove osg-release requirement; ignore missing compat packages; only try to
  update packages that are installed (SOFTWARE-2146)

* Thu Oct 22 2015 Brian Lin <blin@cs.wisc.edu> - 1.3-1
- Bug fix for verifying osg-release version

* Thu Oct 22 2015 Brian Lin <blin@cs.wisc.edu> - 1.2-1
- Verify OSG version with osg-release instead of osg-version

* Thu Oct 22 2015 Brian Lin <blin@cs.wisc.edu> - 1.1-1
- Fix updates on OSG 3.3 due to missing compat packages (SOFTWARE-2076)

* Wed Nov 12 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0-1
- Add --enablerepo option (SOFTWARE-1663)

* Mon Mar 11 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 0.5-1
- SOFTWARE-968 (make repoquery use plugins)

* Thu Nov 01 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 0.4-1
- Add absolute path to script to cron.d entry

* Wed Oct 24 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 0.3-1
- Add chkconfig line

* Tue Oct 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 0.2-1
- Handle bad logfile name gracefully

* Tue Oct 23 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 0.1-1
- First release
