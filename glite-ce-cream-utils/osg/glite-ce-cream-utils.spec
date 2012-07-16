Summary: Tools and utilities for the CREAM service
Name: glite-ce-cream-utils
Version: 1.2.0
%global upstream_release 4
Release: %{upstream_release}.3%{?dist}
License: Apache Software License
Vendor: EMI
URL: http://glite.cern.ch/
Group: System Environment/Libraries
BuildRequires: libtool, docbook-style-xsl, libxslt
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv: yes
Source5: %{name}-%{version}-%{upstream_release}.sl5.tar.gz
Source6: %{name}-%{version}-%{upstream_release}.sl6.tar.gz

%global debug_package %{nil}

%description
This package contains a set of executables called by the CREAM service

%prep
 
%setup -c -q -T -b %{rhel}

%build
%{!?extbuilddir:%define extbuilddir "--"}
if test "x%{extbuilddir}" == "x--" ; then
  ./configure --prefix=%{buildroot}/usr --sysconfdir=%{buildroot}/etc --disable-static PVER=%{version}
  make
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
strip -s %{buildroot}/usr/bin/glite-ce-cream-purge-proxy
strip -s %{buildroot}/usr/bin/glite-cream-createsandboxdir
strip -s %{buildroot}/usr/bin/glite-ce-cream-purge-sandbox
strip -s %{buildroot}/usr/bin/glite-ce-cream-create-wrapper

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir /etc/glite-ce-glue2/
%config(noreplace) /etc/glite-ce-glue2/glite-ce-glue2.conf.template
%dir /etc/glite-ce-dbtool
%config(noreplace) /etc/glite-ce-dbtool/creamdb_min_access.conf.template
%dir /etc/glite-ce-cream-utils
%config(noreplace) /etc/glite-ce-cream-utils/glite_cream_load_monitor.conf
/usr/libexec/glite-ce-glue2-*
/usr/libexec/glite-ce-check-submission-state
/usr/bin/glite-ce-cream-purge-proxy
/usr/bin/glite-cream-createsandboxdir
/usr/bin/glite-ce-cream-purge-sandbox
/usr/bin/glite-cream-copyProxyToSandboxDir.sh
/usr/bin/createAndPopulateDB.sh
/usr/bin/glite_cream_load_monitor
/usr/bin/glite-cream-purger.sh
/usr/bin/glite-ce-cream-create-wrapper
%attr(750,root,root) /usr/sbin/JobDBAdminPurger.sh

%dir /usr/share/doc/%{name}-%{version}/
%doc /usr/share/doc/%{name}-%{version}/LICENSE
%doc /usr/share/man/man1/*.1.gz


%post
if [ $1 -eq 1 ] ; then
  if [ ! "x`grep tomcat /etc/passwd`" == "x" ] ; then
    chown tomcat.tomcat /usr/bin/glite_cream_load_monitor 
  fi
fi

%changelog
* Mon Jul 16 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.0-4.3.osg
- Include both el5 and el6 tarball in srpm

* Tue Jun 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.0-4.2.osg
- Removed BuildArch line

* Tue Jun 26 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1.2.0-4.1.osg
- Rebuilt for OSG

* Wed May 16 2012 CREAM group <cream-support@lists.infn.it> - 1.2.0-4.sl5
- Major bugs fixed

