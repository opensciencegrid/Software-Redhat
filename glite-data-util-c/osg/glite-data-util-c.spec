Name:		glite-data-util-c
Version:	1.2.3
Release:	1
Summary:	gLite data C utilties

Group:		System/Libraries
License:	EGEE Middleware license
URL:		http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.util-c
# Retrieved on Jul 3 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/org.glite.data.util-c.tar.gz?view=tar&pathrev=glite-data-util-c_R_1_2_3_1
Source0:        org.glite.data.util-c.tar.gz
Patch0:         glite_data_util_c_fedora.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  glib2-devel
BuildRequires:  glite-build-common-cpp
BuildRequires:  glite-service-discovery-api-c-devel
BuildRequires:  glite-service-discovery-build-common-cpp
BuildRequires:  gridsite-devel

%description
%{summary}

%prep
%setup -n org.glite.data.util-c

%patch0 -p0

%build
./bootstrap
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
* Sun Jul  3 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.2.3-1
- Initial RPM packaging.

%package devel
Summary: Development headers and libraries for the gLite data util package
Group:   System Development/Libraries

%description devel
%{summary}

%files devel
%defattr(-,root,root,-)
%{_includedir}/glite/data
%{_libdir}/libglite_data_util.so

