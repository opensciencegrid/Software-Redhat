
Name: cryptix-asn1
Summary: An ASN.1 parser for Cryptix
License: BSD
Version: 20011119
Release: 1%{?dist}
URL: http://www.rtfm.com/puretls/
Group: System Environment/Libraries

# NOTE: PureTLS claims the actual cryptix project provides a bum version of
# this library, and that they can only work with the one they distribute.

# http://www.rtfm.com/cgi-bin/distrib.cgi?Cryptix-asn1-20011119.tar.gz
Source0: Cryptix-asn1-20011119.tar.gz
Source1: build.xml
BuildArch: noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: ant
BuildRequires: jpackage-utils
BuildRequires: cryptix >= 3.2

Requires: java
Requires: jpackage-utils
Requires: cryptix >= 3.2

%description
%{summary}

%prep
%setup -q -n Cryptix-asn1-20011119

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

cp %{SOURCE1} .

mkdir src
mv cryptix src

mkdir lib
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


