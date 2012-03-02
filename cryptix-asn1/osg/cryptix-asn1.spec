
Name: cryptix-asn1
Summary: An ASN.1 parser for Cryptix
License: BSD
Version: 20011119
Release: 1%{?dist}
URL: http://www.rtfm.com/puretls/
Group: System Environment/Libraries

# NOTE: PureTLS claims the actual cryptix project provides a bum version of
# this library, and that they can only work with the one they distribute.
# NOTE: Globus took the PureTLS fork and created another fork.
# Performed on March 2, 2012
# cvs -d:pserver:anonymous@cvs.globus.org:/home/dsl/cog/CVS export -r HEAD cryptix-asn1
# tar zcf cryptix-asn1.tar.gz cryptix-asn1/
Source0: cryptix-asn1.tar.gz
Source1: build.xml
BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: ant
BuildRequires: jpackage-utils
BuildRequires: cryptix >= 3.2.0-2

Requires: java
Requires: jpackage-utils
Requires: cryptix >= 3.2.0-2

%description
%{summary}

%prep
%setup -q -n %{name}

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

cp %{SOURCE1} .

mkdir src
mv cryptix src

mkdir -p lib
build-jar-repository -s -p lib cryptix

%build
ant jar

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/cryptix-asn1.jar $RPM_BUILD_ROOT%{_javadir}/cryptix-asn1.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*

%changelog
* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 20011119-1
- Initial packaging of Cryptix ASN1 (from PureTLS).


