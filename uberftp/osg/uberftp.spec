# $ git rev-parse  Version_2_8
# 012788f5430c9f7eb03e65b7aa8bcb106f472518

%global commit 012788f5430c9f7eb03e65b7aa8bcb106f472518
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           uberftp
Version:        2.8
Release:        2.1%{?dist}
Summary:        GridFTP-enabled ftp client

Group:          Applications/Internet

License:        NCSA
URL:            https://github.com/JasonAlt/UberFTP
Source0:        https://github.com/JasonAlt/UberFTP/archive/%{commit}/UberFTP-%{commit}.tar.gz
# https://github.com/JasonAlt/UberFTP/pull/6
Patch0:         uberftp-32bit-pkg-config.patch
Patch1:         disconnected_server.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  globus-gssapi-gsi-devel

%description
UberFTP is the first interactive, GridFTP-enabled ftp client. 
It supports GSI authentication, parallel data channels and 
third party transfers. 

%prep
%setup -q -n UberFTP-%{commit}
iconv -f iso8859-1 -t utf-8 copyright > copyright.conv && mv -f copyright.conv copyright
touch -r configure.ac x
%patch0 -p1
%patch1 -p0
touch -r x configure.ac

%build
%configure --with-globus=%{_usr}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/uberftp
%{_mandir}/man1/uberftp.1*
%doc Changelog.mssftp Changelog copyright

%changelog
* Thu Mar 05 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 2.8-2.1.osg
- Merge OSG changes

* Mon Sep 29 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.8-2
- Adapt to Globus Toolkit 6.0

* Tue Sep 2 2014 Steve Traylen <steve.traylen@cern.ch> - 2.8-1
- Upstream to 2.8, upstream has moved to github.
- Add patch for 32 bit.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 2.6-4.osg
- Prevent uberftp from hanging when the command socket closes

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 2 2012 Steve Traylen <steve.traylen@cern.ch> - 2.6-4
- Adapt for globus toolkit 5.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 Steve Traylen <steve.traylen@cern.ch> - 2.6-1
- Update to uberftp-2.6

* Fri Sep 11 2009 Steve Traylen <steve.traylen@cern.ch> - 2.5-1
- Update to uberftp-2.5

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.4-5
- rebuilt with new openssl

* Wed Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> 2.4-4
- Update source to version 2.4
- Include copyright file in package.

* Tue Jun 23 2009 Steve Traylen <steve.traylen@cern.ch> 2.3-3
- Better inclusion of globus header files.
* Fri Jun 19 2009 Steve Traylen <steve@traylen.net> -  2.3-2
- Remove my debugging.
* Fri Jun 19 2009 Steve Traylen <steve@traylen.net> -  2.3-1
- Initial version.


