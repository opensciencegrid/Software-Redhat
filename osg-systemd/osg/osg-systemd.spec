%{!?_unitdir: %global _unitdir %{_prefix}/lib/systemd/system}

Name:           osg-systemd
Version:        1
Release:        1%{?dist}
Summary:        SystemD file for OSG services
Source0:        osg.target
BuildArch:      noarch
Requires:       systemd
License:        Apache Software License 2.0


%description
A SystemD target file for starting/stopping all OSG services.

%prep
exit 0

%build
%if 0%{?rhel} < 7
echo "This package is for EL 7 or greater" >&2
exit 1
%endif


%install
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE0} %{buildroot}%{_unitdir}

%files
%{_unitdir}/osg.target

%post
if [ $1 -eq 1 ]; then
    systemctl daemon-reload > /dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ]; then
    systemctl daemon-reload > /dev/null 2>&1 || :
fi

%changelog
* Tue Sep 19 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1-1
- Created

