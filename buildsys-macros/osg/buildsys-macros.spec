%define dver %{?rhel}%{?!rhel:5}
%define osgver up
Name:		buildsys-macros
Summary:	Macros for the OSG Buildsystem
Version:        7
Release:	5%{?dist}
License:	GPL
Group:		Development/Buildsystem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:	rpmdevtools

%description
Macros for the OSG Buildsystem

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
DVER=%{dver}
OSGVER=%{osgver}
printf %s%b "%" "rhel $DVER\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "dist .osg$OSGVER.el$DVER\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "el$DVER 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "osg 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "__arch_install_post /usr/lib/rpm/check-buildroot\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.checkbuild
if [[ $DVER -eq 5 ]]; then
    printf %s%b "%" "_source_filedigest_algorithm 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.digest
    printf %s%b "%" "_binary_filedigest_algorithm 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.digest
    printf %s%b "%" "_binary_payload w9.gzdio\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.digest
    printf %s%b "%" "_source_payload w9.gzdio\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.digest
    printf %s%b "%" "_default_patch_fuzz 2\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.digest
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%if %{dver} == 5
/etc/rpm/macros.digest
%endif
/etc/rpm/macros.disttag
/etc/rpm/macros.checkbuild

%changelog
* Wed Oct 30 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 7-5
- Bump to rebuild with buildsys-macros 7-4

* Wed Oct 30 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 7-4
- Create upcoming version of buildsys-macros

* Tue Oct 29 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 7-2
- Bump to rebuild with buildsys-macros 7-1

* Tue Oct 29 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 7-1
- Add osg major version to dist tag (e.g. .osg32.el5)
- No longer base Version on the %%rhel macro

* Fri Aug 09 2013 Matyas Selmeci <matyas@cs.wisc.edu> - 6-8
- Added 'osg' macro that's 1 for all osg builds

* Wed Jan 18 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 6-7.osg
- Added rhel6 version

* Thu Aug 04 2011 Brian Bockelman <bbockelm@cse.unl.edu> - 5-6.osg
- Creation of the OSG buildsys-macros.

* Mon May 21 2007 Dennis Gilmore <dennis@ausil.us> 
- add el<ver> 1  fro new disttag guidelines

* Wed Sep 27 2006 Dennis Gilmore <dennis@ausil.us>
- add macro to run check-buildroot

* Mon Jul 07 2006 Dennis Gilmore <dennis@ausil.us>
- rhel version

* Tue May 10 2005 Tom "spot" Callaway <tcallawa@redhat.com>
- Initial build.
