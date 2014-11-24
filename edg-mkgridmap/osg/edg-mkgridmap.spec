Name:           edg-mkgridmap
Version:        4.0.0
Release:        8%{?dist}
Summary:        Contains the init.d script and crontab for edg-mkgridmap

Group:          system environment/base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Source0:        %{name}-%{version}.tar.gz
Source1:        edg-mkgridmap
Source2:        edg-mkgridmap-cron

Patch0:         edg-mkgridmap-wrapper-osg.patch
Patch1:         use-net-ssl.patch
Patch2:         skip_blank_entries.patch	

# Steps to make tarball (correctly packaged):
# Get GOC's tarball, edg-mkgridmap-10.tar.gz
# tar xzf edg-mkgridmap-4.0.0.tar.gz
# cp edg-mkgridmap ./
# cp edg-mkgridmap-cron ./

Requires:       osg-edg-mkgridmap-config
Requires:       osg-vo-map

Requires:       perl-libwww-perl
Requires:       perl-Net-SSLeay
Requires:       perl-Crypt-SSLeay

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts

%description
%{summary}

%prep

%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%build


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/
mkdir -p $RPM_BUILD_ROOT/%{_var}/lib/osg
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/edg-mkgridmap
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/edg-mkgridmap-cron

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add edg-mkgridmap

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service edg-mkgridmap stop >/dev/null 2>&1
    /sbin/chkconfig --del edg-mkgridmap
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service edg-mkgridmap condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_sysconfdir}/rc.d/init.d/edg-mkgridmap
%{_sysconfdir}/cron.d/edg-mkgridmap-cron
%docdir %{_defaultdocdir}/%{name}
%docdir %{_mandir}/man5
%docdir %{_mandir}/man8
%{_libexecdir}/edg-mkgridmap
%{_libexecdir}/edg-mkgridmap/edg-mkgridmap.pl
%{_sbindir}/edg-mkgridmap
%{_defaultdocdir}/%{name}
%{_defaultdocdir}/%{name}/AUTHORS
%{_defaultdocdir}/%{name}/LICENSE
%{_defaultdocdir}/%{name}/MAINTAINERS
%{_mandir}/man5/edg-mkgridmap.conf.5*
%{_mandir}/man8/edg-mkgridmap.8*
%dir %{_var}/lib/osg

%changelog
* Mon Nov 24 2014 Brian Lin <blin@cs.wisc.edu> - 4.0.0-8
- Handle blank entries in edg-mkgridmap (SOFTWARE-1698)

* Tue May 27 2014 Carl Edquist <edquist@cs.wisc.edu> - 4.0.0-7
- use Net::SSL module in edg-mkgridmap.pl (SOFTWARE-1489)

* Thu Oct 17 2013 Carl Edquist <edquist@cs.wisc.edu> - 4.0.0-6
- Provide missing /var/lib/osg dir (SOFTWARE-495)

* Thu Mar 22 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 4.0.0-5
- Require osg-edg-mkgridmap-config instead of vo-client-edgmkgridmap

* Fri Dec 02 2011 Alain Roy <roy@cs.wisc.edu> - 4.0.0-3
- Fix logging to be more clear.

* Thu Aug 11 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 4.0.0-3
- Create VO map when edg-mkgridmap is run.
- Correct the runtime requirements.
- Properly register with chkconfig.

* Fri Jul 22 2011 Neha Sharma <neha@fnal.gov> - 400-2
- Included a patch for wrapper script to redirect stdout and stderr properly

* Thu Jul 21 2011 Neha Sharma <neha@fnal.gov> - 400-1
- Initial build of edg-mkgridmap cron and init.d package


