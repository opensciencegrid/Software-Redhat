# Instructions:
# Just define osg_version and dver here, use osg-build rpmbuild, then
# "osg-koji import" the resulting rpm and osg-koji tag-pkg the build into the
# appropriate osg-*-development tag
# This will require koji admin permissions.
%define osg_version 23
%define dver   8

%define osgver 23
%define dist .osg%{osgver}.el%{dver}
%define macros_dist .osg%{osgver}contrib.el%{dver}

Name:		buildsys-macros
Summary:	Macros for the OSG Buildsystem
Version:        %{dver}
Release:	12%{macros_dist}
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
* Wed Jun 4 2024 Matt Westphall <westphall@wisc.edu> - 8-20.osg23empty.el8
- Bump to re-sign with auto key

* Fri Oct 6 2023 Matt Westphall <westphall@wisc.edu> - 8-15.osg23empty.el8
- Update for osg-23-empty-el8

* Fri Oct 6 2023 Matt Westphall <westphall@wisc.edu> - 8-15.osg23.el8
- Revert osg-23-internal-el8

* Tue Aug 22 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 8-11.osg23int.el8
- osg-23-internal-el8 (SOFTWARE-5657)

* Thu Jul 27 2023 Matt Westphall <westphall@wisc.edu> - 9-8.osg23.el8
- osg 23 el8 version

* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 8-8.osg36.el7
- Cap _smp_ncpus_max to 12 (SOFTWARE-4728)

* Wed Feb 03 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 8-7.osg36.el8
- 3.6 el8 version
