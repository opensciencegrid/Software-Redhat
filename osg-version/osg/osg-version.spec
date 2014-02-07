Name:      osg-version
Summary:   OSG Version
Version:   3.2.4
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
* Fri Feb 07 2014 Brian Lin <blin@cs.wisc.edu> - 3.2.4-1
- Updated to 3.2.4-1

* Fri Dec 13 2013 Tim Theisen <tim@cs.wisc.edu> - 3.2.2-1
- Updated to 3.2.2-1

* Thu Dec 05 2013 Tim Theisen <tim@cs.wisc.edu> - 3.2.1-1
- Updated to 3.2.1-1

* Tue Oct 29 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.2.0-1
- Updated to 3.2.0-1 -- forked from 3.1.25-1

