Name:           osg-update-vos
Version:        1.3.0
Release:        1%{?dist}
Summary:        VO data updater for OSG

Group:          System Environment/Tools
License:        Apache 2.0

Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%doc %{_defaultdocdir}/%{name}-%{version}/README*

%files -n osg-update-data
%{_sbindir}/osg-update-data

%changelog
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
