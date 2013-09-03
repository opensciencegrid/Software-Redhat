Name:		missing-java-1.7.0-dirs
Version:	1.0
Release:	2%{?dist}
Summary:	Provides /usr/{share,lib}/java-1.7.0/ dirs

Group:		Applications/System
License:	BSD
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch


%description
The directories /usr/share/java-1.7.0/ and /usr/lib/java-1.7.0/ are not
created automatically in el5 when java7 is installed, but they are required
by some java packages, even though not explicitly.  This just creates them.

%prep

%build

%install
rm -rf %{buildroot}

# this problem is really el5 specific
%if 0%{?rhel} == 5
mkdir -p %{buildroot}/usr/share/java-1.7.0/
mkdir -p %{buildroot}/usr/lib/java-1.7.0/
%endif

%clean

%files
%defattr(-,root,root,-)
%if 0%{?rhel} == 5
%dir /usr/share/java-1.7.0/
%dir /usr/lib/java-1.7.0/
%endif

%changelog
* Tue May 07 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0-2
- BuildArch = noarch

* Mon Mar 25 2013 Carl Edquist <edquist@cs.wisc.edu> - 1.0-1
- Initial release

