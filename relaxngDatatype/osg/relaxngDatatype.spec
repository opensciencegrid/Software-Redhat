Name:		relaxngDatatype
Version:	0.1
Release:	1%{?dist}
Summary:	relaxngDatatype package blocker for el5

Group:		Development/Tools
License:	ASL 2.0
#URL:		
#Source0:	
#BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Phony relaxngDatatype package to block problematic real one for el5

For osg-el5-internal only!

%install

%clean
rm -rf %{buildroot}

%if 0%{?rhel} < 6
%files
%endif

%changelog
* Mon Apr 27 2015 Carl Edquist <edquist@cs.wisc.edu> - 0.1-1
- workaround for jpp5 build issue, relaxngDatatype Obsoletes msv w/o Provides

