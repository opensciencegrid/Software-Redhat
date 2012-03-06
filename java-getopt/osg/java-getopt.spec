
Name: java-getopt
Summary: A re-implementation of GNU's getopt in Java
License: LGPL
Version: 1.0.14
Release: 1%{?dist}
URL: http://www.urbanophile.com/arenn/hacking/download.html
Group: System Environment/Libraries
# Tar file from repo https://github.com/arenn/java-getopt.git
Source0: java-getopt-1.0.14.tar.gz
BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: ant
BuildRequires: jpackage-utils

Requires: java
Requires: jpackage-utils

%description
%{summary}

%prep
%setup -q -c

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
mv gnu/getopt/buildx.xml ./build.xml
ant jar

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/gnu.getopt.jar $RPM_BUILD_ROOT%{_javadir}/gnu.getopt.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*

%changelog
* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.0.14-1
- Initial packaging of getopt for cryptix-asn1.


