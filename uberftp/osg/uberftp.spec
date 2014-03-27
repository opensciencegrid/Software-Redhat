Name:           uberftp
Version:        2.8
%global _version %(tr . _ <<< %{version})
Release:        1%{?dist}
Summary:        GridFTP-enabled FTP client

Group:          Applications/Internet

License:        NCSA
URL:            https://github.com/JasonAlt/UberFTP
Source0:        UberFTP-Version_%{_version}.tar.gz
Patch1:         disconnected_server.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  grid-packaging-tools, globus-gssapi-gsi-devel

%description
UberFTP is the first interactive, GridFTP-enabled ftp client.
It supports GSI authentication, parallel data channels and
third party transfers.

%prep
%setup -q -n UberFTP-Version_%{_version}
iconv -f iso8859-1 -t utf-8 copyright > copyright.conv && mv -f copyright.conv copyright
%patch1 -p0

%build
mkdir pkgdata
ln pkg_data_src.gpt.in pkgdata/pkg_data_src.gpt.in

# lib64 is hardcoded in configure.ac -- fix it for 32-bit builds before running globus-bootstrap.sh
%ifarch i386
sed -i -e 's/lib64/lib/g' configure.ac
%endif
unset GLOBUS_LOCATION GPT_LOCATION
%{_datadir}/globus/globus-bootstrap.sh

%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/uberftp
%{_mandir}/man1/uberftp.1.gz
%doc Changelog.mssftp Changelog copyright

%changelog
* Wed Mar 26 2014 Mátyás Selmeci <matyas@cs.wisc.edu> 2.8-1
- New version 2.8 (SOFTWARE-1436)
- Changed URL to GitHub
- Remove configure.ac.patch (no longer needed)
- Refresh disconnected_server.patch

* Fri Jan 04 2013 Brian Bockelman <bbockelm@cse.unl.edu> - 2.6-4
- Prevent uberftp from hanging when the command socket closes.

* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.6-3
- rebuilt

* Tue Sep 13 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 2.6-2
- Rebuilt against updated Globus libraries

* Sun Sep 5 2011 Alain Roy <roy@cs.wisc.edu> 2.6-1
- Updated source to version 2.6
- Changed to build against Globus 5.2
* Wed Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> 2.4-4
- Update source to version 2.4
- Include copyright file in package.
* Tue Jun 23 2009 Steve Traylen <steve.traylen@cern.ch> 2.3-3
- Better inclusion of globus header files.
* Fri Jun 19 2009 Steve Traylen <steve@traylen.net> -  2.3-2
- Remove my debugging.
* Fri Jun 19 2009 Steve Traylen <steve@traylen.net> -  2.3-1
- Initial version.


