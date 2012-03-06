
Name: puretls
Summary: An implementation of SSL/TLS for Java
License: BSD
Version: 0.9b4
Release: 1%{?dist}
URL: http://www.rtfm.com/puretls/
Group: System Environment/Libraries
# Globus forked off puretls awhile back.  To create this tarball:
# cvs -d:pserver:anonymous@cvs.globus.org:/home/dsl/cog/CVS export -r HEAD puretls-0.9b4
# tar zcf puretls-0.9b4.tar.gz puretls-0.9b4
Source0: %{name}-%{version}.tar.gz
Source1: build.xml
Source2: build.properties
BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: ant
BuildRequires: jpackage-utils
BuildRequires: cryptix >= 3.2
BuildRequires: cryptix-asn1
BuildRequires: java-getopt

Requires: java
Requires: jpackage-utils
Requires: cryptix >= 3.2
Requires: cryptix-asn1

%description
%{summary}

%prep
%setup -q

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

cp %{SOURCE1} .
cp %{SOURCE2} .

mkdir -p lib
build-jar-repository -s -p lib cryptix cryptix-asn1 gnu.getopt

%build
ant

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/puretls.jar $RPM_BUILD_ROOT%{_javadir}/puretls.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*

%changelog
* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.9b5-1
- Initial packaging of PureTLS.


