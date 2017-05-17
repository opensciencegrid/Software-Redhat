Name:		glite-build-common-cpp
Version:	3.3.0.2
Release:	1%{?dist}
Summary:	gLite build macros

Group:		Development/Libraries/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.build.common-cpp/
# Retrieved on May 28, 2012
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.build.common-cpp.tar.gz?view=tar&pathrev=glite-build-common-cpp_R_3_3_0_2
Source0:        org.glite.build.common-cpp.tar.gz
# Path0 fixes the globus build macros to use the Fedora/EPEL flavour-less libraries
Patch0:         fedora_globus_macros.patch
BuildArch:	noarch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:	globus-common-progs

%description
Common m4 macros used for the C++ autotools builds in gLite

%prep
%setup -n org.glite.build.common-cpp
#%patch0 -p0

%build

%install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/m4
install -m 0644 m4/*.m4 $RPM_BUILD_ROOT%{_datadir}/%{name}/m4/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/m4/*.m4

%changelog
* Mon May 28 2012 Brian Bockelman <bbockelm@cse.unl.edu> 3.3.0.2-1
- Update to latest upstream release.

* Sat Sep 11 2010 Brian Bockelman <bbocklem@cse.unl.edu> 3.2.9.1-6
- Fix for using the CGSI found in Fedora.
- Fix globus version check.
- Add a requires for the globus-version binary.
- Fix includes for 32-bit builds

* Thu Sep 9 2010 Brian Bockelman <bbockelm@cse.unl.edu> 3.2.9.1-1
- Initial import from gLite and creation of RPM packaging
- Patched the GLOBUS macro to fit Fedora/EPEL scheme

