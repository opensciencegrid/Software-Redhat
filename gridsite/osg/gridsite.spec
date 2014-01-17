%define aprversion 1
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}


%global vercompat 1.5.20
%if 0%{?el5} 
%global compat 1
%endif


Name:           gridsite
Version:        1.7.25
Release:        1.1%{?dist}
Summary:        Grid Security for the Web, Web platforms for Grids

Group:          System Environment/Daemons

#  - src/gsexec.c ASL 2.0
#  - src/gsexec.h ASL 2.0
#  - src/mod_gridsite.c BSD but includes ASL 2.0 based code.
#  - src/mod_ssl-private.h BSD but includes ASL 2.0 based code.
# All other files are BSD
License:        ASL 2.0 and BSD
URL:            http://www.gridsite.org
Source0:        http://www.gridsite.org/download/sources/gridsite-%{version}.src.tar.gz
Source1:        gridsite-httpd.conf
Source2:        gridsitehead.txt
Source3:        gridsitefoot.txt
Source4:        root-level.gacl
Source5:        gridsitelogo.png

Source10:       http://www.gridsite.org/download/sources/gridsite-%{vercompat}.src.tar.gz

#Change location of cgi-scripts.
Patch1:         cgi-bin-location-1.7.25.patch
#Change location of cgi-scripts.
Patch2:         cgi-bin-location-1.5.20.patch
# Includes are wrong.
#https://bugzilla.redhat.com/show_bug.cgi?id=612109
#https://savannah.cern.ch/bugs/index.php?69632
Patch3:         gridsite-include-1.5.20.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildRequires:  libcurl-devel
%else
BuildRequires:  curl-devel
%endif

BuildRequires:  libxml2-devel 
BuildRequires:  httpd-devel
BuildRequires:  doxygen
BuildRequires:  openssl-devel
BuildRequires:  gsoap-devel

Requires:       httpd-mmn = %{_httpd_mmn}
Requires:       mod_ssl
Requires:       gridsite-libs = %{version}-%{release}

Provides:       gridsite-apache = %{version}-%{release}
Obsoletes:      gridsite-apache <= 1.7.20
Provides:       gridsite-services = %{version}-%{release}
Obsoletes:      gridsite-services <= 1.7.20

%description
GridSite was originally a web application developed for managing and formatting 
the content of the http://www.gridpp.ac.uk/ website. Over the past years it 
has grown into a set of extensions to the Apache web server and a toolkit for 
Grid credentials, GACL access control lists and HTTP(S) protocol operations. 

This package gridsite contains apache httpd modules for enabling 
mod_gridsite.

%package  libs
Group:    System Environment/Daemons
Summary:  Run time libraries for mod_gridsite and gridsite-clients

%description libs
GridSite was originally a web application developed for managing and formatting 
the content of the http://www.gridpp.ac.uk/ website. Over the past years it 
has grown into a set of extensions to the Apache web server and a toolkit for 
Grid credentials, GACL access control lists and HTTP(S) protocol operations. 

This package contains the runtime libraries.

%package  clients
Group:    System Environment/Daemons
Summary:  Clients to gridsite including htcp, htrm, htmv
Requires: gridsite-libs = %{version}-%{release}
Provides: gridsite-commands = %{version}-%{release}
Obsoletes:gridsite-commands <= 1.7.20

%description  clients
GridSite was originally a web application developed for managing and formatting 
the content of the http://www.gridpp.ac.uk/ website. Over the past years it 
has grown into a set of extensions to the Apache web server and a toolkit for 
Grid credentials, GACL access control lists and HTTP(S) protocol operations. 

This package gridsite-clients, contains clients for using against gridsite, 
htcp, htrm, ...

%package  gsexec
Group:    System Environment/Daemons
Summary:  Setuid gsexec tools for gridsite
Requires: gridsite-libs = %{version}-%{release}

%description  gsexec
GridSite was originally a web application developed for managing and formatting 
the content of the http://www.gridpp.ac.uk/ website. Over the past years it 
has grown into a set of extensions to the Apache web server and a toolkit for 

This package gridsite-setuid, contains the setuid gsexec program.

%package  devel
Group:    System Environment/Daemons
Summary:  Developers tools for gridsite
Requires: gridsite-libs = %{version}-%{release}
Requires: openssl-devel

%description  devel
GridSite was originally a web application developed for managing and formatting 
the content of the http://www.gridpp.ac.uk/ website. Over the past years it 
has grown into a set of extensions to the Apache web server and a toolkit for 

This package gridsite-devel, contains developer tools for using gridsite.

