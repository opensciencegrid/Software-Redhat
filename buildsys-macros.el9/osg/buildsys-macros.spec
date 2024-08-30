# Instructions:
# Just define osg_version and dver here, use osg-build rpmbuild, then
# "osg-koji import" the resulting rpm and osg-koji tag-pkg the build into the
# appropriate osg-*-development tag
# This will require koji admin permissions.
%define osg_version 23up
%define dver   9

%define osgver 23up
%define dist .osg%{osgver}.el%{dver}

Name:		buildsys-macros
Summary:	Macros for the OSG Buildsystem
Version:        %{dver}
Release:	10%{dist}
License:	GPL
BuildArch:      noarch
Requires:	rpmdevtools

%description
Macros for the OSG Buildsystem

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/etc/rpm/
DVER=%{dver}
OSGVER=%{osgver}
DIST=%{dist}
printf %s%b "%" "rhel $DVER\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "dist $DIST\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "el$DVER 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "osg 1\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.disttag
printf %s%b "%" "__arch_install_post /usr/lib/rpm/check-buildroot\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.checkbuild
printf %s%b "%" "_smp_ncpus_max 12\n" >> $RPM_BUILD_ROOT/etc/rpm/macros.kojibuilder


%files
/etc/rpm/macros.disttag
/etc/rpm/macros.checkbuild
/etc/rpm/macros.kojibuilder

%changelog
* Mon Oct 02 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 9.10
- Bump to rebuild with new signing key

* Thu Jul 27 2023 Matt Westphall <westphall@wisc.edu>
- osg 23 el9 version

* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 9-7
- Cap _smp_ncpus_max to 12 (SOFTWARE-4728)

* Thu Dec 08 2022 Carl Edquist <edquist@cs.wisc.edu> - 9-1
- build for el9 (SOFTWARE-5395)

* Tue Feb 02 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 8-6
- split upcoming repo

* Wed May 06 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 8-2
- bump to rebuild for upcoming

* Wed Oct 02 2019 Mátyás Selmeci <matyas@cs.wisc.edu> - 8-1
- el8 version

* Wed Jul 31 2019 Carl Edquist <edquist@cs.wisc.edu> - 7-7
- Bump to rebuild for OSG 3.5 (SOFTWARE-3761)

* Tue Apr 25 2017 Mátyás Selmeci <matyas@cs.wisc.edu> 7-6
- Bump to rebuild for OSG 3.4 (SOFTWARE-2622)

* Wed Apr 29 2015 Mátyás Selmeci <matyas@cs.wisc.edu> 7-5
- Bump to rebuild for OSG 3.3

* Fri Jul 11 2014 Mátyás Selmeci <matyas@cs.wisc.edu> - 7-4.osg.el7
- Bump to rebuild with buildsys-macros 7-3 for el7

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
