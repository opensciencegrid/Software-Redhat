Summary: Maven parent module for argus
Name: argus-parent
Version: 1.5.0
%global upstream_release 3
Release: %{?upstream_release}.1%{?dist}
License: ASL 2.0
Group: System Environment/Libraries
BuildArch: noarch
%if 0%{?el6}
BuildRequires: maven
%else
BuildRequires: maven2
%endif
BuildRequires: java-devel
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv: yes
Source: argus-parent-1.5.0.tar.gz

%description
maven parent module for argus

%prep
 

%setup  

%build
mkdir -p /tmp/m2-repository
  
  
  

%install
rm -rf $RPM_BUILD_ROOT
 mkdir -p $RPM_BUILD_ROOT
 export JAVA_HOME=/usr/java/latest && mvn -B -Dmaven.repo.local=/tmp/m2-repository install
 find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf {} \;
 find $RPM_BUILD_ROOT -name '*.pc' -exec sed -i -e "s|$RPM_BUILD_ROOT||g" {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
 

%changelog
* Fri Jun 08 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.5.0-3.1
- Add dist tag
 
