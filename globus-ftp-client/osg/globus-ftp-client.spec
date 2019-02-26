%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		globus-ftp-client
%global _name %(tr - _ <<< %{name})
Version:	9.1
Release:	2.1%{?dist}
Summary:	Grid Community Toolkit - GridFTP Client Library

License:	ASL 2.0
URL:		https://github.com/gridcf/gct/
Source:		https://repo.gridcf.org/gct6/sources/%{_name}-%{version}.tar.gz
Source8:	README

BuildRequires:	gcc
BuildRequires:	globus-common-devel >= 15
BuildRequires:	globus-ftp-control-devel >= 4
BuildRequires:	globus-gsi-callback-devel >= 4
BuildRequires:	globus-gsi-credential-devel >= 5
BuildRequires:	globus-gsi-sysconfig-devel >= 5
BuildRequires:	globus-gssapi-gsi-devel >= 10
BuildRequires:	globus-xio-devel >= 3
BuildRequires:	globus-xio-popen-driver-devel >= 2
BuildRequires:	openssl-devel
BuildRequires:	doxygen
#		Additional requirements for make check
BuildRequires:	globus-gridftp-server-devel >= 7
BuildRequires:	globus-gridftp-server-progs >= 7
BuildRequires:	openssl
BuildRequires:	perl(Test::More)

Requires:	globus-xio-popen-driver%{?_isa} >= 2

%package devel
Summary:	Grid Community Toolkit - GridFTP Client Library Development Files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%package doc
Summary:	Grid Community Toolkit - GridFTP Client Library Documentation Files
BuildArch:	noarch

%description
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name} package contains:
GridFTP Client Library

%description devel
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-devel package contains:
GridFTP Client Library Development Files

%description doc
The Grid Community Toolkit (GCT) is an open source software toolkit used for
building grid systems and applications. It is a fork of the Globus Toolkit
originally created by the Globus Alliance. It is supported by the Grid
Community Forum (GridCF) that provides community-based support for core
software packages in grid computing.

The %{name}-doc package contains:
GridFTP Client Library Documentation Files

%prep
%setup -q -n %{_name}-%{version}

%build
# Reduce overlinking
export LDFLAGS="-Wl,--as-needed -Wl,-z,defs %{?__global_ldflags}"

export GLOBUS_VERSION=6.2
%configure --disable-static \
	   --includedir=%{_includedir}/globus \
	   --libexecdir=%{_datadir}/globus \
	   --docdir=%{_pkgdocdir}

