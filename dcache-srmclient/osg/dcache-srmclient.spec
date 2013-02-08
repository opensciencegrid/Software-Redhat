
%if 0
%define install_root %{_javadir}/%{name}
%else
%define install_root %{_datadir}/java/%{name}
%endif

Name:    dcache-srmclient 
Version: 1.9.5.23
Release: 6.1%{?dist}
URL:     http://dcache.org
Summary: SRM clients from dCache.org
License: http://www.dcache.org/manuals/dCacheSoftwareLicence.html
Group:   Development/Tools
Obsoletes: SRM-Client-Fermi

BuildRequires: java-devel >= 1.7
BuildRequires: ant
Requires: java >= 1.7
Requires: /usr/bin/globus-url-copy

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Source0: srmclient-1.9.5-23.tar.gz
Source1: dcache-srmclient-config.xml

Patch0: remove-srm-path-warnings.patch

%description
%{summary}

%prep
%setup -q -n srmclient-1.9.5-23

%patch0 -p0

%build
unset JAVA_HOME
ant srmclient

%install

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 dist/package/srmclient/opt/d-cache/srm/bin/* $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{install_root}
mv dist/package/srmclient/opt/d-cache/srm/{sbin,lib,conf} $RPM_BUILD_ROOT%{install_root}/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/dcache-srmclient << EOF
export SRM_PATH=/usr/share/java/dcache-srmclient
export SRM_CONFIG=/etc/dcache-srmclient-config.xml
EOF
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/dcache-srmclient-config.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{install_root}/*
%config(noreplace) %{_sysconfdir}/sysconfig/dcache-srmclient
%config(noreplace) %{_sysconfdir}/dcache-srmclient-config.xml

%changelog
* Thu Feb 07 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1.9.5.23-6.1
- Rebuild with openjdk 7

* Wed Jan 18 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.9.5.23-6
- Fixing patch command for sl6

* Mon Nov 21 2011 Doug Strain <dstrain@fnal.gov> 1.9.5.23-5
- Added %{?dist} tag to release

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.9.5.23-4
- Bump to rebuild against updated Globus libs

* Tue Aug 30 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.9.5.23-3
- Rebuilt against Globus 5.2

* Fri Jul  7 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.9.5.23-2
- Set buildarch to noarch.

* Fri Jul  7 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.9.5.23-1
- Don't use upstream version number in release value.
- Rename to use the upstream vendor's RPM name.

* Fri Jul 1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.9.5-23
- Initial packaging
- Allow client scripts to be packaged outside $SRM_PATH

