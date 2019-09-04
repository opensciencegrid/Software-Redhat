Name:      rsv
Summary:   Transitional dummy package for rsv
Version:   3.19.8
Release:   2%{?dist}
License:   Apache 2.0
URL:       https://github.com/opensciencegrid/rsv
BuildArch: noarch
%description
This is an empty package created as a workaround for 3.4->3.5 upgrade issues.
It may safely be removed.

%package consumers
Summary:  Transitional dummy package for rsv-consumers
%description consumers
This is an empty package created as a workaround for 3.4->3.5 upgrade issues.
It may safely be removed.

%package core
Summary: Transitional dummy package for rsv-core
%description core
This is an empty package created as a workaround for 3.4->3.5 upgrade issues.
It may safely be removed.

%package metrics
Summary: Transitional dummy package for rsv-metrics
%description metrics
This is an empty package created as a workaround for 3.4->3.5 upgrade issues.
It may safely be removed.

%prep
exit 0


%install
exit 0
%files
%files consumers
%files core
%files metrics

%changelog
* Mon Aug 26 2019 Mátyás Selmeci <matyas@cs.wisc.edu>
- Create transitional dummy packages for OSG 3.5

