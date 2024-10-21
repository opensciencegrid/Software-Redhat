Name:           pegasus
Version:        5.0.6
Release:        1.3%{?dist}
Summary:        Workflow management system for HTCondor, grids, and clouds
Group:          Applications/System
License:        ASL 2.0
URL:            http://pegasus.isi.edu/
Packager:       Pegasus Development Team <pegasus-support@isi.edu>

Source:         pegasus-%{version}.tar.gz

BuildRequires:  ant-apache-regexp, gcc, gcc-c++, jpackage-utils, make, openssl-devel, ant, R-devel
Requires:       java >= 1:1.8.0, python3, condor >= 8.8, graphviz, perl-Getopt-Long

ExclusiveArch: x86_64

%if 0%{?rhel} <= 7
# Jinja2 v2.11 has async code, which uses py36 syntax, and is never imported in < py36, but
# byte compiling in RPM fails as py27 interpreter tries to compile all files.
# To resolve the above we set default interpreter to py3.
# Alternatively, we can set % global _python_bytecompile_errors_terminate_build to 0, to ignore
# byte compile errors
%global __python %{python3}

# Ignore byte compile errors -- they fail on Python 2 code in the examples
%global _python_bytecompile_errors_terminate_build 0

BuildRequires:  java-devel = 1:1.8.0, python36-pyOpenSSL, python36-PyYAML, python36-GitPython, python3-devel, python3-setuptools, python36-setuptools_scm
Requires:       java >= 1:1.8.0, python3, condor >= 8.8, graphviz, python36-pika, python36-PyYAML, python36-GitPython, perl-Getopt-Long
%endif

%if 0%{?rhel} >= 8
BuildRequires:  java-11-openjdk-devel, python3-pyOpenSSL, python3-PyYAML, python3-GitPython, python3-devel, python3-setuptools, python3-setuptools_scm
Requires:       jre-11-openjdk-headless, python3, condor >= 8.8, graphviz, python3-pyOpenSSL, python3-pika, python3-PyYAML, python3-GitPython, perl-Getopt-Long
%endif

%define sourcedir %{name}-%{version}

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

%build
ant dist-release

# strip executables
strip dist/pegasus-%{version}/bin/pegasus-cluster
strip dist/pegasus-%{version}/bin/pegasus-kickstart
strip dist/pegasus-%{version}/bin/pegasus-keg

%install

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}

cp -aR dist/pegasus-%{version}/etc/* %{buildroot}/%{_sysconfdir}/%{name}/
cp -aR dist/pegasus-%{version}/bin/* %{buildroot}/%{_bindir}/
cp -aR dist/pegasus-%{version}/lib* %{buildroot}/usr/
cp -aR dist/pegasus-%{version}/share/* %{buildroot}/%{_datadir}/

# rm unwanted files
rm -f %{buildroot}/%{_bindir}/keg.condor
rm -f %{buildroot}/%{_datadir}/%{name}/java/COPYING.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/EXCEPTIONS.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/LICENSE.*
rm -f %{buildroot}/%{_datadir}/%{name}/java/NOTICE.*

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/
%{_bindir}/*
%{_libdir}/pegasus
%{_libdir}/python*
%{_datadir}/%{name}


%changelog
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

