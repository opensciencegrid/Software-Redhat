Name:		buildsys-macros
Summary:	Macros for the OSG Buildsystem
%if 0%{?rhel} < 6
Version:	5
%else
Version:        %{?rhel}
%endif
Release:	7%{?dist}
License:	GPL
Group:		Development/Buildsystem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:  	noarch
Requires:	rpmdevtools

%description
Macros for the Fedora Buildsystem

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
VERSION=%{version}
printf %s%b "%" "rhel $VERSION\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "dist .osg.el$VERSION\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "el$VERSION 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "__arch_install_post /usr/lib/rpm/check-buildroot\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.checkbuild
if [[ $VERSION -eq 5 ]]; then
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
%if %{version} == 5
/etc/rpm/macros.digest
%endif
/etc/rpm/macros.disttag
/etc/rpm/macros.checkbuild

%changelog
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