%package   doc
Group:     System Environment/Daemons
Summary:   Developers Documentation for gridsite
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch: noarch
%endif

%description  doc
GridSite was originally a web application developed for managing and formatting 
the content of the http://www.gridpp.ac.uk/ website. Over the past years it 
has grown into a set of extensions to the Apache web server and a toolkit for 

This package gridsite-doc, contains developer documentation for gridsite.

%if 0%{?compat}
%package compat
Group:    System Environment/Daemons
Summary:  Run time libraries for mod_gridsite and gridsite-clients
Version:  %{vercompat}
Release:  5.1%{?dist}

%description compat
GridSite was originally a web application developed for managing and formatting 
the content of the http://www.gridpp.ac.uk/ website. Over the past years it 
has grown into a set of extensions to the Apache web server and a toolkit for 
Grid credentials, GACL access control lists and HTTP(S) protocol operations. 

This package contains the runtime libraries.
%endif

%prep
%if 0%{?compat}
%setup -q -n org.gridsite.core -a 10
pushd org.gridsite.core
%patch2 -p1
%patch3 -p1
popd

%else
%setup -q -n org.gridsite.core
%endif
# Copy in apache configuration.
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .
cp -p %{SOURCE4} .
cp -p %{SOURCE5} .

## Change installed path of cgi-bins.
%patch1 -p1

%build
%if 0%{?compat}
pushd org.gridsite.core
(cd src && MYCFLAGS="%{optflags} -DLINUX=2 -D_REENTRANT -D_LARGEFILE64_SOURCE -I../interface -I%{_includedir}/httpd -I%{_includedir}/apr-%{aprversion} -fPIC " make )
popd
%endif
(cd src && MYCFLAGS="%{optflags} -DLINUX=2 -D_REENTRANT -D_LARGEFILE64_SOURCE -I../interface -I%{_includedir}/httpd -I%{_includedir}/apr-%{aprversion} -fPIC " make )

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?compat}
pushd org.gridsite.core
(cd src && make install prefix=$RPM_BUILD_ROOT%{_usr} libdir=%{_lib} )
rm  $RPM_BUILD_ROOT/%{_libdir}/libgridsite.a
# Do not remove libgridsite_globus because OSG needs it for glite-data-util-c
# rm  $RPM_BUILD_ROOT/%{_libdir}/libgridsite_globus.*
# Remove all most everything from -compat installation package
# since we don't want it.
rm $RPM_BUILD_ROOT%{_libdir}/libgridsite.so
rm $RPM_BUILD_ROOT%{_libdir}/libgridsite.so.1
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_datadir}
rm -rf $RPM_BUILD_ROOT%{_libexecdir}
rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_sbindir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/httpd
popd
%endif
(cd src && make install prefix=$RPM_BUILD_ROOT%{_usr} libdir=%{_lib} )
(cd src && make install-ws prefix=$RPM_BUILD_ROOT%{_usr} libdir=%{_lib} )

# Remove static libs 
rm  $RPM_BUILD_ROOT/%{_libdir}/libgridsite.a
rm  $RPM_BUILD_ROOT/%{_libdir}/libgridsite_globus.a

# Remove docs we don't want now but will move it in %doc later.
rm -rf $RPM_BUILD_ROOT/%{_defaultdocdir} 
# Do not remove libgridsite_globus because OSG needs it for glite-data-util-c
# rm  $RPM_BUILD_ROOT/%{_libdir}/libgridsite_globus.*

# Set up a root area to serve files from.
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/gridsite
install -p -m 0644 gridsitehead.txt $RPM_BUILD_ROOT%{_var}/lib/gridsite/gridsitehead.txt
install -p -m 0644 gridsitefoot.txt $RPM_BUILD_ROOT%{_var}/lib/gridsite/gridsitefoot.txt
install -p -m 0644 root-level.gacl  $RPM_BUILD_ROOT%{_var}/lib/gridsite/.gacl

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/grid-security/dn-lists

mkdir -p $RPM_BUILD_ROOT%{_var}/cache/mod_gridsite
# Copy in apache configuration, we must name it zgridsite.conf
# so it is loaded after mod_ssl in ssl.conf.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 0644 gridsite-httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/zgridsite.conf

# 
mkdir -p $RPM_BUILD_ROOT%{_var}/www/icons
install -p -m 0644 gridsitelogo.png $RPM_BUILD_ROOT%{_var}/www/icons

# These were work arounds for an old bug in some other
# software never ever in Fedora anyway.
rm -f %{buildroot}%{_libdir}/libgridsite_nossl*

