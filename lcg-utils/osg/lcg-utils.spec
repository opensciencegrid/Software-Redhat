Name:		lcg-utils
Version:	1.11.14
Release:	5
Summary:	gLite file transfer clients

Group:		Productivity/File utilities
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.dm-util
# Retrieved on Sep 10 2010
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.dm-util.tar.gz?view=tar&pathrev=glite-data-dm-util_R_1_11_14_1
Source0:        org.glite.data.dm-util.tar.gz
Patch0:         lcg_utils_makefile_cleanup.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:	gfal
BuildRequires:  automake autoconf libtool swig gfal glite-build-common-cpp globus-ftp-client-devel globus-gass-copy-devel voms-devel CGSI-gSOAP-devel python-devel

%description
%{summary}

%prep
%setup -n org.glite.data.dm-util

%patch0 -p1

%build
mkdir -p src/autogen build; aclocal -I /usr/share/glite-build-common-cpp/m4/; libtoolize --force; autoheader; automake --foreign --add-missing --copy; autoconf
export CFLAGS="%{optflags} -I%{_libdir}/globus/include"
%configure --with-glite-location=/usr --with-globus-nothr-flavor=gcc64dbg --with-globus-thr-flavor=gcc64dbgpthr --with-gfal-location=/usr --with-voms-location=/usr --with-release=%{release} --with-version=%{version}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.4/site-packages/*.so.0.0.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/*
%{_mandir}/*
%{_bindir}/*
%{_docdir}/*
%{_includedir}/*

%changelog
* Fri Jul 8 2011 Derek Weitzel <dweitzel@cse.unl.edu> 1.11.14-2
- Make lcg-utils give the right version.

* Sun Jul  3 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.11.14-1
- Update to latest upstream package.

* Thu Sep 10 2010 Brian Bockelman <bbockelm@cse.unl.edu> 1.3.3.2-1
- Initial RPM packaging

