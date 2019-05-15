Name: scitokens-cpp
Version: 0.3.0
Release: 3%{?dist}
Summary: C++ Implementation of the SciTokens Library
License: Apache 2.0
URL: https://github.com/scitokens/scitokens-cpp

# Generated from:
# git_archive_all.py --prefix=scitokens-cpp-0.3.0/ --force-submodules -9 scitokens-cpp-0.3.0.tar.gz
# Where git_archive_all.py is from https://github.com/Kentzo/git-archive-all.git
Source0: %{name}-%{version}.tar.gz

Patch0: Force-aud-test-in-the-validator.patch

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: sqlite-devel
BuildRequires: openssl-devel
BuildRequires: libcurl-devel
BuildRequires: libuuid-devel

# Needed for C++11
%if 0%{?el6}
BuildRequires: devtoolset-2-toolchain
BuildRequires: scl-utils
%endif

%description
%{summary}

%package devel
Summary: Header files for the scitokens-cpp public interfaces.

Requires: %{name} = %{version}

%description devel
%{summary}

%prep
%setup -q
%patch0 -p1

%build
do_build () {
    set -x
    mkdir build
    cd build
    %cmake ..
    make
}
export -f do_build
%if 0%{?el6}
scl enable devtoolset-2 do_build
%else
do_build
%endif

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
* Mon May 13 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.3.0-3
- Add Force-aud-test-in-the-validator.patch from
  https://github.com/scitokens/scitokens-cpp/pull/8

* Fri May 03 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.3.0-2
- Fix requirements

* Thu May 02 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 0.3.0-1
- Update to v0.3.0
- Add dependencies on libcurl-devel, libuuid-devel

* Thu Jan 03 2019 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1.0-1
- Initial version of the SciTokens C++ RPM.
