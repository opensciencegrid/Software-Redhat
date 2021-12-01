Name:		xrootd-lcmaps-dummy
Version:	99
Release:	1%{?dist}
Summary:	Transitional dummy package to ease upgrades from OSG 3.5

License:	ASL 2.0

%description
%{summary}


%package -n xrootd-lcmaps
Summary: Transitional dummy package to ease upgrades from OSG 3.5

%description -n xrootd-lcmaps
This is a transitional dummy package for xrootd-lcmaps; it may safely be removed.


%prep
exit 0


%build
exit 0


%install
exit 0


%files -n xrootd-lcmaps


%changelog
* Thu Oct 28 2021 Mátyás Selmeci <matyas@cs.wisc.edu>
- Created (SOFTWARE-4881)

