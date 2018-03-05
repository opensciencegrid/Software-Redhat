Name:      repo-update-cadist
Summary:   repo-update-cadist
Version:   1.0.0
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       https://github.com/opensciencegrid/repo-update-cadist
BuildArch: noarch


Source0:   %{name}

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{summary}

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -pm 755 %{SOURCE0}  $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}

%changelog
* Mon Mar 05 2018 Tim Theisen <tim@cs.wisc.edu> 1.0.0-1
- First RPM 1.0.0 (SOFTWARE-3102)
