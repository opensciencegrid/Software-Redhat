Summary: the missing CA certs for java-1.7.0 needed to avoid empty trustAnchor issues
Name: missing-java-1.7.0-cacerts
Version: 1
Release: 1%{?dist}
License: ASL 2.0
Group: Applications/Grid
Source0: cacerts
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

%description
%{summary}

%install
[ %{buildroot} != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}/etc/pki/java
cp %{SOURCE0} %{buildroot}/etc/pki/java

%clean
[ %{buildroot} != / ] && rm -rf %{buildroot}

%files
/etc/pki/java

%changelog
* Wed May 15 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1-1
- Created

# vim:ft=spec

