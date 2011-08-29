
Name: xrootd-cmstfc
Version: 1.4.3
Release: 2
Summary: CMS TFC plugin for xrootd

Group: System Environment/Daemons
License: BSD
URL: svn://t2.unl.edu/brian/XrdCmsTfc
Source0: %{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: xrootd-libs-devel
BuildRequires: xerces-c-devel
BuildRequires: pcre-devel

#Requires: /usr/bin/xrootd pcre xerces-c

%description
%{summary}

%prep
%setup -q

%build
%configure --with-xrootd-incdir=/usr/include/xrootd
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libXrdCmsTfc*
%{_includedir}/xrootd/XrdCmsTfc/XrdCmsTfc.hh

%changelog
* Mon Aug 29 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.4.3-2
Rebuild for OSG Koji.

* Wed May 18 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.3-1
- Apply path matching only at the beginning of the path.

* Mon Mar 28 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.2-2
- Rebuild to reflect the updated RPM names.

* Wed Sep 29 2010 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.2-1
- Reduce verbosity of the logging.
- Fix for TFC parsing to better respect rule order; request from Florida.

* Tue Aug 24 2010 Brian Bockelman <bbockelm@cse.unl.edu> 1.4.0-1
- Break xrootd-cmstfc off into its own standalone RPM.

