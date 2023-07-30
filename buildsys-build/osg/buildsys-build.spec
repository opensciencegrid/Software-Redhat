Name:      buildsys-build
Summary:   Minimal set of packages required to build in a chroot
Version:   7
Release:   2%{?dist}
License:   Apache 2.0
Group:     Development
URL:       http://www.opensciencegrid.org


Requires: bash
Requires: buildsys-macros = %{version}
Requires: bzip2
Requires: /etc/redhat-release
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
Requires: python3
Requires: redhat-rpm-config
Requires: rpm-build
Requires: sed
Requires: shadow-utils
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
Requires: /etc/redhat-release
Requires: cvs
Requires: epel-rpm-macros
Requires: fetch-sources
Requires: git
Requires: gnupg
Requires: make
Requires: python3
Requires: redhat-rpm-config
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
* Sun Jul 30 2023 Mátyás Selmeci <matyas@cs.wisc.edu> - 7-2
- Ask for /etc/redhat-release instead of a variant-specific package

* Mon Oct 17 2022 Carl Edquist <edquist@cs.wisc.edu> - 7-1
- Encore! Encore!  This time with buildsys-srpm-build, too. (SOFTWARE-4849)

* Wed Jul 11 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 5-3 / 6-3
- Removed util-linux-ng from el5 deps

* Wed Jul 11 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 5-2 / 6-2
- Fixed typo: 'gask' changed to 'gawk'
- Added xz for el6

* Wed Jul 11 2012 Matyas Selmeci <matyas@cs.wisc.edu> - 5-1 / 6-1
- Created

