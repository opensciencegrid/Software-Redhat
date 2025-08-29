%define osgver 23

Name: ospool-ep
Version: 23
Release: 10%{?dist}
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
* Mon Aug 25 2025 Matt Westphall <westphall@wisc.edu> 23-10
- Set a PID limit on the EP container (SOFTWARE-6142)

* Wed Jul 16 2025 Matt Westphall <westphall@wisc.edu> 23-9
- Explicitly specify the NVidia container runtime when GPUs are enabled (SOFTWARE-6189)

* Mon May 12 2025 Matt Westphall <westphall@wisc.edu> 23-8
- Use unconfined seccomp rather than privileged (SOFTWARE-6128)

* Tue Apr 01 2025 Matt Westphall <westphall@wisc.edu> 23-7
- Add retry logic to systemd service (SOFTWARE-6118)

* Wed Feb 19 2025 Matt Westphall <westphall@wisc.edu> 1.0-6
- Use the CUDA ospool-ep image when PROVIDE_NVIDIA_GPU=true

* Tue Oct 15 2024 Matt Westphall <westphall@wisc.edu> 1.0-5
- Fix misnamed environment variable

* Tue Nov 14 2023 Matt Westphall <westphall@wisc.edu> 1.0-1
- Initial version
