Summary: Hashicorp packer (binary install)
Name: packer-io-bin
Version: 1.10.1
Release: 1%{?dist}
License: MPL-2.0
Url: https://packer.io
Source0: packer_%{version}_linux_amd64.zip
ExclusiveArch: x86_64
Requires: qemu-system-x86
Requires: qemu-kvm
Provides: packer-io = %{version}-%{release}

%description
A VM builder.  This is a pre-compiled binary.

%package -n packer-symlink
Summary: Convenience symlink for packer.io
Requires: %{name}

%description -n packer-symlink
Convenience symlink for packer.io in /usr/local/bin

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
install -D packer %{buildroot}/usr/bin/packer.io
mkdir -p %{buildroot}/usr/local/bin
ln -s /usr/bin/packer.io %{buildroot}/usr/local/bin/packer


%files
/usr/bin/packer.io

%files -n packer-symlink
/usr/local/bin/packer

%changelog
* Thu Feb 01 2024 Matt Westphall <westphall@wisc.edu> - 1.10.1-1
- Bump release to upstream 1.10.1

* Fri Dec 30 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.6.0-2
- Bump and rebuild for new gpg key (SOFTWARE-5422)

* Tue Jul 07 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.6.0-1
- Created


# vim:ft=spec
