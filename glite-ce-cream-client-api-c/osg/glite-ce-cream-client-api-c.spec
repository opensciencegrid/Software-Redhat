Summary: Transitional dummy package for glite-ce-cream-client-api-c
Name: glite-ce-cream-client-api-c
Version: 1.15.4
Release: 2.5%{?dist}
License: Apache Software License

%description
This is an empty package created as a workaround for 3.4->3.5 upgrade issues.
It may safely be removed.

%prep
exit 0

%install
exit 0

%files



%package -n glite-ce-cream-client-devel
Summary: Transitional dummy package for glite-ce-cream-client-devel

%description -n glite-ce-cream-client-devel
This is an empty package created as a workaround for 3.4->3.5 upgrade issues.
It may safely be removed.

%files -n glite-ce-cream-client-devel


%changelog
* Mon Aug 26 2019 Mátyás Selmeci <matyas@cs.wisc.edu>
- Create transitional dummy packages for OSG 3.5
