
Summary: CMS meta-RPM for Xrootd
Name: cms-xrootd
Version: 1.2
Release: 9%{?dist}
Group: System Environment/Daemons
License: Public Domain
URL: https://twiki.cern.ch/twiki/bin/view/Main/CmsXrootdArchitecture

# Note that we aren't shipping the T3 config until caching is better
# understood.
Source0:  xrootd.sample.t3.cfg.in
Source1:  xrootd.sample.posix.cfg.in
Source2:  Authfile
Source3:  xrootd.sample.dcache.cfg.in
Source4:  xrootd.sample.proxy.cfg.in

Requires: xrootd >= 1:4.1.0

%ifarch %{ix86}
Requires: libXrdLcmaps.so.0
Requires: libXrdCmsTfc.so.0
%else
Requires: libXrdLcmaps.so.0()(64bit)
Requires: libXrdCmsTfc.so.0()(64bit)
%endif
%if 0%{?rhel} < 6
Requires: fetch-crl3
%else
Requires: fetch-crl
%endif
Requires: grid-certificates

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
%{summary}

%package hdfs
Summary: CMS meta-RPM for Xrootd over HDFS
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: xrootd-hdfs >= 1.8.4-2
%ifarch %{ix86}
Requires: libXrdHdfs.so.0
%else
Requires: libXrdHdfs.so.0()(64bit)
%endif

%description hdfs
%{summary}

%package proxy
Summary: CMS meta-RPM for Xrootd proxies
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description proxy
%{summary}

%package dcache
Summary: CMS meta-RPM for Xrootd over dCache
Group: System Environment/Daemons
Requires: xrootd >= 1:4.1.0

%description dcache
%{summary}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xrootd

#sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE0} > $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd.sample.t3.cfg
sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd.sample.posix.cfg
sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE3} > $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd.sample.dcache.cfg
sed -e "s#@LIBDIR@#%{_libdir}#" %{SOURCE4} > $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/xrootd.sample.proxy.cfg
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/xrootd/Authfile

%clean
rm -rf $RPM_BUILD_ROOT

%files
#%{_sysconfdir}/xrootd/xrootd.sample.t3.cfg
%{_sysconfdir}/xrootd/xrootd.sample.posix.cfg
%{_sysconfdir}/xrootd/Authfile

%files hdfs

%files dcache
%{_sysconfdir}/xrootd/xrootd.sample.dcache.cfg

%files proxy
%{_sysconfdir}/xrootd/xrootd.sample.proxy.cfg

%changelog
* Tue Mar 31 2015 Edgar Fajardo <emfajard@ucsd.edu> - 1.2-9
- Remove xrootd4 and replaced it with xrootd and version number

* Wed Aug 13 2014 Carl Edquist <edquist@cs.wisc.edu> - 1.2-8
- Update to use xrootd4

* Thu Apr 18 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2-7
- Fix epoch in xrootd requires lines

* Mon Apr 08 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2-5
- Require xrootd instead of xrootd-server to match renaming in 3.3.1
- Remove Conflicts: xrootd-server < 3.1.0 lines -- that's not the way to require minimum versions

* Fri Feb 22 2013 Brian Lin <blin@cs.wisc.edu> - 1.2-4
- Update rhel5 to require fetch-crl3 instead of fetch-crl.

* Tue Dec 11 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.2-3
- Fix ofs.authorize line in the dCache example file.

* Tue Oct 23 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.2-2
- Add proxy config file.

* Mon Sep 17 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.2-1
- Tweaks for default configs, based on feedback from Estonia, Legnaro, and UCL.


