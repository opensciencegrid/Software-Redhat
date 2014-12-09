Name:		glite-data-util-c
Version:	1.2.3
Release:	5%{?dist}
Summary:	gLite data C utilties

Group:		System/Libraries
License:	EGEE Middleware license
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.util-c
# Retrieved on Jul 3 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.util-c.tar.gz?view=tar&pathrev=glite-data-util-c_R_1_2_3_1
Source0:        org.glite.data.util-c.tar.gz
Patch0:         glite_data_util_c_fedora.patch
Patch1:         remove_gridsite_globus.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  glib2-devel
BuildRequires:  glite-build-common-cpp
BuildRequires:  glite-service-discovery-api-c-devel
BuildRequires:  glite-service-discovery-build-common-cpp
BuildRequires:  gridsite-devel
BuildRequires:  globus-gsi-sysconfig-devel
BuildRequires:  globus-core
BuildRequires:  libxml2-devel

%description
%{summary}

%prep
%setup -n org.glite.data.util-c

%patch0 -p0
%patch1 -p1

%build
./bootstrap
export CFLAGS="%{optflags} -I%{_libdir}/globus/include -I/usr/include/globus"
%configure --with-glite-location=/usr
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT/usr/share/test/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libglite_data_util.so.*
#%{_mandir}/*
#%{_bindir}/*
%{_docdir}/*

%changelog
* Tue Dec 09 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 1.2.3-5
- Patch to remove gridsite_globus dep

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.3-4
- rebuilt

* Tue Sep 13 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.3-3
- Rebuilt against updated Globus libraries

* Wed Jul  6 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.2.3-2
- Added glite-service-discovery-api-c-devel to the devel subpackage requirements
  Necessary for including the header files.

* Sun Jul  3 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.2.3-1
- Initial RPM packaging.

%package devel
Summary: Development headers and libraries for the gLite data util package
Group:   System Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glite-service-discovery-api-c-devel

%description devel
%{summary}

%files devel
%defattr(-,root,root,-)
%{_includedir}/glite/data
%{_libdir}/libglite_data_util.so

