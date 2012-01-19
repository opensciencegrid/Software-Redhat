Name:		glite-service-discovery-build-common-cpp
Version:	0.3.0
Release:	2%{?dist}
Summary:	Build macros for the org.glite.service-discovery family.

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.service-discovery.build-common-cpp
# Retrieved on Jul 5 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.service-discovery.build-common-cpp.tar.gz?view=tar&pathrev=HEAD
Source0:        org.glite.service-discovery.build-common-cpp.tar.gz

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch

%description
%{summary}

%prep
%setup -n org.glite.service-discovery.build-common-cpp

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/
mv m4 $RPM_BUILD_ROOT%{_datadir}/%{name}/m4

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}

%changelog
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 0.3.0-2
- rebuilt

* Sat Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 0.3.0-1
- Initial OSG packaging.
- Note that we use HEAD, not the release tag: there is a bug in the lib64 macro.

