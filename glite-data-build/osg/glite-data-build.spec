Name:		glite-data-build
Version:	3.2.0
Release:	2%{?dist}
Summary:	Build macros for the org.glite.data family.

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.gfal
# Retrieved on Sep 10 2010
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.tar.gz?view=tar&pathrev=glite-data_branch_3_2_0
Source0:        org.glite.data.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

%description
%{summary}

%prep
%setup -n org.glite.data

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp project/*.m4 $RPM_BUILD_ROOT%{_datadir}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}

%changelog
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.2.0-2
- rebuilt

* Sat Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.2.0-1
- Creation of the package for the purpose of making the build macros available.

