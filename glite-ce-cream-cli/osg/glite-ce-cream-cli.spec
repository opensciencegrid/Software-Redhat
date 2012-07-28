Summary: Commands for accessing the CREAM service
Name: glite-ce-cream-cli
Version: 1.14.0
%global upstream_release 4
Release: %{upstream_release}.3%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: Applications/Internet
Requires: uberftp
BuildRequires: %{!?extbuilddir:glite-jdl-api-cpp-devel,} chrpath
BuildRequires: %{!?extbuilddir:glite-ce-cream-client-devel,} libtool
BuildRequires: globus-common-devel, globus-callout-devel, globus-openssl-devel
BuildRequires: globus-openssl-module-devel, globus-gsi-callback-devel, globus-gsi-cert-utils-devel
BuildRequires: globus-gsi-credential-devel, globus-gsi-openssl-error-devel, globus-gsi-proxy-core-devel
BuildRequires: globus-gsi-proxy-ssl-devel, globus-gsi-sysconfig-devel,globus-gssapi-error-devel
BuildRequires: globus-gssapi-gsi-devel, globus-gss-assist-devel
BuildRequires: globus-ftp-client-devel, globus-ftp-control-devel
BuildRequires: %{!?extbuilddir: gridsite-devel, voms-devel,} libxml2-devel, boost-devel
BuildRequires: %{!?extbuilddir: glite-jobid-api-c-devel,} classads-devel, 
BuildRequires: %{!?extbuilddir: glite-lbjp-common-gsoap-plugin-devel,} docbook-style-xsl
BuildRequires: %{!?extbuilddir:glite-build-common-cpp, } libxslt
BuildRequires: gsoap-devel, libxml2-devel, log4cpp-devel, c-ares-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source5: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Source6: %{name}-%{version}-%{upstream_release}.sl6.tar.gz

%global debug_package %{nil}

%description
The CREAM client is a collection of commands for accessing the CREAM service

%prep
 

%setup -c -T -b %{rhel}

%build
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  # Some packages that we either don't have pkg-config files for
  # or configure just can't plain find them.
  export GSOAP_PLUGIN_CFLAGS=-I/usr/include
  %if 0%{?el6}
  export GSOAP_PLUGIN_LIBS=-lglite_security_gsoap_plugin_2716_cxx
  %endif
  %if 0%{?el5}
  export GSOAP_PLUGIN_LIBS=-lglite_security_gsoap_plugin_2713_cxx
  %endif
  export GLITE_JOBID_CFLAGS=-I/usr/include
  export GLITE_JOBID_LIBS=-lglite_jobid
  export CLASSAD_CFLAGS=-I/usr/include/classad
  export CLASSAD_LIBS=-lclassad
  export GRIDSITE_OPENSSL_CFLAGS=-I/usr/include
  export GRIDSITE_OPENSSL_LIBS="-lgridsite"
  ./configure --prefix=%{buildroot}/usr --sysconfdir=%{buildroot}/etc --disable-static PVER=%{version}
  make -j1
fi

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  make install
else
  cp -R %{extbuilddir}/* %{buildroot}
fi
rm %{buildroot}%{_libdir}/*.la
strip -s %{buildroot}%{_libdir}/*.so.0.0.0
strip -s %{buildroot}%{_bindir}/*
chrpath --delete %{buildroot}%{_bindir}/*
export QA_SKIP_BUILD_ROOT=yes

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig 

%files
%defattr(-,root,root)
%dir /etc/glite-ce-cream-cli/
%config(noreplace) /etc/glite-ce-cream-cli/glite_cream.conf.template
%{_bindir}/glite-ce-*
%{_bindir}/glite-es-*
%dir /usr/share/doc/%{name}-%{version}/
%doc /usr/share/doc/%{name}-%{version}/LICENSE
%doc /usr/share/man/man1/glite-ce-*.1.gz
%{_libdir}/libglite_ce_cream_cli_*.so
%{_libdir}/libglite_ce_cream_cli_*.so.0
%{_libdir}/libglite_ce_cream_cli_*.so.0.0.0



%changelog
* Fri Jul 27 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.3.osg
- Link against c++ version of gsoap plugin

* Mon Jul 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.2.osg
- Include both el5 and el6 tarballs in srpm

* Mon Jun 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.14.0-4.1.osg
- Rebuild for OSG
- Use sl6 tarball for rhel6 builds (based on %%rhel macro)
- Fix 64-bit specific lines in install section and files section

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 1.14.0-4.sl5
- Major bugs fixed
 
