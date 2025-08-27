Name:           pegasus
Version:        5.1.1
Release:        1.1%{?dist}
Summary:        Workflow management system for HTCondor, grids, and clouds
Group:          Applications/System
License:        ASL 2.0
URL:            http://pegasus.isi.edu/
Packager:       Pegasus Development Team <pegasus-support@isi.edu>

Source:         pegasus-%{version}.tar.gz

# OSG additions for building in an offline environment (Koji)
Patch1:         comment-out-s3transfer-and-urllib3-2.0.7-lines.patch
Patch2:         Install-wheels.patch
Source8:        el8-wheels-x86_64.tar
Source9:        el9-wheels-x86_64.tar
Source10:       el10-wheels-x86_64_v2.tar
Source11:       el8-wheels-aarch64.tar
Source12:       el9-wheels-aarch64.tar
Source13:       el10-wheels-aarch64.tar
BuildRequires:  python3-wheel
# End OSG additions

BuildRequires:  gcc, gcc-c++, javapackages-tools, make, openssl-devel, ant, python3-devel, python3-pip, python3-setuptools
Requires:       which, python3, condor >= 10.0, graphviz, %{?systemd_requires}


%global debug_package %{nil}

%if 0%{?rhel} == 8
BuildRequires:  python3-setuptools_scm, java-1.8.0-openjdk-devel
Requires:       java-1.8.0-openjdk-headless, python3-cryptography, python3-PyYAML, python3-GitPython, python3-dataclasses
# OSG
%ifarch aarch64
%define wheelsource %{SOURCE11}
%define wheeldir el8-wheels-aarch64
%else
%define wheelsource %{SOURCE8}
%define wheeldir el8-wheels-x86_64
%endif
# End OSG
%endif

%if 0%{?rhel} == 9
BuildRequires:  ant-apache-regexp, java-21-openjdk-devel
Requires:       java-21-openjdk-headless, python3-cryptography, python3-PyYAML, python3-GitPython
# OSG
%ifarch aarch64
%define wheelsource %{SOURCE12}
%define wheeldir el9-wheels-aarch64
%else
%define wheelsource %{SOURCE9}
%define wheeldir el9-wheels-x86_64
%endif
# End OSG
%endif

%if 0%{?rhel} == 10
BuildRequires:  ant-apache-regexp, java-21-openjdk-devel
Requires:       java-21-openjdk-headless, python3-cryptography, python3-PyYAML, python3-GitPython
# OSG
%ifarch aarch64
%define wheelsource %{SOURCE13}
%define wheeldir el10-wheels-aarch64
%else
%define wheelsource %{SOURCE10}
%define wheeldir el10-wheels-x86_64_v2
%endif
# End OSG
%endif

%define sourcedir %{name}-%{version}

# Disables the automatic dependency generator, which will include
# Python deps on packages we include inside our package
%{?python_disable_dependency_generator}

# Turn off automatic python bytecompilation
# Will bytecompile manually with Python 2 and 3 separately
%undefine __brp_python_bytecompile

%description
The Pegasus project encompasses a set of technologies that
help workflow-based applications execute in a number of
different environments including desktops, campus clusters,
grids, and now clouds. Scientific workflows allow users to
easily express multi-step computations. Once an application
is formalized as a workflow the Pegasus Workflow Management
Service can map it onto available compute resources and
execute the steps in appropriate order.


%prep
%setup -q -n %{sourcedir}
%autopatch -p1

%build
%if 0%{?osg}
tar -xf %{wheelsource}
export PYTHON_WHEELDIR=$(cd %{wheeldir} && pwd -P)
# Must delete pyproject.toml or pip will try to download 'setuptools<69' (even though it's already installed)
rm packages/*/pyproject.toml
%endif

ant -verbose dist-release

# strip executables
strip dist/pegasus-%{version}/bin/pegasus-cluster
strip dist/pegasus-%{version}/bin/pegasus-kickstart
strip dist/pegasus-%{version}/bin/pegasus-keg

%install

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}
mkdir -p %{buildroot}/%{_unitdir}

cp -aR dist/pegasus-%{version}/etc/* %{buildroot}/%{_sysconfdir}/%{name}/
cp -aR dist/pegasus-%{version}/bin/* %{buildroot}/%{_bindir}/
cp -aR dist/pegasus-%{version}/lib* %{buildroot}/usr/
cp -aR dist/pegasus-%{version}/share/* %{buildroot}/%{_datadir}/

install -m 0644 dist/%{name}-%{version}/share/pegasus/systemd-unit/pegasus-service.service %{buildroot}/%{_unitdir}/

# rm unwanted files
rm -f  %{buildroot}/%{_bindir}/keg.condor
rm -f  %{buildroot}/%{_datadir}/%{name}/java/COPYING.*
rm -f  %{buildroot}/%{_datadir}/%{name}/java/EXCEPTIONS.*
rm -f  %{buildroot}/%{_datadir}/%{name}/java/LICENSE.*
rm -f  %{buildroot}/%{_datadir}/%{name}/java/NOTICE.*
rm -rf %{buildroot}/%{_datadir}/%{name}/systemd-unit

%pre
# Handle previous install where /usr/lib64/pegasus/python was a directory
if [ -d /usr/lib64/pegasus/python ] && [ ! -L /usr/lib64/pegasus/python ]; then
    echo "Removing old /usr/lib64/pegasus/python directory to allow symlink install"
    rm -rf /usr/lib64/pegasus/python
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/
%{_bindir}/*
%{_libdir}/pegasus
%{_libdir}/python*
%{_datadir}/%{name}
%{_unitdir}/pegasus-service.service

%post
# Enable the systemd user service
systemctl daemon-reload

%preun
# Disable the service before uninstalling
systemctl stop pegasus-service.service
systemctl disable pegasus-service.service
systemctl daemon-reload

%changelog
* Wed Jul 16 2025 Mátyás Selmeci <mselmeci@wisc.edu> - 5.1.1-1.1
- Update to 5.1.1 (SOFTWARE-6163)
- Unset exclusiveArch

* Thu May 29 2025 Pegasus Development Team <pegasus-support@isi.edu> 5.1.1
- 5.1.1 automatic build

* Mon Oct 21 2024 Matt Westphall <westphall@wisc.edu> - 5.0.6-1.3
- Set exclusiveArch to x86_64 for initial OSG 24 build

* Mon Aug 14 2023 Matt Westphall <westphall@wisc.edu> - 5.0.6-1.1
- Build from upstream 5.0.6 (SOFTWARE-5648)

* Fri Nov 12 2021 Mátyás Selmeci <matyas@cs.wisc.edu> - 5.0.1-1.1
- Build for OSG; add setuptools_scm build dependency (SOFTWARE-4877)
  Ignore byte-compile errors: they fail on Python 2 code in the examples

* Thu Oct 07 2021 Pegasus Development Team <pegasus-support@isi.edu> 5.0.1
- 5.0.1 automatic build

* Mon Dec 02 2013 Pegasus Development Team <pegasus-support@isi.edu> 4.3.2cvs
- Relaxed the "java" requirements in order for the package to work on plan
  CentOS machines