# Add an empty /etc/grid-security/vomsdir since this gridsite version
# supports .lsc files.
mkdir -p %{buildroot}%{_sysconfdir}/grid-security/vomsdir

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%if 0%{?compat}
%post compat -p /sbin/ldconfig

%postun compat -p /sbin/ldconfig
%endif

%files 
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/mod_gridsite.so
%dir %{_libexecdir}/gridsite
%dir %{_libexecdir}/gridsite/cgi-bin
%{_libexecdir}/gridsite/cgi-bin/gridsite-copy.cgi 
%{_libexecdir}/gridsite/cgi-bin/gridsite-delegation.cgi 
%{_libexecdir}/gridsite/cgi-bin/gridsite-storage.cgi 
%{_libexecdir}/gridsite/cgi-bin/real-gridsite-admin.cgi 
%{_var}/www/icons/gridsitelogo.png
%dir %attr(0755,apache,apache) %{_var}/lib/gridsite
%dir %attr(0755,root,root) %{_sysconfdir}/grid-security
%dir %attr(0755,apache,apache) %{_sysconfdir}/grid-security/dn-lists
%dir %attr(0755,apache,apache) %{_var}/cache/mod_gridsite
%dir %{_sysconfdir}/grid-security/vomsdir

%{_mandir}/man8/mod_gridsite.8.*
%{_mandir}/man8/gridsite-*.8.*

%config(noreplace) %{_sysconfdir}/httpd/conf.d/zgridsite.conf
%config(noreplace) %attr(-,apache,apache) %{_var}/lib/gridsite/.gacl
%config(noreplace) %attr(-,apache,apache) %{_var}/lib/gridsite/gridsitehead.txt
%config(noreplace) %attr(-,apache,apache) %{_var}/lib/gridsite/gridsitefoot.txt

%doc doc/httpd-fileserver.conf doc/httpd-webserver.conf 
%doc doc/httpd-storage.conf

%doc CHANGES LICENSE

%files gsexec
%defattr(-,root,root,-)
%attr(4754,root,apache) %{_sbindir}/gsexec
%{_mandir}/man8/gsexec.8.*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libgridsite.so.1
%{_libdir}/libgridsite.so.1.7*
%{_libdir}/libgridsite_globus.so.1
%{_libdir}/libgridsite_globus.so.1.7*
%doc LICENSE 

%if 0%{?compat}
%files compat
%defattr(-,root,root,-)
%{_libdir}/libgridsite.so.1.5*
%{_libdir}/libgridsite_globus.so.1.5*
%doc LICENSE
%endif


%files  clients
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/findproxyfile
%attr(0755,root,root) %{_bindir}/htcp
%attr(0755,root,root) %{_bindir}/htfind
%attr(0755,root,root) %{_bindir}/htll
%attr(0755,root,root) %{_bindir}/htls
%attr(0755,root,root) %{_bindir}/htmkdir
%attr(0755,root,root) %{_bindir}/htmv
%attr(0755,root,root) %{_bindir}/htping
%attr(0755,root,root) %{_bindir}/htproxydestroy
%attr(0755,root,root) %{_bindir}/htproxyinfo
%attr(0755,root,root) %{_bindir}/htproxyput
%attr(0755,root,root) %{_bindir}/htproxyrenew
%attr(0755,root,root) %{_bindir}/htproxytime
%attr(0755,root,root) %{_bindir}/htproxyunixtime
%attr(0755,root,root) %{_bindir}/htrm
%attr(0755,root,root) %{_bindir}/urlencode

%{_mandir}/man1/findproxyfile.1.gz
%{_mandir}/man1/htcp.1.gz
%{_mandir}/man1/htfind.1.gz
%{_mandir}/man1/htll.1.gz
%{_mandir}/man1/htls.1.gz
%{_mandir}/man1/htmkdir.1.gz
%{_mandir}/man1/htmv.1.gz
%{_mandir}/man1/htping.1.gz
%{_mandir}/man1/htproxydestroy.1.gz
%{_mandir}/man1/htproxyinfo.1.gz
%{_mandir}/man1/htproxyput.1.gz
%{_mandir}/man1/htproxyrenew.1.gz
%{_mandir}/man1/htproxytime.1.gz
%{_mandir}/man1/htproxyunixtime.1.gz
%{_mandir}/man1/htrm.1.gz
%{_mandir}/man1/urlencode.1.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/gridsite-gacl.h
%{_includedir}/gridsite.h
%{_libdir}/libgridsite.so
%{_libdir}/libgridsite_globus.so
%{_libdir}/pkgconfig/gridsite-openssl.pc

