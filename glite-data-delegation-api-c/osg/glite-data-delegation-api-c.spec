Name:		glite-data-delegation-api-c
Version:	2.0.0.7
Release:	7%{?dist}
Summary:	Library for using the gLite delegation API from C

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.delegation-api-c
# Retrieved on Jul 5 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.delegation-api-c.tar.gz?view=tar&pathrev=glite-data-delegation-api-c_R_2_0_0_7
Source0:        org.glite.data.delegation-api-c.tar.gz
Patch0:         glite_data_delegation_api_c_fedora.patch
Patch1:        no_stdsoap2.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  automake autoconf libtool
BuildRequires:  CGSI-gSOAP-devel
BuildRequires:  glite-build-common-cpp
BuildRequires:  glite-security-delegation-interface
BuildRequires:  glite-data-build
BuildRequires:  globus-gssapi-gsi-devel
BuildRequires:  globus-gss-assist-devel

%description
%{summary}

%prep
%setup -n org.glite.data.delegation-api-c

%patch0 -p0
%patch1 -p0
#cp %{SOURCE1} stdsoap2.c

%build
./bootstrap

# Note the gsoap version is hardcoded.  The true gsoap version doesn't matter, only that it is greater than 2.3
export CGSI_GSOAP_LOCATION=/usr
export CGSI_GSOAP_CFLAGS=-I/usr/include
export CGSI_GSOAP_LIBS='-L/usr/lib64 -lcgsi_plugin'
%configure \
    --with-delegation-wsdl=/usr/share/glite-security-delegation-interface/interface/www.gridsite.org-delegation-2.0.0.wsdl \
    --with-gsoap-version=2.7.13 \
    --with-interface-version=2.0.0 \
    --with-globus-nothr-flavor=gcc64dbg \
    --with-globus-thr-flavor=gcc64dbgpthr \
    --disable-static

# libcgsi_plugin_gsoap_2.7 is now just called libcgsi_plugin.
# Globus no longer uses flavors
# The configure script ignores these settings so I have to fix the makefiles myself.
find . -name Makefile -exec sed -i -e 's/cgsi_plugin_gsoap_2.7/cgsi_plugin/g' {} \;
find . -name Makefile -exec sed -r -i -e 's/_gcc64dbg(pthr)?//g' {} \;

make -j1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
# All the binaries are unittest stuff
rm -f $RPM_BUILD_ROOT%{_bindir}/*
rm -f $RPM_BUILD_ROOT%{python_sitearch}/*.la
rm -f $RPM_BUILD_ROOT%{python_sitearch}/*.so.0.0.0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/*
%{_docdir}/glite-data-delegation-api-c
%{_includedir}/glite/data/delegation

%changelog
* Mon Oct 06 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.0.7-7
- Fix name of cgsi_plugin library and remove globus flavors so this builds again
  (SOFTWARE-1298)
- Single process build to avoid race condition
- First build for el7 (SOFTWARE-1604)

* Thu Jan 19 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 2.0.0.7-6
- Remove stdsoap2.c dependency, making it less dependent on a specific version of gsoap.

* Thu Jan 19 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 2.0.0.7-5
- Adding stdsoap2.c from el6 distribution.

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.0.7-4
- rebuilt

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.0.7-3
- Rebuilt against updated Globus libraries

* Wed Aug 31 2011 Matyas Selmeci <matyas@cs.wisc.edu> 1.11.14-2
- Rebuild against Globus 5.2

* Sat Jul  2 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.11.14-1
- Update to latest release.

* Fri Sep 10 2010 Brian Bockelman <bbockelm@cse.unl.edu> 1.3.3.2-1
- Initial RPM packaging
- A few configure changes in order to force the builds to find the Fedora/EPEL
  globus libraries and includes
- Fix a few code generation errors in the SRMv2 stubs

