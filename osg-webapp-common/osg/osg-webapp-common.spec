Name:           osg-webapp-common
Version:        1
Release:        2%{?dist}
Summary:        Common files to be used for tomcat webapps.

Group:          System Environment/Base
License:        Apache 2.0
URL:            http://www.opensciencegrid.org/osg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%if 0%{?el5}
Requires:       tomcat5
%global         webappsdir %{_datadir}/tomcat5/webapps/ROOT/
%endif
%if 0%{?el6}
Requires:       tomcat6
%global         webappsdir %{_datadir}/tomcat6/webapps/ROOT/
%endif
%if 0%{?el7}
Requires:       tomcat
%global         webappsdir %{_datadir}/tomcat/webapps/ROOT/
%endif

Source0:        robots.txt

%description
%{summary}
Currently contains a robots.txt file that disallows crawlers from hitting
webapps.

%prep

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{webappsdir}
cp %{SOURCE0} $RPM_BUILD_ROOT%{webappsdir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %{webappsdir}/robots.txt

%changelog
* Fri Jun 19 2015 Jose Caballero <jcaballero@bnl.gov> - 1.2
- added support for Tomcat7 on EL7

* Fri May 25 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 1-1
- Created.