%files doc
%defattr(-,root,root,-)
%doc src/doxygen LICENSE

%changelog
* Thu Jan 31 2013 Matyas Selmeci <matyas@cs.wisc.edu> 1.7.25-1.1
- Upstream 1.7.25
- Removed gridsite-cred-segfault.patch, proxy_path_length.patch, now in upstream

* Thu Jan 31 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 1.7.21-4.1
- Merge EPEL 1.7.21-4:

    * Thu Sep 13 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 1.7.21-4
    - Added patch for segfault under high load

    * Thu Jul 19 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 1.7.21-3
    - Up release of compat package

    * Mon Jul 16 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 1.7.21-2
    - Rebuild with proper tarballs

    * Mon Jul 16 2012 Ricardo Rocha <ricardo.rocha@cern.ch> - 1.7.21-1
    - Upstream to 1.7.21, compliance with EMI project gridsite packaging
    - Removed unused patches

    * Sun Mar 18 2012 Steve Traylen <steve.traylen@cern.ch>  - 1.7.19-1
    - Upstream 1.7.19
    - Drop EPEL4 support since EOL.
    - Requires httpd-mmn, rhbz#803062

    * Wed Jul 6 2011 Steve Traylen <steve.traylen@cern.ch>  - 1.7.15-4
    - devel package require openssl devel rhbz#719174

* Mon Oct 29 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 1.7.15-4.6
- Allow gridsite to handle CAs with path constraints.
- Multiple version bumps to handle issues with NVRA uniqueness for the campat package.

* Mon Oct 31 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.7.15-4.3
- also needed to bump release of compat package

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.7.15-4.2
- rebuilt

* Sun Jul 3 2011 Brian Bockelman <bbockelm@cse.unl.edu>  - 1.7.15-3
- Add back libgridsite_globus.so, as they are needed by glite-data-util-c
- Add dependency on openssl-devel for gridsite-devel.

* Sun Jul 3 2011 Steve Traylen <steve.traylen@cern.ch>  - 1.7.15-2 2
- Release of compat package must also be increased.

* Sun Jul 3 2011 Steve Traylen <steve.traylen@cern.ch>  - 1.7.15-2 1
- Correct dependency mistake.

* Thu Jun 30 2011 Steve Traylen <steve.traylen@cern.ch>  - 1.7.15-2
- Add a gridsite-compat-1.5 package on EPEL4 & EPEL5.
- Remove doc package requiring devel package.

* Thu Jun 30 2011 Steve Traylen <steve.traylen@cern.ch>  - 1.7.15-1
- Upstream 1.7.15, drop gridsite-include-1.7.9.patch since upstream,
  redo cgi-location patch.

* Mon Jun 27 2011 Steve Traylen <steve.traylen@cern.ch>  - 1.7.13-1
- Upstream 1.7.13

* Wed Apr 6 2011 Steve Traylen <steve.traylen@cern.ch>  - 1.7.12-1
- Upstream 1.7.12

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Steve Traylen <steve.traylen@cern.ch>  - 1.7.9-1
- Add empty /etc/grid-security/vomsdir since this gridsite
  support .lsc files.
- Upstream to 1.7.9
- Update gridsite-include.patch for 1.7.9
  https://savannah.cern.ch/bugs/index.php?69632

* Wed Sep 29 2010 jkeating - 1.5.19-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Steve Traylen <steve.traylen@cern.ch> - 1.5.19-1
- Upstream to 1.5.19.
- Add gridsite-include.patch 
  https://savannah.cern.ch/bugs/index.php?69632 
  https://bugzilla.redhat.com/show_bug.cgi?id=612109
- Alter default .gacl
  https://bugzilla.redhat.com/show_bug.cgi?id=612187
- Change setuid binary from 4510 to 4754

* Thu May 20 2010 Steve Traylen <steve.traylen@cern.ch> - 1.5.18-4
- For .el4 use /usr/include/apr-0 rather than apr-1

* Wed May 19 2010 Steve Traylen <steve.traylen@cern.ch> - 1.5.18-3
- Don't use _sharedstatedir macro for .el4,5 support.

* Wed May 19 2010 Steve Traylen <steve.traylen@cern.ch> - 1.5.18-2
- Split docs of to a seperate package.
- License corrected to ASL 2.0 and BSD

* Mon May 17 2010 Steve Traylen <steve.traylen@cern.ch> - 1.5.18-1
- Initial package.


