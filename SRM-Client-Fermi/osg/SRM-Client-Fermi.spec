
%if 0
%define install_root %{_javadir}/%{name}
%else
%define install_root %{_datadir}/java/%{name}
%endif

Name:    SRM-Client-Fermi
Version: 1.9.5
Release: 23
URL:     http://dcache.org
Summary: SRM clients from dCache.org
License: http://www.dcache.org/manuals/dCacheSoftwareLicence.html
Group:   Development/Tools

BuildRequires: java-1.6.0-openjdk-devel
BuildRequires: ant
Requires: java-1.6.0-openjdk
Requires: /usr/bin/globus-url-copy

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Source0: srmclient-%{version}-%{release}.tar.gz
Source1: SRM-Client-Fermi-config.xml

Patch0: remove-srm-path-warnings.patch

%description
%{summary}

%prep
%setup -q -n srmclient-%{version}-%{release}

%patch -p0

%build
unset JAVA_HOME
ant srmclient

%install

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 dist/package/srmclient/opt/d-cache/srm/bin/* $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{install_root}
mv dist/package/srmclient/opt/d-cache/srm/{sbin,lib,conf} $RPM_BUILD_ROOT%{install_root}/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/SRM-Client-Fermi << EOF
export SRM_PATH=/usr/share/java/SRM-Client-Fermi
export SRM_CONFIG=/etc/SRM-Client-Fermi-config.xml
EOF
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/SRM-Client-Fermi-config.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{install_root}/*
%config(noreplace) %{_sysconfdir}/sysconfig/SRM-Client-Fermi
%config(noreplace) %{_sysconfdir}/SRM-Client-Fermi-config.xml

%changelog
* Fri Jul 1 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.9.5-23
- Initial packaging
- Allow client scripts to be packaged outside $SRM_PATH

