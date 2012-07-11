Name:      buildsys-build
Summary:   Minimal set of packages required to build in a chroot
Version:   %{rhel}
Release:   1%{?dist}
License:   Apache 2.0
Group:     Grid
URL:       http://www.opensciencegrid.org

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


Requires: bash
Requires: buildsys-macros = %{version}
Requires: bzip2
Requires: coreutils
Requires: cpio
Requires: diffutils
Requires: findutils
Requires: gask
Requires: gcc
Requires: gcc-c++
Requires: grep
Requires: gzip
Requires: info
Requires: make
Requires: patch
Requires: redhat-release
Requires: redhat-rpm-config
Requires: rpm-build
Requires: sed
Requires: shadow-utils
Requires: tar
Requires: unzip
Requires: util-linux-ng
Requires: which


%description
%{summary}


%install

%clean
rm -rf $RPM_BUILD_ROOT

%files


%changelog
* Wed Jul 11 2012 Matyas Selmeci <matyas@cs.wisc.edu>
- Created

