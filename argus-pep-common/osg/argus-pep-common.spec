Summary: Argus PEP client and server common library (with hessian)
Name: argus-pep-common
Version: 2.2.0
%global upstream_release 1
Release: %{upstream_release}.1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
BuildArch: noarch
%if 0%{?el6}
BuildRequires: maven
%else
BuildRequires: maven2
%endif
BuildRequires: argus-parent
BuildRequires: java-devel
Requires: java
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv: yes
Source0: %{name}-%{version}.tar.gz
Source1: maven-surefire-plugin-2.4.3.jar
Source2: maven-surefire-plugin-2.4.3-fixed.pom

%description
Argus PEP client and server Java common library (EMI)

%prep
 

%setup  

%build
mkdir -p /tmp/m2-repository && cp -rvf m2-repository/* /tmp/m2-repository
export JAVA_HOME=%{java_home}
%if 0%{?rhel} == 6
mvn -B -Dmaven.repo.local=/tmp/m2-repository -Dfile=%{SOURCE1} -DpomFile=%{SOURCE2} install:install-file
%endif
mvn -B -Dmaven.repo.local=/tmp/m2-repository -PEMI install
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT/usr/share/java $RPM_BUILD_ROOT/usr/share/doc/argus-pep-common-2.2.0 && test -f target/pep-common.jar && cp target/pep-common.jar $RPM_BUILD_ROOT/usr/share/java/argus-pep-common-2.2.0.jar && cp doc/* $RPM_BUILD_ROOT/usr/share/doc/argus-pep-common-2.2.0 && cd $RPM_BUILD_ROOT/usr/share/java && ln -s argus-pep-common-2.2.0.jar argus-pep-common.jar
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/java/argus-pep-common.jar
/usr/share/java/argus-pep-common-2.2.0.jar
%dir /usr/share/doc/argus-pep-common-2.2.0/
/usr/share/doc/argus-pep-common-2.2.0/RELEASE-NOTES
/usr/share/doc/argus-pep-common-2.2.0/COPYRIGHT
/usr/share/doc/argus-pep-common-2.2.0/Hessian.LICENSE
/usr/share/doc/argus-pep-common-2.2.0/LICENSE

%changelog
* Fri Jun 08 2012 Matyas Selmeci <matyas@cs.wisc.edu> 2.2.0-1.1
- Add dist tag
- Added tweaks for building on el6

* Tue Apr 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 2.2.0-1
- Initial PEP Server and client library for EMI 2.



