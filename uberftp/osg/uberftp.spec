Name:           uberftp
Version:        2.6
Release:        1%{?dist}
Summary:        GridFTP-enabled ftp client

Group:          Applications/Internet

License:        NCSA
URL:            http://dims.ncsa.illinois.edu/set/uberftp/
Source0:        http://dims.ncsa.illinois.edu/set/uberftp/download/uberftp-client-%{version}.tar.gz
Patch0:         configure.ac.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  grid-packaging-tools, globus-gssapi-gsi-devel

%description
UberFTP is the first interactive, GridFTP-enabled ftp client. 
It supports GSI authentication, parallel data channels and 
third party transfers. 

%prep
%setup -q -n uberftp-client-%{version}
iconv -f iso8859-1 -t utf-8 copyright > copyright.conv && mv -f copyright.conv copyright
%patch0 -p0

%build
mkdir pkgdata
ln pkg_data_src.gpt.in pkgdata/pkg_data_src.gpt.in

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


