
Name: cryptix
Summary: An implementation of strong cryptography for Java
License: http://www.cryptix.org/LICENSE.TXT
Version: 3.2.0
Release: 2%{?dist}
URL: http://www.cryptix.org/
Group: System Environment/Libraries
# Done on March 12, 2012:
# cvs -d:pserver:anonymous@cvs.globus.org:/home/dsl/cog/CVS export -r HEAD cryptix32
# tar zcf cryptix32.tar.gz cryptix32
Source0: cryptix32.tar.gz
Source1: build.xml
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
%setup -q -n cryptix32

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

cp %{SOURCE1} .

%build
ant jar

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/cryptix.jar $RPM_BUILD_ROOT%{_javadir}/cryptix.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_javadir}/*

%changelog
* Fri Mar 02 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 3.2.0-2
- Switch to a build based upon the Globus fork.

* Thu Mar 01 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 3.2.0-1
- Initial packaging of cryptix.


