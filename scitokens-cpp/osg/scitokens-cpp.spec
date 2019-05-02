Name: scitokens-cpp
Version: 0.3.0
Release: 1%{?dist}
Summary: C++ Implementation of the SciTokens Library
License: Apache 2.0
URL: https://github.com/scitokens/scitokens-cpp

# Generated from:
# git_archive_all.py --prefix=scitokens-cpp-0.3.0/ --force-submodules -9 scitokens-cpp-0.3.0.tar.gz
# Where git_archive_all.py is from https://github.com/Kentzo/git-archive-all.git
Source0: %{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: sqlite-devel
BuildRequires: openssl-devel
BuildRequires: libcurl-devel
BuildRequires: libuuid-devel

%description
%{summary}

%package devel
Summary: Header files for the scitokens-cpp public interfaces.

Requires: %{name}-%{version}

%description devel
%{summary}

%prep
%setup -q

%build
%if 0{?el6}
echo "*** This does not build on EL 6 ***"
exit 1
%endif
mkdir build
cd build
%cmake ..
make

%install
pushd build
rm -rf $RPM_BUILD_ROOT
echo $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/libSciTokens.so*

%files devel
%{_includedir}/scitokens/scitokens.h

%defattr(-,root,root,-)

%changelog
* Thu May 02 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.3.0-1
- Update to v0.3.0
- Add dependencies on libcurl-devel, libuuid-devel

* Thu Jan 03 2019 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1.0-1
- Initial version of the SciTokens C++ RPM.
