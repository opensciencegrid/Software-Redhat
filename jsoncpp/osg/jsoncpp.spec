Name: jsoncpp
Version: 1.9.4
Release: 2%{?dist}
Summary: jsoncpp

%if %{rhel} == 7
%define CMAKE cmake3
%else
%define CMAKE cmake
%endif




Group: System Environment/Daemons
License: BSD
Source0: %{name}-1.9.4.tar.gz
BuildRequires: %{CMAKE} gcc make
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%package devel
Summary: Development headers and libraries for Xrootd CMSTFC plugin
Group: System Environment/Development

%define _unpackaged_files_terminate_build 0
%global __cmake_in_source_build 1

%description
%{summary}

%description devel
%{summary}

%prep
%setup -q -c -n %{name}-%{version}

%build
cd %{name}-%{version}

%if %{rhel} == 7
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_LIBDIR=%{_lib} -DBUILD_STATIC_LIBS=OFF -DJSONCPP_WITH_TESTS=OFF .
%else
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_LIBDIR=%{_lib} -DBUILD_STATIC_LIBS=OFF -DJSONCPP_WITH_TESTS=OFF .
%endif

make VERBOSE=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libjsoncpp.so
%{_libdir}/libjsoncpp.so.*
%files devel
%defattr(-,root,root,-)
%{_includedir}/json/*

%changelog
