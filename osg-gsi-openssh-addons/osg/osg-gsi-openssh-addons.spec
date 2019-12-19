Summary: OSG additions for gsi-openssh
Name: osg-gsi-openssh-addons
Version: 1.0.0
Release: 2%{?dist}

Source100: gsisshd.osg-sysconfig
Source101: gsisshd.service-osg.conf

License: ASL 2.0

%description
%summary

%prep

%build

%install
install -d -m755 $RPM_BUILD_ROOT/usr/share/osg/sysconfig
install -m644 %{SOURCE100} $RPM_BUILD_ROOT/usr/share/osg/sysconfig/gsisshd

install -d -m755 $RPM_BUILD_ROOT/usr/lib/systemd/system/gsisshd.d
install -m644 %{SOURCE101} $RPM_BUILD_ROOT/usr/lib/systemd/system/gsisshd.service.d/osg.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(0644,root,root) /usr/share/osg/sysconfig/gsisshd
/usr/lib/systemd/system/gsisshd.service.d/osg.conf

%posttrans
# needs to be run after gsi-openssh-server is installed
systemctl daemon-reload >/dev/null 2>&1 || :

%changelog
* Mon Dec 16 2019 Carl Edquist <edquist@cs.wisc.edu> - 1.0.0-2
- Break out OSG addons to separate package (SOFTWARE-3915)

