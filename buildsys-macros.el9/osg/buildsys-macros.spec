# Instructions:
# Just define osg_version and dver here, use osg-build rpmbuild, then
# "osg-koji import" the resulting rpm and osg-koji tag-pkg the build into the
# appropriate osg-*-development tag
# This will require koji admin permissions.
%define osg_version 3.6
%define dver   9

%define osgver %(tr -d . <<< %{osg_version})
%define dist .osg%{osgver}.el%{dver}

Name:		buildsys-macros
Summary:	Macros for the OSG Buildsystem
Version:        %{dver}
Release:	1%{dist}
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


%files
/etc/rpm/macros.disttag
/etc/rpm/macros.checkbuild

%changelog
* Thu Dec 08 2022 Carl Edquist <edquist@cs.wisc.edu> - 9-1.osg36.el9
- 3.6 el9 version (SOFTWARE-5395)

* Wed Feb 03 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 8-7.osg36.el8
- 3.6 el8 version
