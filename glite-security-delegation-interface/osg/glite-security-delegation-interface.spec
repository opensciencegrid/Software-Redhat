Name:		glite-security-delegation-interface
Version:	2.0.3
Release:	3%{?dist}
Summary:	Interface files for glite proxy delegation API

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.security.delegation-interface
# Retrieved on Jul 5 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.security.delegation-interface.tar.gz?view=tar&pathrev=emi-delegation-interface_R_2_0_3
Source0:        org.glite.security.delegation-interface.tar.gz
Patch0:         gsoap2_7_13_fix.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  docbook-style-xsl

%description
%{summary}

%prep
%setup -n org.glite.security.delegation-interface
%patch0 -p0

%build
make documentation

%install
rm -rf $RPM_BUILD_ROOT

make install prefix=$RPM_BUILD_ROOT%{_prefix}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/interface
mv $RPM_BUILD_ROOT%{_prefix}/var/lib/delegation-interface/interface/* $RPM_BUILD_ROOT%{_datadir}/%{name}/interface
mv $RPM_BUILD_ROOT%{_prefix}/var/lib/delegation-interface/schema $RPM_BUILD_ROOT%{_datadir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_prefix}/var/lib/delegation-interface/doc/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE
%doc %{_docdir}/%{name}-%{version}/RELEASE-NOTES
%{_datadir}/%{name}

%changelog
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.3-3
- rebuilt

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.3-2
- Rebuilt against updated Globus libraries

* Tue Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.3-1
- Initial OSG packaging.

