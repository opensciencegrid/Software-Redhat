
%define targetdir modules/srmclient/target/srmclient-%{version}
%define srm_path %{_datadir}/srm

Name:    dcache-srmclient
Version: 2.2.27
Release: 1%{?dist}
URL:     http://dcache.org
Summary: SRM clients from dCache.org
License: http://www.dcache.org/manuals/dCacheSoftwareLicence.html
Group:   Development/Tools
Obsoletes: SRM-Client-Fermi

BuildRequires: ant
BuildRequires: jpackage-utils
BuildRequires: /usr/share/java/xml-commons-apis.jar
# maven >= 2.0.10 is needed for maven-ant
%if %rhel < 7
BuildRequires: maven22
%else
BuildRequires: maven-local
BuildRequires: java7-devel
%endif

%if 0%{?el7}
Requires: java-headless >= 1:1.7.0
Requires: jpackage-utils
%else
Requires: java7
%endif

Requires: /usr/bin/globus-url-copy
Requires: /usr/share/java/xml-commons-apis.jar

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Source0: dcache-%{version}.tar.gz
Source1: dcache-srmclient-config.xml

# have srm scripts source /etc/sysconfig/dcache-srmclient if it exists
Patch0: source-sysconfig.patch
# fix build.xml so it works with the maven OSG uses for building
Patch1: maven22.patch

%description
%{summary}

%prep
%setup -q -n dcache-%{version}

%patch0 -p0
%if %rhel < 7
%patch1 -p0
%endif

%build
export JAVA_HOME=%{java_home}
# This uses ant but actually starts up a maven build
%if 0%{?el7}
sed -i -e "/maven\.home/s#/usr/share/maven2/#/usr/share/maven/#"  build.xml
%endif

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
* Thu Aug 14 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 2.2.27-1
- New version; some build tweaks (SOFTWARE-1566)

* Thu Jun 06 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.2.11.1-2
- Move /usr/sbin/url-copy.sh to /usr/share/srm/sbin since that's where scripts expect it.
- Fix repeat count in supplied config

* Thu May 30 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 2.2.11.1-1
- New major version; update patch: remove the sections that are already
  upstream, and rename to match what's left
- Fix RPM to work with new paths -- almost everything in
  /usr/share/java/dcache-srmclient was moved to /usr/share/srm except
  /usr/share/java/dcache-srmclient/sbin/* was moved to /usr/sbin
- Add xml-commons-apis dependency
- Add maven22 build dependency

* Thu Feb 07 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1.9.5.23-6.1
- Rebuild with openjdk 7 and ant17

* Wed Jan 18 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.9.5.23-6
- Fixing patch command for sl6

* Mon Nov 21 2011 Doug Strain <dstrain@fnal.gov> 1.9.5.23-5
- Added %{?dist} tag to release

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.9.5.23-4
- Bump to rebuild against updated Globus libs

* Tue Aug 30 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.9.5.23-3
- Rebuilt against Globus 5.2

* Thu Jul  7 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.9.5.23-2
- Set buildarch to noarch.

* Thu Jul  7 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.9.5.23-1
- Don't use upstream version number in release value.
- Rename to use the upstream vendor's RPM name.

* Fri Jul 1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.9.5-23
- Initial packaging
- Allow client scripts to be packaged outside $SRM_PATH

