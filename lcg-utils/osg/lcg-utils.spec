Name:		lcg-utils
Version:	1.11.14
Release:	12%{?dist}
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

%if 0%{?el6}
BuildRequires:  libuuid-devel
%else
BuildRequires:  e2fsprogs-devel
%endif


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

# Python macros
%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/*.la

# Python expects modules to be names .so, not a symlink to the real module
# So we fix them.
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/*.so
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/*.so.0
rename .so.0.0.0 .so $RPM_BUILD_ROOT%{python_sitearch}/*.so.0.0.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/lib*
%{python_sitearch}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/*
%{_docdir}/*
%{_includedir}/*

%changelog
* Thu Jan 19 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 1.11.14-12
- Adding libuuid-devel to build requires
- Adding python macros to detect python file locations

* Thu Jan 12 2012 Alain Roy <roy@cs.wisc.edu> - 1.11.14-11
- Fixed missing Python module files

* Wed Nov 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.11.14-10
- Previous issue was not quite fixed.

* Wed Nov 30 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 1.11.14-9
- Do not try and own python site directories.

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.11.14-8
- rebuilt

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.11.14-7
- Rebuilt against updated Globus libraries

* Mon Aug 29 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.11.14-6
- Rebuild against Globus 5.2

* Fri Jul 8 2011 Derek Weitzel <dweitzel@cse.unl.edu> 1.11.14-2
- Make lcg-utils give the right version.

* Sun Jul  3 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.11.14-1
- Update to latest upstream package.

* Thu Sep 10 2010 Brian Bockelman <bbockelm@cse.unl.edu> 1.3.3.2-1
- Initial RPM packaging

