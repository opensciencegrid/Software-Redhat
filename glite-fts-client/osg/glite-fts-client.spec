Name:		glite-fts-client
Version:	3.7.4
Release:	9%{?dist}
Summary:	gLite FTS client

Group:		Development/Languages/C and C++
License:	Apache 2.0
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.transfer-cli
# Retrieved on Jul 5 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.transfer-cli.tar.gz?view=tar&pathrev=glite-data-transfer-cli_R_3_7_4_1
Source0:        org.glite.data.transfer-cli.tar.gz

Patch0:         glite_fts_client_fedora.patch
Patch1:         channel_internal_fixelsif.sl6.patch
Patch2:         add_gsoap_support.patch
Patch3:         add_gsoap_tools.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:	CGSI-gSOAP
BuildRequires:  automake autoconf libtool
BuildRequires:  CGSI-gSOAP-devel%{?_isa}
BuildRequires:  glite-build-common-cpp
BuildRequires:  glite-data-build
BuildRequires:  glite-data-util-c-devel%{?_isa}
BuildRequires:  glite-data-delegation-cli-devel%{?_isa}
BuildRequires:  glite-data-transfer-interface
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  glib2-devel%{?_isa}
%if 0%{?rhel} >= 6
BuildRequires:  libuuid-devel
%else
BuildRequires:  e2fsprogs-devel
%endif
BuildRequires:  globus-gssapi-gsi-devel%{?_isa}
BuildRequires:  globus-gss-assist-devel%{?_isa}
BuildRequires:  gridsite-devel%{?_isa}
BuildRequires:  python-devel%{?_isa}
BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen

%description
%{summary}

%prep
%setup -n org.glite.data.transfer-cli

%patch0 -p0

# Fix elsif in channel_internal.h
%if 0%{?rhel} >= 6
%patch1 -p0
%endif

%patch2 -p0
%patch3 -p0

%build
./bootstrap
# Note the gsoap version is hardcoded.  The true gsoap version doesn't matter, only that it is greater than 2.3
export CGSI_GSOAP_LOCATION=/usr
export CGSI_GSOAP_CFLAGS=-I/usr/include
export CGSI_GSOAP_LIBS='-L/usr/lib64 -lcgsi_plugin'
%if 0%{?rhel} >= 7
export LIBS='-lgridsite_globus -lcrypto'
%endif
%configure \
    --with-channel-wsdl=/usr/share/glite-data-transfer-interface/interface/org.glite.data-channel-3.7.0.wsdl \
    --with-fts-wsdl=/usr/share/glite-data-transfer-interface/interface/org.glite.data-fts-3.7.0.wsdl \
    --with-gsoap-version=2.7.13 \
    --with-version=%{version}  \
    --with-interface-version=3.7.0 \
    --with-globus-nothr-flavor=DELETEME \
    --with-globus-thr-flavor=DELETEME \
    --disable-static

# Remove globus flavors and rename cgsi_plugin by hand
find . -name Makefile -exec \
    sed -r -i \
        -e 's/_?DELETEME//g' \
        -e 's/cgsi_plugin_gsoap_2.7/cgsi_plugin/g' \
    {} +

make -j1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Python macros
%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/fts.a
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/fts.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitearch}/fts*
%{_libdir}/lib*.so.*

%{_mandir}/man1/glite*
%{_bindir}/glite-transfer*


%package devel
Summary: C libraries and headers for working with FTS
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}

%files devel
%{_includedir}/glite/data/transfer*
%{_libdir}/libglite_data_transfer_api_simple_c.so
%{_libdir}/libglite_data_transfer_channel_api_c.so
%{_libdir}/libglite_data_transfer_channel_api_simple_c.so
%{_libdir}/libglite_data_transfer_fts_api_c.so
%{_libdir}/libglite_data_transfer_fts_api_simple_c.so

%package doc
Summary: Documentation files for FTS
Group: Documentation

%description doc
%{summary}

%files doc
%defattr(-,root,root)
%doc %{_docdir}/glite-data-transfer-cli

%changelog
* Tue Oct 07 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 3.7.4-9
- Fix name of cgsi_plugin library and remove globus flavors so this builds
  again (SOFTWARE-1298)
- Build on EL7

* Thu Jan 19 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.7.4-7
- Adding patch for malformed elsif

* Thu Jan 19 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.7.4-6
- Adding libuuid dependency for sl6

* Thu Jan 19 2012 Derek Weitzel <dweitzel@cse.unl.edu> - 3.7.4-5
- Adding python macros

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.7.4-4
- rebuilt

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 3.7.4-3
- Rebuilt against updated Globus libraries

* Fri Jul 15 2011 Brian Bockelman <bbockelm@cse.unl.edu> 3.7.4-2
- Added interface-version to build script.

* Tue Jul  5 2011 Brian Bockelman <bbockelm@cse.unl.edu> 2.0.1.3-1
- Initial OSG packaging.

