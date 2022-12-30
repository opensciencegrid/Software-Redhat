%global debug_package %{nil}
# ^^ debuginfo is pointless in a statically linked binary. Also it fails on el8 due to the absence of a build-id file.

Summary: Kubernetes Kustomize (binary install)
Name: kustomize-bin
Version: 3.7.0
Release: 2%{?dist}
License: ASL-2.0
Url: https://kustomize.io
Source0: kustomize_v%{version}_linux_amd64.tar.gz
ExclusiveArch: x86_64
Provides: kustomize = %{version}-%{release}

%description
Kubernetes Kustomize.  This is a pre-compiled binary.

%prep
# %%setup quick reference:
#   -a N        Unpack source N after cd
#   -b N        Unpack source N before cd
#   -c          Create and cd to dir before unpacking
#   -D          Do not delete dir before unpacking
#   -n DIR      Name of extract dir (instead of NAME-VERSION)
#   -T          Do not autounpack Source0

%setup -c %{name}-%{version}

%build
exit 0

%install
install -D kustomize %{buildroot}/usr/bin/kustomize


%files
/usr/bin/kustomize

%changelog
* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 3.7.0-2
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Tue Mar 23 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 3.7.0-1
- Created (SOFTWARE-4543)

# vim:ft=spec
