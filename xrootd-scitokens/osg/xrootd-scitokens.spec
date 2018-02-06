Name: xrootd-scitokens
Version: 0.3.1
Release: 1%{?dist}
Summary: SciTokens authentication plugin for XRootD
License: Apache 2.0
URL: https://github.com/scitokens/xrootd-scitokens

# Generated from:
# git archive v%{version} --prefix=xrootd-scitokens-%{version}/ | gzip -7 > ~/rpmbuild/SOURCES/xrootd-scitokens-%{version}.tar.gz
Source0: %{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: python-devel
BuildRequires: xrootd-server-devel

Requires: python2-scitokens
#Requires: boost-python

%description
SciTokens authentication plugin for XRootD

%prep
%setup -q

%build
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/libXrdAccSciTokens-4.so
%{_libdir}/python2.7/site-packages/_scitokens_xrootd.so
%{_libdir}/python2.7/site-packages/scitokens_xrootd.py*

%defattr(-,root,root,-)

%changelog
* Mon Nov 06 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 0.3.1-1
- Fix issue with translating write authz.

* Wed Sep 20 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 0.2.0-1
- Remove urltools dependency.

* Wed Sep 20 2017 Lincoln Bryant <lincolnb@uchicago.edu> - 0.1.0-1
- Initial package
