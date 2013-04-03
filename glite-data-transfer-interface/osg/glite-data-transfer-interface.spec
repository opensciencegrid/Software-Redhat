Name:		glite-data-transfer-interface
Version:	3.7.0
Release:	4%{?dist}
Summary:	WSDL and interface docs for FTS.

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.transfer-interface
# Retrieved on Jul 5 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.transfer-interface.tar.gz?view=tar&pathrev=glite-data-transfer-interface_R_3_7_0_1
Source0:        org.glite.data.transfer-interface.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  java7-devel
BuildRequires:  jpackage-utils

%description
%{summary}

%prep
%setup -n org.glite.data.transfer-interface

%build
make javadoc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}
make install prefix=$RPM_BUILD_ROOT%{_prefix}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{_prefix}/interface $RPM_BUILD_ROOT%{_datadir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_docdir}/html $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_docdir}/LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{_docdir}/RELEASE-NOTES $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
%{_datadir}/%{name}/interface
%doc %{_docdir}/%{name}-%{version}/LICENSE
%doc %{_docdir}/%{name}-%{version}/RELEASE-NOTES

%changelog
* Wed Apr 03 2013 Carl Edquist <edquist@cs.wisc.edu> - 3.7.0-4
- Build with OpenJDK7

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.7.0-3
- rebuilt

* Tue Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.7.0-2
- Put the interface files in a well-known directory, not tied to the RPM version

* Tue Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.7.0-1
- Initial OSG packaging.

