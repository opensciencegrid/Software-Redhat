%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-ftp-control
%global _name %(tr - _ <<< %{name})
Version:	6.6
Release:	1.1%{?dist}
Summary:	Globus Toolkit - GridFTP Control Library

Group:		System Environment/Libraries
License:	ASL 2.0
URL:		http://www.globus.org/
Source:		http://www.globus.org/ftppub/gt6/packages/%{_name}-%{version}.tar.gz
#		README file
Source8:	GLOBUS-GRIDFTP
Patch0:         level-out-connection-speeds.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	globus-common-devel >= 15
BuildRequires:	globus-gss-assist-devel >= 8
BuildRequires:	globus-gssapi-gsi-devel >= 9
BuildRequires:	globus-io-devel >= 11
BuildRequires:	globus-xio-devel >= 3
BuildRequires:	globus-gssapi-error-devel >= 4
BuildRequires:	doxygen
#		Additional requirements for make check
BuildRequires:	openssl
Requires:	globus-io%{?_isa} >= 11

%package devel
Summary:	Globus Toolkit - GridFTP Control Library Development Files
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	globus-common-devel%{?_isa} >= 15
Requires:	globus-gss-assist-devel%{?_isa} >= 8
Requires:	globus-gssapi-gsi-devel%{?_isa} >= 9
Requires:	globus-io-devel%{?_isa} >= 11
Requires:	globus-xio-devel%{?_isa} >= 3
Requires:	globus-gssapi-error-devel%{?_isa} >= 4

%package doc
Summary:	Globus Toolkit - GridFTP Control Library Documentation Files
Group:		Documentation
%if %{?fedora}%{!?fedora:0} >= 10 || %{?rhel}%{!?rhel:0} >= 6
BuildArch:	noarch
%endif

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
GridFTP Control Library

%description devel
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-devel package contains:
GridFTP Control Library Development Files

%description doc
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name}-doc package contains:
GridFTP Control Library Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%patch0 -p 0

%build
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

%configure --disable-static \
	   --includedir='${prefix}/include/globus' \
	   --libexecdir='${datadir}/globus' \
	   --docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC \(.*-shared\) !CC \\\${wl}--as-needed \1 !' -i libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Remove license file from pkgdocdir if licensedir is used
%{?_licensedir: rm %{buildroot}%{_pkgdocdir}/GLOBUS_LICENSE}

%check
GLOBUS_HOSTNAME=localhost make %{?_smp_mflags} check VERBOSE=1

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libglobus_ftp_control.so.*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%files devel
%{_includedir}/globus/*
%{_libdir}/libglobus_ftp_control.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%changelog
* Mon Feb 16 2015 Matyas Selmeci <matyas@cs.wisc.edu> - 6.6-1.1
- Merge OSG changes
- Drop ip-logging-bug.patch (fixed upstream)

* Fri Jan 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.6-1
- Implement updated license packaging guidelines
- GT6 update (test fixes, missing return value)
- Set GLOBUS_HOSTNAME during make check

* Thu Nov 13 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.3-1
- GT6 update
- Drop patches globus-ftp-control-memleak.patch and
  globus-ftp-control-tests-localhost.patch (fixed upstream)

* Sun Oct 26 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.12-1
- GT6 update
- Drop patch globus-ftp-control-doxygen.patch (fixed upstream)

* Tue Sep 30 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.11-2
- Fix memory leak

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.11-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata
- Enable checks

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 01 2014 Edgar Fajardo <efajardo@physics.ucsd.edu> - 4.7-1.2
- Added the Ip logging patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Brent Baude <baude@us.ibm.com> - 4.7-2
- Replace arch def of ppc64 with power64 macro for ppc64le enablement

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.7-1
- Update to Globus Toolkit 5.2.5
- Drop patch globus-ftp-control-authinfo.patch (fixed upstream)
- Remove obsolete workaround for broken RHEL 5 epstopdf

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.5-4
- Implement updated packaging guidelines

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.5-3
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.5-2
- Fix modification to wrong authinfo object

* Wed Feb 20 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.5-1
- Update to Globus Toolkit 5.2.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.4-3
- Add build requires for TexLive 2012

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.4-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-ftp-control-deps.patch (fixed upstream)

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-2
- Fix broken links in README file

* Wed Dec 14 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 4.2-1
- Update to Globus Toolkit 5.2.0
- Drop patches globus-ftp-control-backcompat.patch,
  globus-ftp-control-doxygen.patch, globus-ftp-control-format.patch and
  globus-ftp-control-type-punned-pointer.patch (fixed upstream)

* Sun Dec 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.2-5
- Fix for connection speed leveling on servers with different buffer sizes.

* Wed Nov 16 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.2-4
- Auto-level the connection speed of each TCP connection.

* Thu Jun 23 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.12-2
- Fix backward incompatibility

* Fri Jun 03 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.12-1
- Update to Globus Toolkit 5.0.4

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.11-3
- Add README file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.11-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Thu Jun 04 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.3
- Adapt to updated GPT package

* Mon Oct 20 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.10-0.2
- Update to Globus Toolkit 4.2.1

* Tue Jul 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.8-0.1
- Autogenerated
