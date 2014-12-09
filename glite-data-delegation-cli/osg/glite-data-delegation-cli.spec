Name:		glite-data-delegation-cli
Version:	2.0.1.3
Release:	8%{?dist}
Summary:	gLite delegation API command-line tools

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.delegation-cli
# Retrieved on Jul 5 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.delegation-cli.tar.gz?view=tar&pathrev=glite-data-delegation-cli_R_2_0_1_3
Source0:        org.glite.data.delegation-cli.tar.gz
Patch0:         glite_data_delegation_cli_fedora.patch
Patch1:         testcase_new_gsoap.patch
Patch2:         rename_doxygen_output-sl6.patch
Patch3:         el7-autoconf.patch
Patch4:         disable_test_33641.patch
Patch5:         remove_gridsite_globus.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  automake autoconf libtool
BuildRequires:  CGSI-gSOAP-devel
BuildRequires:  glite-build-common-cpp
BuildRequires:  glite-data-build
BuildRequires:  glite-data-util-c-devel
BuildRequires:  glite-data-delegation-api-c
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  gridsite-devel
BuildRequires:  docbook-style-xsl
BuildRequires:  libxml2-devel
BuildRequires:  glib2-devel
BuildRequires:  globus-gsi-sysconfig-devel
BuildRequires:  globus-core
BuildRequires:  glite-service-discovery-api-c-devel
BuildRequires:  globus-gssapi-gsi-devel
BuildRequires:  globus-gss-assist-devel
BuildRequires:  doxygen

%description
%{summary}

%prep
%setup -n org.glite.data.delegation-cli

%patch0 -p0
%patch1 -p0

%if 0%{?rhel} >= 6
%patch2 -p0
%endif

%if 0%{?rhel} >= 7
%patch3 -p1
%patch4 -p1
%endif

%patch5 -p1

%build
./bootstrap
export CGSI_GSOAP_LOCATION=%{_prefix}
export CGSI_GSOAP_CFLAGS=-I%{_includedir}
export CGSI_GSOAP_LIBS="-L%{_libdir} -lcgsi_plugin"
export CFLAGS="%{optflags} -I%{_libdir}/globus/include -I%{_includedir}/globus"
%configure \
    --with-interface-version=2.0.0 \
    --with-version=2.0.1 \
    --with-gsoap-version=2.7.13 \
    --with-globus-nothr-flavor=gcc32dbg \
    --with-globus-thr-flavor=gcc32dbgpthr \
    --disable-static

# Remove globus flavors and rename cgsi_plugin by hand
find . -name Makefile -exec \
    sed -r -i \
        -e 's/_?gcc32dbg(pthr)?//g' \
        -e 's/cgsi_plugin_gsoap_2.7/cgsi_plugin/g' \
    {} +

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_bindir}/test-glite-delegation-bug-33641
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
%{_mandir}/man1/*
%{_bindir}/glite-*

%changelog
* Tue Dec 09 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.1.3-8
- Replace gridsite_globus dependency with gridsite dependency (SOFTWARE-1298)

* Tue Oct 07 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 2.0.1.3-7
- Patch configure.ac to get this to build with el7's autoconf
- Fix name of cgsi_plugin library and remove globus flavors so this builds again
  (SOFTWARE-1298)
- Remove test_33641 from EL 7 build (broken)

* Fri Jan 20 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 2.0.1.3-6
- Rebuild again for gsoap support

* Fri Jan 20 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 2.0.1.3-5
- Rebuild for gsoap support

* Thu Jan 19 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 2.0.1.3-4
- Add rename_doxygen_output-sl6.patch for el6 doxygen

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.1.3-3
- rebuilt

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.0.1.3-2
- Rebuilt against updated Globus libraries

* Tue Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.1.3-1
- Initial OSG packaging.

%package devel
Summary: C libraries and headers for the gLite delegation CLI
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}

%files devel
%{_libdir}/libglite_data_delegation_api_simple_c.so
%{_includedir}/glite/data/delegation

%package doc
Summary: Documentation for the gLite delegation CLI
Group: Documentation

%description doc
%{summary}

%files doc
%{_docdir}/%{name}

