
Summary: GridFTP client commands
Name: edg-gridftp-client
Version: 1.2.9.2
Release: 3%{?dist}
URL: http://www.edg.org/

# Retrieved on Jul 3 2011
# http://glite.cvs.cern.ch/cgi-bin/glite.cgi/edg-gridftp-client.tar.gz?view=tar&pathrev=v1_2_9_2
Source: %{name}.tar.gz
Patch0: globus_flavor_fix.patch

License: European DataGrid License
Group: Applications/File
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: globus-common-devel
BuildRequires: globus-ftp-client-devel
BuildRequires: globus-xio-devel
BuildRequires: globus-gssapi-error-devel

%description
The edg-gridftp-client package is a thin command line interface on top
of the GridFTP libraries supplied by Globus.  They provide a useful
set of commands to do basic management of files on a GridFTP server.

%prep
%setup -q -n %{name}
%patch0 -p0

%build
./autogen.sh
CFLAGS="${CFLAGS:-%optflags} -I/usr/include/globus -I%{_libdir}/globus/include" ; export CFLAGS ;
%configure

make %{?smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/edg-gridftp-exists
%{_bindir}/edg-gridftp-mkdir
%{_bindir}/edg-gridftp-rmdir
%{_bindir}/edg-gridftp-rm
%{_bindir}/edg-gridftp-ls
%{_bindir}/edg-gridftp-rename
%{_libexecdir}/edg-gridftp-base-exists
%{_libexecdir}/edg-gridftp-base-ls
%{_libexecdir}/edg-gridftp-base-mkdir
%{_libexecdir}/edg-gridftp-base-rename
%{_libexecdir}/edg-gridftp-base-rm
%{_libexecdir}/edg-gridftp-base-rmdir
%{_mandir}/man1/edg-gridftp-exists.1.gz
%{_mandir}/man1/edg-gridftp-mkdir.1.gz
%{_mandir}/man1/edg-gridftp-rmdir.1.gz
%{_mandir}/man1/edg-gridftp-rm.1.gz
%{_mandir}/man1/edg-gridftp-ls.1.gz
%{_mandir}/man1/edg-gridftp-rename.1.gz
%doc %{_docdir}/%{name}-%{version}/LICENSE
%doc %{_docdir}/%{name}-%{version}/README

%changelog
* Fri Oct 28 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9.2-3
- rebuilt

* Mon Sep 12 2011 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.9.2-2
- Rebuilt against updated Globus libraries

* Sun Jul  3 2011 Brian Bockelman <bbockelm@cse.unl.edu> 1.2.9.2-1
- Pull to latest upstream.
- Tweaked the RPM so it can be built from a CVS tarball.

* Fri May 27 2011 Derek Weitzel <dweitzel@cse.unl.edu> 1.0-1
- Initial build of edg-gridftp-client

