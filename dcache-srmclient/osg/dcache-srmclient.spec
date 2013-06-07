
%define majorver 2.2.11
%define minorver 1
%define targetdir modules/srmclient/target/srmclient-%{majorver}-SNAPSHOT
%define srm_path %{_datadir}/srm

Name:    dcache-srmclient
Version: %{majorver}.%{minorver}
Release: 2%{?dist}
URL:     http://dcache.org
Summary: SRM clients from dCache.org
License: http://www.dcache.org/manuals/dCacheSoftwareLicence.html
Group:   Development/Tools
Obsoletes: SRM-Client-Fermi

BuildRequires: java-devel
BuildRequires: ant
BuildRequires: /usr/share/java/xml-commons-apis.jar
# maven >= 2.0.10 is needed for maven-ant
BuildRequires: maven22
Requires: java
Requires: /usr/bin/globus-url-copy
Requires: /usr/share/java/xml-commons-apis.jar

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Source0: srmclient-%{majorver}-%{minorver}.tgz
#                             ^ note the dash in the tarball name
Source1: dcache-srmclient-config.xml

# have srm scripts source /etc/sysconfig/dcache-srmclient if it exists
Patch0: source-sysconfig.patch
# fix build.xml so it works with the maven OSG uses for building
Patch1: maven22.patch

%description
%{summary}

%prep
%setup -q -n srmclient-%{majorver}-%{minorver}

%patch0 -p0
%patch1 -p0

%build
unset JAVA_HOME
# This uses ant but actually starts up a maven build
ant srmclient


%install
# DEBUG:
find . -type f | cut -b 3- | sort

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 %{targetdir}/usr/bin/* $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 0755 %{targetdir}/usr/sbin/srm $RPM_BUILD_ROOT%{_sbindir}

mkdir -p $RPM_BUILD_ROOT%{srm_path}/sbin
install -m 0755 %{targetdir}/usr/sbin/url-copy.sh $RPM_BUILD_ROOT%{srm_path}/sbin
mv %{targetdir}/usr/share/srm/{conf,lib} $RPM_BUILD_ROOT%{srm_path}/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name} << EOF
export SRM_PATH=%{srm_path}
export SRM_CONFIG=/etc/%{name}-config.xml
EOF
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-config.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{srm_path}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}-config.xml

%changelog
* Thu Jun 06 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.2.11.1-2
- Move /usr/sbin/url-copy.sh to /usr/share/srm/sbin since that's where scripts expect it.

* Thu May 30 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.2.11.1-1
- New major version; update patch: remove the sections that are already
  upstream, and rename to match what's left
- Fix RPM to work with new paths -- almost everything in
  /usr/share/java/dcache-srmclient was moved to /usr/share/srm except
  /usr/share/java/dcache-srmclient/sbin/* was moved to /usr/sbin
- Add xml-commons-apis dependency
- Add maven22 build dependency

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