# Reduce overlinking
sed 's!CC \(.*-shared\) !CC \\\${wl}--as-needed \1 !' -i libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove libtool archives (.la files)
rm %{buildroot}%{_libdir}/*.la

# Install README file
install -m 644 -p %{SOURCE8} %{buildroot}%{_pkgdocdir}/README

# Remove license file from pkgdocdir if licensedir is used
%{?_licensedir: rm %{buildroot}%{_pkgdocdir}/GLOBUS_LICENSE}

%check
if grep -q @SSH_BIN@ %{buildroot}%{_datadir}/globus/gridftp-ssh; then
    echo @SSH_BIN@ unexpanded
    exit 1
fi
GLOBUS_HOSTNAME=localhost make %{?_smp_mflags} check VERBOSE=1

%ldconfig_scriptlets

%files
%{_libdir}/libglobus_ftp_client.so.*
%dir %{_datadir}/globus
%{_datadir}/globus/gridftp-ssh
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%files devel
%{_includedir}/globus/*
%{_libdir}/libglobus_ftp_client.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%doc %{_mandir}/man3/*
%dir %{_pkgdocdir}
%dir %{_pkgdocdir}/html
%doc %{_pkgdocdir}/html/*
%{!?_licensedir: %doc %{_pkgdocdir}/GLOBUS_LICENSE}
%{?_licensedir: %license GLOBUS_LICENSE}

%changelog
* Tue Feb 26 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 9.1-2.1
- Merge OSG changes (SOFTWARE-3586)

* Fri Nov 16 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.1-2
- Bump GCT release version to 6.2

* Thu Sep 13 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.1-1
- Switch upstream to Grid Community Toolkit
- First Grid Community Toolkit release (9.0)
- Use 2048 bit RSA key for tests (9.1)

* Sat Sep 01 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.37-1
- GT6 update: Use 2048 bit keys to support openssl 1.1.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 04 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.36-1
- GT6 update: Replace deprecated perl POSIX::tmpnam with File::Temp::tmpnam
- Drop patch globus-ftp-client-perl-posix.patch (accepted upstream)

* Sun Jun 25 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.35-2
- Adapt to Perl 5.26 - POSIX::tmpnam() no longer available

* Thu Jun 22 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.35-1
- GT6 update: Remove some redundant tests to reduce test time

* Mon Mar 27 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.34-2
- EPEL 5 End-Of-Life specfile clean-up
  - Remove Group and BuildRoot tags
  - Remove _pkgdocdir macro definition
  - Drop redundant Requires corresponding to autogenerated pkgconfig Requires
  - Don't clear the buildroot in the install section
  - Remove the clean section
  - Drop the globus-ftp-client-openssl098.patch

* Fri Mar 17 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.34-1
- GT6 update: Add FTP_TEST_RESTART_AFTER_RANGE=n to force restarts after n
  range markers for restart points 22 and 24 (RETR_RESPONSE and STOR_RESPONSE)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.33-1
- GT6 update

* Thu Oct 13 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.32-2
- Rebuild for openssl 1.1.0 (Fedora 26)

* Thu Sep 01 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.32-1
- GT6 update: Updates for OpenSSL 1.1.0

* Mon Aug 08 2016 Matyas Selmeci <matyas@cs.wisc.edu> - 8.29-1.1
- Merge OSG changes (SOFTWARE-2197)

* Fri May 06 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.29-1
- GT6 update: Don't overwrite LDFLAGS - Fix for regression in 8.28

* Mon May 02 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.28-1
- GT6 update

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.27-2
- Extra rebuild for EPEL 7 ppc64le

* Wed Nov 25 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.27-1
- GT6 update
  - Prevent endless loop when auto-retrying failed pasv on other server (8.27)
  - Disable mandatory IPv6 in tests (8.26)

* Tue Oct 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.25-1
- GT6 update (upstream's release of the fix for GT-604)
- Drop patch globus-ftp-client-ipv6.patch (fixed upstream)

* Sun Oct 25 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.23-2
- Fix for GT-604: fix ipv6 negotiation when source does not pre-connect
  (backported from upstream git)

* Mon Jul 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.23-1
- GT6 update (Fix crash in error handling)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.22-1
- GT6 update (test improvements)

* Fri Mar 27 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.21-1
- GT6 update (undefined configure macro in gridftp-ssh)

* Wed Mar 25 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 8.19-1.2.osg
- Fix @SSH_BIN@ in gridftp-ssh script (SOFTWARE-1853)

* Fri Mar 13 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 8.19-1.1.osg
- Disable checks because they hang

* Fri Mar 06 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.20-1
- GT6 update (upstream's release of previous fix)

* Thu Mar 05 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.19-2
- Improved fix for GGUS 109089/109576 (from upstream git)

* Tue Feb 17 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.19-1
- GT6 update (GGUS 105158 and 109089/109576)

* Fri Jan 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.17-2
- Implement updated license packaging guidelines
- Set GLOBUS_HOSTNAME during make check and enable tests on EPEL5 and EPEL6

* Fri Dec 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.17-1
- GT6 update

* Thu Nov 13 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.16-1
- GT6 update
- Drop patch globus-ftp-client-undef-macro.patch (fixed upstream)

* Sun Oct 26 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.13-1
- GT6 update
- Drop patches globus-ftp-client-doxygen.patch and globus-ftp-client-deps.patch
  (fixed upstream)

* Fri Sep 12 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 8.12-1
- Update to Globus Toolkit 6.0
- Drop GPT build system and GPT packaging metadata
- Enable checks
- Disable checks on EPEL5 and EPEL6

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Brent Baude <baude@us.ibm.com> - 7.6-2
- Replace arch def of ppc64 with power64 macro for ppc64le enablement

* Thu Nov 07 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.6-1
- Update to Globus Toolkit 5.2.5
- Remove obsolete workaround for broken RHEL 5 epstopdf

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.4-5
- Implement updated packaging guidelines

* Tue May 21 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.4-4
- Add aarch64 to the list of 64 bit platforms

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.4-2
- Add build requires for TexLive 2012

* Sun Jul 22 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.4-1
- Update to Globus Toolkit 5.2.2
- Drop patch globus-ftp-client-v2def.patch (obsolete - gridftp v2 now default)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.3-1
- Update to Globus Toolkit 5.2.1
- Drop patch globus-ftp-client-deps.patch (fixed upstream)

* Fri Apr 27 2012 Emmanouil Paisios <paisios@lrz.de> - 7.2-3
- Added patch from VDT for enabling gridftp v2 via the environment variable
  GLOBUS_FTP_CLIENT_GRIDFTP2.
  See https://ggus.eu/tech/ticket_show.php?ticket=81230 for details.

* Tue Jan 24 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.2-2
- Fix broken links in README file

* Wed Dec 14 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 7.2-1
- Update to Globus Toolkit 5.2.0
- Drop patches globus-ftp-client-doxygen.patch, globus-ftp-client-format.patch
  and globus-ftp-client-type-punned-pointer.patch (fixed upstream)

* Mon Apr 25 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.0-2
- Add README file

* Thu Feb 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 6.0-1
- Update to Globus Toolkit 5.0.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-2
- Update to Globus Toolkit 5.0.2

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.3-1
- Update to Globus Toolkit 5.0.1

* Sat Jan 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.2-1
- Update to Globus Toolkit 5.0.0

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-3
- Add instruction set architecture (isa) tags
- Make doc subpackage noarch

* Thu Jun 04 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.4
- Add s390x to the list of 64 bit platforms

* Thu Jan 01 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.3
- Adapt to updated GPT package

* Tue Oct 21 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.14-0.2
- Update to Globus Toolkit 4.2.1

* Tue Jul 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.11-0.1
- Autogenerated
