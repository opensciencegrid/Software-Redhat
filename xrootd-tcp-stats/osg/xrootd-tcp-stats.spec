Summary: xrootd-tcp-stats
Name: xrootd-tcp-stats
Version: 1.0.0
Release: 1%{?dist}
License: Unknown
Url: https://github.com/sand-ci/xrootd-tcp-stats
Source0: %{name}-%{version}.tar.gz
# to create:
#
# name=%%name
# version=%%version
# git clone https://github.com/sand-ci/$name
# cd $name
# git archive --prefix "${name}-${version}/" -o "${name}-${version}.tar" v${version}
# git submodule update --init
# git submodule foreach --recursive "git archive --prefix=${name}-${version}/\$path/ --output=\$sha1.tar HEAD && tar --concatenate --file=$(pwd)/${name}-${version}.tar \$sha1.tar && rm \$sha1.tar"
# gzip -n ${name}-${version}.tar

%if 0%{?rhel} < 8
BuildRequires: cmake3
%else
BuildRequires: cmake >= 3
%endif
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: xrootd-server-devel >= 1:5, xrootd-server-devel < 1:6


%description
xrootd-tcp-stats


%prep
# %%setup quick reference:
#   -a N        Unpack source N after cd
#   -b N        Unpack source N before cd
#   -c          Create and cd to dir before unpacking
#   -D          Do not delete dir before unpacking
#   -n DIR      Name of extract dir (instead of NAME-VERSION)
#   -T          Do not autounpack Source0

%setup


%build
%cmake3
%cmake3_build


%install
%cmake3_install


%files
/usr/lib64/libXrdTCPStats-5.so


%post -p /sbin/ldconfig


%changelog
* Wed Dec 22 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.0-1
- Created (SOFTWARE-4744)


# vim:ft=spec
