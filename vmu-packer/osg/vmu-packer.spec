Summary: Scripts for using packer for making VMU images
Name: vmu-packer
Version: 1.7.0
Release: 1%{?dist}
License: Apache 2.0
Source0: %{name}-%{version}.tar.gz
Requires: packer-io
BuildArch: noarch
%define _debuginfo_subpackages %{nil}

%description
%{summary}

%prep
%autosetup

%build
exit 0

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/var/log/%{name}
echo '{"password":"ENTER PASSWORD HERE"}' > %{buildroot}/etc/%{name}/password.json

%files
/usr/bin/vmu-rebuild-one
/usr/bin/vmu-rebuild-all
/usr/share/%{name}
%attr(700,root,root) %dir /etc/%{name}
%attr(600,root,root) %config(noreplace) /etc/%{name}/password.json
%dir /var/log/%{name}

%changelog
* Fri Dec 02 2022 Carl Edquist <edquist@cs.wisc.edu> - 1.7.0-1
- Add EL9 images (SOFTWARE-5337)
  - Alma 9.1
  - CentOS Stream 9 2022-11-29
  - Rocky 9.1

* Fri Jun 17 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.6.0-1
- Add Alma Linux 8.6 (SOFTWARE-5177)

* Tue Feb 01 2022 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.5.0-1
- Don't auto-rebuild vanilla CentOS 8 image

* Thu Dec 02 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.1-1
- Remove deprecated "install" command from EL 8 kickstart files (SOFTWARE-4906)
- Fix image creation failure in CentOS Stream 8 and Rocky 8 due to not partitioning the disk (SOFTWARE-4913)

* Mon Nov 22 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.4.0-1
- Improve logging
- ISO updates (SOFTWARE-4913):
    - SL 7.9
    - CentOS 7.9
    - CentOS Stream 8 2021-07-28
    - Rocky 8.5

* Mon Nov 15 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.3.0-1
- Update to CentOS 8.4 (SOFTWARE-4886)

* Wed Jun 23 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.2.0-1
- Name the CentOS Stream 8 image centos_stream_8 instead of centos_8_stream
- Add Rocky Linux 8.4
- Use default file system type in CentOS 8 images instead of forcing ext4

* Tue Jan 12 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1.1-1
- Build CentOS 8 Stream in vmu-rebuild-all

* Fri Dec 18 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.1.0-1
- Add CentOS 8 Stream

* Wed Dec 09 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.1-1
- Update to CentOS 8.3

* Tue Jul 21 2020 Mátyás Selmeci <matyas@cs.wisc.edu> - 1.0.0-1
- Initial release
