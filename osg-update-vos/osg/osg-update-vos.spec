Name:           osg-update-vos
Version:        1.4.1
Release:        2%{?dist}
Summary:        VO data updater for OSG

License:        Apache 2.0

Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       yum-utils
Requires:       osg-release

%description
%{summary}

%package -n osg-update-data
Requires: %{name}
Requires: osg-ca-scripts
Summary: Data updater for OSG

%description -n osg-update-data
Data updater for OSG


%prep
%setup -q

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%doc %{_defaultdocdir}/%{name}-%{version}/README*

%files -n osg-update-data
%{_sbindir}/osg-update-data

%changelog
* Fri May 26 2023 Matt Westphall <westphall@wisc.edu> - 1.4.1-1
- Updated Python dependency to 3 on all EL version (SOFTWARE-5545)

* Mon Dec 12 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.4.0-3
- Bump to rebuild (SOFTWARE-5384)

* Tue Jun 23 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.0-2
- Use Python 3 on EL8 (SOFTWARE-4140)

* Tue May 16 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.0-1
- osg-update-vos: clean cache before downloading data (SOFTWARE-2731)

* Fri Jan 06 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.3.0-1
- Add osg-release requirement
- Allow taking osg repo definition from osg-release installed in a tarball client (SOFTWARE-2527)

* Tue Jan 03 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2.1-1
- osg-update-data: update VOs before CAs and CRLs (SOFTWARE-2528)

* Thu Dec 29 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2-1
- Add osg-update-data subpackage (SOFTWARE-2528)

* Wed Dec 28 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-2
- Move script to /usr/sbin (SOFTWARE-2527)

* Wed Dec 28 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1-1
- Use --location argument to specify destination; use /etc or $OSG_LOCATION/etc if not specified (SOFTWARE-2527)

* Tue Dec 20 2016 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0-1
- Created (SOFTWARE-2527)
