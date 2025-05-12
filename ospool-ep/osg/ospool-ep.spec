%define osgver 24

Name: ospool-ep
Version: %{osgver}
Release: 4%{?dist}
Summary: Systemd service for the OSPool Backfill Container

License: Unknown
URL: https://github.com/opensciencegrid/osgvo-docker-pilot


Source0: ospool-ep.service
Source1: start_ospool_ep_container.sh
Source2: ospool-ep.cfg

BuildArch: noarch
Requires: /usr/bin/docker systemd

%description
Systemd service for the OSPool Backfill Container

%prep
exit 0

%build
# Set the docker image to the appropriate osg version
sed -i "s/%%{OSGVER}/%{osgver}/" %{SOURCE1}

%install

mkdir -p %{buildroot}/usr/lib/systemd/system %{buildroot}/etc/osg %{buildroot}/usr/sbin
mv %{SOURCE0} %{buildroot}/usr/lib/systemd/system
mv %{SOURCE1} %{buildroot}/usr/sbin
mv %{SOURCE2} %{buildroot}/etc/osg/

%files
%defattr(0644,root,root,-)
/usr/lib/systemd/system/ospool-ep.service
%config(noreplace) /etc/osg/ospool-ep.cfg 
%attr(0755,root,root) /usr/sbin/start_ospool_ep_container.sh

%changelog

* Mon May 12 2025 Matt Westphall <westphall@wisc.edu> 24-4
- Use unconfined seccomp rather than privileged (SOFTWARE-6128)

* Tue Apr 01 2025 Matt Westphall <westphall@wisc.edu> 24-3
- Add retry logic to systemd service (SOFTWARE-6118)

* Thu Feb 20 2025 Matt Westphall <westphall@wisc.edu> 24-2
- Use the CUDA ospool-ep image when PROVIDE_NVIDIA_GPU=true

* Wed Oct 16 2024 Matt Westphall <westphall@wisc.edu> 24-1
- OSG 24 release

* Tue Nov 14 2023 Matt Westphall <westphall@wisc.edu> 1.0-1
- Initial version
