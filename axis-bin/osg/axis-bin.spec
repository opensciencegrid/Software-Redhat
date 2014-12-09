Summary: A Web Services / SOAP / WSDL engine provided by Apache
%define realname axis
Name: %{realname}-bin
Version: 1.4
%define _version %(echo %version | tr . _)
Release: 1%{?dist}
License: ASL 2.0
Group: Development/Libraries/Java
Url: http://axis.apache.org
Source0: %{name}-%{_version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: %{realname} = %{version}
BuildRequires: java-devel
Requires: java
AutoReq: yes
AutoProv: yes
BuildArch: noarch

# disable jar repacking
%global __os_install_post /bin/true


%define  webappsdir  %{_datadir}/%{realname}-%{version}/webapps

%description
%{summary}


%package docs
Summary: Documentation for %{name}
Group: Development/Libraries/Java

%description docs
Documentation for %{name}.


%prep
%setup -n %{realname}-%{_version}

%build
exit 0

%install
[[ %{buildroot} != / ]] && rm -rf %{buildroot}
mkdir -p %{buildroot}

# skip samples
rm -rf  samples/
# skip xmls
rm -rf  xmls/

# libs
mkdir -p  %{buildroot}%{_javadir}/%{realname}
mv  lib/*.jar  %{buildroot}%{_javadir}/%{realname}/

# docs
mkdir -p  %{buildroot}%{_datadir}/doc/%{realname}-%{version}/
mv  LICENSE NOTICE README release-notes.html docs/  \
       %{buildroot}%{_datadir}/doc/%{realname}-%{version}/

# webapps and related
pushd webapps/%{realname}
    jar cf ../%{realname}.war  *
popd
mkdir -p  %{buildroot}%{webappsdir}
mv  webapps/%{realname}.war  %{buildroot}%{webappsdir}/
# lib symlinks
mkdir -p  %{buildroot}%{webappsdir}/WEB-INF/lib
for jar in %{buildroot}%{_javadir}/%{realname}/*.jar; do
    jar_no_buildroot=${jar##%{buildroot}}
    ln -sf $jar_no_buildroot \
              %{buildroot}%{webappsdir}/WEB-INF/lib/$(basename $jar)
done


%clean
[[ %{buildroot} != / ]] && rm -rf %{buildroot}




%files
%dir %{_javadir}/%{realname}
%{_javadir}/%{realname}/*.jar
%docdir %{_datadir}/doc/%{realname}-%{version}
%doc %{_datadir}/doc/%{realname}-%{version}/LICENSE
%doc %{_datadir}/doc/%{realname}-%{version}/NOTICE
%doc %{_datadir}/doc/%{realname}-%{version}/README
%doc %{_datadir}/doc/%{realname}-%{version}/release-notes.html
%dir %{webappsdir}
%{webappsdir}/%{realname}.war
%{webappsdir}/WEB-INF/lib/*

%files docs
%{_datadir}/doc/%{realname}-%{version}/docs







%changelog
* Mon Dec 08 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.4-1
- Created


# vim:ft=spec
