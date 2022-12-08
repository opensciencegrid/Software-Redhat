Name:      buildsys-build
Summary:   Minimal set of packages required to build in a chroot
Version:   8
Release:   1%{?dist}
License:   Apache 2.0
Group:     Development
URL:       http://www.opensciencegrid.org


Requires: bash
Requires: buildsys-macros = %{version}
Requires: bzip2
Requires: coreutils
Requires: cpio
Requires: diffutils
Requires: epel-rpm-macros
Requires: findutils
Requires: gawk
Requires: gcc
Requires: gcc-c++
Requires: grep
Requires: gzip
Requires: info
Requires: make
Requires: patch
Requires: redhat-rpm-config
Requires: rocky-release
Requires: rpm-build
Requires: sed
Requires: shadow-utils
Requires: systemd
Requires: tar
Requires: unzip
Requires: util-linux
Requires: which


%description
%{summary}


%package -n buildsys-srpm-build
Summary:   Minimal set of packages required to build srpms in a chroot

Requires: bash
Requires: buildsys-macros = %{version}
Requires: epel-rpm-macros
Requires: fetch-sources
Requires: git
Requires: gnupg
Requires: make
Requires: redhat-rpm-config
Requires: rocky-release
Requires: rpm-build
Requires: subversion

%description -n buildsys-srpm-build
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT


%files

%files -n buildsys-srpm-build


%changelog
* Mon Oct 17 2022 Carl Edquist <edquist@cs.wisc.edu> - 8-1
- Encore! Encore!  This time with buildsys-srpm-build, too. (SOFTWARE-4849)

* Wed Jul 11 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 5-3 / 6-3
- Removed util-linux-ng from el5 deps

* Wed Jul 11 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 5-2 / 6-2
- Fixed typo: 'gask' changed to 'gawk'
- Added xz for el6

* Wed Jul 11 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 5-1 / 6-1
- Created

